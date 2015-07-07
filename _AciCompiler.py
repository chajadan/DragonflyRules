print "importing " + __file__
from dragonfly import *
import Base
import inspect

context = AppContext(executable="python" , title="AciCompiler ~~" )
grammar = Base.ContinuousGrammar("AciCompiler grammar", context=context)

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
class AciCompilerShortcutsRule(Base.QuickContinuousRules):
    mapping = {
        "hot word": Key("a-h"),
        "skip word": Key("a-k"),
        "save words": Key("a-s"),
        "add [new] words": Key("a-a"),
        "[view] order": Key("a-v, o"),
        "[view] work file": Key("a-v, w"),
        "[view] plat map": Key("a-v, p"),
        "[view] import notes": Key("a-v, i"),
        "[view] realist [records]": Key("a-v, r"),
        "[view] (questions|comments)": Key("a-v, q"),
        "[view] hours": Key("a-v, h"),
        "[view] report": Key("a-v, d"),
        "[view] import (folder|directory)": Key("a-v, f"),
        "new file": Key("a-f, n"),
        "save [file]": Key("a-f, s"),
        "exit": Key("a-f, x"),
        "set name": Key("a-f, t"),
    }

grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None