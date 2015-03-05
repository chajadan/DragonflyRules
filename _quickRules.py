
from _decorators import *

@ChainedRule
class QuickChainedRule(CompoundRule):
    spec = " "
    extras = ()
    def __init__(self, voicedAs, action):
        CompoundRule.__init__(self, name = "qcr_" + voicedAs + action.__str__(), spec = voicedAs + self.spec)
        self.action = action
    def _process_recognition(self, node, extras):
        self.action.execute()