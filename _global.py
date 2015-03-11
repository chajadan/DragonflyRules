# the file for all context that is global to any specific grammar

from dragonfly import *
import _general as glib # general library
from collections import Counter 

class GlobalGrammar(Grammar):
    _commandWords = Counter()           # represents the active commands of all "in force" continuous grammars
    _commandWordPartials = Counter()    # partials are all substrings of active commands that consist of full words
                                        # starting from command string beginning
    magicKey = "chaj.magicKey"
    magicWords = []                     # a magic key is a word that is incredibly unlikely to be said ever in dictation
    
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
                    raise TypeError("The following rule's intro is invalid. It must not contain any of |, (, ), [, or ]: rule = " + str(rule) + ", intro = " + intros)    
    
    @staticmethod
    def DetermineRuleIntros(rule):
        """Can handle a single embedded [] optional. Intro ends at first extra <>."""
        intros = getattr(rule, "intro", None)
        if not intros:
            if getattr(rule, "_spec", None) and len(rule._spec) > 0:
                spec_intro = rule._spec
                if spec_intro.find("<")  != -1:
                    spec_intro = spec_intro[:spec_intro.find("<")]
                if len(spec_intro) > 0 and spec_intro[-1] == "[":
                    spec_intro = spec_intro[:-1]               
                spec_intro.replace("[ ", "[") # ensure no space within optional
                spec_intro.replace(" ]", "]") # ensure no space within optional
                spec_intro.replace("[", " [") # ensure space around optional
                spec_intro.replace("]", "] ") # ensure space around optional
                if spec_intro.count("[") == 1:
                    intro_intro = spec_intro.split("[")
                    intro_optional = intro_intro[1].split("]")
                    intro_altro = intro_optional[1]
                    without_optional = glib.Single_Spaces_Only(intro_intro[0] + intro_altro)
                    with_optional = glib.Single_Spaces_Only(intro_intro[0] + intro_optional[0] + intro_altro)
                    intros = [with_optional, without_optional]                    
                else:
                    intros = spec_intro.strip()
            else:
                return None
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
    