from dragonfly import *
import Base
import inspect
from chajLib.ui import docnav

grammar = Base.ContinuousGrammar("text buffer manipulations grammar")

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
class CaretCalls(Base.QuickContinuousCalls):
    mapping = [
        ["after left <RunOn>", docnav.caret_after_left, "target"],
        ["after right <RunOn>", docnav.caret_after_right, "target"],
        ["before left <RunOn>", docnav.caret_before_left, "target"],
        ["before right <RunOn>", docnav.caret_before_right, "target"],
    ]
    
@GrammarRule
class SelectCalls(Base.QuickContinuousCalls):
    mapping = [
        ["select left through <RunOn>", docnav.select_through_left, "target"],
        ["select right through <RunOn>", docnav.select_through_right, "target"],
    ]


grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None