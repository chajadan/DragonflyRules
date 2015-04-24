from dragonfly import *
import  _BaseGrammars
from _BaseRules import *
import inspect

grammar = _BaseGrammars.ContinuousGrammar("python grammar", enableCommand="load language python", disableCommand="unload language python", initiallyDisabled=True)

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
    ["assert", "assert", True],
    ["class", "class", True],
    ["def", "define", True],
    ["del", "dell", True],
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
    grammar.add_rule(KeywordRule(entry[0], entry[1], alwaysFollowed = entry[2]))
     
@GrammarRule            
class python_keywords_rule(QuickContinuousRules):
    mapping = {
        "pass": Text("pass") + Key("enter"),
        "else": Text("else:") + Key("enter"),
    }
    extrasDict = {}
    defaultsDict = {}
    
@GrammarRule            
class python_special_methods_rule(QuickContinuousRules):
    mapping = {
        "special initialize": Text("__init__"),
        "special represent": Text("__repr__"),
        "special string": Text("__str__"),
        "special bytes": Text("__bytes__"),
        "special format": Text("__format__"),
        "special represent": Text("__repr__"),
        "special contains": Text("__contains__"),
        "special length": Text("__len__"),
        "special non zero": Text("__nonzero__"),
        "special bool": Text("__bool__"),
    }
    extrasDict = {}
    defaultsDict = {}    
  
@GrammarRule
class python_ops_rule(QuickContinuousRules):
    name = "python_ops_rule"
    mapping = {
        "plus": Text(" + "),
        "minus": Text(" - "),
        "times": Text(" * "),
        "not equal": Text(" != "),
        "[is] less than": Text(" < "),
        "compares": Text(" == "),
    }
  
@GrammarRule
class BuiltInFunctionRules(QuickContinuousRules):
    name = "built in function rules"
    mapping = {
        "print": Text("print"),
        "length": Text("len"),
    }
  
@GrammarRule
class python_docnav_rule(QuickContinuousRules):
    name = "python_docnav_rule"
    mapping = {
        "indent": Key("end, colon, enter"),
        "unindent": Key("end, enter, backspace"),
    }

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