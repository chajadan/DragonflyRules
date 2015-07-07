print "importing " + __file__
from dragonfly import *
import Base
import inspect
import ctypes
import dfconfig
AciAware = ctypes.cdll.LoadLibrary(dfconfig.aciAwareDllPath);
grammar_context = AppContext(executable="ACISketch")
grammar = Base.GlobalGrammar("ACISketch", context=grammar_context)

# decorator
def GrammarRule(Rule):
    if inspect.isclass(Rule):
        if issubclass(Rule, Base.BaseQuickRules):
            Rule(grammar)
        else:
            grammar.add_rule(Rule())
    else:
        grammar.add_rule(Rule)

def GoToFirstPage():
    AciAware.GoToFirstPage()

@GrammarRule
class AddSingleLabel(Base.RegisteredRule):
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
class AddMultiLabel(Base.RegisteredRule):
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
class AciSketchRules(Base.QuickContinuousRules):
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