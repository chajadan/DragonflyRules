from dragonfly import *
import inspect
import Base

grammar_context = AppContext(executable="devenv")        
grammar = Base.ContinuousGrammar("Visual Studio Community grammar", grammar_context)

#decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, (Base.BaseQuickRules,)):
            rule(grammar)
        else:
            grammar.add_rule(rule())
    else:
        grammar.add_rule(rule)


@GrammarRule
class ShortcutRules(Base.QuickContinuousRules):
    mapping = {
        "add new item": Key("cs-a"),
        "build solution": Key("f7"),
        "find all references": Mouse("left:1") + Key("apps, a:2, enter"),
        "comment selection": Key("c-k, c-c"),
        "uncomment selection": Key("c-k, c-u"),
        "go to definition": Key("f12"),
        "go to declaration": Key("ca-f12"),
        "toggle file": Key("c-k, c-o"), # swaps from cpp to h file, and vice versa
        "recent projects": Key("a-f, j"),
        "save all": Key("cs-s"),
        "build this project only": Key("a-b, j, b"),
        "rebuild this project only": Key("a-b, j, r"),
        "clean this project only": Key("a-b, j, c"),
        "parameter info": Key("cs-space"),
        "go to last project": Key("a-f, j, down, enter"),
        "go to line <n>": Key("c-g") + Text("%(n)s") + Key("enter"),
    }
    extrasDict = {"n": IntegerRef("n", 1, 100000)}
    defaultsDict = {"n": 1}


@GrammarRule
class PreprocessorRules(Base.QuickContinuousRules):
    mapping = {
        "pragma once": Text("#pragma once"),
    }


grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None    