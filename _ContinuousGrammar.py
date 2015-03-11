from dragonfly import *
import _general as glib # general library
from _global import *
from _quickRules import *
from collections import Counter
import inspect
from dragonfly.engines.backend_natlink.dictation import NatlinkDictationContainer


class ContinuousGrammar(GlobalGrammar):
    isContinuous = True
    literalTags = ["English"] # a literal tag ensures the following will be recognized as dictation speech and not commands  
    
    def translateLiterals(self, wordList):
        if len(wordList) == 0:
            return wordList
        literals = self.literalTags + ContinuousGrammar.literalTags
        max_index = len(wordList) - 1
        current_index = 0
        while current_index < max_index:           
            if wordList[current_index] in literals:
                wordList = wordList[:current_index] + wordList[(current_index+1):]
                max_index -= 1
            current_index += 1
        return wordList

    def add_rule(self, ruleInstanceOrClass):
        ruleInstance = glib.EnsureInstance(ruleInstanceOrClass)
        if getattr(ruleInstance, "isContinuing", False):
            ruleInstance = self._makeRuleContinuing(ruleInstance)
        GlobalGrammar.add_rule(self, ruleInstance)
    
    def _makeRuleContinuing(self, ruleInstance):
        """expects the rule to have a _spec which CompoundRules generate upon initialization from the class spec or the __init__ spec argument"""
        spec = getattr(ruleInstance, "_spec", None)
        if not spec:
            raise AttributeError("The following rule added to continuous grammar " + self.name + " has no _spec attribute: " + ruleInstance)
        
        if spec.find("<RunOn>") == -1:
            spec += " [<RunOn>]"
            setattr(ruleInstance, "_spec", spec)
            ruleInstance.extras += (Dictation("RunOn"),)
            ruleInstance.runOnAdded = True
        else:
            ruleInstance.runOnAdded = False

        _orig_process_recognition = ruleInstance._process_recognition

        def _instance_process_recognition(node, extras):
            if not extras.has_key("RunOn"):
                _orig_process_recognition(node, extras)              
            elif ruleInstance.runOnAdded:
                _orig_process_recognition(node, extras)
                Mimic(*extras["RunOn"].words).execute()                  
            else: # RunOn may need to be split
                recognized_words = extras["RunOn"].words
                inLiteralContext = False
                for i, word in enumerate(recognized_words):
                    if inLiteralContext:
                        inLiteralContext = False
                    elif word in self.literalTags:
                        inLiteralContext = True
                    elif word in self._commandWords: # self here is this grammar
                        extras["RunOn"] = NatlinkDictationContainer(self.translateLiterals(recognized_words[:i])) # limit run on to part before new command
                        _orig_process_recognition(node, extras)
                        Mimic(*recognized_words[i:]).execute()
                        return
                    elif word in self._commandWordPartials:
                        j = i + 1
                        running_match = word
                        while j < len(recognized_words):
                            running_match += " " + recognized_words[j]
                            if running_match in self._commandWords:
                                extras["RunOn"] = NatlinkDictationContainer(self.translateLiterals(recognized_words[:i])) # limit run on to part before new command
                                _orig_process_recognition(node, extras)
                                Mimic(*recognized_words[i:]).execute()
                                return
                            else:
                                j += 1
                extras["RunOn"] = NatlinkDictationContainer(self.translateLiterals(recognized_words))
                _orig_process_recognition(node, extras)
                           
        ruleInstance._process_recognition = _instance_process_recognition
        return ruleInstance
