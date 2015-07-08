print "importing " + __file__
from dragonfly import *
from dragonfly.engines.backend_natlink.dictation import NatlinkDictationContainer
import Base
from decorators import ActiveGrammarRule
from chajLib.ui import docnav
from keyboard_keys import printable_keys_as_text

grammar = Base.ContinuousGrammar("text buffer manipulations grammar")


@ActiveGrammarRule(grammar)
class CaretCalls(Base.QuickContinuousCalls):
    mapping = [
        ["after left <RunOn>", docnav.caret_after_left, "target"],
        ["after right <RunOn>", docnav.caret_after_right, "target"],
        ["before left <RunOn>", docnav.caret_before_left, "target"],
        ["before right <RunOn>", docnav.caret_before_right, "target"],
    ]


@ActiveGrammarRule(grammar)
class AfterLeftCharacter(Base.ContinuousRule):
    spec = "after left <characters>"
    extras = (Repetition(Choice("character", {voicedAs: letter for letter, voicedAs in printable_keys_as_text}), name="characters", min=1, max=20),)
    def _process_recognition(self, node, extras):
        letters = extras["characters"]
        target = "".join(letters)
        docnav.caret_after_left(target, True)


@ActiveGrammarRule(grammar)
class AfterRightCharacter(Base.ContinuousRule):
    spec = "after right <characters>"
    extras = (Repetition(Choice("character", {voicedAs: letter for letter, voicedAs in printable_keys_as_text}), name="characters", min=1, max=20),)
    def _process_recognition(self, node, extras):
        letters = extras["characters"]
        target = "".join(letters)
        docnav.caret_after_right(target, True)


@ActiveGrammarRule(grammar)
class BeforeLeftCharacter(Base.ContinuousRule):
    spec = "before left <characters>"
    extras = (Repetition(Choice("character", {voicedAs: letter for letter, voicedAs in printable_keys_as_text}), name="characters", min=1, max=20),)
    def _process_recognition(self, node, extras):
        letters = extras["characters"]
        target = "".join(letters)
        docnav.caret_before_left(target, True)


@ActiveGrammarRule(grammar)
class BeforeRightCharacter(Base.ContinuousRule):
    spec = "before right <characters>"
    extras = (Repetition(Choice("character", {voicedAs: letter for letter, voicedAs in printable_keys_as_text}), name="characters", min=1, max=20),)
    def _process_recognition(self, node, extras):
        letters = extras["characters"]
        target = "".join(letters)
        docnav.caret_before_right(target, True)


TextTarget = Alternative(name="RunOn", children=[
                Sequence([
                    Repetition(
                        Choice("character", {voicedAs: letter for letter, voicedAs in printable_keys_as_text}),
                        name="characters", min=1, max=20),
                    Optional(Dictation("RunOn"))
                ]),
                Dictation("RunOn")
            ])

Direction = Choice("direction", {"left":"left", "right":"right"})


@ActiveGrammarRule(grammar)
class SelectThroughTarget(Base.ContinuousRule):
    spec = "select <direction> through <RunOn>"
    intro_spec = "select (right|left) through <RunOn>"
    extras = (Direction, TextTarget)

    def _process_extras(self, extras):
        if type(extras["RunOn"]) == NatlinkDictationContainer:
            extras["letters"] = ""
        else:
            extras["letters"] = "".join(extras["RunOn"][0]) # spelled by user
            extras["RunOn"] = extras["RunOn"][1]

    def _process_recognition(self, node, extras):
        target = extras["letters"]
        if "RunOn" in extras:
            target += extras["RunOn"].format()
        
        docnav.select_through(extras["direction"], target)

grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None