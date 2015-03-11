import dragonfly as dfly
from _baseRules import *
import inspect
import _global
import _quickRules as qr

#decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, (qr.BaseQuickRules,)):
            rule(visual_studio_express_grammar)
        elif issubclass(rule, ContinuousGrammarRule):
            visual_studio_express_grammar.add_rule(rule())
        elif issubclass(rule, (Rule, MappingRule, CompoundRule)):
            visual_studio_express_grammar.add_rule(rule())
        else:
            raise TypeError("Unexpected rule type added to visual_studio_express_grammar: " + str(inspect.getmro(rule)))
    else:
        visual_studio_express_grammar.add_rule(rule)
        
visual_studio_express_grammar = _global.GlobalGrammar("Visual Studio express grammar")

@GrammarRule
class ShortcutRules(qr.QuickContinuousRules):
    mapping = {
        "build solution": Key("f7"),
        "comment selection": Key("c-e, c-c"),
        "uncommon selection": Key("c-e, c-u"),
        "go to definition": Key("f12"),
        "toggle file": Key("c-m, c-o"),
    }