from dragonfly import *
import BaseGrammars
from BaseRules import *
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
class DocNavRules(QuickContinuousRules):
    extrasDict = {
    }
    defaultsDict = {
    }    
    mapping = {
        "(clap|capitalize hovered)": Mouse("left:2") + Function(docnav.capitalize_first_word_of_selection),
        "(clop|lowercase hovered)": Mouse("left:2") + Function(docnav.lowercase_first_word_of_selection),
    }


@GrammarRule
class ReplaceSurroundingCharacters(ContinuousRule_EatDictation):
    spec = "replace <direction> [<n> [times]] (character|characters)"
    introspec = "replace (left|right)"
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


@GrammarRule
class ReplaceTrim(ContinuousRule_EatDictation):
    spec = "replace <direction>"
    introspec = "replace (left|right)"
    extras = (Choice("direction", {"left":"home", "right":"end"}),)
    def _process_recognition(self, node, extras):
        action = Key("s-" + extras["direction"])
        if "RunOn" in extras:
            replacement = extras["RunOn"].format()
            action += Text(replacement)
        else:
            action += Key("delete")
        action.execute()


@GrammarRule
class DocNavEditCalls(QuickContinuousCalls):
    mapping = [
        ["paste left", docnav.replace_left_from_clipboard],
        ["paste right", docnav.replace_right_from_clipboard],
        ["replace left <RunOn>", docnav.replace_left, "replacement"],
        ["replace right <RunOn>", docnav.replace_right, "replacement"],
        ["[make] space count <count>", docnav.respace_around_caret],
    ]
    extras = (IntegerRef("count", 0, 1000),)


grammar.load()
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None