#decorator
#def GrammarRule(RuleClass):
#    ??.add_rule(RuleClass())

from dragonfly import *
import inspect
from dragonfly.engines.backend_natlink.dictation import NatlinkDictationContainer

#decorator
def BombRule(CompoundRuleClass):
    _orig_process_recognition = CompoundRuleClass._process_recognition
    def _new_process_recognition(self, node, extras):
        words = []
        bombCount = 0
        
        #seek out bomb
        for name, value in extras.items():
            if type(value) == NatlinkDictationContainer:
                if value.words.count("bomb") == 0:
                    continue # try to find another dictation container with a bomb
                else:
                    words = value.words
                    bombCount = words.count("bomb")
                    break
                
        if bombCount:
            bombIndex = words.index("bomb")
            extras[name] = NatlinkDictationContainer(words[0:bombIndex])
            
        _orig_process_recognition(self, node, extras)
        
        if bombCount:
            Mimic(*words[bombIndex + 1:]).execute()
            
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