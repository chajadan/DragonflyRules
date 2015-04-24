print "importing cmd"
from dragonfly import *
import BaseGrammars
print "cmd, GlobalGrammar id", id(BaseGrammars.GlobalGrammar)
from _BaseRules import *

grammar = BaseGrammars.ContinuousGrammar("cmd")

class CmdRules(QuickContinuousRules):
    mapping={
        "paste": Key("a-space, e, p"),
        "repeat last": Key("up, enter"),
        "interrupt": Key("c-c"),
        "change directory": Text("cd "),
        "list": Text("dir") + Key("enter"),
    }
CmdRules(grammar)
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
