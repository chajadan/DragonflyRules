from dragonfly import *
import Base
import inspect

grammar = Base.ContinuousGrammar("file extensions grammar")

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
class PrefixedKeypressRule(Base.ContinuousRule):
    spec = "extension <ext>"
    extensions = {
        "Python": "py",
        "text": "txt",
        "see plus plus": "cpp",
        "header file": "h",
    }
    extras = (Choice("ext", {name: extension for name, extension in extensions.items()}),)
    def _process_recognition(self, node, extras):
        Text("." + extras["ext"]).execute()

grammar.load()
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None