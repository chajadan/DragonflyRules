from dragonfly import *
import inspect
import BaseGrammars
from BaseRules import *

grammar_context = AppContext(executable="WDExpress")        
grammar = BaseGrammars.ContinuousGrammar("Visual Studio express grammar", grammar_context)

#decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, (BaseQuickRules,)):
            rule(grammar)
        elif issubclass(rule, ContinuousGrammarRule):
            grammar.add_rule(rule())
            print "cgr", rule.__name__
        elif issubclass(rule, (Rule, MappingRule, CompoundRule)):
            print "rmc", rule.__name__
            grammar.add_rule(rule())
        else:
            raise TypeError("Unexpected rule type added to grammar: " + str(inspect.getmro(rule)))
    else:
        grammar.add_rule(rule)

# @GrammarRule
# class RecentProjectsRule(ContinuousRule):
#     spec = "recent projects"
#     def _process_recognition(self, node, extras):
#         Key("c-f, j").execute()

@GrammarRule
class ShortcutRules(QuickContinuousRules):
    mapping = {
        "add new item": Key("cs-a"),
        "build solution": Key("f7"),
        "find all references": Mouse("left:1") + Key("c-k, c-r"),
        "comment selection": Key("c-e, c-c"),
        "uncomment selection": Key("c-e, c-u"),
        "go to definition": Key("f12"),
        "go to declaration": Key("ca-f12"),
        "toggle file": Key("c-k, c-o"), # swaps from cpp to h file, and vice versa
        "recent projects": Key("a-f, j"),
        "save all": Key("cs-s"),
        "build this project only": Key("a-b, j, b"),
        "rebuild this project only": Key("a-b, j, r"),
        "clean this project only": Key("a-b, j, c"),
        "parameter info": Key("c-k, c-p"),
        "recent projects": Key("a-f, j"),
        "go to last project": Key("a-f, j, down, enter"),
    }


@GrammarRule
class PreprocessorRules(QuickContinuousRules):
    mapping = {
        "pragma once": Text("#pragma once"),
    }


@GrammarRule
class RulesWithArguments(QuickContinuousRules):
    mapping = {
        "go to line <n>": Key("c-g") + Text("%(n)s") + Key("enter"),
    }
    extrasDict = {"n": IntegerRef("n", 1, 100000)}
    defaultsDict = {"n": 1}


@GrammarRule
class ContextSpecificRules(QuickContinuousRules):
    extrasDict = {
    }
    defaultsDict = {
    }    
    mapping = {      
    }


grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None    