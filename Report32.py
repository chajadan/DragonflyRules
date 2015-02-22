from dragonfly import *

grammar_context = AppContext(executable="Report32")
grammar = Grammar("ACI", context=grammar_context)


aci_rule = MappingRule(
    name="aci_rule",
    mapping={
             "launch sketch": Key("a-t, d, 1"),
             "import pics": Key("a-t, i") + Pause("200") + Mouse("(22,101), left:1"),
             "import flood map": Key("a-s, f, 1"),
             "first page": Key("a-v, 6, enter"),
             "hex": Key("f3"),
             "next page": Key("c-pgdown"),
             "delete this comp": Key("c-z") + Pause("30") + Key("enter"),
             "import field": Key("a-e, e, f"),
             "import section": Key("a-e, e, s"),
             "view image": Mouse("right:1") + Key("down:2, enter"),
             "delete image": Mouse("right:1") + Key("down:3, enter"),
            },
    )
grammar.add_rule(aci_rule)


grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
