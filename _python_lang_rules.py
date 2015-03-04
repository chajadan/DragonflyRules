from dragonfly import *
from _decorators import *

langName = "python"
langRuleList = []

class KeywordRule(CompoundRule):
    def __init__(self, keyword, voicedAs, alwaysFollowed = False):
        CompoundRule.__init__(self, 
                              name = "python_keyword_" + keyword,
                              spec = voicedAs + "[<code>]",
                              extras = [Dictation("code"),]
                              )
        self.keyword = keyword
        self.alwaysFollowed = alwaysFollowed
     
    def _process_recognition(self, node, extras):
        isFollowed = self.alwaysFollowed or extras.has_key("code") and extras["code"].words[0] != "stay"
        action = Text(self.keyword)
        if isFollowed:
            action += Text(" ")
        if extras.has_key("code"):
            if extras["code"].words[0] == "stay":
                if len(extras["code"].words) > 1:
                    toMimic = extras["code"].words[1:]
                else:
                    toMimic = None
            else:
                toMimic = extras["code"].words
            if toMimic:
                action += Mimic(*extras["code"].words)
        action.execute()
        
# keyword format: written form, spoken form, isAlwaysFollowed (and so necessarily a space afterwards) 
keywords = [
    ["and", "and", True],
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
    langRuleList.append(KeywordRule(entry[0], entry[1], alwaysFollowed = entry[2]))

                
python_keywords_rule = MappingRule(
    name = "python_keywords_rule",
    mapping = {
        "pass": Text("pass") + Key("enter"),
        "then": Text("then:") + Key("enter"),
        },
    extras=[],
    defaults={})
langRuleList.append(python_keywords_rule)

python_ops_rule = MappingRule(
    name = "python_ops_rule",
    mapping = {
        "plus": Text(" + "),
        "minus": Text(" - "),
        "times": Text(" * "),
        },
    extras=[],
    defaults={})
langRuleList.append(python_ops_rule)

python_docnav_rule = MappingRule(
    name = "python_docnav_rule",
    mapping = {
        "indent": Key("end, colon, enter"),
        },
    extras=[],
    defaults={})
langRuleList.append(python_docnav_rule)
    