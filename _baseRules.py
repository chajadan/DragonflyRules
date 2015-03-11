from dragonfly import *
import _global

# To contain any custom classes derived ultimately from dragonfly Rule

class ContinuousGrammarRule(CompoundRule):
    pass

class ContinuingRule(ContinuousGrammarRule):
    isContinuing = True
    def __init__(self, name = None, spec = None, extras = None, defaults = None, exported = None, context = None):
        _spec = spec if spec else getattr(self, "spec", None)
        _defaults = defaults if defaults else getattr(self, "defaults", None)
        _exported = exported if exported else getattr(self, "exported", None)
        _context = context if context else getattr(self, "context", None)
        _extras = extras if extras else getattr(self, "extras", None)
        
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

class RegisteredRule(CompoundRule):
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
            self.intro = _global.GlobalGrammar.DetermineRuleIntros(self)
        CompoundRule.__init__(self, name = name, spec = _spec, extras = _extras, defaults = _defaults, exported = _exported, context = _context)        
    
class ContinuousRule(RegisteredRule, ContinuingRule):
    isContinuous = True
    def __init__(self, name = None, spec = None, extras = None, defaults = None, exported = None, context = None, intro = None):
        RegisteredRule.__init__(self, name = name, spec = spec, extras = extras, defaults = defaults, exported = exported, context = context, intro = intro)
        ContinuingRule.__init__(self, name = name, spec = spec, extras = extras, defaults = defaults, exported = exported, context = context)