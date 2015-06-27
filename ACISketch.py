from dragonfly import *
from BaseRules import *
import BaseGrammars
import inspect
import ctypes
AciAware = ctypes.cdll.LoadLibrary(r"C:\Users\chajadan\git\AciImporter\Release\AciAware.dll");
grammar_context = AppContext(executable="ACISketch")
grammar = BaseGrammars.GlobalGrammar("ACISketch", context=grammar_context)

# decorator
def GrammarRule(Rule):
    if inspect.isclass(Rule):
        if issubclass(Rule, BaseQuickRules):
            Rule(grammar)
        else:
            grammar.add_rule(Rule())
    else:
        grammar.add_rule(Rule)

def GoToFirstPage():
    AciAware.GoToFirstPage()

@GrammarRule
class AddSingleLabel(RegisteredRule):
    spec = "label <RunOn>"
    extras = (Dictation("RunOn"),)
    def _process_recognition(self, node, extras):
        AciAware.AciSketch_AddLabelAtMouseHover.argtypes = [ctypes.c_wchar_p]
        words = extras["RunOn"].words
        for i, word in enumerate(words):
            words[i] = word.capitalize()
        label = " ".join(words)
        AciAware.AciSketch_AddLabelAtMouseHover(label)
        
@GrammarRule
class AddMultiLabel(RegisteredRule):
    spec = "multi label <RunOn>"
    extras = (Dictation("RunOn"),)
    def _process_recognition(self, node, extras):
        AciAware.AciSketch_AddMultiLabelAtMouseHover.argtypes = [ctypes.c_wchar_p]
        words = extras["RunOn"].words
        for i, word in enumerate(words):
            words[i] = word.capitalize()
        label = " ".join(words)
        AciAware.AciSketch_AddMultiLabelAtMouseHover(label)        

@GrammarRule
class AciSketchRules(QuickContinuousRules):
    mapping = {
        "show labels": Key("alt, v, l"),
    }
    extrasDict = {
    }
    defaultsDict = {
    }

grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None