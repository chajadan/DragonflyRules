from dragonfly import *
from _decorators import *
import inspect

ruleList = []

#decorator
def ExportedRule(Rule):
    if inspect.isclass(Rule):
        ruleList.append(Rule())
    else:
        ruleList.append(Rule)

@ExportedRule
@BombRule
class CapFirstRule(CompoundRule):
    spec = "capital <wordOrPhrase>" 
    extras = (Dictation("wordOrPhrase"),)
    def _process_recognition(self, node, extras):
        wordOrPhrase = extras["wordOrPhrase"].format().capitalize()
        Text(wordOrPhrase).execute()

@ExportedRule
@BombRule
class LowercaseJoined(CompoundRule):
    spec = "joined <words>"
    extras = Dictation("words"),
    def _process_recognition(self, node, extras):
        Text("".join(extras["words"].words)).execute()

@ExportedRule
@BombRule
class CamelCaseRule(CompoundRule):
    spec = "camel <text>"
    extras = Dictation("text"),
    def _process_recognition(self, node, extras):
        msg = extras["text"].format()
        wrds = msg.split(" ")
        for i, word in enumerate(wrds):
            if i > 0:
                if len(word) > 1:
                    wrds[i] = word[0].upper() + word[1:]
                else:
                    wrds[i] = word.upper()
        Text("".join(wrds)).execute()

@ExportedRule
@BombRule
class TitleCaseRule(CompoundRule):
    spec = "title <text>"
    extras = Dictation("text"),
    def _process_recognition(self, node, extras):
        msg = extras["text"].format()
        wrds = msg.split(" ")
        for i, word in enumerate(wrds):
            if len(word) > 1:
                wrds[i] = word[0].upper() + word[1:]
            else:
                wrds[i] = word.upper()
        Text(" ".join(wrds)).execute()

@ExportedRule
@BombRule
class ConstCaseRule(CompoundRule):
    spec = "constant <text>"
    extras = Dictation("text"),
    def _process_recognition(self, node, extras):
        msg = extras["text"].format()
        wrds = msg.split(" ")
        for i, word in enumerate(wrds):
            wrds[i] = word.upper()
        Text("_".join(wrds)).execute()

@ExportedRule
@BombRule
class CapCamelCaseRule(CompoundRule):
    spec = "(studly|Studley) <text>"
    extras = Dictation("text"),
    def _process_recognition(self, node, extras):
        msg = extras["text"].format()
        wrds = msg.split(" ")
        for i, word in enumerate(wrds):
            if len(word) > 1:
                wrds[i] = word[0].upper() + word[1:]
            else:
                wrds[i] = word.upper()
        Text("".join(wrds)).execute()

@ExportedRule
@BombRule
class ScupRule(CompoundRule):
    spec = "scup <text>"
    extras = (Dictation("text"), Dictation("chain"))
    def _process_recognition(self, node, extras):
        Text("_".join(extras["text"].words)).execute()