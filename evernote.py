from dragonfly import *
import Base
import inspect

context = AppContext(executable="evernote")
grammar = Base.ContinuousGrammar("evernote grammar", context=context)

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
class MenuRules(Base.QuickContinuousRules):
    mapping = {
        "new note": Key("c-n"),
    }

grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None