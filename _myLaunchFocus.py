import BaseGrammars
print "import _myLaunchFocus"
from dragonfly import *
from BaseRules import *
import os
import collections
import inspect

grammar = BaseGrammars.ContinuousGrammar("launch and focus grammar")

executable_info_field_names = ["name", "path", "window_title"]
executable_info_list = [
    ["ACI", r"C:\Program Files (x86)\ACI32\Applications\Report32.exe", None],
    ["chrome", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", None],
    ["compiler", None, "AciCompiler ~~"],
    ["eclipse", r"C:\Program Files\eclipse\eclipse.exe",  "- Eclipse"],
    ["process Explorer", r"D:\Install Files\procexp.exe", "Process Explorer - Sysinternals"],
    ["sketch", None, "ACI Sketch"],
    ["Visual Studio", r"C:\Program Files (x86)\Microsoft Visual Studio 12.0\Common7\IDE\WDExpress.exe", None],
    ]
ExecutableInfo = collections.namedtuple("ExecutableInfo", executable_info_field_names)
executable_info = [ExecutableInfo(*values) for values in executable_info_list]

#decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, BaseQuickRules):
            rule(grammar)
        else:
            grammar.add_rule(rule())
    else:
        grammar.add_rule(rule)

@GrammarRule
class LaunchRule(ContinuousRule):
    spec = "launch <program>"
    program_choices = {exe.name: exe.path for exe in executable_info if exe.path}
    extras = (Choice("program", program_choices),)
    def _process_recognition(self, node, extras):
        StartApp(extras["program"]).execute()


@GrammarRule
class FocusRule(ContinuousRule):
    spec = "<program>"
    intro = [exe.name for exe in executable_info]
    program_choices = dict((exe.name, exe) for exe in executable_info)
    extras = (Choice("program", program_choices),)
    def _process_recognition(self, node, extras):
        exe = extras["program"]
        if exe.window_title:
            FocusWindow(title=exe.window_title).execute()
        else:
            FocusWindow(executable=os.path.basename(exe.path)).execute()


@GrammarRule
class LaunchAndFocusRules(QuickContinuousRules):
    mapping= {      
        #"compiler": FocusWindow(title="AciCompiler ~~"),
        #"launch explorer": StartApp(r"C:\Windows\Explorer.exe"),
        #"sketch": FocusWindow(title="ACI Sketch"),
        #"task manager": Key("cs-escape"),
        #"launch eclipse": StartApp(r"C:\Program Files\eclipse\eclipse.exe"),
        #"eclipse": FocusWindow(title=" - Eclipse"),
        #"launch process explorer": StartApp(r"D:\Install Files\procexp.exe"),
    }
    
grammar.load()
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None