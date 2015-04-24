print "importing _meta"
from dragonfly import *
import BaseGrammars
print "_meta, GlobalGrammar id", id(BaseGrammars.GlobalGrammar)
from _BaseRules import *
import inspect
import time
import _general as glib
import os
import win32ui
import win32gui
 
grammar = BaseGrammars.ContinuousGrammar("meta grammar")
 
#decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, BaseQuickRules):
            rule(grammar)
        else:
            grammar.add_rule(rule())
    else:
        grammar.add_rule(rule)
 

def ExitDragon():
    (Mimic("exit", "dragon") + Pause("100") + Key("enter")).execute()
     
def DragonMicrophoneOff():
    get_engine().natlink.setMicState('off')
     
def DragonMicrophoneOn():
    get_engine().natlink.setMicState('on')    
     
def CopyMacroFiles():
    os.system(r"C:\Users\chajadan\git\DragonflyRules\DragonflyRules\src\deploy.bat")
    time.sleep(2)
     
def LaunchDragon():
    pass  
     
def LaunchDragonAsync(profile):
    glib.LaunchExeAsyncWithArgList(r"C:\Program Files (x86)\Nuance\NaturallySpeaking13\Program\natspeak.exe", ["/user", profile])
    #glib.RunBatchFileAsync(r"C:\Users\chajadan\git\DragonflyRules\DragonflyRules\src\startDragon.bat")
    #import thread
    #thread.start_new_thread(LaunchDragon(), ())
              
def DeployDragonfly_Restart():
    ExitDragon()
    CopyMacroFiles()
    
def DeployDragonfly_RestartHeadset():
    DeployDragonfly_Restart()
    LaunchDragonAsync("Charles J. Daniels")

def DeployDragonfly_RestartArray():
    DeployDragonfly_Restart()
    LaunchDragonAsync("Superbeam")
 
def DeployDragonfly_Refresh():
    DragonMicrophoneOff()
    CopyMacroFiles()
    DragonMicrophoneOn()
    try:
        res = win32gui.FindWindow(None, "Messages from NatLink - built 01/01/2014")
        win32gui.SetForegroundWindow(res)
    except:
        pass

@GrammarRule
class ListRegisteredIntros(ContinuousRule):
    spec = "list registered rules"
    def _process_recognition(self, node, extras):
        print "id", id(BaseGrammars.GlobalGrammar)
        print BaseGrammars.GlobalGrammar._commandWords
    
@GrammarRule
class CloseDragonRule(RegisteredRule):
    spec = "close dragon"
    def _process_recognition(self, node, extras):
        Function(ExitDragon).execute()

@GrammarRule    
class DeployRestartHeadSetRule(RegisteredRule):
    spec = "restart head set"
    def _process_recognition(self, node, extras):
        Function(DeployDragonfly_RestartHeadset).execute()
        
@GrammarRule    
class DeployRestartArrayRule(RegisteredRule):
    spec = "restart array"
    def _process_recognition(self, node, extras):
        Function(DeployDragonfly_RestartArray).execute()
    
@GrammarRule     
class DeployRefreshRule(RegisteredRule):
    spec = "refresh dragonfly"
    def _process_recognition(self, node, extras):
        Function(DeployDragonfly_Refresh).execute()        
     

grammar.load()
 
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None