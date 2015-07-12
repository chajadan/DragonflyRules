print "importing " + __file__
from dragonfly import *
import BaseGrammars
from BaseRules import *
import inspect

grammar = BaseGrammars.ContinuousGrammar("python grammar", enableCommand="load language python", disableCommand="unload language python", initiallyDisabled=True)

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
    ["while", "while", True],
]
  
for entry in keywords:
    grammar.add_rule(KeywordRule(entry[0], entry[1], alwaysFollowed = entry[2]))
     
@GrammarRule            
class python_keywords_rule(QuickContinuousRules):
    mapping = {
        "break": Text("break") + Key("enter"),
        "else": Text("else:") + Key("enter"),
        "pass": Text("pass") + Key("enter"),
        "try": Text("try:") + Key("enter"),
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
        "special call": Text("__call__"),
        "special class": Text("__class__"),
        "special dictionary": Text("__dict__"),
        "special format": Text("__format__"),
        "special get attribute": Text("__getattr__"),
        "special get": Text("__get__"),
        "special set attribute": Text("__setattr__"),
        "special set": Text("__set__"),
        "special slots": Text("__slots__"),
        "special delete attribute": Text("__delattr__"),
        "special delete": Text("__del__"),
        "special hash": Text("__hash__"),
        "special represent": Text("__repr__"),
        "special comparison": Text("__cmp__"),
        "special contains": Text("__contains__"),
        "special length": Text("__len__"),
        "special non zero": Text("__nonzero__"),
        "special boolean": Text("__bool__"),
        "special future": Text("__future__"),
        "special all": Text("__all__"),
        "special representation": Text("__repr__"),
        "special delete": Text("__delete__"),
        "special less than": Text("__lt__"),
        "special greater than": Text("__gt__"),
        "special equal": Text("__eq__"),
        "special name": Text("__name__"),
        "special not equal": Text("__ne__"),
        "special greater than or equal": Text("__ge__"),
        "special less than or equal": Text("__le__"),
        "special unicode": Text("__unicode__"),
        "special weak reference": Text("__weakref__"),
        "special meta class": Text("__metaclass__"),
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
        "[(do|does)] not equal": Text(" != "),
        "[(is|was|are|were)] less than": Text(" < "),
        "[(is|was|are|were)] less than [or] equal": Text(" <= "),
        "leak": Text(" <= "),
        "[(is|was|are|were)] greater than": Text(" > "),
        "[(is|was|are|were)] greater than [or] equal": Text(" >= "),
        "Greek": Text(" >= "),                
        "compares": Text(" == "),
    }


@GrammarRule
class CodeTemplatesRules(QuickContinuousRules):
    mapping = {
        "call": Text("()"),
        "empty dictionary": Text("{}"),
        "empty list": Text("[]"),
        "slice": Text("[:]") + Key("left:2"),
    }

@GrammarRule
class MemberOperator(ContinuousRule_OptionalRunOn):
    spec = "member"
    def _process_recognition(self, node, extras):
        action = Text(".")
        if "RunOn" in extras:
            member = extras["RunOn"].format()
            action += Text(member)
        action.execute()

@GrammarRule
class CallWithRule(ContinuousRule_OptionalRunOn):
    spec = "call with"
    def _process_recognition(self, node, extras):
        action = Text("()") + Key("left")
        if "RunOn" in extras:
            call_with = extras["RunOn"].format()
            action += Text(call_with)
        action.execute()

@GrammarRule
class BuiltInFunctionRules(QuickContinuousRules):
    name = "built in function rules"
    mapping = {
        "length": Text("len"),
        "print": Text("print"),
        "super": Text("super"),
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