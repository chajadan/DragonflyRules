print "importing _extensions"
from dragonfly import *
import BaseGrammars
print "_extensions, GlobalGrammar id", id(BaseGrammars.GlobalGrammar)
from _BaseRules import *

grammar = BaseGrammars.ContinuousGrammar("file extensions grammar")

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
class PrefixedKeypressRule(ContinuousRule):
    spec = "extension <ext>"
    extensions = {
        "Python": "py",
        "text": "txt",
    }
    extras = (Choice("ext", {name: extension for name, extension in extensions.items()}),)
    def _process_recognition(self, node, extras):
        Text(extras["ext"]).execute()

grammar.load()
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None