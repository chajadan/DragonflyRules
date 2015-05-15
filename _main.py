  # -*- coding: utf-8 -*-
print "import _main"

from dragonfly import *
import Base
import _keyboard as kb
import inspect

grammar = Base.ContinuousGrammar("_main grammar")


#decorator
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
    name="GlobalQuickRules"
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
    mapping= {      
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
        "trim left": Key("s-home, delete"),
        "trim right": Key("s-end, delete"),
    }

 
def ReplaceAllInLine(toReplace, replaceWith, sensitive = True):
    pass
#     kb.sendHome()
#     kb.sendEnd()
#     kb.sendShiftHome()
#     line = ReadSelection()
#     if not sensitive:
#         toReplace = toReplace.lower()
#     Text(selection.replace(toReplace, replaceWith)).execute()

@GrammarRule
class ReplaceAllInLineRule(Base.RegisteredRule):
    spec = "replace line <toReplace> with <replaceWith>"
    extras = (Dictation("toReplace"), Dictation("replaceWith"))
    def _process_recognition(self, node, extras):
        toReplace = extras["toReplace"].format()
        replaceWith = extras["replaceWith"].format()
        Function(ReplaceAllInLine).execute({"toReplace": toReplace, "replaceWith": replaceWith})


@GrammarRule
class InterDocNavRules(Base.QuickContinuousRules):
    name="inter_doc_nav"
    extrasDict = {
        "keyCount": IntegerRef("keyCount", 1, 1000),
        "n": IntegerRef("n", 1, 1000),
        "text": Dictation("text"),
    }
    defaultsDict = {
        "keyCount": 1,
        "n": 1,
    }    
    mapping = {
        "renter [<n> [times]]": Key("end, enter") * Repeat(extra="n"),
        "renter down [<n> [times]]": (Key("down") * Repeat(extra="n")) + Key("end, enter"),
        "renter up [<n> [times]]": (Key("up") * Repeat(extra="n")) + Key("end, enter"),
        "crater": Mouse("left:1") + Key("end, enter"),
        "last character but <n>": Key("end") + (Key("left") * Repeat(extra="n")),
        "first character but <n>": Key("home") + (Key("right") * Repeat(extra="n")),             
        "word left [<n> [times]]": {
            "action": Key("c-left") * Repeat(extra="n"),},
        "word right [<n> [times]]": {
            "action": Key("c-right") * Repeat(extra="n"),},                
        "inner wedge": Key("enter:2, up"),
        "copy line": Key("end, s-home") + Mimic("copy"),
        "cut line": Key("end, s-home") + Mimic("cut"),
        "copy full left": Key("s-home, s-home") + Mimic("copy"),
        "delete last word [<n> [times]]": Key("end") + Key("c-left") * Repeat(extra="n") + Key("s-end, delete"),
        "delete line": Key("end, s-home, s-home") + Mimic("delete"),
        "lineless [<n> [times]]": Key("end, s-home, s-home, delete, backspace") * Repeat(extra="n"),
        "plaster": Key("c-v, enter"),
    }
    

@GrammarRule
class system_shortcuts_rule(Base.QuickContinuousRules):
    name="system_shortcuts"
    mapping={
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
