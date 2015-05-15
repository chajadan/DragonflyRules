"""
Rules only active when IrfanView is the foreground window should be placed in a file named i_view32.py.
This is for rules that use IrfanView at other times, such as when IrfanView is not open at all.
"""

from dragonfly import *
import Base
import inspect
import paths
from chajLib.ui import keyboard as kb

grammar = Base.ContinuousGrammar("supplementary always on irfan view grammar")

#decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, Base.BaseQuickRules):
            rule(grammar)
        else:
            grammar.add_rule(rule())
    else:
        grammar.add_rule(rule)

@GrammarRule
class FullScreenToIrfanView(Base.ContinuousRule):
    spec = "screen to image"
    def _process_recognition(self, node, extras):
        kb.sendPrintScreen()
        action = StartApp(paths.IRFANVIEW_PATH) + Pause("50") + Key("c-v")
        action.execute()

@GrammarRule
class WindowToIrfanView(Base.ContinuousRule):
    spec = "window to image"
    def _process_recognition(self, node, extras):
        kb.sendAltPrintScreen()
        action = StartApp(paths.IRFANVIEW_PATH) + Pause("50") + Key("c-v")
        action.execute()


@GrammarRule
class ClipboardToIrfanView(Base.ContinuousRule):
    spec = "clipboard to image"
    def _process_recognition(self, node, extras):
        action = StartApp(paths.IRFANVIEW_PATH) + Pause("50") + Key("c-v")
        action.execute()

grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None