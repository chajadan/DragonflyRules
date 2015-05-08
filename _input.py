print "import _input"
from dragonfly import *
import input_conversion as conv
import Base
import inspect

grammar = Base.ContinuousGrammar("input elements and sequences grammar")


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
class NumbersRule(Base.ContinuousRule):
    spec = "digits <digits>"
    extras = (Repetition(Choice("digit", choices=conv._digits), name="digits", min=1, max=50),)
    def _process_recognition(self, node, extras):
        digits = map(str, extras["digits"])
        Text("".join(digits)).execute()


grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None