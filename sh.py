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
        "save commit message": Key("escape") + Text(":wq") + Key("enter"),
        
        "go to ACI Compiler": Text("cd ~/git/AciCompiler/AciCompiler/AciCompiler") + Key("enter"),
        "go to AciImporter": Text("cd ~/git/AciImporter") + Key("enter"),
        "go to chajLib": Text("cd ~/git/chajLib") + Key("enter"),
        "go to dragonfly rules": Text("cd ~/git/DragonflyRules/DragonflyRules/src") + Key("enter"),
        "go to pyChajLib": Text("cd ~/git/pyChajLib") + Key("enter"),
        
        "get add": Text("git add "),
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
        "[do [get]] diff": {
            "action":Text("git diff") + Key("enter"),
            "intro":["do get diff", "do diff", "diff"]},
        "[do [get]] push": {
            "action":Text("git push") + Key("enter"),
            "intro":["do get push", "do push", "push"]},
        "do [get] force clean": Text("git clean -f") + Key("enter"),
        "do [get] stash list": Text("git stash list") + Key("enter"),
        "[do [get]] status": {
            "action":Text("git status") + Key("enter"),
            "intro":["do get status", "do status", "status"]},
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
