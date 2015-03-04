from dragonfly import *

grammar_context = AppContext(executable = "sh")
grammar = Grammar("sh")

GitBashRules = MappingRule(
    context= AppContext(title = "MINGW32"),
    name="static",
    mapping={
             "add all": Text("git add .") + Key("enter"),
             "add all with deletes": Text("git add -A") + Key("enter"),
             "status": Text("git status") + Key("enter"),
             "diff": Text("git diff") + Key("enter"),
             "commit": Text("git commit"),
             "commit [[with] message] <text>": Text('git commit -m "%(text)s"'),
             "push": Text("git push") + Key("enter"),
            },
    extras = [
        Dictation("text"),
    ]
    )


grammar.add_rule(GitBashRules)
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
