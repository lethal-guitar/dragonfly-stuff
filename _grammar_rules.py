#
# This file is a command-module for Dragonfly.
# (c) Copyright 2008 by Christo Butcher
# Licensed under the LGPL, see <http://www.gnu.org/licenses/>
#

"""
Command-module for cursor movement and **editing**
============================================================================

This module allows the user to control the cursor and
efficiently perform multiple text editing actions within a
single phrase.


Example commands
----------------------------------------------------------------------------

*Note the "/" characters in the examples below are simply
to help the reader see the different parts of each voice
command.  They are not present in the actual command and
should not be spoken.*

Example: **"up 4 / down 1 page / home / space 2"**
   This command will move the cursor up 4 lines, down 1 page,
   move to the beginning of the line, and then insert 2 spaces.

Example: **"left 7 words / backspace 3 / insert hello Cap world"**
   This command will move the cursor left 7 words, then delete
   the 3 characters before the cursor, and finally insert
   the text "hello World".

Example: **"home / space 4 / down / 43 times"**
   This command will insert 4 spaces at the beginning of
   of this and the next 42 lines.  The final "43 times"
   repeats everything in front of it that many times.


Discussion of this module
----------------------------------------------------------------------------

This command-module creates a powerful voice command for
editing and cursor movement.  This command's structure can
be represented by the following simplified language model:

 - *CommandRule* -- top-level rule which the user can say
    - *repetition* -- sequence of actions (name = "sequence")
       - *KeystrokeRule* -- rule that maps a single
         spoken-form to an action
    - *optional* -- optional specification of repeat count
       - *integer* -- repeat count (name = "n")
       - *literal* -- "times"

The top-level command rule has a callback method which is
called when this voice command is recognized.  The logic
within this callback is very simple:

1. Retrieve the sequence of actions from the element with
   the name "sequence".
2. Retrieve the repeat count from the element with the name
   "n".
3. Execute the actions the specified number of times.

"""

try:
    import pkg_resources
    pkg_resources.require("dragonfly >= 0.6.5beta1.dev-r99")
except ImportError:
    pass

from dragonfly import *
from dragonfly.language.en.characters import *


#---------------------------------------------------------------------------
# Here we globally defined the release action which releases all
#  modifier-keys used within this grammar.  It is defined here
#  because this functionality is used in many different places.
#  Note that it is harmless to release ("...:up") a key multiple
#  times or when that key is not held down at all.

release = Key("shift:up, ctrl:up")


#---------------------------------------------------------------------------
# Set up this module's configuration.

