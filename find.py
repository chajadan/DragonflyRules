from dragonfly import (Grammar, AppContext, MappingRule, Dictation,
                       Key, Text, FocusWindow, Mouse, StartApp, Repeat, IntegerRef, Text, CompoundRule, Mimic, Pause)

grammar = Grammar("global")

def selectUpThrough(beginning):


class SelectToWordRule(CompoundRule):
	spec = "select up to <word>"
	extras = Dictation("word"),
	def _process_recognition(self, node, extras):
		Text(" ").execute()
		msg = extras["word"].format()
		Mimic(msg).execute()
		Mimic("space").execute()

grammar.load()

# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
