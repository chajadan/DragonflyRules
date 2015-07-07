# the file for all context that is global to any specific grammar
print "importing " + __file__
from dragonfly import *
import BaseRules as br
import _general as glib # general library
from collections import Counter
import inspect
import itertools
from xml.dom import minidom
from chajLib import cstring as strfuncs
from chajLib import ops
import _globals
from dragonfly.engines.backend_natlink.dictation import NatlinkDictationContainer

def xmlize_spec(spec):
    # "escape" angle brackets
    spec = spec.replace("<", "{")
    spec = spec.replace(">", "}")
    spec = spec.replace("[", "<optional>(")
    spec = spec.replace("]", ")</optional>")    
    spec = spec.replace("(", "<alternatives><alternative>")
    spec = spec.replace(")", "</alternative></alternatives>")
    spec = spec.replace("|", "</alternative><alternative>")
    # wrap as alternatives in case of embedded top-level option, e.g. "command one | command two"
    spec = "<alternatives><alternative>" + spec + "</alternative></alternatives>"    
    return spec

class XmlSpecNode:
    TEXT_NODE = 3
    def __init__(self, soup):
        self.soup = minidom.parseString(soup)

    def get_intros(self):
        intros = [""]
        for child in self.soup.firstChild.childNodes:
            tag = child.nodeName
            if child.nodeType == XmlSpecNode.TEXT_NODE:
                new_intros = [child.nodeValue]
            elif tag == "alternatives":
                new_intros = xAlternativesNode(child.toxml()).get_intros()
            elif tag == "optional":
                new_intros = [""] + XmlSpecNode(child.toxml()).get_intros()                        
            else:
                new_intros = XmlSpecNode(child.toxml()).get_intros()
            new_intros = itertools.product(intros, new_intros)
            # replace intros with a cartesian product by new_intros
            intros = [" ".join(parts) for parts in new_intros]
        intros = map(strfuncs.rstrip_from, intros, "{" * len(intros))
        intros = map(lambda x: x.strip(), intros)
        intros = map(strfuncs.reduce_spaces, intros) # only single spaces
        intros = filter(None, intros) # remove empty intros
        return intros

class xAlternativesNode(XmlSpecNode):
    def get_intros(self):
        intros = []
        for child in self.soup.firstChild.childNodes:
            assert child.nodeName == "alternative" # will only have <alternative> children
            intros += XmlSpecNode(child.toxml()).get_intros()
        return intros

class XmlSpec(XmlSpecNode):
    def __init__(self, spec):
        self.soup = minidom.parseString(xmlize_spec(spec))


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
        try:
            intros = XmlSpec(spec).get_intros()
            return intros
        except:
            print "Could not parse intros of spec:", spec
            print "Spec xmlized as:", xmlize_spec(spec)
    
    @staticmethod
    def DetermineRuleIntros(rule):
        """
        Expected to be able to parse any spec as long as it is well-formed::
        - balanced parentheses and brackets
        - outside of <extra> references,contains no < or > characters
        """
        intros = getattr(rule, "intro", None)
        if intros:            
            # user explicitly supplied intro(s), go with that
            if type(intros) != list:
                intros = [intros]            
        else:
            intro_spec = ops.first_not_none(getattr(rule, "intro_spec", None), getattr(rule, "_spec", None))
            if not intro_spec:
                return intro_spec
            intros = GlobalGrammar._parseSpecString(intro_spec)
        assert type(intros) == list
        return intros
    
    @staticmethod
    def DeterminePartialsFromIntros(intros):
        partials = []
        if not intros:
            return []
        for intro in intros:
            position = intro.rfind(" ")
            if position == -1:
                partials.append(intro)
            else:
                while position != -1:
                    partials.append(intro[0:position])
                    position = intro.rfind(" ", 0, position)
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
    
    def get_words_from_runon(self, RunOn):
        if type(RunOn) == NatlinkDictationContainer:
            return RunOn.words
        elif issubclass(type(RunOn), basestring):
            return RunOn.split()
        else:
            return None

    def determine_command_index(self, RunOn):
        recognized_words = self.get_words_from_runon(RunOn)
        if recognized_words is None:
            return None

        inLiteralContext = False
        for i, word in enumerate(recognized_words):
            if inLiteralContext:
                inLiteralContext = False # literal context lasts for one word only
                continue # skip current word, force status as non command word
            elif word in self.literalTags:
                inLiteralContext = True
                continue
            elif word in self._commandWords:
                return i # even if a longer command starts here, we just mimic the whole remainder and let the engine determine that
            elif word in self._commandWordPartials:
                # look ahead and figure out if a full command starts here or not
                running_match = word # running_match accrues words to seek a full command
                offset_index = 1 # used to index past the index of 'word'
                while i + offset_index < len(recognized_words):
                    running_match += " " + recognized_words[i + offset_index]
                    if running_match in self._commandWords:
                        return i
                    else:
                        offset_index +=1
        # no embedded registered command
        return len(recognized_words) # should be able to slice recognized_words into non-command/command parts in all cases 

    def split_runon(self, RunOn):
        recognized_words = self.get_words_from_runon(RunOn)
        if recognized_words is None:
            return None, None
        
        split_index = self.determine_command_index(RunOn)
        if split_index is None:
            return None, None
        else:
            return recognized_words[:split_index], recognized_words[split_index:]
    
    def _makeRuleContinuing(self, ruleInstance):

        _orig_process_recognition = ruleInstance._process_recognition

        def _instance_process_recognition(node, extras):
            if not extras.has_key("RunOn"):
                _orig_process_recognition(node, extras)
            elif ruleInstance.runOnAdded and not getattr(ruleInstance, "eatDictation", False):
                # RunOn added means the original rule isn't requesting access to part of that result
                # unless eatDictation is enabled, in which case it's optional but not required
                _orig_process_recognition(node, extras)
                _globals.saveResults = False # we are repeating part of the last utterance, so don't partially overwrite the last saved result
                Mimic(*extras["RunOn"].words).execute()
            else: # RunOn may need to be split
                extras["_original_extras"] = {key: item for key, item in extras.items()}
                keep_on, pass_on = self.split_runon(extras["RunOn"])

                # set value return to processing rule
                if not keep_on:
                    del extras["RunOn"]
                else:
                    extras["RunOn"] = NatlinkDictationContainer(self.translateLiterals(keep_on))
                    extras["RunOn_UnEscaped"] = NatlinkDictationContainer(keep_on)

                _orig_process_recognition(node, extras) # call rule processing
                _globals.saveResults = False # we're about to parrot part of a command
                if pass_on:
                    Mimic(*pass_on).execute()                

        ruleInstance._process_recognition = _instance_process_recognition
        return ruleInstance
