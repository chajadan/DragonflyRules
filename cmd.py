from dragonfly import *

grammar = Grammar("cmd")

cmd_rule = MappingRule(
    name="static",
    mapping={
             "paste":                     Key("a-space, e, p"),
             "repeat last":	          Key("up, enter"),
             "interrupt": Key("c-c"),
            },
    )


grammar.add_rule(cmd_rule)
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
