from dragonfly import *
import  _BaseGrammars
from _BaseRules import *

grammar = _BaseGrammars.ContinuousGrammar("cmd")

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
