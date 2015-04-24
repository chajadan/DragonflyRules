
# Implements the ability to capture a simple string by name, supporting lower- and uppercase letters.

# commands are:

# remember string [as] <name>   -- then type in the string, followed by the return key
# by name <name>                -- types out the named string
# clear named strings           -- forgets all named strings

from dragonfly import *
import _BaseGrammars
import pyHook # http://sourceforge.net/projects/pyhook/
import inspect
from _BaseRules import *

grammar = _BaseGrammars.ContinuousGrammar("named strings grammar")

#decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, BaseQuickRules):
            rule(grammar)
        else:
            grammar.add_rule(rule())
    else:
        grammar.add_rule(rule)

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
    return False

pyHookManager.SubscribeKeyDown(OnKeyDown)
pyHookManager.SubscribeKeyUp(OnKeyUp)

@GrammarRule
class CreateNamedString(CorrectableRule):
    spec = "remember string [as] <NamedString>"
    intro = ["remember string", "remember string as"]
    extras = Dictation("NamedString"),
    def _process_recognition(self, node, extras):
        stringName = " ".join(extras["NamedString"].words)
        Function(startNamedStringsHook).execute({"stringName": stringName})
        
@GrammarRule
class RetrieveNamedString(CorrectableRule):
    spec = "by name <NamedString>"
    extras = Dictation("NamedString"),
    def _process_recognition(self, node, extras):
        stringName = " ".join(extras["NamedString"].words)
        try:
            Text(NamedStrings[stringName]).execute()
        except:
            print "No string named " + stringName
            
@GrammarRule
class ClearNamedString(CorrectableRule):
    spec = "clear named strings"
    def _process_recognition(self, node, extras):
        NamedStrings = {}
        
grammar.load()
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None