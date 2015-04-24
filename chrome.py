print "importing chrome"
from dragonfly import *
import BaseGrammars
print "chrome, GlobalGrammar id", id(BaseGrammars.GlobalGrammar)
from _BaseRules import *

grammar_context = AppContext(executable="chrome")
grammar = BaseGrammars.ContinuousGrammar("chrome", context=grammar_context)

#decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, BaseQuickRules):
            rule(grammar)
        else:
            grammar.add_rule(rule())
    else:
        grammar.add_rule(rule)

@GrammarRule
class GoToTabRule(ContinuousRule):
    spec = "go to tab <goToTabNum>"
    extras = IntegerRef("goToTabNum", 1, 8),
    def _process_recognition(self, node, extras):
        Key("c-" + str(extras["goToTabNum"])).execute()

@GrammarRule
class ChromeRules(QuickContinuousRules):
    name="chrome_rule"
    mapping = {
		"next tab [<n> [times]]": Key("c-tab") * Repeat(extra="n"),
		"previous tab [<n> [times]]": Key("cs-tab") * Repeat(extra="n"),
		"close (tab | pop up)": {
			"action": Key("c-w"),
			"intro": ["close tab", "close pop up"]},
		"new tab": Key("c-t"),
		"new window": Key("c-n"),
		"incognito window": Key("cs-n"),
		"reopen [last] [tab]": Key("cs-t"),
		"[go to] last tab": Key("c-9"),
        "[go to] last tab but <n>": Key("c-9") + Key("cs-tab") * Repeat(extra="n"),
		"browse back": Key("backspace"),
		"browse forward": Key("s-backspace"),
		"toggle bookmarks": Key("cs-b"),
		"toggle full-screen": Key("f11"),
		"[open] history": Key("c-h"),
		"[open] downloads": Key("c-j"),
		"(go to|select) address": Key("a-d"),
		"refresh": Key("c-f5"),
		"stop (load | loading)": Key("escape"),
		"(open | show) source": Key("c-u"),
		"(save | do | make) bookmark": Key("c-d"),
		"zoom in": Key("c-plus"),
		"zoom out": Key("c-minus"),
		"zoom (default | normal)": Key("c-0"),
		"go to gmail": Key("c-t") + Pause("20") + Text("gmail.com") + Key("enter"),
		"go to PEGym": Key("c-t") + Pause("20") + Text("PEGym.com/forums/") + Key("enter"),      
	}
    extrasDict = {
		"n": IntegerRef("n", 1, 30),
	}
    defaultsDict = {
		"n":1,
	}

@GrammarRule
class GmailRules(QuickContinuousRules):
	name="gmail_rule"
	context = AppContext(title="Gmail")
	mapping = {
		"mark read": Key("s-i"),
		"mark unread": Key("s-u"),
		"read it": Key("x/20, s-i") + Pause("20") + Key("x"),
		"read hover": Mouse("left") + Pause("20") + Key("s-i") + Pause("20") + Mouse("left"),
		"main window": Key("s-escape"),
		"inbox": Key("g/20, i"),
		"go to label <text>": Key("g/20, l") + Pause("20") + Text("%(text)s"),
		"select all": Key("asterisk/20, a"),
		"select read": Key("asterisk/20, r"),
		"select unread": Key("asterisk/20, u"),
		"select none": Key("asterisk/20, n"),
		"(toggle [selection|mark]|mark|un mark)": {
			"action": Key("x"),
			"intro": ["mark", "un mark", "toggle", "toggle selection", "toggle mark"]},
		"search": Text("/"),
		"new message": Text("c"),      
	}
	extrasDict = {
        "text": Dictation("text"),
    }


#---------------------------------------------------------------------------
# Load the grammar instance and define how to unload it.

grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
