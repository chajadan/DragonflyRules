"""
Alternative ways to issue commands
"""
print "importing " + __file__
from dragonfly import *
import Base
from decorators import ActiveGrammarRule
import pyHook # http://sourceforge.net/projects/pyhook/
 
grammar = Base.ContinuousGrammar("alternate commands grammar")
 
 
pyHookManager = pyHook.HookManager()
byKeysCommandBuffer = ""
NamedStrings = {}
namedStringBuffer = ""
currentStringName = ""
isShifted = False
 
 
def OnKeyDown_ByKeys(event):
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

 
def OnKeyDown_NamedString(event):
    global namedStringBuffer
    global currentStringName
    global isShifted
    if len(event.Key) == 1:
        character = chr(event.Ascii)
        if isShifted:
            character = character.upper()
        namedStringBuffer += character
    elif event.Key == "Space":
        namedStringBuffer += " "
    elif event.Key in ["Lshift", "Rshift"]:
        isShifted = True
    elif event.Key == "Return":
        pyHookManager.UnhookKeyboard()
        pyHookManager.KeyDown = None
        pyHookManager.KeyUp = None
        NamedStrings[currentStringName] = namedStringBuffer
        # set clean initial state 
        isShifted = False 
        currentStringName = ""
        namedStringBuffer = ""
    return False
 
 
def OnKeyUp_NamedString(event):
    global isShifted
    if event.Key in ["Lshift", "Rshift"]:
        isShifted = False
    return False
 
 
def startByKeysCommandHook():
    pyHookManager.KeyDown = OnKeyDown_ByKeys
    pyHookManager.Keyup = None
    pyHookManager.HookKeyboard()
 
     
def startNamedStringsHook(stringName):
    global currentStringName
    currentStringName = stringName
    pyHookManager.KeyDown = OnKeyDown_NamedString
    pyHookManager.Keyup = OnKeyUp_NamedString
    pyHookManager.HookKeyboard()
 
 
@ActiveGrammarRule(grammar)
class ByKeysRule(Base.ContinuousRule):
    spec = "by keys"
    def _process_recognition(self, node, extras):
        Function(startByKeysCommandHook).execute()
 
 
@ActiveGrammarRule(grammar)
class CreateNamedString(Base.CorrectableRule):
    spec = "remember string [as] <NamedString>"
    extras = Dictation("NamedString"),
    def _process_recognition(self, node, extras):
        stringName = " ".join(extras["NamedString"].words)
        Function(startNamedStringsHook).execute({"stringName": stringName})
         
@ActiveGrammarRule(grammar)
class RetrieveNamedString(Base.CorrectableRule):
    spec = "by name <NamedString>"
    extras = Dictation("NamedString"),
    def _process_recognition(self, node, extras):
        stringName = " ".join(extras["NamedString"].words)
        try:
            Text(NamedStrings[stringName]).execute()
        except:
            print "No string named " + stringName
             
@ActiveGrammarRule(grammar)
class ClearNamedString(Base.CorrectableRule):
    spec = "clear named strings"
    def _process_recognition(self, node, extras):
        NamedStrings = {}
 
grammar.load()
 
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None