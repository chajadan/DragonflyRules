  # -*- coding: utf-8 -*-
print "import _main"

from dragonfly import *
from dragonfly.timer import _Timer
import BaseGrammars
from BaseRules import *
import _general as glib
import _decorators as dec
import _keyboard as kb
import inspect
import _globals
import paths
import sys
sys.argv = [""]
import subprocess
import easygui
import chajLib.ui.docnav as docnav
TIMER_MANAGER = _Timer(1)

masterRunOn = BaseGrammars.ContinuousGrammar("master run on grammar")
grammar = BaseGrammars.GlobalGrammar("master non run on grammar")
listener = Grammar("wake up grammar")

# history = RecognitionHistory()
# history.register()
# 
# class ROD(RecognitionObserver):
#     def on_begin(self):
#         print "on_begin, history:", history
#     def on_recognition(self, words):
#         print "on_recognition:", words
#     def on_failure(self):
#         print "on_failure"
# rod = ROD()
# rod.register()


class EnableDragonfly(ContinuousRule):
    spec = "(enable|load) dragonfly"
    def _process_recognition(self, node, extras):
        listener.set_exclusiveness(False)
        get_engine().speak("dragonfly alive")
listener.add_rule(EnableDragonfly())


# Clipboard _support
clip = Clipboard()

#decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, (QuickChainedRules, QuickRules)):
            rule(grammar)
        elif issubclass(rule, (QuickContinuousRules)):
            rule(masterRunOn)
        elif issubclass(rule, ContinuousGrammarRule):
            masterRunOn.add_rule(rule())
        elif issubclass(rule, (Rule, MappingRule, CompoundRule)):
            grammar.add_rule(rule())
        else:
            raise TypeError("Unexpected rule type added to grammar: " + str(inspect.getmro(rule)))
    else:
        grammar.add_rule(rule)


# @GrammarRule
# class FreeFormSpeech(ContinuingRule):
#     spec = "<RunOn>"
#     intro = "~chajBlankchaj~"
#     extras = (Dictation("RunOn"),)
#     def _process_recognition(self, node, extras):
#         Text(extras["RunOn"].format()).execute()


@GrammarRule
class DisableDragonfly(ContinuousRule):
    spec = "(disable|unload) dragonfly"
    def _process_recognition(self, node, extras):
        listener.set_exclusiveness(True)
        get_engine().speak("dragonfly darts off")


@GrammarRule
class SomeQuickRules(QuickContinuousRules):
    name="GlobalQuickRules"
    extrasDict = {
        "keyCount": IntegerRef("keyCount", 1, 1000),
        "n": IntegerRef("n", 1, 10000),
        "clickCount": IntegerRef("clickCount", 1, 1000),
        "lineCount": IntegerRef("lineCount", 1, 1000),
        "text": Dictation("text"),
        "chain": Dictation("chain"),
    }
    defaultsDict = {
        "n": 1,
        "keyCount": 1,
        "clickCount": 1,
        "lineCount": 1,
    }    
    mapping= {      
        "(click|mouse) [<clickCount> [times]]": Mouse("left:1") * Repeat(extra="clickCount"),
        "click paste": Mouse("left:1") + Key("c-v"),
        "control click [<clickCount> [times]]": (Key("ctrl:down") + Mouse("left:1") + Key("ctrl:up")) * Repeat(extra="clickCount"),
        "right click [<clickCount> [times]]": Mouse("right:1") * Repeat(extra="clickCount"),            
        "middle click [<clickCount> [times]]": Mouse("middle:1") * Repeat(extra="clickCount"),
        "double click": Mouse("left:2"),
        "shift down": Key("shift:down"),
        "shift up": Key("shift:up"),
        "shift click": Key("shift:down") + Mouse("left:1") + Key("shift:up"),
        "shift right click": Key("shift:down") + Mouse("right:1") + Key("shift:up"),
        "down click": Mouse("left:down"),
        "up click": Mouse("left:up"),
        "down right click": Mouse("right:down"),
        "up right click": Mouse("right:up"),
        "[toggle] flux": Key("a-end"),         
    }


import Tkinter as tk
import tkMessageBox
root = None
entryWidget = None

