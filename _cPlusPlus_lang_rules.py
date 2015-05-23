print "import cPlusPlus_lang_rules"
from dragonfly import *
import BaseGrammars
from BaseRules import *
from chajLib.ui import docnav

grammar = BaseGrammars.ContinuousGrammar("c++ grammar", enableCommand='load language see plus plus', disableCommand='unload language see plus plus', initiallyDisabled=True)

#decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, BaseQuickRules):
            rule(grammar)
        else:
            grammar.add_rule(rule())
    else:
        grammar.add_rule(rule) 

class KeywordRule(ContinuousRule):
    def __init__(self, keyword, voicedAs, alwaysFollowed = False):
        self.keyword = keyword
        self.alwaysFollowed = alwaysFollowed
        ContinuousRule.__init__(self, name = "c++_keyword_" + keyword, spec = voicedAs)       
     
    def _process_recognition(self, node, extras):
        isFollowed = self.alwaysFollowed 
        action = Text(self.keyword)
        if isFollowed:
            action += Text(" ")
#         if extras.has_key("code"):
#             if extras["code"].words[0] == "stay":
#                 if len(extras["code"].words) > 1:
#                     toMimic = extras["code"].words[1:]
#                 else:
#                     toMimic = None
#             else:
#                 toMimic = extras["code"].words
#             if toMimic:
#                 action += Mimic(*extras["code"].words)
        action.execute()
        
# keyword format: written form, spoken form, isAlwaysFollowed (and so necessarily a space afterwards), isAlwaysPreceded
keywords = [
    ["bool", "Boolean", True, False],
    ["case", "case", True, False],
    ["catch", "catch", True, False],
    ["class", "class", True, False],
    ["const", "const", False, False],
    ["do", "do", True, False],
    ["double", "double", True, False],
    ["else", "else", True, False],
    ["false", "false", False, True],
    ["float", "float", True, False],
    ["for", "for", True, False],
    ["if", "if", True, False],
    ["int", "integer", True, False],
    ["namespace", "namespace", True, False],
    ["return", "return", False, False],
    ["true", "true", False, False],
    ["try", "try", True, False],
    ["using", "using", True, False],
    ["void", "void", True, False],
    ["while", "while", True, False],
]

for entry in keywords:
    grammar.add_rule(KeywordRule(entry[0], entry[1], alwaysFollowed = entry[2]))

@GrammarRule
class OperatorRules(QuickContinuousRules):
    mapping = {
        "address of": Text("& "), 
        "plus": Text(" + "),
        "minus": Text(" - "),
        "times": Text(" * "),
        "not equal": Text(" != "),
        "[is] less than": Text(" < "),
        "[is] greater than": Text(" > "),               
        "compares": Text(" == "),
        "reference": Text("& "),
        "resolve": Text("::"),
        "comment": Text("// "),
        "start comment": Text("/* "),
        "end comment": Text(" */"),
    }

@GrammarRule
class PreprocessorRules(QuickContinuousRules):
    mapping = {
        "include": Text("#include "),
    }


@GrammarRule
class CommonNamesRules(QuickContinuousRules):
    mapping = {
        "standard": Text("std::"),
    }


@GrammarRule
class CodeTemplatesRules(QuickContinuousRules):
    mapping = {
        "new block": Text(" {}") + Key("left, enter:2, up, tab"),
    }


@GrammarRule
class QuickEditRules(QuickContinuousRules):
    mapping = {
        "terminate": Key("end") + Text(";"),
        "next statement": Key("end") + Text(";") + Key("enter"),
    }


@GrammarRule
class MultilineCommentSelection(ContinuousRule):
    """
    only different from "comment selection" in that it surrounds the selections
    with spaces, and is always /* multiline */ style
    """
    spec = "format comment selection"
    def _process_recognition(self, node, extras):
        selection = docnav.read_selection()
        Text("/* " + selection + " */").execute()


grammar.load()
listener = grammar.listener()
listener.load()
         
def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
    global listener
    if listener is not None:
        listener.unload()
    listener = None