config            = Config("multi edit")
config.cmd        = Section("Language section")
config.cmd.map    = Item(
    # Here we define the *default* command map.  If you would like to
    #  modify it to your personal taste, please *do not* make changes
    #  here.  Instead change the *config file* called "_multiedit.txt".
    {
        # Spoken-form    ->    ->    ->     Action object


        "sleep": Mimic("go to sleep"),
        "reload": Mimic("go to sleep") + Mimic("wake up"), # doesn't work...

        "assign": Key("space, equals, space"),
        "kick": Key("comma") + Key("space"),
        "come": Key("comma"),
        "colon": Key("colon"),
        "smack": Key("space"),
        "score": Key("underscore"),
        "tab": Key("tab"),
        "equals": Key("equals"),
        "dot": Key("dot"),
        "and": Key("ampersand") + Key("ampersand"),
        "or": Key("bar") + Key("bar"),
        "bang": Key("bang"),
        "reference": Key("ampersand"),
        "plus": Key("plus"),
        "quote": Key("dquote"),
        "minus": Key("minus"),
        "tick": Key("lparen"),
        "tock": Key("rparen"),
        "chick": Key("lbrace"),
        "Chuck": Key("rbrace"),
        "click": Key("lbracket"),
        "Clark": Key("rbracket"),
        "not equal": Key("bang") + Key("equals"),
        "less equal": Key("leftangle") + Key("equals"),
        "less than": Key("leftangle"),
        "greater than": Key("rightangle"),
        "Sammy": Text(";"),
        "falls": Text("false"),
        "hash": Key("hash"),
        "back slash": Key("backslash"),
        "slash": Key("slash"),
        "dub slash": Key("slash") + Key("slash"),
        "arrow": Key("minus") + Key("rangle"),

        "undo": Key("u"),
        "redo": Key("c-r"),
        "up":            Key("k"),
        "down":         Key("j"),
        "left":  Key("h"),
        "right":            Key("l"),
        "<n> [lines] down": Text("%(n)d") + Key("j"),
        "<n> [lines] up": Text("%(n)d") + Key("k"),

        "go line <n>": Text("%(n)dG"),

        "word": Key("w"),
        "back": Key("b"),
        "big word": Key("W"),
        "big back": Key("B"),
        "end": Key("dollar"),
        "begin": Key("caret"),
        "page up": Key("c-u"),
        "page down": Key("c-d"),
        "scroll top": Key("z, t"),
        "scroll middle": Key("z, z"),

        "visual line": Key("V"),

        "next tab": Key("g, t"),
        "previous tab": Key("g, T"),
        "new tab": Key("c-t"),
        "last position": Key("c-o"),

        "P match": Key("percent"),
        "scratch": Key("c-w"),

        "find": Key("slash"),
        "find next": Key("n"),
        "find previous": Key("N"),
        "stop find": Key("colon, n, o, h, enter"),

        "change word": Key("c, i, w"),
        "change line": Key("c, c"),
        "change in quote": Key("c, i, quote"),

        "big open": Key("O"),
        "open": Key("o"),
        "join": Key("J"),
        "substitute": Key("s"),
        "dedent line": Key("leftangle") + Key("leftangle"),
        "indent line": Key("rightangle") + Key("rightangle"),
        "inner dedent": Key("c-d"),
        "inner indent": Key("c-t"),

        "out": Key("escape"),
        "auto complete": Key("c-n"),

        "double col": Key("colon, colon"),
        "command": Key("colon"),
        "working": Key("colon, p, w, d, enter"),
        "go to rigel": Key("colon, c, d, space") + Text('C:\\Users\\Niko\\Desktop\\New\\ Duke2\\RigelEngine\\src') + Key("enter"),
        "edit file": Key("colon, e, space"),

        "jump <c>": Key("f") + Text("%(c)s"),
        "back jump <c>": Key("F") + Text("%(c)s"),

        "Yank": Key("y"),
        "delete": Key("d"),
        "change": Key("c"),
        "until": Key("t"),
        "big kill": Key("d, W"),
        "kill": Key("d, w"),
        "big append": Key("A"),
        "append": Key("a"),
        "insert": Key("i"),
        "big insert": Key("I"),
        "toggle commie": Key("backslash, c"),
        "toggle app": Mimic("press alt tab"),

        "split win": Key("c-w, v"),
        "close win": Key("c-w, c"),
        "swap win": Key("c-w, x"),
        "left win": Key("c-w, h"),
        "right win": Key("c-w, l"),

        "replace <c>": Key("r") + Text("%(c)s"),
        "X": Key("x"),
        "s": Key("s"),

        "slap": Key("enter"),
        "delete line": Key("d, d"),
        "yank line": Key("y, y"),
        "yank word": Key("y, w"),

        "put": Key("p"),
        "big put": Key("P"),

        "save it": Key("colon, w, enter"),
        "ship it": Key("colon, x, enter"),

        "<c>": Text("%(c)s"),
        "number <n2>": Text("%(n2)d"),
        #"say <text>":                       release + Text("%(text)s"),
        "mimic <text>":                     release + Mimic(extra="text"),

        # this is actually for console
        "git stat": Text("git st") + Key("enter"),
        "git fetch": Text("gfetch") + Key("enter"),
        "git amend": Text("git commit --amend") + Key("enter"),
        "git commit": Text("git commit") + Key("enter"),
        "git push": Text("git push") + Key("enter"),
        "git add": Text("git add") + Key("space"),
        "git checkout": Text("git co") + Key("space"),
        "git interactive rebase": Text("git rebase -i") + Key("space"),
        "origin master": Text("origin/master"),
        "generate": Text("gen") + Key("enter"),
        "build debug": Text("_buildLive -D") + Key("enter"),
        "build release": Text("_buildLive") + Key("enter"),

    },
    namespace={
     "Key":   Key,
     "Text":  Text,
    }
)
namespace = config.load()

#---------------------------------------------------------------------------
# Here we prepare the list of formatting functions from the config file.

# Retrieve text-formatting functions from this module's config file.
#  Each of these functions must have a name that starts with "format_".
format_functions = {}

# Format: some_words
def format_score(dictation):          # Function name must start with "format_".
    """ snake <dictation> """         # Docstring defining spoken-form.
    text = str(dictation)             # Get written-form of dictated text.
    return "_".join(text.split(" "))  # Put underscores between words.

# Format: SomeWords
def format_studley(dictation):
    """ studley <dictation> """
    text = str(dictation)
    words = [word.capitalize() for word in text.split(" ")]
    return "".join(words)

# Format: somewords
def format_one_word(dictation):
    """ [all] one word <dictation> """
    text = str(dictation)
    return "".join(text.split(" "))

# Format: SOMEWORDS
def format_upper_one_word(dictation):
    """ one word upper <dictation> """
    text = str(dictation)
    words = [word.upper() for word in text.split(" ")]
    return "".join(words)

# Format: SOME_WORDS
def format_upper_score(dictation):
    """ upper snake <dictation> """
    text = str(dictation)
    words = [word.upper() for word in text.split(" ")]
    return "_".join(words)

# Format: someWords
def format_camel(dictation):
    """ camel <dictation> """
    text = str(dictation)
    words = text.split(" ")
    return words[0] + "".join(w.capitalize() for w in words[1:])

