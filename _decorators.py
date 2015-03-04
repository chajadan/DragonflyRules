#decorator
#def GrammarRule(RuleClass):
#    ??.add_rule(RuleClass())

from dragonfly import *

#decorator
def BombRule(CompoundRuleClass):
    CompoundRuleClass.spec += " [bomb [<chain>]]"
    CompoundRuleClass.extras += (Dictation("chain"),)
    _orig_process_recognition = CompoundRuleClass._process_recognition
    def _new_process_recognition(self, node, extras):
        _orig_process_recognition(self, node, extras)
        if extras.has_key("chain"):
            Mimic(*extras["chain"].words).execute()
    CompoundRuleClass._process_recognition = _new_process_recognition
    return CompoundRuleClass

def OptionalBombRule(CompoundRuleClass):
    orig_spec = CompoundRuleClass.spec
    CompoundRuleClass = BombRule(CompoundRuleClass)
    CompoundRuleClass.spec = orig_spec + " [[bomb] [<chain>]]"
    return CompoundRuleClass

def ChainedRule(CompoundRuleClass):
    CompoundRuleClass.spec += " [<chain>]"
    CompoundRuleClass.extras += (Dictation("chain"),)
    _orig_process_recognition = CompoundRuleClass._process_recognition
    def _new_process_recognition(self, node, extras):
        _orig_process_recognition(self, node, extras)
        if extras.has_key("chain"):
            Mimic(*extras["chain"].words).execute()
    CompoundRuleClass._process_recognition = _new_process_recognition
    return CompoundRuleClass

def BombChain(CompoundRuleClass):
    CompoundRuleClass = BombRule(CompoundRuleClass)
    _orig_process_recognition = CompoundRuleClass._process_recognition
    def _new_process_recognition(self, node, extras):
        for i, word in enumerate(extras["bombChain"].words):
            if word == "then":
                extras["bombChain"].words[i] = "bomb"        
        _orig_process_recognition(self, node, extras)
    CompoundRuleClass._process_recognition = _new_process_recognition
    return CompoundRuleClass

def CallInPlace(function):
    function()


# string camel many people bomb space three say people = "manyPeople"   people
# string camel many people then space three say people = "manyPeople   people"