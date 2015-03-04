
# Implements the ability to capture a simple string by name, supporting lower- and uppercase letters.

# commands are:

# remember string [as] <name>   -- then type in the string, followed by the return key
# by name <name>                -- types out the named string
# clear named strings           -- forgets all named strings

from dragonfly import *
import pyHook # http://sourceforge.net/projects/pyhook/
import inspect

ruleList = []

#decorator
def ExportedRule(Rule):
    if inspect.isclass(Rule):
        ruleList.append(Rule())
    else:
        ruleList.append(Rule)

NamedStrings = {}
namedStringBuffer = ""
currentStringName = ""
isShifted = False
pyHookManager = pyHook.HookManager()

def startNamedStringsHook(stringName):
    global currentStringName
    currentStringName = stringName
    pyHookManager.HookKeyboard()

def OnKeyDown(event):
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
        NamedStrings[currentStringName] = namedStringBuffer
        # set clean initial state 
        isShifted = False 
        currentStringName = ""
        namedStringBuffer = ""
    return False

def OnKeyUp(event):
    global isShifted
    if event.Key in ["Lshift", "Rshift"]:
        isShifted = False

pyHookManager.KeyDown = OnKeyDown
pyHookManager.KeyDown = OnKeyUp

@ExportedRule
class CreateNamedString(CompoundRule):
    spec = "remember string [as] <NamedString>"
    extras = Dictation("NamedString"),
    def _process_recognition(self, node, extras):
        stringName = " ".join(extras["NamedString"].words)
        Function(startNamedStringsHook).execute({"stringName": stringName})
        
@ExportedRule
class RetrieveNamedString(CompoundRule):
    spec = "by name <NamedString>"
    extras = Dictation("NamedString"),
    def _process_recognition(self, node, extras):
        stringName = " ".join(extras["NamedString"].words)
        try:
            Text(NamedStrings[stringName]).execute()
        except:
            print "No string named " + stringName
            
@ExportedRule
class ClearNamedString(CompoundRule):
    spec = "clear named strings"
    def _process_recognition(self, node, extras):
        NamedStrings = {}