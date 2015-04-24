print "importing _BaseRules"
from dragonfly import *
import _decorators as dec
import inspect
import _general as glib
import _globals


# To contain any custom classes derived ultimately from dragonfly Rule

class CorrectableRule(CompoundRule):
    def process_recognition(self, node, results):
        if _globals.saveResults and getattr(self, "saveResults", True):
            _globals.lastSavedResults = results
        else:
            _globals.saveResults = True
        CompoundRule.process_recognition(self, node, results)

class ContinuousGrammarRule(CorrectableRule):
    pass

class ContinuingRule(ContinuousGrammarRule):
    isContinuing = True
    def __init__(self, name = None, spec = None, extras = None, defaults = None, exported = None, context = None):
        _spec = spec if spec else getattr(self, "spec", None)
        _defaults = glib.FirstNotNone(defaults, getattr(self, "defaults", None))
        _exported = glib.FirstNotNone(exported, getattr(self, "exported", None))
        _context = glib.FirstNotNone(context, getattr(self, "context", None))
        _extras = glib.FirstNotNone(extras, getattr(self, "extras", None))
        
        self.runOnAdded = False # so far
        if not _extras:
            _extras = []
        _extras = dict((element.name, element) for element in _extras)
        if not _extras.has_key("RunOn"):
            _spec += " [<RunOn>]"
            _extras["RunOn"] = Dictation("RunOn")
            self.runOnAdded = True
        _extras = [value for (_, value) in _extras.items()]     

        CompoundRule.__init__(self, name = name, spec = _spec, extras = _extras, defaults = _defaults, exported = _exported, context = _context)    

class RegisteredRule(CorrectableRule):
    isRegistered = True
    def __init__(self, name = None, spec = None, extras = None, defaults = None, exported = None, context = None, intro = None):
        _spec = spec if spec else getattr(self, "spec", None)
        _extras = extras if extras else getattr(self, "extras", None)
        _defaults = defaults if defaults else getattr(self, "defaults", None)
        _exported = exported if exported else getattr(self, "exported", None)
        _context = context if context else getattr(self, "context", None)
        if intro:
            self.intro = intro
        elif not getattr(self, "intro", None):
            pass#self.intro = _GlobalGrammar.GlobalGrammar.DetermineRuleIntros(self)
        CompoundRule.__init__(self, name = name, spec = _spec, extras = _extras, defaults = _defaults, exported = _exported, context = _context)        
    
class ContinuousRule(RegisteredRule, ContinuingRule):
    isContinuous = True
    def __init__(self, name = None, spec = None, extras = None, defaults = None, exported = None, context = None, intro = None):
        #super(RegisteredRule, self).__init__(name = name, spec = spec, extras = extras, defaults = defaults, exported = exported, context = context, intro = intro)
        #super(ContinuingRule, self).__init__(name = name, spec = spec, extras = extras, defaults = defaults, exported = exported, context = context)
        RegisteredRule.__init__(self, name = name, spec = spec, extras = extras, defaults = defaults, exported = exported, context = context, intro = intro)
        ContinuingRule.__init__(self, name = name, spec = spec, extras = extras, defaults = defaults, exported = exported, context = context)
        
class ContinuousRule_EatDictation(ContinuousRule):
    """
    Passes an extra 'RunOn' dictation of any following non-command dictation.
    This allows the rule spec to leave out <RunOn> and process rules without dictation if no non-command dictation is not present.
    """
    eatDictation = True
    def __init__(self, name = None, spec = None, extras = None, defaults = None, exported = None, context = None, intro = None):
        ContinuousRule.__init__(self, name = name, spec = spec, extras = extras, defaults = defaults, exported = exported, context = context, intro = intro)


class BaseQuickRules():
    def __init__(self, grammar):
        self.grammer = grammar
        self._rules = []
    def add_rule(self, rule):
        self._rules.append(rule)
        #if self.__class__.__name__ == "QuickCRules":
            #print rule._name
        self.grammer.add_rule(rule)

@dec.ChainedRule
class QuickChainedRule(CorrectableRule):
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
                if "intro" in attributes:
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
                if hasattr(self, "defaultsDict") and extraName in self.defaultsDict:
                    defaults[extraName] = self.defaultsDict[extraName]
            self.add_rule(QuickContinuousRule(voicedAs, action, extras = extras, defaults = defaults, intro = intro))

class QuickRule(CorrectableRule):
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
            
# class TRule():
#     def __init__(self,):