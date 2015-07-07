print "importing " + __file__
from dragonfly import *
import Base
from decorators import ActiveGrammarRule

grammar = Base.ContinuousGrammar("cmd", AppContext(executable="cmd"))

@ActiveGrammarRule(grammar)
class CmdRules(Base.QuickContinuousRules):
    mapping = {
        "paste": Key("a-space, e, p"),
        "repeat last": Key("up, enter"),
        "interrupt": Key("c-c"),
        "change directory": Text("cd "),
        "list": Text("dir") + Key("enter"),
    }
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
