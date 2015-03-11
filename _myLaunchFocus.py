from dragonfly import *
from _ruleExport import *
import  _quickRules

exports = ExportedRules()

@ExportedRule(exports)
class LaunchAndFocusRules(_quickRules.QuickContinuousRules):
    name="LaunchAndFocusRules"
    extrasDict = {
    }
    defaultsDict = {
    }    
    mapping= {      
        "compiler": FocusWindow(title="AciCompiler"),
        "launch explorer": StartApp(r"C:\Windows\Explorer.exe"),
        "sketch": FocusWindow(title="ACI Sketch"),
        "task manager": Key("cs-escape"),
        "launch chrome": StartApp(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        "chrome": FocusWindow(executable="chrome"),
        "launch eclipse": StartApp(r"C:\Program Files\eclipse\eclipse.exe"),
        "eclipse": FocusWindow(executable="javaw", title="Eclipse"),
        "launch ACI": StartApp(r"C:\Program Files (x86)\ACI32\Applications\Report32.exe"),
        "ACI": FocusWindow(executable="Report32"),
        "launch Visual Studio": StartApp(r"C:\Program Files (x86)\Microsoft Visual Studio 12.0\Common7\IDE\WDExpress.exe"),
        "Visual Studio": FocusWindow(executable="WDExpress.exe")   
    }