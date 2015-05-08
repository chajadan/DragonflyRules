from dragonfly import *
from BaseRules import *

grammar = Grammar("global")

def selectUpThrough(beginning):
    pass

class SelectToWordRule(CorrectableRule):
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