def SubmitCorrection():
    global root
    global entryWidget
    results = _globals.lastSavedResults
    words = results.getWords(0)
    recognized_phrase = " ".join(words)    
    correction = entryWidget.get()
    if correction is not None and correction != recognized_phrase:
        corrected_words = correction.split()
        status = results.correction(corrected_words)
        print "Correction status is", status    
    root.destroy()
    root = None

import xmlrpclib
import natlink
TRIES = 0

def check_for_correction_response():
    global TRIES
    correction = "-1"
    try:
        correction = xmlrpclib.ServerProxy("http://127.0.0.1:" + str(1338)).get_message()
    except:
        TRIES+=1
        if TRIES>29:
            TRIES=0
            #TIMER_MANAGER.remove_callback(check_for_correction_response)
            natlink.setTimerCallback(None, 0)
            return
    
    if correction == "-1":
        return
    
    if hasattr(_globals, "lastSavedResults") and _globals.lastSavedResults is not None:
        results = _globals.lastSavedResults
        corrected_words = correction.split()
        status = results.correction(corrected_words)
        print "Correction status is", status
        natlink.setTimerCallback(None, 0)        
    else:
        #TIMER_MANAGER.remove_callback(check_for_correction_response)
        natlink.setTimerCallback(None, 0)
        return   
         
def DisplayTextToCorrect():
    if getattr(_globals, "lastSavedResults", None) is None:
        print "No results to correct..."
    if hasattr(_globals, "lastSavedResults") and _globals.lastSavedResults is not None:
        results = _globals.lastSavedResults
        words = results.getWords(0)
        recognized_phrase = " ".join(words)
        glib.LaunchExeAsyncWithArgList("C:\\Python27_32bit\\python.exe", ["C:\\NatLink\\NatLink\\MacroSystem\\DragonCorrectionDialog.py", recognized_phrase])
        natlink.setTimerCallback(check_for_correction_response, 1000)

@GrammarRule
class CorrectionRule(RegisteredRule):
    spec = "correction"
    saveResults = False
    def _process_recognition(self, node, extras):
        Function(DisplayTextToCorrect).execute()

@GrammarRule
class QuickCRules(QuickContinuousRules):
    mapping = {
        "(in quotes|string it)": Text("\"\"") + Key("left"),
        "in brackets": Text("[]") + Key("left"),
        "in apostrophes": Text("''") + Key("left"),
        "brackets": Text("[]"),
        "angle brackets": Text("<>"),
        "parentheses": Text("()"),
        "in curly brackets": Text("{}") + Key("left"),
        "in angle brackets": Text("<>") + Key("left"),
        "call with": Text("()") + Key("left"),
        "call": Text("()"),
        "spinster": Text("()") + Key("enter"),
        "item": Text(", "),
        "assign": Text(" = "),
        "dereference": Text("->"),
        "dot": Key("dot"),
        "trim left": Key("s-home, delete"),
        "trim right": Key("s-end, delete"),
    }

          
def ReplaceAllInSelection(toReplace, replaceWith):
    toReplace = toReplace.lower()
    kb.copy()
    clip.copy_from_system(formats=Clipboard.format_text)
    selection = clip.get_text().lower()
    Text(selection.replace(toReplace, replaceWith)).execute()
    
@GrammarRule
class ReplaceAllInSelectionRule(RegisteredRule):
    spec = "replace selection <toReplace> with <replaceWith>"
    extras = (Dictation("toReplace"), Dictation("replaceWith"))
    def _process_recognition(self, node, extras):
        toReplace = extras["toReplace"].format()
        replaceWith = extras["replaceWith"].format()
        Function(ReplaceAllInSelection).execute({"toReplace": toReplace, "replaceWith": replaceWith})
 
def ReplaceAllInLine(toReplace, replaceWith, sensitive = True):
    pass
#     kb.sendHome()
#     kb.sendEnd()
#     kb.sendShiftHome()
#     line = ReadSelection()
#     if not sensitive:
#         toReplace = toReplace.lower()
#     Text(selection.replace(toReplace, replaceWith)).execute()

@GrammarRule
class ReplaceAllInLineRule(RegisteredRule):
    spec = "replace line <toReplace> with <replaceWith>"
    extras = (Dictation("toReplace"), Dictation("replaceWith"))
    def _process_recognition(self, node, extras):
        toReplace = extras["toReplace"].format()
        replaceWith = extras["replaceWith"].format()
        Function(ReplaceAllInLine).execute({"toReplace": toReplace, "replaceWith": replaceWith})

        
