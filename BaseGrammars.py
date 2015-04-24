# the file for all context that is global to any specific grammar
print "importing _BaseGrammars"
from dragonfly import *
import _BaseRules as br
import _general as glib # general library
from collections import Counter
import inspect
import _globals
from dragonfly.engines.backend_natlink.dictation import NatlinkDictationContainer

class GlobalGrammar(Grammar):
    _commandWords = Counter()           # represents the active commands of all "in force" continuous grammars
    _commandWordPartials = Counter()    # partials are all substrings of active commands that consist of full words
                                        # starting from command string beginning
    magicKey = "chaj.magicKey"
    magicWords = []                     # a magic key is a word that is incredibly unlikely to be said ever in dictation
    
    def __init__(self, name=None, context=None, enableCommand=None, disableCommand=None, initiallyDisabled=False):
        Grammar.__init__(self, name, context=context)
        self.initiallyDisabled = initiallyDisabled
        if enableCommand is not None:
            self.enableCommand = enableCommand
            objContext = self
            class ListenerRule(br.ContinuousRule):
                spec = objContext.enableCommand
                def _process_recognition(self, node, extras):
                    objContext.enable()
            self.enableRule = ListenerRule()
        if disableCommand is not None:
            self.disableCommand = disableCommand
            objContext = self
            class DisableRule(br.ContinuingRule):
                spec = objContext.disableCommand
                def _process_recognition(self, node, extras):
                    objContext.disable()
            self.disableRule = DisableRule()
            self.add_rule(self.disableRule)
            
    def load(self):
        Grammar.load(self)
        if self.initiallyDisabled:
            self.disable()
            
    def listener(self):
        if getattr(self, "enableRule", None) is not None:
            listener = GlobalGrammar("enable listener for " + self.name)
            listener.add_rule(self.enableRule)
            return listener
        else:
            return None
    
    def add_rule(self, ruleInstance):
        if getattr(ruleInstance, "isRegistered", False):
            self._validateRuleIntro(ruleInstance)
        Grammar.add_rule(self, ruleInstance)
    
    def activate_rule(self, rule):
        if getattr(rule, "isRegistered", False):
            intros = self.DetermineRuleIntros(rule)
            partials = self.DeterminePartialsFromIntros(intros)
            GlobalGrammar._commandWords.update(intros)
            GlobalGrammar._commandWordPartials.update(partials)
            #if rule._name == "quickContinuousRule_call withActionSeries(Text('()'), Key('left'))":
            #    print "GlobalGrammar id", id(GlobalGrammar)
        return Grammar.activate_rule(self, rule)
    
        
    def deactivate_rule(self, rule):
        if getattr(rule, "isRegistered", False):
            intros = self.DetermineRuleIntros(rule)
            partials = self.DeterminePartialsFromIntros(intros)
            GlobalGrammar._commandWords.subtract(intros)
            GlobalGrammar._commandWords += Counter() # removes zero and negative counts
            GlobalGrammar._commandWordPartials.subtract(partials)
            GlobalGrammar._commandWordPartials += Counter()
        return Grammar.deactivate_rule(self, rule)
    
    def _validateRuleIntro(self, rule):
        intros = self.DetermineRuleIntros(rule)
        if not intros:
            raise AttributeError("The following rule added to grammar " + self.name + " has no valid intro: " + str(rule))
        
        for intro in intros:
            unacceptable = "|()[]"
            for entry in unacceptable:
                if intro.find(entry) != -1:
                    raise TypeError("The following rule's intro is invalid. It must not contain any of |, (, ), [, or ]: rule = " + str(rule) + ", intro = " + str(intros))    
    
    @staticmethod
    def _specHasOptional(spec):
        lbrack = spec.find("[")
        if lbrack != -1 and spec.find("]", lbrack) != -1:
            return True
        return False
    
    @staticmethod
    def _specHasAlternative(spec):
        lparen = spec.find("(")
        if lparen != -1 and spec.find(")", lparen) != -1:
            return True
        return False
    
    @staticmethod
    def _reduceOptionals(spec):
        if GlobalGrammar._specHasOptional(spec):
            spec = spec.replace("[ ", "[") # ensure no space within optional
            spec = spec.replace(" ]", "]") # ensure no space within optional
            spec = spec.replace("[", " [") # ensure space around optional
            spec = spec.replace("]", "] ") # ensure space around optional
            intro_intro = spec.split("[")
            intro_rest = intro_intro[1].split("]")
            intro_altro = intro_rest[1]
            without_optional = glib.Single_Spaces_And_Trimmed(intro_intro[0] + " " + intro_altro)
            with_optional = glib.Single_Spaces_And_Trimmed(intro_intro[0] + " " + intro_rest[0] + " " + intro_altro)
            intros = [with_optional, without_optional]
            return intros
        return None
    
    @staticmethod
    def _reduceAlternatives(spec):
        if GlobalGrammar._specHasAlternative(spec):
            spec = spec.replace("( ", "(") # ensure no space within optional
            spec = spec.replace(" )", ")") # ensure no space within optional
            spec = spec.replace("(", " (") # ensure space around optional
            spec = spec.replace(")", ") ") # ensure space around optional
            intro_intro = spec.split("(")
            intro_rest = intro_intro[1].split(")")
            alternatives = intro_rest[0].split("|")            
            intro_altro = intro_rest[1]
            if len(alternatives) > 0:
                intros = []
                for alternative in alternatives:
                    intros.append(glib.Single_Spaces_And_Trimmed(intro_intro[0] + " " + alternative + " " + intro_altro))
            return intros
        return None
    
    @staticmethod
    def _baseIntro(rule):
        intro_spec = None
        if getattr(rule, "intro_spec", None):
            intro_spec = rule.intro_spec
        elif getattr(rule, "_spec", None):
            intro_spec = rule._spec
        
        if intro_spec and intro_spec.find("<")  != -1:
            intro_spec = intro_spec[:intro_spec.find("<")]
        if intro_spec and intro_spec[-1] == "[":
            intro_spec = intro_spec[:-1]
        return intro_spec
        
    @staticmethod
    def _introSetNeedsParsing(introSet):
        for item in introSet:
            if GlobalGrammar._specHasAlternative(item):
                return True
            if GlobalGrammar._specHasOptional(item):
                return True
        return False
    
    @staticmethod
    def _parseSpecString(spec):   
        spec = spec.strip()
        introSet = set([spec])
        while GlobalGrammar._introSetNeedsParsing(introSet):
            localSet = set()
            for intro in introSet:
                alts = GlobalGrammar._reduceAlternatives(intro)
                if alts is not None:
                    localSet.update(alts)
                opts = GlobalGrammar._reduceOptionals(intro)
                if opts is not None:
                    localSet.update(opts)
            introSet = localSet
        return list(introSet)
    
    @staticmethod
    def DetermineRuleIntros(rule):
        """
        Can handle any number of optionals or alternatives, so long as an optional doesn't not contain optionals within it,
        and likewise for alternatives.
        This is fine: "a ([really] big|short) command (I use|to use) [a lot]"
        This is not fine: "do that [[right] now]"
        """
        intros = getattr(rule, "intro", None)
        if intros is None:
            spec_intro = GlobalGrammar._baseIntro(rule)
            if spec_intro is None:
                return spec_intro
            return GlobalGrammar._parseSpecString(spec_intro)
        if type(intros) != list:
            intros = [intros]
        return intros
    
    @staticmethod
    def DeterminePartialsFromIntros(intros):
        partials = []
        if not intros:
            return []
        for intro in intros:
            if intro.find(" ") != -1: # determine all subsets of intro that start with first word
                position = len(intro)
                while position != -1:
                    partials.append(intro[:intro.rfind(" ", position)])
                    position -= 1
            else:
                partials.append(intro)
        return partials    
    
    

