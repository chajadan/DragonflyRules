  # -*- coding: utf-8 -*-
print "import _main"

from dragonfly import *
import Base
import _keyboard as kb
import inspect

grammar = Base.ContinuousGrammar("_main grammar")


# decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, Base.BaseQuickRules):
            rule(grammar)
        else:
            grammar.add_rule(rule())
    else:
        grammar.add_rule(rule)


@GrammarRule
class SomeQuickRules(Base.QuickContinuousRules):
    name = "GlobalQuickRules"
    extrasDict = {
        "keyCount": IntegerRef("keyCount", 1, 1000),
        "n": IntegerRef("n", 1, 10000),
        "clickCount": IntegerRef("clickCount", 1, 1000),
        "lineCount": IntegerRef("lineCount", 1, 1000),
        "text": Dictation("text"),
        "chain": Dictation("chain"),
    }
    defaultsDict = {
        "n": 1,
        "keyCount": 1,
        "clickCount": 1,
        "lineCount": 1,
    }    
    mapping = {      
        "(click|mouse) [<clickCount> [times]]": Mouse("left:1") * Repeat(extra="clickCount"),
        "click paste": Mouse("left:1") + Key("c-v"),
        "control click [<clickCount> [times]]": (Key("ctrl:down") + Mouse("left:1") + Key("ctrl:up")) * Repeat(extra="clickCount"),
        "right click [<clickCount> [times]]": Mouse("right:1") * Repeat(extra="clickCount"),
        "middle click [<clickCount> [times]]": Mouse("middle:1") * Repeat(extra="clickCount"),
        "double click": Mouse("left:2"),
        "shift down": Key("shift:down"),
        "shift up": Key("shift:up"),
        "shift click": Key("shift:down") + Mouse("left:1") + Key("shift:up"),
        "shift right click": Key("shift:down") + Mouse("right:1") + Key("shift:up"),
        "down click": Mouse("left:down"),
        "up click": Mouse("left:up"),
        "down right click": Mouse("right:down"),
        "up right click": Mouse("right:up"),
        "[toggle] flux": Key("a-end"),
    }


@GrammarRule
class QuickCRules(Base.QuickContinuousRules):
    mapping = {
        "(in quotes|string it)": Text("\"\"") + Key("left"),
        "in brackets": Text("[]") + Key("left"),
        "in apostrophes": Text("''") + Key("left"),
        "brackets": Text("[]"),
        "angle brackets": Text("<>"),
        "parentheses": Text("()"),
        "in curly brackets": Text("{}") + Key("left"),
        "in angle brackets": Text("<>") + Key("left"),
        "call with": Text("()") + Key("left"),
        "call": Text("()"),
        "spinster": Text("()") + Key("enter"),
        "item": Text(", "),
        "assign": Text(" = "),
        "dereference": Text("->"),
        "dot": Key("dot"),
    }


@GrammarRule
class system_shortcuts_rule(Base.QuickContinuousRules):
    name = "system_shortcuts"
    mapping = {
             "save": Key("c-s"),
             "copy": Key("c-c"),
             "(paste|from clip|from clipboard)": Key("c-v"),
             "cut": Key("c-x"),
             "top": Key("c-home"),
             "bottom": Key("c-end"),
             "tab windows": Key("alt:down, tab:down"),
             "go to tab <n>": (Key("right") * Repeat(extra="n")) + Key("alt:up, tab:up"),
             "last window": Key("a-tab"),
             "undo": Key("c-z"),
             "find": Key("c-f"),
             "desktop": Key("w-d"),
             "dock left": Key("w-left"),
             "dock left twice": Key("w-left") * Repeat(2),
             "dock right": Key("w-right"),
             "dock right twice": Key("w-right") * Repeat(2),
             "hide [(others | other windows)]": {
                "action": Key("w-home"),
                "intro": ["hide", "hide others", "hide other windows"]},
             "minimize": Key("w-down") * Repeat(2),
             "maximize": Key("w-up"),
             "close window": Key("a-f4"),
            }
    extrasDict = {
        "keyCount": IntegerRef("keyCount", 1, 1000),
        "n": IntegerRef("n", 0, 1000),
    }
    defaultsDict = {
        "keyCount": 1,
        "n": 1,
    }

grammar.load()
    
# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
