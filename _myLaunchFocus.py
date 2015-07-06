import BaseGrammars
print "import _myLaunchFocus"
from dragonfly import *
from BaseRules import *
import os
import collections
import inspect

grammar = BaseGrammars.ContinuousGrammar("launch and focus grammar")

executable_info_field_names = ["name", "path", "window_title", "launch_args"]
executable_info_list = [
    ["ACI", r"C:\Program Files (x86)\ACI32\Applications\Report32.exe", None, None],
    ["AciCompiler", None, "AciCompiler ~~", [r"C:\Python27_10_32bit\python.exe", r"D:\git\AciCompiler\AciCompiler\AciCompiler\AciCompiler.py"]],
    ["chrome", r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", None, None],
    ["command window", r"C:\Windows\System32\cmd.exe", "Windows Command Processor", None],
    ["compiler", None, "AciCompiler ~~", [r"C:\Python27_10_32bit\python.exe", r"D:\git\AciCompiler\AciCompiler\AciCompiler\AciCompiler.py"]],
    ["eclipse", r"D:\eclipse\eclipse.exe",  "- Eclipse", None],
    ["get bash", None, "MINGW32:/", [r"C:\Program Files (x86)\Git\bin\sh.exe", "--login", "-i"]],
    ["pdfsam", r"C:\Program Files (x86)\PDF Split And Merge Basic\pdfsam-starter.exe", "PDF Split and Merge basic", None],
    ["process Explorer", r"F:\Install Files\procexp.exe", "Process Explorer - Sysinternals", None],
    ["sketch", None, "ACI Sketch", None],
    ["Visual Studio", r"C:\Program Files (x86)\Microsoft Visual Studio 14.0\Common7\IDE\devenv.exe", None, None],
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
    intro = ["launch " + exe.name for exe in executable_info if exe.path is not None]
    program_choices = {exe.name: first_not_none(exe.path, exe.launch_args) for exe in executable_info if exe.path or exe.launch_args}
    extras = (Choice("program", program_choices),)
    def _process_recognition(self, node, extras):
        if isinstance(extras["program"], (list,tuple)):
            StartApp(*extras["program"]).execute()
        else:
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