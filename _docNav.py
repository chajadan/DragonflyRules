from dragonfly import *
import Base
import inspect
from chajLib.ui import docnav
from keyboard_keys import printable_keys_as_text

grammar = Base.ContinuousGrammar("text buffer manipulations grammar")

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
class CaretCalls(Base.QuickContinuousCalls):
    mapping = [
        ["after left <RunOn>", docnav.caret_after_left, "target"],
        ["after right <RunOn>", docnav.caret_after_right, "target"],
        ["before left <RunOn>", docnav.caret_before_left, "target"],
        ["before right <RunOn>", docnav.caret_before_right, "target"],
    ]


@GrammarRule
class SelectCalls(Base.QuickContinuousCalls):
    mapping = [
        ["select left through <RunOn>", docnav.select_through_left, "target"],
        ["select right through <RunOn>", docnav.select_through_right, "target"],
    ]


@GrammarRule
class AfterLeftCharacter(Base.ContinuousRule):
    spec = "after last <characters>"
    extras = (Repetition(Choice("character", {voicedAs: letter for letter, voicedAs in printable_keys_as_text}), name="characters", min=1, max=20),)
    def _process_recognition(self, node, extras):
        letters = extras["characters"]
        target = "".join(letters)
        docnav.caret_after_left(target, True)


@GrammarRule
class AfterRightCharacter(Base.ContinuousRule):
    spec = "after right <characters>"
    extras = (Repetition(Choice("character", {voicedAs: letter for letter, voicedAs in printable_keys_as_text}), name="characters", min=1, max=20),)
    def _process_recognition(self, node, extras):
        letters = extras["characters"]
        target = "".join(letters)
        docnav.caret_after_right(target, True)


@GrammarRule
class BeforeLeftCharacter(Base.ContinuousRule):
    spec = "before left <characters>"
    extras = (Repetition(Choice("character", {voicedAs: letter for letter, voicedAs in printable_keys_as_text}), name="characters", min=1, max=20),)
    def _process_recognition(self, node, extras):
        letters = extras["characters"]
        target = "".join(letters)
        docnav.caret_before_left(target, True)


@GrammarRule
class BeforeRightCharacter(Base.ContinuousRule):
    spec = "before right <characters>"
    extras = (Repetition(Choice("character", {voicedAs: letter for letter, voicedAs in printable_keys_as_text}), name="characters", min=1, max=20),)
    def _process_recognition(self, node, extras):
        letters = extras["characters"]
        target = "".join(letters)
        docnav.caret_before_right(target, True)


grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None