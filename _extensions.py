print "importing " + __file__
from dragonfly import *
import Base
import inspect
from decorators import ActiveGrammarRule

grammar = Base.ContinuousGrammar("file extensions grammar")
              
@ActiveGrammarRule(grammar)
class PrefixedKeypressRule(Base.QuickContinuousRules):
    extensions = {
        "Python": "py",
        "text": "txt",
        "see plus plus": "cpp",
        "header file": "h",
    }    
    mapping = {
        "[with|give] extension <extension>": Text(".%(extension)s"),
        "[the] extension [for] <extension>": Text(".%(extension)s"),
    }
    extrasDict = {
        "extension": Choice("extension", {name: extension for name, extension in extensions.items()})
    }

grammar.load()
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None