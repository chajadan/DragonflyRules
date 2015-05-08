# Implements the ability to capture a command typed from the keyboard, rather than by voice 

from dragonfly import *
import BaseGrammars
from BaseRules import *
import inspect
import pyHook # http://sourceforge.net/projects/pyhook/

grammar = BaseGrammars.ContinuousGrammar("by keys grammar")

#decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, BaseQuickRules):
            rule(grammar)
        else:
            grammar.add_rule(rule())
    else:
        grammar.add_rule(rule)

byKeysCommandBuffer = ""
pyHookManager = pyHook.HookManager()

def startByKeysCommandHook():
    pyHookManager.HookKeyboard()

def OnKeyDown(event):
    global byKeysCommandBuffer
    if len(event.Key) == 1:
        byKeysCommandBuffer += event.Key
    elif event.Key == "Space":
        byKeysCommandBuffer += " "
    elif event.Key == "Return":
        pyHookManager.UnhookKeyboard()
        words = byKeysCommandBuffer.lower().split()
        byKeysCommandBuffer = ""
        Mimic(*words).execute()
    return False

pyHookManager.KeyDown = OnKeyDown

@GrammarRule
class ByKeysRule(ContinuousRule):
    name="ByKeysRule"
    spec = "by keys"
    def _process_recognition(self, node, extras):
        Function(startByKeysCommandHook).execute()

grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None