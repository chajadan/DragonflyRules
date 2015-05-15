from dragonfly import *
import Base
import inspect

grammar_context = AppContext(executable="sh")
grammar = Base.ContinuousGrammar("sh", context=grammar_context)


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
class GitBashRules(Base.QuickContinuousRules):
    context= AppContext(title = "MINGW32"),
    name="GitBashRules"
    mapping = {
        "add all": Text("git add .") + Key("enter"),
        "add all with deletes": Text("git add -A") + Key("enter"),
        "add updated": Text("git add -u") + Key("enter"),
        "status": Text("git status") + Key("enter"),
        "diff": Text("git diff") + Key("enter"),
        "commit": Text("git commit"),
        "push": Text("git push") + Key("enter"),
        "go to ACI Compiler": Text("cd ~/git/AciCompiler/AciCompiler/AciCompiler") + Key("enter"),
        "go to AciImporter": Text("cd ~/git/AciImporter") + Key("enter"),
        "go to dragonfly rules": Text("cd ~/git/DragonflyRules/DragonflyRules/src") + Key("enter"),
        "go to pyChajLib": Text("cd ~/git/pyChajLib") + Key("enter"),
        "do git clean": Text("git clean") + Key("enter"),
        "do force git clean": Text("git clean -f") + Key("enter"),
        "undo last commit": Text("git reset --soft HEAD~1") + Key("enter"),
    }
    extrasDict = {
        "text": Dictation("text"),
    }


@GrammarRule
class GitCommitWithMessage(Base.ContinuousRule_EatDictation):
    spec = "commit [with] message"
    def _process_recognition(self, node, extras):
        action = Text("git commit -m ''") + Key("left")
        if "RunOn" in extras:
            message = " ".join(extras["RunOn"].words)
            action += Text(message)
        action.execute()


grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
