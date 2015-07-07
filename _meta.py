print "importing " + __file__
from dragonfly import *
import Base
import inspect
import time
import _globals
import _general as glib
import xmlrpclib
import natlink
import os
import win32gui
import dfconfig

CORRECTION_TRIES = 0
 
grammar = Base.ContinuousGrammar("meta grammar")
listener = Grammar("wake up grammar")
 
#decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, Base.BaseQuickRules):
            rule(grammar)
        else:
            grammar.add_rule(rule())
    else:
        grammar.add_rule(rule)


class EnableDragonfly(Base.ContinuousRule):
    spec = "(enable|load) dragonfly"
    def _process_recognition(self, node, extras):
        listener.set_exclusiveness(False)
        get_engine().speak("dragonfly alive")
listener.add_rule(EnableDragonfly())


@GrammarRule
class DisableDragonfly(Base.ContinuousRule):
    spec = "(disable|unload) dragonfly"
    def _process_recognition(self, node, extras):
        listener.set_exclusiveness(True)
        get_engine().speak("dragonfly darts off")


def ExitDragon():
    (Mimic("exit", "dragon") + Pause("100") + Key("enter")).execute()
     
def DragonMicrophoneOff():
    get_engine().natlink.setMicState('off')
     
def DragonMicrophoneOn():
    get_engine().natlink.setMicState('on')    
     
def CopyMacroFiles():
    os.system(dfconfig.macroSourceFolder + r"\deploy.bat")
    time.sleep(2)
     
def LaunchDragon():
    pass  
     
def LaunchDragonAsync(profile):
    glib.LaunchExeAsyncWithArgList(dfconfig.dragonNatSpeakPath, ["/user", profile])
              
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
        import win32con
        win32gui.ShowWindow(res, win32con.SW_SHOW)
        win32gui.SetForegroundWindow(res)
    except:
        pass


@GrammarRule
class ListRegisteredCommands(Base.ContinuousRule):
    spec = "(list|show) registered commands"
    def _process_recognition(self, node, extras):
        commands = list(Base.GlobalGrammar._commandWords)
        commands.sort()
        print commands

        
@GrammarRule
class ListRegisteredCommandIntros(Base.ContinuousRule):
    spec = "(list|show) registered partials"
    def _process_recognition(self, node, extras):
        partials = list(Base.GlobalGrammar._commandWordPartials)
        partials.sort()
        print partials

    
@GrammarRule
class CloseDragonRule(Base.RegisteredRule):
    spec = "close dragon"
    def _process_recognition(self, node, extras):
        Function(ExitDragon).execute()

@GrammarRule    
class DeployRestartHeadSetRule(Base.RegisteredRule):
    spec = "restart head set"
    def _process_recognition(self, node, extras):
        Function(DeployDragonfly_RestartHeadset).execute()
        
@GrammarRule    
class DeployRestartArrayRule(Base.RegisteredRule):
    spec = "restart array"
    def _process_recognition(self, node, extras):
        Function(DeployDragonfly_RestartArray).execute()
    
@GrammarRule     
class DeployRefreshRule(Base.RegisteredRule):
    spec = "refresh dragonfly"
    def _process_recognition(self, node, extras):
        Function(DeployDragonfly_Refresh).execute()        


def check_for_correction_response():
    global CORRECTION_TRIES
    correction = "-1"
    try:
        correction = xmlrpclib.ServerProxy("http://127.0.0.1:" + str(1338)).get_message()
    except:
        CORRECTION_TRIES += 1
        if CORRECTION_TRIES > 29:
            CORRECTION_TRIES = 0
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
        glib.LaunchExeAsyncWithArgList(dfconfig.pythonPath, [dfconfig.macroHomeFolder + r"\DragonCorrectionDialog.py", recognized_phrase])
        natlink.setTimerCallback(check_for_correction_response, 1000)

@GrammarRule
class CorrectionRule(Base.RegisteredRule):
    spec = "correction"
    saveResults = False
    def _process_recognition(self, node, extras):
        Function(DisplayTextToCorrect).execute()


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


grammar.load()
 
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None