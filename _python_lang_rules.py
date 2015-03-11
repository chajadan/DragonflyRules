from dragonfly import *
from _decorators import *
from _baseRules import ContinuousRule
from _quickRules import *
from _ruleExport import *

lang = ExportedLang("python")

class KeywordRule(ContinuousRule):
    def __init__(self, keyword, voicedAs, alwaysFollowed = False):
        self.keyword = keyword
        self.alwaysFollowed = alwaysFollowed
        ContinuousRule.__init__(self, name = "python_keyword_" + keyword, spec = voicedAs)       
     
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
        
# keyword format: written form, spoken form, isAlwaysFollowed (and so necessarily a space afterwards) 
keywords = [
    ["and", "and", True],
    ["as", "as", True],
    ["class", "class", True],
    ["def", "define", True],
    ["do", "do", False],
    ["elif", "elif", True],
    ["except", "except", False],
    ["False", "false", False],
    ["for", "for", True],
    ["from", "from", True],
    ["global", "global", True],
    ["if", "if", True],
    ["in", "in", True],
    ["import", "import", True],
    ["None", "none", False],
    ["not", "not", True],
    ["or", "or", True],
    ["pass", "pass", False],
    ["return", "return", True],
    ["self", "self", False],
    ["True", "true", False],
    ["try", "try", False],
    ["while", "while", True],
]

for entry in keywords:
    lang.add(KeywordRule(entry[0], entry[1], alwaysFollowed = entry[2]))

@ExportedRule(lang)                
class python_keywords_rule(QuickContinuousRules):
    name = "python_keywords_rule"
    mapping = {
        "pass": Text("pass") + Key("enter"),
        "else": Text("else:") + Key("enter"),
    }

@ExportedRule(lang)
class python_ops_rule(QuickContinuousRules):
    name = "python_ops_rule"
    mapping = {
        "plus": Text(" + "),
        "minus": Text(" - "),
        "times": Text(" * "),
        "not equal": Text(" != "),
        "[is] less than": {
            "action": Text(" < "),
            "intro": ["less than", "is less than"]},
        "compares": Text(" == "),
    }

@ExportedRule(lang)
class BuiltInFunctionRules(QuickContinuousRules):
    name = "built in function rules"
    mapping = {
        "print": Text("print"),
        "length": Text("len"),
    }

@ExportedRule(lang)
class python_docnav_rule(QuickContinuousRules):
    name = "python_docnav_rule"
    mapping = {
        "indent": Key("end, colon, enter"),
        "unindent": Key("end, enter, backspace"),
    }