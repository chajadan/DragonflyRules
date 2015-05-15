from dragonfly import *
import BaseGrammars
from BaseRules import *
import chajLib.ui.docnav as docnav
import chajLib.ui.keyboard as kb

grammar = BaseGrammars.ContinuousGrammar("document navigation - selection grammar")

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
class InterDocNavRules(QuickContinuousRules):
    name="inter_doc_nav"
    extrasDict = {
        "keyCount": IntegerRef("keyCount", 1, 1000),
        "lineCount": IntegerRef("lineCount", 1, 1000),
        "n": IntegerRef("n", 1, 1000),
        "text": Dictation("text"),
    }
    defaultsDict = {
        "keyCount": 1,
        "lineCount": 1,
        "n": 1,
    }    
    mapping = {       
        "copy bottom": Key("cs-end, c-c"),
        "copy full left": Key("s-home, s-home") + Mimic("copy"),
        "copy left": Key("s-home, c-c"),
        "copy line": Key("end, s-home") + Mimic("copy"),
        "copy right": Key("s-end, c-c"),
        "copy top": Key("cs-home, c-c"),       
        "first character but <n>": Key("home") + (Key("right") * Repeat(extra="n")),       
        "last character but <n>": Key("end") + (Key("left") * Repeat(extra="n")),
        "select all": Key("c-a"),
        "select top": Key("cs-home"),       
        "select bottom": Key("cs-end"),
        "select full left": Key("s-home, s-home"),
        "select line": Key("end, s-home"),
        "select full line": Key("end, s-home, s-home"),
        "select up [<lineCount> [times]]": Key("shift:down, up, shift:up") * Repeat(extra="lineCount"),
        "select down [<lineCount> [times]]": Key("shift:down, down, shift:up") * Repeat(extra="lineCount"),
        "select lines up <n>": Key("end, s-home") + Key("s-up") * Repeat(count=-1, extra="n"),
        "select lines down <n>": Key("end, s-home") + Key("s-down") * Repeat(count=-1, extra="n"),
        "select final word [<n> [times]]": Key("end") + Key("sc-left") * Repeat(extra="n"),
        "select first word [<n> [times]]": Key("home") + Key("sc-right") * Repeat(extra="n"),        
        "(sword|select word) left [<n> [times]]": {
            "action": Key("cs-left") * Repeat(extra="n"),
            "intro": ["sword left", "select word left"]},
        "(sword|select word) right [<n> [times]]": {
            "action": Key("cs-right") * Repeat(extra="n"),
            "intro": ["sword right", "select word right"]},
        "select just word right": Key("cs-right, s-left"),
        "(scare|select character) left [<keyCount> [times]]": {
            "action": Key("s-left") * Repeat(extra="keyCount"),
            "intro": ["scare left", "select character left"]},
        "(scare|select character) right [<keyCount> [times]]": {
            "action": Key("s-right") * Repeat(extra="keyCount"),
            "intro": ["scare right", "select character right"]},               
        "sword": Mouse("left:2") + Key("c-c"),
        "word left [<n> [times]]": {
            "action": Key("c-left") * Repeat(extra="n"),},
        "word right [<n> [times]]": {
            "action": Key("c-right") * Repeat(extra="n"),}, 
    }


@GrammarRule
class SelectPhraseLeft(ContinuousRule_EatDictation):
    spec = "select left"
    def _process_recognition(self, node, extras):
        if not extras.has_key("RunOn"):
            Key("s-home").execute()
        else:
            words = "before left".split() + extras["RunOn"].words
            Mimic(*words).execute()
            kb.shiftDown()
            for _ in range(len(extras["RunOn"].format())):
                kb.sendRight(extended = True, delay = 0)
            kb.shiftUp()

@GrammarRule
class SelectPhraseRight(ContinuousRule_EatDictation):
    spec = "select right"
    def _process_recognition(self, node, extras):
        if not extras.has_key("RunOn"):
            Key("s-end").execute()   
        else:
            words = "before right".split() + extras["RunOn"].words
            Mimic(*words).execute()
            kb.shiftDown()
            for _ in range(len(extras["RunOn"].format())):
                kb.sendRight(extended = True, delay = 0)
            kb.shiftUp()


grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
