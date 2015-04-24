print "importing _docNav_edit"
from dragonfly import *
import BaseGrammars
print "_docNav_edit, GlobalGrammar id", id(BaseGrammars.GlobalGrammar)
from _BaseRules import *
import chajLib.ui.docnav as docnav
import chajLib.ui.keyboard as kb

grammar = BaseGrammars.ContinuousGrammar("document navigation - edit grammar")

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
class ReplaceLeftCharacters(ContinuousRule_EatDictation):
    spec = "replace <direction> (character|characters) [<n> [times]]"
    introspec = "replace (left|right) (character|characters)"
    #intro = ["replace left character", "replace left characters", "replace right character", "replace right characters"]
    extras = (IntegerRef("n", 1, 200), Choice("direction", {"left":"left", "right":"right"}))
    defaults = { "n": 1}
    def _process_recognition(self, node, extras):
        action = Key("s-" + extras["direction"]) * Repeat(count=extras["n"])
        if "RunOn" in extras:
            replacement = " ".join(extras["RunOn"].words)
            action += Text(replacement)
        else:
            action += Key("delete")
        action.execute()


grammar.load()
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None