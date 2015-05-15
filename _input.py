print "import _input"
from dragonfly import *
import input_conversion as conv
import Base
import inspect

grammar = Base.ContinuousGrammar("input elements and sequences grammar")


#decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, Base.BaseQuickRules):
            rule(grammar)
        else:
            grammar.add_rule(rule())
    else:
        grammar.add_rule(rule)


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
    extras = (Repetition(Choice("digit", choices=conv._digits), name="digits", min=1, max=50),)
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


grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None