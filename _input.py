print "importing " + __file__
from dragonfly import *
from keyboard_keys import all_keys_by_keyname
from keyboard_keys import number_names_proper
import Base
import inspect

grammar = Base.ContinuousGrammar("input elements and sequences grammar")


# decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, Base.BaseQuickRules):
            rule(grammar)
        else:
            grammar.add_rule(rule())
    else:
        grammar.add_rule(rule)


# @GrammarRule
# class FreeFormSpeech(ContinuingRule):
#     spec = "<RunOn>"
#     intro = "~chajBlankchaj~"
#     extras = (Dictation("RunOn"),)
#     def _process_recognition(self, node, extras):
#         Text(extras["RunOn"].format()).execute()


@GrammarRule
class StreamWordsAtCursorRule(Base.ContinuousRule):
    spec = "(stream|fling) <RunOn>"
    extras = (Dictation("RunOn"),)
    def _process_recognition(self, node, extras):
        Text(extras["RunOn"].format()).execute()

@GrammarRule
class PureWordsDictationRule(Base.RegisteredRule):
    """
    intended for long pure speech dictation where you don't want to worry about literalizing command words
    """
    spec = "words <RunOn>"
    extras = (Dictation("RunOn"),)
    def _process_recognition(self, node, extras):
        Text(extras["RunOn"].format()).execute()
        
    
@GrammarRule
class PrependSpaceRule(Base.ContinuousRule):
    spec = "tack <RunOn>"
    extras = (Dictation("RunOn"),)
    def _process_recognition(self, node, extras):
        Text(" " + extras["RunOn"].format()).execute()


@GrammarRule
class NumericDigitsRule(Base.RegisteredRule):
    spec = "numeric <n> [decimal <part>]"
    extras = (IntegerRef("n", 0, 9999999999), IntegerRef("part", 0, 999999999))
    n = 0
    def _process_recognition(self, node, extras):
        self.n += 1
        Text(str(extras["n"])).execute()
        if extras.has_key("part"):
            Text("." + str(extras["part"])).execute()


@GrammarRule
class NumbersRule(Base.ContinuousRule):
    spec = "digits <digits>"
    extras = (Repetition(Choice("digit", choices={voicedAs: digit for digit, voicedAs in number_names_proper}), name="digits", min=1, max=50),)
    def _process_recognition(self, node, extras):
        digits = map(str, extras["digits"])
        Text("".join(digits)).execute()


@GrammarRule
class FullDateRule(Base.ContinuousRule):
    spec = "full date <month> <day> <year>"
    extras = (IntegerRef("month", 1, 12), IntegerRef("day", 1, 31), IntegerRef("year", 1, 9999))
    def _process_recognition(self, node, extras):
            month = extras["month"]
            day = extras["day"]
            year = extras["year"]
            month = str(month) if month >= 10 else "0" + str(month)
            day = str(day) if day >= 10 else "0" + str(day)
            if year >= 100:
                year = str(year)
            elif year <= 10:
                year = "200" + str(year)
            else: 
                year = "20" + str(year)
            Text(month + "/" + day + "/" + year).execute()


@GrammarRule                     
class ShortTimeRule(Base.ContinuousRule):
    spec = "short time <hour> <minutes> (anti|post)"
    extras = (IntegerRef("hour", 1, 12), IntegerRef("minutes", 0, 59))
    def _process_recognition(self, node, extras):
        hour = str(extras["hour"])
        minutes = extras["minutes"]
        minutes = str(minutes) if minutes >= 10 else "0" + str(minutes)
        heard = " ".join(node.words())
        am_pm = "p"
        if heard.find("anti") != -1:
            am_pm = "a"
        Text(hour + ":" + minutes + am_pm).execute()


@GrammarRule
class SimpleStringRule(Base.RegisteredRule):
    spec = "simple string <string>"
    extras = (Dictation("string"),)
    def _process_recognition(self, node, extras):
        action = Text('""') + Key("left") + Text(extras["string"].format()) + Key("right")
        action.execute()    


class KeypressRule(Base.ContinuousRule): 
    extras = (IntegerRef("keyCount", 0, 1000),)
    defaults = {"keyCount": 1}
    def __init__(self, keyName, voicedAs):
        Base.ContinuousRule.__init__(self,
            name="keypress_rule_" + keyName + "_" + voicedAs,
            spec=voicedAs + " [<keyCount> [times]]")          
        self.keyName = keyName
    def _process_recognition(self, node, extras):          
        (Key(self.keyName) * Repeat(extras["keyCount"])).execute()


for keyName, voicedAs in all_keys_by_keyname:
    grammar.add_rule(KeypressRule(keyName, voicedAs))


@GrammarRule
class QuickKeyRules(Base.QuickContinuousRules):
    mapping = {
        "clear special keys": Key("alt:up, ctrl:up, shift:up"),
    }

grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