def format_symbols(dictation):
    """ symbols <dictation> """
    text = str(dictation)
    words = text.split(" ")
    return " ".join([w.split("\\")[0] for w in words])

def format_say(dictation):
    """ say <dictation> """
    text = str(dictation)
    return text

print "----------------------------------------"
print "reloading"
print "----------------------------------------"

for name, function in globals().items():
 if name.startswith("format_") and callable(function):
    spoken_form = function.__doc__.strip()

    # We wrap generation of the Function action in a function so
    #  that its *function* variable will be local.  Otherwise it
    #  would change during the next iteration of the namespace loop.
    def wrap_function(function):
        def _function(dictation):
            formatted_text = function(dictation)
            Text(formatted_text).execute()
        return Function(_function)

    action = wrap_function(function)
    format_functions[spoken_form] = action


# Here we define the text formatting rule.
# The contents of this rule were built up from the "format_*"
#  functions in this module's config file.
if format_functions:
    class FormatRule(MappingRule):

        mapping  = format_functions
        extras   = [Dictation("dictation")]

else:
    FormatRule = None


#---------------------------------------------------------------------------
# Here we define the keystroke rule.

# This rule maps spoken-forms to actions.  Some of these
#  include special elements like the number with name "n"
#  or the dictation with name "text".  This rule is not
#  exported, but is referenced by other elements later on.
#  It is derived from MappingRule, so that its "value" when
#  processing a recognition will be the right side of the
#  mapping: an action.
# Note that this rule does not execute these actions, it
#  simply returns them when it's value() method is called.
#  For example "up 4" will give the value Key("up:4").
# More information about Key() actions can be found here:
#  http://dragonfly.googlecode.com/svn/trunk/dragonfly/documentation/actionkey.html
class KeystrokeRule(MappingRule):

    exported = False

    mapping  = config.cmd.map
    extras   = [
                IntegerRef("n", 1, 100),
                IntegerRef("n2", 0, 1000000),
                CharChoice("c"),
                Dictation("text"),
                Dictation("text2"),
               ]
    defaults = {
                "n": 1,
               }
    # Note: when processing a recognition, the *value* of
    #  this rule will be an action object from the right side
    #  of the mapping given above.  This is default behavior
    #  of the MappingRule class' value() method.  It also
    #  substitutes any "%(...)." within the action spec
    #  with the appropriate spoken values.


#---------------------------------------------------------------------------
# Here we create an element which is the sequence of keystrokes.

# First we create an element that references the keystroke rule.
#  Note: when processing a recognition, the *value* of this element
#  will be the value of the referenced rule: an action.
alternatives = []
alternatives.append(RuleRef(rule=KeystrokeRule()))
if FormatRule:
    alternatives.append(RuleRef(rule=FormatRule()))
single_action = Alternative(alternatives)

# Second we create a repetition of keystroke elements.
#  This element will match anywhere between 1 and 16 repetitions
#  of the keystroke elements.  Note that we give this element
#  the name "sequence" so that it can be used as an extra in
#  the rule definition below.
# Note: when processing a recognition, the *value* of this element
#  will be a sequence of the contained elements: a sequence of
#  actions.
sequence = Repetition(single_action, min=1, max=16, name="sequence")


#---------------------------------------------------------------------------
# Here we define the top-level rule which the user can say.

# This is the rule that actually handles recognitions.
#  When a recognition occurs, it's _process_recognition()
#  method will be called.  It receives information about the
#  recognition in the "extras" argument: the sequence of
#  actions and the number of times to repeat them.
class RepeatRule(CompoundRule):

    # Here we define this rule's spoken-form and special elements.
    spec     = "<sequence> [[[and] repeat [that]] <n> times]"
    extras   = [
                sequence,                 # Sequence of actions defined above.
                IntegerRef("n", 1, 100),  # Times to repeat the sequence.
               ]
    defaults = {
                "n": 1,                   # Default repeat count.
               }

    # This method gets called when this rule is recognized.
    # Arguments:
    #  - node -- root node of the recognition parse tree.
    #  - extras -- dict of the "extras" special elements:
    #     . extras["sequence"] gives the sequence of actions.
    #     . extras["n"] gives the repeat count.
    def _process_recognition(self, node, extras):
        sequence = extras["sequence"]   # A sequence of actions.
        count = extras["n"]             # An integer repeat count.
        for i in range(count):
            for action in sequence:
                action.execute()
        release.execute()


#---------------------------------------------------------------------------
# Create and load this module's grammar.

gvim_context = AppContext(executable="gvim")
console_context = AppContext(executable="Console.exe")
grammar_context = gvim_context | console_context
grammar = Grammar("multi edit", context=grammar_context)   # Create this module's grammar.
grammar.add_rule(RepeatRule())    # Add the top-level rule.
grammar.load()                    # Load the grammar.

# Unload function which will be called at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
