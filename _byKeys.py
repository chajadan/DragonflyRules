
# Implements the ability to capture a command typed from the keyboard, rather than by voice 

from dragonfly import (Function, MappingRule, Mimic)
import _quickRules
from _ruleExport import *
import pyHook # http://sourceforge.net/projects/pyhook/
import inspect

exports = ExportedRules()

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


@ExportedRule(exports)
class ByKeysRule(_quickRules.QuickRules):
    name="ByKeysRule"
    mapping = {
        "by keys": Function(startByKeysCommandHook),
    }