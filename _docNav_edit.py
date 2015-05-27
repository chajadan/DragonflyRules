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
class DocNavEditRules(QuickContinuousRules):
    extrasDict = {
        "n": IntegerRef("n", 1, 1000),
    }
    defaultsDict = {
        "n": 1,
    }    
    mapping = {
        "(clap|capitalize hovered)": Mouse("left:2") + Function(docnav.capitalize_first_word_of_selection),
        "(clop|lowercase hovered)": Mouse("left:2") + Function(docnav.lowercase_first_word_of_selection),
        "crater": Mouse("left:1") + Key("end, enter"),
        "cut line": Key("end, s-home") + Mimic("cut"),
        "delete last word [<n> [times]]": Key("end") + Key("c-left") * Repeat(extra="n") + Key("s-end, delete"),
        "delete line": Key("end, s-home, s-home") + Mimic("delete"),
        "inner wedge": Key("enter:2, up"),
        "lineless [<n> [times]]": Key("home, end, s-home:2, delete, backspace") * Repeat(extra="n"),
        "lineless down [<n> [times]]": Key("down, home, end, s-home:2, delete, backspace") * Repeat(extra="n"),
        "plaster": Key("c-v, enter"),
        "renter [<n> [times]]": Key("end, enter") * Repeat(extra="n"),
        "renter down [<n> [times]]": (Key("down") * Repeat(extra="n")) + Key("end, enter"),
        "renter up [<n> [times]]": (Key("up") * Repeat(extra="n")) + Key("end, enter"),
        "trim left": Key("s-home, delete"),
        "trim right": Key("s-end, delete"),       
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
        ["replace selection <to_replace> with <RunOn>",
            docnav.replace_all_in_selection, "replacement"],
        ["replace line <to_replace> with <RunOn>",
            docnav.replace_all_in_line, "replacement"],
    ]
    extras = (IntegerRef("count", 0, 1000),
              Dictation("to_replace"),
              )
        
        
grammar.load()
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None