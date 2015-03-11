from dragonfly import (Grammar, AppContext, MappingRule, Dictation,
                       Key, Text, Repeat, IntegerRef, CompoundRule,
                       Function, Pause, Mouse)


#---------------------------------------------------------------------------
# Create this module's grammar and the context under which it'll be active.

grammar_context = AppContext(executable="chrome")
grammar = Grammar("chrome", context=grammar_context)

class GoToTabRule(CompoundRule):
	spec = "go to tab <goToTabNum>"
	extras = IntegerRef("goToTabNum", 1, 8),
	def _process_recognition(self, node, extras):
		Key("c-" + str(extras["goToTabNum"])).execute()

grammar.add_rule(GoToTabRule())

chrome_rule = MappingRule(
    name="chrome_rule",
    mapping={
             "next tab [<n> times]":                           Key("c-tab") * Repeat(extra="n"),
             "previous tab [<n> times]":                   Key("cs-tab") * Repeat(extra="n"),
             "close (tab | pop up)":                         Key("c-w"),
             "new tab":                           Key("c-t"),
             "new window":                   Key("c-n"),
             "incognito window":          Key("cs-n"),
             "reopen [last] [tab]":         Key("cs-t"),
             "[go to] last tab":                Key("c-9"),
             "browse back":                 Key("backspace"),
             "browse forward":            Key("s-backspace"),
             "toggle bookmarks":       Key("cs-b"),
             "toggle full-screen":        Key("f11"),
             "[open] history":                Key("c-h"),
             "[open] downloads":        Key("c-j"),
             "(go to|select) address":	 Key("a-d"),
             "refresh":                           Key("c-f5"),
             "stop (load | loading)":    Key("escape"),
             "(open | show) source":               Key("c-u"),
             "(save | do | make) bookmark":  Key("c-d"),
             "zoom in":                         Key("c-plus"),
             "zoom out":                       Key("c-minus"),
             "zoom (default | normal)":     Key("c-0"),
             "go to gmail": Key("c-t") + Pause("20") + Text("gmail.com") + Key("enter"),
             "go to PEGym": Key("c-t") + Pause("20") + Text("PEGym.com/forums/") + Key("enter"),         
            },
    extras=[
             IntegerRef("n", 1, 30),
             ],
    defaults={
             "n":1,
             }
    )
grammar.add_rule(chrome_rule)

gmail_rule = MappingRule(name="gmail_rule",
    mapping={
             "read": Key("s-i"),
             "unread": Key("s-u"),
             "read it": Key("x/20, s-i") + Pause("20") + Key("x"),
             "read hover": Mouse("left") + Pause("20") + Key("s-i") + Pause("20") + Mouse("left"),
             "main window": Key("s-escape"),
             "inbox": Key("g/20, i"),
             "go to label <text>": Key("g/20, l") + Pause("20") + Text("%(text)s"),
             "select none": Key("asterisk/20, n"),
             "(toggle [selection|mark]|mark|un mark)": Key("x"),
            },
    extras = [
        Dictation("text"),
    ],
    context=AppContext(title="Gmail")
    )
grammar.add_rule(gmail_rule)


#---------------------------------------------------------------------------
# Load the grammar instance and define how to unload it.

grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
