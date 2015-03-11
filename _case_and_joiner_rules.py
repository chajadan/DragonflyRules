from dragonfly import *
from _ruleExport import *
import inspect
from _baseRules import ContinuousRule

exports = ExportedRules()

@ExportedRule(exports)
class CapFirstRule(ContinuousRule):
    spec = "capital <RunOn>" 
    extras = (Dictation("RunOn"),)
    def _process_recognition(self, node, extras):
        wordOrPhrase = extras["RunOn"].format().capitalize()
        Text(wordOrPhrase).execute()

@ExportedRule(exports)
class LowercaseJoined(ContinuousRule):
    spec = "joined <RunOn>"
    extras = Dictation("RunOn"),
    def _process_recognition(self, node, extras):
        Text("".join(extras["RunOn"].words)).execute()

@ExportedRule(exports)
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

@ExportedRule(exports)
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

@ExportedRule(exports)
class ClassicConstantVariableCaseRule(ContinuousRule):
    spec = "constant <RunOn>"
    extras = Dictation("RunOn"),
    def _process_recognition(self, node, extras):
        msg = extras["RunOn"].format()
        wrds = msg.split(" ")
        for i, word in enumerate(wrds):
            wrds[i] = word.upper()
        Text("_".join(wrds)).execute()

@ExportedRule(exports)
class CapitalCamelCaseRule(ContinuousRule):
    spec = "capital camel <RunOn>"
    extras = Dictation("RunOn"),
    def _process_recognition(self, node, extras):
        msg = extras["RunOn"].format()
        wrds = msg.split(" ")
        for i, word in enumerate(wrds):
            if len(word) > 1:
                wrds[i] = word[0].upper() + word[1:]
            else:
                wrds[i] = word.upper()
        Text("".join(wrds)).execute()

@ExportedRule(exports)
class UnderscoreJoinedTextRule(ContinuousRule):
    spec = "scored <RunOn>"
    extras = (Dictation("RunOn"),)
    def _process_recognition(self, node, extras):
        Text("_".join(extras["RunOn"].words)).execute()