class ContinuousGrammar(GlobalGrammar):
    isContinuous = True
    literalTags = ["English"] # a literal tag ensures the following will be recognized as dictation speech and not commands  
    
    def __init__(self, name = None, context=None, enableCommand=None, disableCommand=None, initiallyDisabled=False):
        GlobalGrammar.__init__(self, name, context=context, enableCommand=enableCommand, 
                                       disableCommand=disableCommand, initiallyDisabled=initiallyDisabled)
        
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

        _orig_process_recognition = ruleInstance._process_recognition

        def _instance_process_recognition(node, extras):
            if not extras.has_key("RunOn"):
                _orig_process_recognition(node, extras)              
            elif ruleInstance.runOnAdded and not getattr(ruleInstance, "eatDictation", False):
                _orig_process_recognition(node, extras)
                _globals.saveResults = False
                Mimic(*extras["RunOn"].words).execute()                  
            else: # RunOn may need to be split
                original_extras = {key: item for key, item in extras.items()}
                extras["_original_extras"] = original_extras
                recognized_words = extras["RunOn"].words
                inLiteralContext = False
                for i, word in enumerate(recognized_words):
                    if inLiteralContext:
                        inLiteralContext = False
                    elif word in self.literalTags:
                        inLiteralContext = True
                    elif word in self._commandWords: # self here is this grammar
                        if i > 0:
                            extras["RunOn"] = NatlinkDictationContainer(self.translateLiterals(recognized_words[:i])) # limit run on to part before new command
                        else:
                            del extras["RunOn"]
                        _orig_process_recognition(node, extras)
                        _globals.saveResults = False
                        Mimic(*recognized_words[i:]).execute()
                        return
                    elif word in self._commandWordPartials:
                        j = i + 1
                        running_match = word
                        while j < len(recognized_words):
                            running_match += " " + recognized_words[j]
                            if running_match in self._commandWords:
                                if i > 0:
                                    extras["RunOn"] = NatlinkDictationContainer(self.translateLiterals(recognized_words[:i])) # limit run on to part before new command
                                else:
                                    del extras["RunOn"]
                                _orig_process_recognition(node, extras)
                                _globals.saveResults = False
                                Mimic(*recognized_words[i:]).execute()
                                return
                            else:
                                j += 1
                extras["RunOn"] = NatlinkDictationContainer(self.translateLiterals(recognized_words))
                _orig_process_recognition(node, extras)
                           
        ruleInstance._process_recognition = _instance_process_recognition
        return ruleInstance

print "_BaseGrammars, GlobalGrammar id", id(GlobalGrammar)