@GrammarRule
class FullScreenToIrfanView(ContinuousRule):
    spec = "screen to image"
    def _process_recognition(self, node, extras):
        kb.sendPrintScreen()
        action = StartApp(paths.IRFANVIEW_PATH) + Pause("50") + Key("c-v")
        action.execute()

@GrammarRule
class WindowToIrfanView(ContinuousRule):
    spec = "window to image"
    def _process_recognition(self, node, extras):
        kb.sendAltPrintScreen()
        action = StartApp(paths.IRFANVIEW_PATH) + Pause("50") + Key("c-v")
        action.execute()


@GrammarRule
class ClipboardToIrfanView(ContinuousRule):
    spec = "clipboard to image"
    def _process_recognition(self, node, extras):
        action = StartApp(paths.IRFANVIEW_PATH) + Pause("50") + Key("c-v")
        action.execute()


@GrammarRule
class InterDocNavRules(QuickContinuousRules):
    name="inter_doc_nav"
    extrasDict = {
        "keyCount": IntegerRef("keyCount", 1, 1000),
        "n": IntegerRef("n", 1, 1000),
        "text": Dictation("text"),
    }
    defaultsDict = {
        "keyCount": 1,
        "n": 1,
    }    
    mapping = {
        "renter [<n> [times]]": Key("end, enter") * Repeat(extra="n"),
        "renter down [<n> [times]]": (Key("down") * Repeat(extra="n")) + Key("end, enter"),
        "renter up [<n> [times]]": (Key("up") * Repeat(extra="n")) + Key("end, enter"),
        "crater": Mouse("left:1") + Key("end, enter"),
        "last character but <n>": Key("end") + (Key("left") * Repeat(extra="n")),
        "first character but <n>": Key("home") + (Key("right") * Repeat(extra="n")),             
        "word left [<n> [times]]": {
            "action": Key("c-left") * Repeat(extra="n"),},
        "word right [<n> [times]]": {
            "action": Key("c-right") * Repeat(extra="n"),},                
        "inner wedge": Key("enter:2, up"),
        "copy line": Key("end, s-home") + Mimic("copy"),
        "cut line": Key("end, s-home") + Mimic("cut"),
        "copy full left": Key("s-home, s-home") + Mimic("copy"),
        "delete last word [<n> [times]]": Key("end") + Key("c-left") * Repeat(extra="n") + Key("s-end, delete"),
        "delete line": Key("end, s-home, s-home") + Mimic("delete"),
        "lineless [<n> [times]]": Key("end, s-home, s-home, delete, backspace") * Repeat(extra="n"),
        "plaster": Key("c-v, enter"),
    }
    

@GrammarRule
class system_shortcuts_rule(QuickContinuousRules):
    name="system_shortcuts"
    mapping={
             "save": Key("c-s"),
             "copy": Key("c-c"),
             "(paste|from clip|from clipboard)": Key("c-v"),
             "cut": Key("c-x"),
             "top": Key("c-home"),
             "bottom": Key("c-end"),
             "tab windows": Key("alt:down, tab:down"),
             "go to tab <n>": (Key("right") * Repeat(extra="n")) + Key("alt:up, tab:up"),
             "last window": Key("a-tab"),
             "undo": Key("c-z"),
             "find": Key("c-f"),
             "desktop": Key("w-d"),
             "dock left": Key("w-left"),
             "dock left twice": Key("w-left") * Repeat(2),
             "dock right": Key("w-right"),
             "dock right twice": Key("w-right") * Repeat(2),
             "hide [(others | other windows)]": {
                "action": Key("w-home"),
                "intro": ["hide", "hide others", "hide other windows"]},
             "minimize": Key("w-down") * Repeat(2),
             "maximize": Key("w-up"),
             "close window": Key("a-f4"),
            }
    extrasDict = {
        "keyCount": IntegerRef("keyCount", 1, 1000),
        "n": IntegerRef("n", 0, 1000),
    }
    defaultsDict = {
        "keyCount": 1,
        "n": 1,
    }

grammar.load()
masterRunOn.load()
listener.load()
print "grammar loaded"
    
# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    global listener
    global masterRunOn
    if grammar: grammar.unload()
    grammar = None
    if listener: listener.unload()
    listener = None
    if masterRunOn: masterRunOn.unload()
    masterRunOn = None
