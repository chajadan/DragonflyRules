from dragonfly import *
import BaseGrammars
from BaseRules import *

eclipse_context = AppContext(executable = "eclipse", title = "Eclipse")
grammar = BaseGrammars.ContinuousGrammar("eclipse grammar", context = eclipse_context)

#decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, BaseQuickRules):
            rule(grammar)
        else:
            grammar.add_rule(rule())
    else:
        grammar.add_rule(rule)


@GrammarRule
class EclipseShortcuts(QuickContinuousRules):
    mapping = {
        "global find": Key("c-h"),
        "new file": Key("a-f, n, down:6"),
        "next view": Key("c-f7"),
        "next tab [<n> [times]]": Key("c-pgdown") * Repeat(extra="n"),
        "previous tab [<n> [times]]": Key("c-pgup") * Repeat(extra="n"),
        "save all": Key("cs-s"),
        "toggle comment": Key("c-slash"),
        "switch workspace": Key("a-f, w"),
    }
    extrasDict = {"n": IntegerRef("n", 1, 20)}
    defaultsDict = {"n": 1}


@GrammarRule
class EclipseRules(QuickContinuousRules):
    mapping = {
        "go to line <n>": Key("c-l") + Text("%(n)s") + Key("enter"),
    }
    extrasDict = {"n": IntegerRef("n", 1, 100000)}
    defaultsDict = {"n": 1}
    

grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None