from dragonfly import *
from _quickRules import *
import inspect
import ctypes
AciAware = ctypes.cdll.LoadLibrary(r"C:\Users\chajadan\git\AciImporter\Release\AciAware.dll");
grammar_context = AppContext(executable="Report32")
grammar = Grammar("ACI", context=grammar_context)

# decorator
def GrammarRule(Rule):
    if inspect.isclass(Rule):
        if issubclass(Rule, QuickChainedRules):
            Rule(grammar)
        else:
            grammar.add_rule(Rule())
    else:
        grammar.add_rule(Rule)

def GoToFirstPage():
    AciAware.GoToFirstPage()

@GrammarRule
class AciChainedRules(QuickChainedRules):
    mapping = {
    "to do": Text("??"),
    "next item": Key("enter") + Text("- "),
    "new item": Text("- "),
    "next page": Key("c-pgdown"),
    "launch sketch": Key("a-t, d, 1"),
    "import pics": Key("a-t, i") + Pause("200") + Mouse("(22,101), left:1"),
    "import flood map": Key("a-s, a, right, 3"),
    "first page": Key("a-v, 6, enter"),
    "hex": Key("f3"),
    "delete this comp": Key("c-z") + Pause("30") + Key("enter"),
    "import field": Key("a-e, e, f"),
    "import section": Key("a-e, e, s"),
    "view image": Mouse("right:1") + Key("down:2, enter"),
    "delete image": Mouse("right:1") + Key("down:3, enter"),    
    "go to first page": Function(GoToFirstPage),
}

grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
