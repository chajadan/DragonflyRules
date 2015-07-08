print "importing " + __file__
from dragonfly import *
import Base
import inspect

grammar_context = AppContext(executable="sh")
grammar = Base.ContinuousGrammar("sh", context=grammar_context)

gitRepositoriesPath = "/d/git/"
changeDirIntro = "cd " + gitRepositoriesPath

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
        "save commit message": Key("escape") + Text(":wq") + Key("enter"),
        
        "go to ACI Compiler": Text(changeDirIntro + "AciCompiler/AciCompiler/AciCompiler") + Key("enter"),
        "go to AciImporter": Text(changeDirIntro + "AciImporter") + Key("enter"),
        "go to chajLib": Text(changeDirIntro + "chajLib") + Key("enter"),
        "go to dragonfly rules": Text(changeDirIntro + "DragonflyRules/DragonflyRules/src") + Key("enter"),
        "go to pyChajLib": Text(changeDirIntro + "pyChajLib") + Key("enter"),
        
        "get add": Text("git add "),
        "get check out": Text("git checkout "),
        "get commit": Text("git commit "),
        "get commit amend": Text("git commit --amend "),
        "get diff": Text("git diff "),
        "get status": Text("git status "),
        "[do] [get] add content": Text("git add .") + Key("enter"),
        "[do] [get] add all changes": Text("git add -A") + Key("enter"),
        "[do] [get] add updated": Text("git add -u") + Key("enter"),        
        "do [get] clean": Text("git clean") + Key("enter"),
        "do [get] commit": Text("git commit") + Key("enter"),
        "do [get] commit amend": Text("git commit --amend ") + Key("enter"),
        "[do [get]] diff": Text("git diff") + Key("enter"),
        "[do [get]] push": Text("git push") + Key("enter"),
        "do [get] force clean": Text("git clean -f") + Key("enter"),
        "do [get] log": Text("git log") + Key("enter"),
        "do [get] stash clear": Text("git stash clear") + Key("enter"),
        "do [get] stash list": Text("git stash list") + Key("enter"),
        "[do [get]] status": Text("git status") + Key("enter"),
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
