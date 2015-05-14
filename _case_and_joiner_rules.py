print "import _case_and_joiner_rules"
from dragonfly import *
import BaseGrammars
from BaseRules import *
import inspect

grammar = BaseGrammars.ContinuousGrammar("case and joiner rules")

#decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, BaseQuickRules):
            rule(grammar)
        else:
            grammar.add_rule(rule())
    else:
        grammar.add_rule(rule)

@GrammarRule
class CapFirstRule(ContinuousRule):
    spec = "capital <RunOn>" 
    extras = (Dictation("RunOn"),)
    def _process_recognition(self, node, extras):
        wordOrPhrase = extras["RunOn"].format().capitalize()
        Text(wordOrPhrase).execute()

@GrammarRule
class LowerCaseFirstRule(ContinuousRule):
    spec = "low case <RunOn>" 
    extras = (Dictation("RunOn"),)
    def _process_recognition(self, node, extras):
        wordOrPhrase = extras["RunOn"].format()
        if len(wordOrPhrase) > 0:
            wordOrPhrase = wordOrPhrase[0].lower() + wordOrPhrase[1:]
            Text(wordOrPhrase).execute()

@GrammarRule
class LowercaseJoined(ContinuousRule):
    spec = "joined <RunOn>"
    extras = Dictation("RunOn"),
    def _process_recognition(self, node, extras):
        Text("".join(extras["RunOn"].words)).execute()

@GrammarRule
class CamelCaseRule(ContinuousRule):
    spec = "camel <RunOn>"
    extras = Dictation("RunOn"),
    def _process_recognition(self, node, extras):
        msg = extras["RunOn"].format()
        wrds = msg.split(" ")
        for i, word in enumerate(wrds):
            if i > 0:
                if len(word) > 1:
                    wrds[i] = word[0].upper() + word[1:]
                else:
                    wrds[i] = word.upper()
        Text("".join(wrds)).execute()

@GrammarRule
class TitleCaseRule(ContinuousRule):
    spec = "title <RunOn>"
    extras = Dictation("RunOn"),
    def _process_recognition(self, node, extras):
        msg = extras["RunOn"].format()
        wrds = msg.split(" ")
        for i, word in enumerate(wrds):
            if len(word) > 1:
                wrds[i] = word[0].upper() + word[1:]
            else:
                wrds[i] = word.upper()
        Text(" ".join(wrds)).execute()

@GrammarRule
class ClassicConstantVariableCaseRule(ContinuousRule):
    spec = "constant <RunOn>"
    extras = Dictation("RunOn"),
    def _process_recognition(self, node, extras):
        msg = extras["RunOn"].format()
        wrds = msg.split(" ")
        for i, word in enumerate(wrds):
            wrds[i] = word.upper()
        Text("_".join(wrds)).execute()

@GrammarRule
class CapitalCamelCaseRule(ContinuousRule):
    spec = "capital camel <RunOn>"
    extras = Dictation("RunOn"),
    def _process_recognition(self, node, extras):
        msg = extras["RunOn"].format()
        msg = msg.lower()
        wrds = msg.split(" ")
        for i, word in enumerate(wrds):
            if len(word) > 1:
                wrds[i] = word[0].upper() + word[1:]
            else:
                wrds[i] = word.upper()
        Text("".join(wrds)).execute()

@GrammarRule
class UnderscoreJoinedTextRule(ContinuousRule):
    spec = "scored <RunOn>"
    extras = (Dictation("RunOn"),)
    def _process_recognition(self, node, extras):
        Text("_".join(extras["RunOn"].words)).execute()

grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None        