print "importing sh"
from dragonfly import *
import BaseGrammars
print "sh, GlobalGrammar id", id(BaseGrammars.GlobalGrammar)
from _BaseRules  import *

grammar_context = AppContext(executable = "sh")
grammar = BaseGrammars.GlobalGrammar("sh", context = grammar_context)


class GitBashRules(QuickRules):
    context= AppContext(title = "MINGW32"),
    name="GitBashRules"
    mapping = {
         "add all": Text("git add .") + Key("enter"),
         "add all with deletes": Text("git add -A") + Key("enter"),
         "status": Text("git status") + Key("enter"),
         "diff": Text("git diff") + Key("enter"),
         "commit": Text("git commit"),
         "commit [with] message <text>": {
            "action": Text('git commit -m "%(text)s"'),
            "intro": ["commit message", "commit with message"]},
         "push": Text("git push") + Key("enter"),
    }
    extrasDict = {
        "text": Dictation("text"),
    }

GitBashRules(grammar)
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
