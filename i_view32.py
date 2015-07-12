print "importing " + __file__
from dragonfly import *
import Base
import inspect
import win32gui
import chajLib.ui.keyboard as kb
from chajLib.ui import docnav

grammar = Base.ContinuousGrammar("IrfanView grammar", context=AppContext(executable="i_view32"))

#decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, Base.BaseQuickRules):
            rule(grammar)
        else:
            grammar.add_rule(rule())
    else:
        grammar.add_rule(rule)


# @GrammarRule
# class FlipDimensionsRule(Base.ContinuousRule):
#     spec = "flip dimensions"
#     def _process_recognition(self, node, extras):
#         kb.sendCtrlKey(kb.KEY_R)
#         hDlg = win32gui.FindWindow(None, "Resize/Resample image")
#         hButton = win32gui.FindWindowEx(hDlg, None, "BUTTON", "Preserve &aspect ratio (proportional)")
#         win32gui.SendMessage(hButton, 0x00F1, 0, None)
#         current_width = docnav.read_selection()
#         kb.sendCtrlKey(kb.KEY_X)
#         kb.sendTab()
#         current_height = docnav.read_selection()
#         kb.paste()
#         kb.sendShiftTab()
#         kb.SendString(current_height)
#         kb.sendReturn()


grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None