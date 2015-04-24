from dragonfly import *
import  _BaseGrammars
from _BaseRules import *

eclipse_context = AppContext(executable = "eclipse", title = "Eclipse")
grammar = _BaseGrammars.ContinuousGrammar("eclipse grammar", context = eclipse_context)

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
        "new file": Key("a-f, n, down:6"),
        "next view": Key("c-f7"),
        "save all": Key("cs-s"),
        "toggle comment": Key("c-slash"),
    }


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