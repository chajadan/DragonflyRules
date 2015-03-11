from dragonfly import *
from _decorators import *
from _baseRules import *
import _quickRules as qr

langName = "C++"
langRuleList = []

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
    ["catch", "catch", True, False],
    ["class", "class", True, False],
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
    langRuleList.append(KeywordRule(entry[0], entry[1], alwaysFollowed = entry[2]))

class OperatorRules(qr.QuickContinuousRules):
    mapping = {
        "plus": Text(" + "),
        "minus": Text(" - "),
        "times": Text(" * "),
        "not equal": Text(" != "),
        "[is] less than": {
            "action": Text(" < "),
            "intro": ["less than", "is less than"]},
        "[is] greater than": {
            "action": Text(" > "),
            "intro": ["less greater", "is less greater"]},               
        "compares": Text(" == "),
    }
# python_keywords_rule = MappingRule(
#     name = "python_keywords_rule",
#     mapping = {
#         "pass": Text("pass") + Key("enter"),
#         "then": Text("then:") + Key("enter"),
#         },
#     extras=[],
#     defaults={})
# langRuleList.append(python_keywords_rule)
# 
# python_ops_rule = MappingRule(
#     name = "python_ops_rule",
#     mapping = {
#         "plus": Text(" + "),
#         "minus": Text(" - "),
#         "times": Text(" * "),
#         },
#     extras=[],
#     defaults={})
# langRuleList.append(python_ops_rule)
# 
# python_docnav_rule = MappingRule(
#     name = "python_docnav_rule",
#     mapping = {
#         "indent": Key("end, colon, enter"),
#         },
#     extras=[],
#     defaults={})
# langRuleList.append(python_docnav_rule)