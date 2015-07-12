print "importing " + __file__
from dragonfly import *

import Base
from decorators import ActiveGrammarRule
import _general as glib

grammar = Base.ContinuousGrammar("sys admin grammar")


@ActiveGrammarRule(grammar)
class editenv(Base.ContinuousRule):
    spec = "[edit|show] environment variables"
    def _process_recognition(self, node, extras):
        glib.LaunchExeAsyncWithArgList(r"C:\Windows\system32\rundll32.exe", ["sysdm.cpl","EditEnvironmentVariables"])

  
grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None