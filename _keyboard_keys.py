print "importing _keyboard_keys"
from dragonfly import *
#import _ruleExport as rex
import BaseGrammars
print "_keyboard_keys, GlobalGrammar id", id(BaseGrammars.GlobalGrammar)
from _BaseRules import *

#exports = rex.ExportedRules()

grammar = BaseGrammars.ContinuousGrammar("keypress grammar")

#decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, BaseQuickRules):
            rule(grammar)
        else:
            grammar.add_rule(rule())
    else:
        grammar.add_rule(rule)

class KeypressRule(ContinuousRule): 
    extras = (IntegerRef("keyCount", 0, 50000),)
    defaults = {"keyCount": 1}
    def __init__(self, keyName, voicedAs):
        self.intro = voicedAs
        ContinuousRule.__init__(self, name = "keypress_rule_" + keyName + "_" + voicedAs, spec = voicedAs + " [<keyCount> [times]]", )          
        self.keyName = keyName
    def _process_recognition(self, node, extras):          
        (Key(self.keyName) * Repeat(extras["keyCount"])).execute()

lower_alpha_names = [
    ['a', 'acre'],
    ['b', 'beaver'],
    ['c', 'season'],
    ['d', 'deny'],
    ['e', 'easy'],
    ['f', 'effort'],
    ['g', 'jeans'],
    ['h', 'huge'],
    ['i', 'island'],
    ['j', 'jail'],
    ['k', 'cable'],
    ['l', 'elf'],
    ['m', 'emblem'],
    ['n', 'energy'],
    ['o', 'oval'],
    ['p', 'pizza'],
    ['q', 'cute'],
    ['r', 'artsy'],
    ['s', 'essence'],
    ['t', 'team'],
    ['u', 'unit'],
    ['v', 'venus'],
    ['w', 'wish'],
    ['x', 'extra'],
    ['y', 'wise'],
    ['z', 'zebra'],
]

keyboard_keys = [
#     ['f1', 'fun one'],
#     ['f2', 'fun two'],
#     ['f3', 'fun three'],
#     ['f4', 'fun four'],
#     ['f5', 'fun five'],
#     ['f6', 'fun six'],
#     ['f7', 'fun seven'],
#     ['f8', 'fun eight'],
#     ['f9', 'fun nine'],
#     ['f10', 'fun ten'],
#     ['f11', 'fun eleven'],
#     ['f12', 'fun twelve'],
    ['ampersand', '&', 'hamper'],
    ['apostrophe', "'", 'posh'],
    ['alt', None, 'alter'],
    ['apps', None, 'application key'],
    ['asterisk', '*', 'astroid'],
    ['at', '@', 'splat'],
    ['backslash', '\\', 'brash'],
    ['backspace', None, 'back'],
    ['backtick', '`', 'grave'],
    ['bar', '|', 'pipe'],
    ['caret', '^', 'circumflex'],
    ['ctrl', None, 'control'],
    ['colon', ':', 'colonic'],
    ['comma', ',', 'condor'],
    ['delete', None, 'delete'],
    ['dollar', '$', 'dollar'],
    ['dot', '.', 'point'],
    ['down', None, 'down'],
    ['dquote', '"', 'quote'],
    ['end', None, 'extreme'],
    ['enter', None, 'carriage'],
    ['equal', '=', 'quail'],
    ['escape', None, 'escape'],
    ['exclamation', '!', 'exclamation'],
    ['hash', '#', 'hash'],
    ['home', None, 'home'],
    ['hyphen', '-', 'stroke'],
    ['insert', None, 'insert'],
    ['langle', '<', 'languid'],
    ['lbrace', '{', 'lace'],
    ['lbracket', '[', 'lack'],
    ['left', None, 'left'],
    ['lparen', '(', 'leper'],
    ['minus', '-', 'subtraction sign'],
    ['percent', '%', 'percent'],
    ['pgdown', None, 'page down'],
    ['pgup', None, 'page up'],
    ['plus', '+', 'addition sign'],
    ['question', '?', 'question'],
    ['rangle', '>', 'rangle'],
    ['rbrace', '}', 'race'],
    ['rbracket', ']', 'rack'],
    ['right', None, 'right'],
    ['rparen', ')', 'riper'],
    ['semicolon', ';', 'wink'],
    ['shift', None, 'shift'],
    ['slash', '/', 'flask'],
    ['space', ' ', 'space'],
    ['tab', None, 'tab'],
    ['tilde', '~', 'squiggle'],
    ['underscore', '_', 'score'],
    ['up', None, 'up'],
    ['win', None, 'window key'],
]


upper_alpha_names = [[letter.upper(), "upper " + name] for letter, name in lower_alpha_names]

alpha_names = lower_alpha_names + upper_alpha_names

all_keys = alpha_names + [[graph, voicedAs] for name, graph, voicedAs in keyboard_keys if graph is not None]

@GrammarRule
class PrefixedKeypressRule(ContinuousRule):
    spec = "letter <Chr>"
    extras = (Choice("Chr", {voicedAs: letter for letter, voicedAs in alpha_names}),)
    def _process_recognition(self, node, extras):
        Text(extras["Chr"]).execute()

@GrammarRule
class SpellByWordsRule(ContinuousRule):
    spec = "letters <LetterWords>"
    extras = (Repetition(Choice("letter", {voicedAs: letter for letter, voicedAs in all_keys}), name="LetterWords", min=1, max=20),)
    def _process_recognition(self, node, extras):
        letters = extras["LetterWords"]
        Text("".join(letters)).execute()

for keyName, graph, voicedAs in keyboard_keys:
    grammar.add_rule(KeypressRule(keyName, voicedAs))
    
grammar.load()
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
