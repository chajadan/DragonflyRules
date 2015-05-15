from dragonfly.engines.backend_natlink.dictation import NatlinkDictationContainer
print "import _baseRules"
from dragonfly import *
import _decorators as dec
import inspect
import _general as glib
import _globals
from chajLib.ops import first_not_none

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
        _defaults = first_not_none(defaults, getattr(self, "defaults", None))
        _exported = first_not_none(exported, getattr(self, "exported", None))
        _context = first_not_none(context, getattr(self, "context", None))
        _extras = first_not_none(extras, getattr(self, "extras", None))
        
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
    next_unique_id = 1
    def __init__(self, voicedAs, action, name=None, spec=None, extras=None, defaults=None, exported=None, context=None, intro=None, args=None):
        self.intro = first_not_none(intro, getattr(self, "intro", None))
        self.action = first_not_none(action, getattr(self, "action", None))
        self.args = first_not_none(args, getattr(self, "args", None), {}) 
        name = first_not_none(name, getattr(self, "name", None), 
            "quickContinuousRule_" + voicedAs + str(action) + "_id" + str(QuickContinuousRule.next_unique_id))
        QuickContinuousRule.next_unique_id += 1
        ContinuousRule.__init__(self, name=name, spec=voicedAs, extras=extras, defaults=defaults, context=context)
    def _process_recognition(self, node, extras):
        for name, value_callback in self.args.items():
            extras[name] = value_callback(extras)
        self.action.execute(extras)


class QuickContinuousCall(ContinuousRule):
    next_unique_id = 1
    def __init__(self, voicedAs, callable, pass_runon_as=None, context=None, defaults=None, extras=None):
        self.pass_runon_as = first_not_none(pass_runon_as, getattr(self, "pass_runon_as", None))
        if voicedAs.find("<RunOn>") != -1:
            if extras:
                extras = [extra for extra in extras if extra.name != "RunOn"]
            else:
                extras = [] 
            extras.append(Dictation("RunOn"))
        
        self.action = Function(callable)
        name = "QuickContinuousCall_" + voicedAs + str(self.action) + "_id" + str(QuickContinuousCall.next_unique_id)
        QuickContinuousCall.next_unique_id += 1
        ContinuousRule.__init__(self, name=name, spec=voicedAs, extras=extras, defaults=defaults, context=context)
    def _process_recognition(self, node, extras):
        if getattr(self, "pass_runon_as", None) and "RunOn" in extras:
            extras[self.pass_runon_as] = extras["RunOn"].format()
        for name, extra in extras.items():
            if isinstance(extra, NatlinkDictationContainer):
                extras[name] = extra.format()
        self.action.execute(extras)

class QuickContinuousCalls(BaseQuickRules):
    def __init__(self, grammar):
        BaseQuickRules.__init__(self, grammar)
        for entries in self.mapping:
            if len(entries) == 2 and type(entries[1]) == dict and isinstance(entries[0], (list, tuple)):
                args, kwargs = entries
            else:
                args = entries
                kwargs = {}

            self.extras = getattr(self, "extras", None)
            if self.extras:
                if len(args) < 6 and "extras" not in kwargs:
                    kwargs["extras"] = self.extras
            
            self.add_rule(QuickContinuousCall(*args, **kwargs))


class QuickContinuousRules(BaseQuickRules):
    def __init__(self, grammar):
        BaseQuickRules.__init__(self, grammar)
        for voicedAs, attributes in self.mapping.items():
            intro = None
            args = {}
            if type(attributes) == dict:
                action = attributes["action"]
                if "intro" in attributes:
                    intro = attributes["intro"]
                args = attributes.get("args", {})
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
            self.add_rule(QuickContinuousRule(voicedAs, action, extras=extras, defaults=defaults, intro=intro, args=args))

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