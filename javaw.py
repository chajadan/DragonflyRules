from dragonfly import *

eclipse_context = AppContext(executable = "javaw", title = "eclipse")
grammar = Grammar("javaw_grammar", context = eclipse_context)

#decorator
def GrammarRule(RuleClass):
    grammar.add_rule(RuleClass())

@GrammarRule
class GoToLineRule(CompoundRule):
    spec = "go to line <n>"
    extras = IntegerRef("n", 0, 50000),
    def _process_recognition(self, node, extras):
        (Key("c-l") + Text(str(extras["n"])) + Key("enter")).execute()   

@GrammarRule
class EclipseShortcuts(MappingRule):
    name = "eclipse_shortcuts"
    mapping = {
        "new file": Key("a-f, n, down:6"),
        "next view": Key("c-f7"),
        "save all": Key("cs-s"),
        "toggle comment": Key("c-slash"),
    }

grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None