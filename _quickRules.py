
from _decorators import ChainedRule
from _baseRules import *

class BaseQuickRules():
    def __init__(self, grammar):
        self.grammer = grammar
        self._rules = []
    def add_rule(self, rule):
        self._rules.append(rule)
        self.grammer.add_rule(rule)

@ChainedRule
class QuickChainedRule(CompoundRule):
    spec = " "
    extras = ()
    def __init__(self, voicedAs, action):
        CompoundRule.__init__(self, name = "qcr_" + voicedAs + action.__str__(), spec = voicedAs + self.spec)
        self.action = action
    def _process_recognition(self, node, extras):
        self.action.execute()
        
class QuickChainedRules(BaseQuickRules):
    def __init__(self, grammar):
        BaseQuickRules.__init__(self, grammar)
        for voicedAs, action in self.mapping.items():
            self.add_rule(QuickChainedRule(voicedAs, action))
        
class QuickContinuousRule(ContinuousRule):
    def __init__(self, voicedAs, action, name = None, spec = None, extras = None, defaults = None, exported = None, context = None, intro = None):
        self.intro = intro
        self.action = action
        name = name if name else "quickContinuousRule_" + voicedAs + action.__str__()
        ContinuousRule.__init__(self, name = name, spec = voicedAs, extras = extras, defaults = defaults)
    def _process_recognition(self, node, extras):
        self.action.execute(extras)
        
class QuickContinuousRules(BaseQuickRules):
    def __init__(self, grammar):
        BaseQuickRules.__init__(self, grammar)
        for voicedAs, attributes in self.mapping.items():
            intro = None
            if type(attributes) == dict:
                action = attributes["action"]
                if attributes.has_key("intro"):
                    intro = attributes["intro"]
            else:
                action = attributes
            defaults = {}
            extras = ()
            position = 0
            while voicedAs.find("<", position) != -1:
                start = voicedAs.find("<", position)
                end = voicedAs.find(">", start)
                position = end
                extraName = voicedAs[(start+1):end]
                extras += (self.extrasDict[extraName],)
                if self.defaultsDict.has_key(extraName):
                    defaults[extraName] = self.defaultsDict[extraName]
            self.add_rule(QuickContinuousRule(voicedAs, action, extras = extras, defaults = defaults, intro = intro))

class QuickRule(CompoundRule):
    def __init__(self, voicedAs, action, extras = None, defaults = None, intro = None, context = None):
        CompoundRule.__init__(self, name = "quickRule_" + voicedAs + action.__str__(), spec = voicedAs, extras = extras, defaults = defaults, context = context)
        self.action = action
        self.intro = intro
    def _process_recognition(self, node, extras):
        self.action.execute(extras)
        
class QuickRules(BaseQuickRules):
    def __init__(self, grammar):
        BaseQuickRules.__init__(self, grammar)
        for voicedAs, attributes in self.mapping.items():
            intro = None
            if type(attributes) == dict:
                action = attributes["action"]
                if attributes.has_key("intro"):
                    intro = attributes["intro"]
            else:
                action = attributes
            defaults = {}
            extras = ()
            position = 0
            self.defaultsDict = getattr(self, "defaultsDict", {})
                
            while voicedAs.find("<", position) != -1:
                start = voicedAs.find("<", position)
                end = voicedAs.find(">", start)
                position = end
                extraName = voicedAs[(start+1):end]
                extras += (self.extrasDict[extraName],)
                if self.defaultsDict.has_key(extraName):
                    defaults[extraName] = self.defaultsDict[extraName]
            self.add_rule(QuickRule(voicedAs, action, extras = extras, defaults = defaults, intro = intro))