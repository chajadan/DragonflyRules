  # -*- coding: utf-8 -*-

from dragonfly import *
from _support import *
from _decorators import *
from _quickRules import *
import _keyboard as kb
import inspect


imported_rules = [] # list of rules imported from other files for better file structure
lang_rules = {} # keys are "language names", values are list of rules
lang_names = [] # list of imported language names

@CallInPlace
def import_external_rules():
    global imported_rules
    global lang_rules
    global lang_names
    
    # external rules
    import _case_and_joiner_rules
    imported_rules += _case_and_joiner_rules.ruleList
    
    import _keyboard_keys
    imported_rules += _keyboard_keys.ruleList
    
    import _byKeys
    imported_rules += _byKeys.ruleList
    
    import _namedStrings
    imported_rules += _namedStrings.ruleList
    
    # lang rules - intended to be turned on and off
    import _python_lang_rules
    imported_rules += _python_lang_rules.langRuleList
    lang_names += [_python_lang_rules.langName]
    lang_rules[_python_lang_rules.langName] = _python_lang_rules.langRuleList
    
    import _html_lang_rules
    imported_rules += _html_lang_rules.langRuleList
    lang_names += [_html_lang_rules.langName]
    lang_rules[_html_lang_rules.langName] = _html_lang_rules.langRuleList


# Clipboard support

clip = Clipboard()

# master grammar
grammar = Grammar("master grammar")

#decorator
def GrammarRule(Rule):
    if inspect.isclass(Rule):
        if issubclass(Rule, QuickChainedRules):
            Rule(grammar)
        else:
            grammar.add_rule(Rule())
    else:
        grammar.add_rule(Rule)

@GrammarRule
class DisableDragonfly(CompoundRule):
    spec = "(disable|unload) dragonfly"
    def _process_recognition(self, node, extras):
        grammar.disable()
        get_engine().speak("dragonfly darts off")
  
for imported_rule in imported_rules:
    grammar.add_rule(imported_rule)
      
for key in lang_rules.iterkeys():
    for rule in lang_rules[key]:
        rule.disable()

@GrammarRule
class EnableLangRule(CompoundRule):
    spec = "(enable|load) (lang|language|ide) <language>"
    langList = lang_names
    children = (Literal(langName) for langName in langList)
    extras = Alternative(children = children, name="language"),
    def _process_recognition(self, node, extras):
        lang = extras["language"]
        for rule in lang_rules[lang]:
            rule.enable()
        print "lanuage " + lang + " enabled"

@GrammarRule
class DisableLangRule(CompoundRule):
    spec = "(disable|unload) (lang|language) <language>"
    langList = ["python", "html"]
    children = (Literal(langName) for langName in langList)
    extras = Alternative(children = children, name="language"),
    def _process_recognition(self, node, extras):
        lang = extras["language"]
        for rule in lang_rules[lang]:
            rule.disable()

@GrammarRule
class GoToLineRule(CompoundRule):
    spec = "numb <n>"
    extras = IntegerRef("n", 0, 10000000),
    def _process_recognition(self, node, extras):
        Text(str(extras["n"])).execute()
    
@GrammarRule
@BombRule
class ChainRule(CompoundRule):
    spec = "chain <text>"
    extras = Dictation("text"),
    def _process_recognition(self, node, extras):
        msg = extras["text"].format()
        wrds = msg.split(" ")
        for word in wrds:   
            Mimic(word).execute()

@GrammarRule
@BombRule
class LowercaseDictationRule(CompoundRule):
    spec = "words <dictation>"
    extras = (Dictation("dictation"), )
    def _process_recognition(self, node, extras):
        Text(extras["dictation"].format()).execute()
        
@GrammarRule
@BombRule
class LowercaseDictationRule_PrependSpace(CompoundRule):
    spec = "tack <dictation>"
    extras = (Dictation("dictation"), )
    def _process_recognition(self, node, extras):
        Text(" " + extras["dictation"].format()).execute()

@GrammarRule
class GlobalRule(MappingRule):
    name="global_rule"
    mapping={      
             "click [<clickCount> [times]]": Mouse("left:1") * Repeat(extra="clickCount"),
             "trick [<clickCount> [times]]": (Key("ctrl:down") + Mouse("left:1") + Key("ctrl:up")) * Repeat(extra="clickCount"),
             "rick [<clickCount> [times]]": Mouse("right:1") * Repeat(extra="clickCount"),
             "mick [<clickCount> [times]]": Mouse("right:1") * Repeat(extra="clickCount"),
             "double click": Mouse("left:2"),
             "shift": Key("shift:down"),
             "shuft": Key("shift:up"),
             "shaoon [<lineCount> [times]]": Key("shift:down, down, shift:up") * Repeat(extra="lineCount"),
             "shup [<lineCount> [times]]": Key("shift:down, up, shift:up") * Repeat(extra="lineCount"),
             "shlick": Key("shift:down") + Mouse("left:1") + Key("shift:up"),
             "shrick": Key("shift:down") + Mouse("right:1") + Key("shift:up"),
             "lown": Mouse("left:down"),
             "lup": Mouse("left:up"),
             "rown": Mouse("right:down"),
             "rup": Mouse("right:up"),
             "[toggle] flux": Key("a-end"),
             "importer": FocusWindow(title="AciCompiler"),
             "launch explorer": StartApp(r"C:\Windows\Explorer.exe"),
             "sketch": FocusWindow(title="ACI Sketch"),
             "task manager": Key("cs-escape"),
            }
    extras=[
             IntegerRef("keyCount", 1, 1000),
             IntegerRef("n", 1, 10000),
             IntegerRef("clickCount", 1, 1000),
             IntegerRef("lineCount", 1, 1000),
             Dictation("text"),
             Dictation("chain"),
             ]
    defaults={
             "n":1,
             "keyCount":1,
             "clickCount": 1,
             "lineCount": 1,
             }
 
# launch_and_focus_rule is system specific and should be customized for each user's need
@GrammarRule
class LunchAndFocusRule(MappingRule):
    name="launch_and_focus_rule"
    mapping={
        "launch chrome": StartApp(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
        "launch eclipse": StartApp(r"C:\Program Files\eclipse\eclipse.exe"),
        "launch ACI": StartApp(r"C:\Program Files (x86)\ACI32\Applications\Report32.exe"),
        "ACI": FocusWindow(executable="Report32"),
        "chrome": FocusWindow(executable="chrome"),
        "eclipse": FocusWindow(executable="javaw", title="Eclipse"),
    }

@GrammarRule
@BombChain
class SimpleInvokeRule(CompoundRule):
    spec = "call <mimic>"
    extras = Dictation("mimic"),
    def _process_recognition(self, node, extras):
        Mimic(*extras["mimic"].words).execute()
        Mimic("pens").execute()
        
@GrammarRule
class InvokeWithArgumentsRule(CompoundRule):
    spec = "supply <mimic> [with <argMimic>]"
    extras = (Dictation("mimic"), Dictation("argMimic"))
    def _process_recognition(self, node, extras):
        print extras["mimic"].words
        Mimic(*extras["mimic"].words).execute()
        Mimic("park").execute()
        if extras.has_key("argMimic"):
            Mimic(*extras["argMimic"].words).execute()

@GrammarRule
class QuickRules(QuickChainedRules):
    mapping = {
        "strung": Text("\"\"") + Key("left"),
        "brack": Text("[]") + Key("left"),
        "brake": Text("{}") + Key("left"),
        "ankle": Text("<>") + Key("left"),
        "park": Text("()") + Key("left"),
        "pens": Text("()"),
        "quip": Text("(\"\")") + Key("left, left"),
        "spinster": Mimic("pens") + Key("enter"),
        "item": Text(", "),
        "commend": Key("end, comma, enter"),
        "assign": Text(" = "),
        "dref": Text("->"),
        "(monk|upon)": Key("dot"),
        "trim left": Key("s-home, delete"),
        "trim right": Key("s-end, delete"),
    }
 
# for voicedAs, action in QuickChainedRules.items():
#     grammar.add_rule(QuickChainedRule(voicedAs, action))

def JumpRight(jumpTo, sensitive = False):
    copied = ReadLineEnd()
    if not sensitive:
        copied = copied.lower()
        jumpTo = jumpTo.lower()
    places = copied.find(jumpTo)
    if places != -1:
        kb.sendRight(times = places, delay = 0)
        
def JumpLeft(jumpTo, sensitive = False):    
    copied = ReadLineBegin()
    if not sensitive:
        copied = copied.lower()
        jumpTo = jumpTo.lower()
    places = copied.rfind(jumpTo)
    if places != -1:
        places = len(copied) - places
        kb.sendLeft(times = places, delay = 0)

@GrammarRule
@BombRule            
class JeftRule(CompoundRule):
    spec = "jeft <text>"
    extras = Dictation("text"),
    def _process_recognition(self, node, extras):
        where = extras["text"].format()
        Function(JumpLeft).execute({"jumpTo": where})
 
@GrammarRule
@BombRule
class JightRule(CompoundRule):
    spec = "jight <text>"
    extras = Dictation("text"),
    def _process_recognition(self, node, extras):
        where = extras["text"].format()
        Function(JumpRight).execute({"jumpTo": where})
   
def Shule(selectThrough):
    selectThrough = selectThrough.lower()
    copied = ReadLineBegin().lower()
    places = copied.rfind(selectThrough)
    if places != -1:
        kb.shiftDown()
        times = len(copied) - places
        kb.sendLeft(times = times, extended = True, delay = 0)
        kb.shiftUp()
   
def Sure(selectThrough, sensitive = False):
    selectThrough = selectThrough.lower()
    copied = ReadLineEnd().lower()
    places = copied.find(selectThrough)
    if places != -1:
        kb.shiftDown()
        times = places + len(selectThrough)
        kb.sendRight(times = times, extended = True, delay = 0)
        kb.shiftUp()

@GrammarRule
@BombRule   
class SelectThroughLeftRule(CompoundRule):
    spec = "shule <text>"
    extras = Dictation("text"),
    def _process_recognition(self, node, extras):
        where = extras["text"].format()
        Function(Shule).execute({"selectThrough": where})

@GrammarRule
@BombRule
class SelectThroughRightRule(CompoundRule):
    spec = "sure <text>"
    extras = Dictation("text"),
    def _process_recognition(self, node, extras):
        where = extras["text"].format()
        Function(Sure).execute({"selectThrough": where})

def ReplaceAllInSelection(toReplace, replaceWith):
    toReplace = toReplace.lower()
    kb.copy()
    clip.copy_from_system(formats=Clipboard.format_text)
    selection = clip.get_text().lower()
    Text(selection.replace(toReplace, replaceWith)).execute()
    
@GrammarRule
@BombRule
class ReplaceAllInSelectionRule(CompoundRule):
    spec = "replace <toReplace> with <replaceWith>"
    extras = (Dictation("toReplace"), Dictation("replaceWith"))
    def _process_recognition(self, node, extras):
        toReplace = extras["toReplace"].format()
        replaceWith = extras["replaceWith"].format()
        Function(ReplaceAllInSelection).execute({"toReplace": toReplace, "replaceWith": replaceWith})
 
def ReplaceAllInLine(toReplace, replaceWith, sensitive = True):
    pass
#     kb.sendHome()
#     kb.sendEnd()
#     kb.sendShiftHome()
#     line = ReadSelection()
#     if not sensitive:
#         toReplace = toReplace.lower()
#     Text(selection.replace(toReplace, replaceWith)).execute()

@GrammarRule
@BombRule
class ReplaceAllInLineRule(CompoundRule):
    spec = "reline <toReplace> with <replaceWith>"
    extras = (Dictation("toReplace"), Dictation("replaceWith"))
    def _process_recognition(self, node, extras):
        toReplace = extras["toReplace"].format()
        replaceWith = extras["replaceWith"].format()
        Function(ReplaceAllInLine).execute({"toReplace": toReplace, "replaceWith": replaceWith})

@GrammarRule
@BombRule
class SelectWordLeft(CompoundRule):
    spec = "sweft <text>"
    extras = Dictation("text"),
    def _process_recognition(self, node, extras):
        words = ["jeft"] + extras["text"].words
        Mimic(*words).execute()
        kb.shiftDown()
        for _ in range(len(extras["text"].format())):
            kb.sendRight(extended = True, delay = 0)
        kb.shiftUp()

@GrammarRule
@BombRule
class SelectWordRight(CompoundRule):
    spec = "swight <text>"
    extras = Dictation("text"),
    def _process_recognition(self, node, extras):
        words = ["jight"] + extras["text"].words
        Mimic(*words).execute()
        kb.shiftDown()
        for _ in range(len(extras["text"].format())):
            kb.sendRight(extended = True, delay = 0)
        kb.shiftUp()
  
def Respace(spaceCount):
    kb.sendShiftHome()
    kb.copy()
    clip.copy_from_system(formats=Clipboard.format_text)
    leftString = clip.get_text()
    leftSpaceCount = len(leftString) - len(leftString.rstrip())
    kb.sendRight()
    kb.sendShiftEnd()
    kb.copy()
    clip.copy_from_system(formats=Clipboard.format_text)
    rightString = clip.get_text()
    rightSpaceCount = len(rightString) - len(rightString.lstrip())
    kb.sendLeft()
    for _ in range(leftSpaceCount):
        kb.sendLeft()
        print "left"
    kb.shiftDown()
    for _ in range(leftSpaceCount + rightSpaceCount):
        kb.sendRight(True)
        print "right"
    kb.shiftUp()
    (Text(" ") * Repeat(spaceCount)).execute()

@GrammarRule
@ChainedRule
class RespaceRule(CompoundRule):
    spec = "respace <n>"
    extras = IntegerRef("n", 0, 200),
    def _process_recognition(self, node, extras):
        spaceCount = int(extras["n"])
        print spaceCount
        Function(Respace).execute({"spaceCount": spaceCount})
  
def CapitalizeSelection():
    kb.copy()
    clip.copy_from_system(formats = clip.format_text)
    selection = clip.get_text()
    length = len(selection)
    if length > 0:
        kb.sendLeft()
        kb.sendShiftRight()
        Text(selection[0].upper()).execute()

@GrammarRule
@ChainedRule
class CapitalizeSelectionRule(CompoundRule):
    spec = "clap"
    def _process_recognition(self, node, extras):
        Mouse("left:2").execute()
        Function(CapitalizeSelection).execute()

def LowercaseSelection():
    kb.copy()
    clip.copy_from_system(formats = clip.format_text)
    selection = clip.get_text()
    length = len(selection)
    if length > 0:
        kb.sendLeft()
        kb.sendShiftRight()
        Text(selection[0].lower()).execute()

@GrammarRule
@ChainedRule
class LowercaseSelectionRule(CompoundRule):
    spec = "clop"
    def _process_recognition(self, node, extras):
        Mouse("left:2").execute()
        Function(LowercaseSelection).execute()
    
inter_doc_nav_rule = MappingRule(name="inter_doc_nav",
    mapping={
             "rend [<lineCount> [times]]": Key("end, enter") * Repeat(extra="lineCount"),
             "clend": Mouse("left:1") + Key("end, enter"),
             "shome": Key("s-home"),
             "shend": Key("s-end"),
             "lar <n>": Key("end") + (Key("left") * Repeat(extra="n")),
             "far <n>": Key("home") + (Key("right") * Repeat(extra="n")),             
             "trend [<n> [times]]": (Key("down") * Repeat(extra="n")) + Mimic("rend"),
             "cleft [<n> [times]]": Key("c-left") * Repeat(extra="n"),
             "cright [<n> [times]]": Key("c-right") * Repeat(extra="n"),
             "sheft [<keyCount> [times]]": Key("s-left") * Repeat(extra="keyCount"),
             "shite [<keyCount> [times]]": Key("s-right") * Repeat(extra="keyCount"),
             "weft [<n> [times]]": Key("cs-left") * Repeat(extra="n"),
             "white [<n> [times]]": Key("cs-right") * Repeat(extra="n"),
             "lineless [<n> [times]]": (Mimic("end") + Mimic("shomp") + Key("backspace:2")) * Repeat(extra="n"),
             "inner wedge": Key("enter:2, up"),
             "sword": Mouse("left:2") + Key("c-c"),
             "sline": Mimic("end") + Mimic("shome"),
             "sloppy": Mimic("end") + Mimic("shome") + Mimic("copy"),
             "slut": Mimic("'sline") + Mimic("cut"),
             "shomp": Key("s-home, s-home"),
             "shoppy": Key("s-home") + Mimic("copy"),
             "shompy": Key("s-home, s-home") + Mimic("copy"),
             "lean": Mimic("end") + Mimic("shomp") + Mimic("dell"),
             "plaster": Mimic("paste") + Mimic("enter")             
            },
    extras=[
             IntegerRef("keyCount", 1, 1000),
             IntegerRef("lineCount", 1, 100),
             IntegerRef("n", 1, 1000),
             Dictation("text"),
             ],
    defaults={
             "keyCount": 1,
             "lineCount": 1,
             "n": 1,
             }
    )
grammar.add_rule(inter_doc_nav_rule)
   
system_shortcuts_rule = MappingRule(
    name="system_shortcuts",
    mapping={
             "save": Key("c-s"),
             "copy": Key("c-c"),
             "paste": Key("c-v"),
             "cut": Key("c-x"),
             "top": Key("c-home"),
             "bottom": Key("c-end"),
             "select all": Key("c-a"),
             "select top": Key("cs-home"),
             "select bottom": Key("cs-end"),
             "tab windows": Key("alt:down, tab:down"),
             "go to tab <n>": (Key("right") * Repeat(extra="n")) + Key("alt:up, tab:up"),
             "last window": Key("a-tab"),
             "undo": Key("c-z"),
             "find": Key("c-f"),
             "[show] desktop": Key("w-d"),
             "deft": Key("w-left") * Repeat(2),
             "dight":                      Key("w-right") * Repeat(2),
             "hide (others | other windows)": Key("w-home"),
             "minimize":    Key("w-down") * Repeat(2),
             "maximize":   Key("w-up"),
             "close": Key("a-f4"),
            },
    extras=[
             IntegerRef("keyCount", 1, 1000),
             IntegerRef("n", 0, 1000),
             ],
    defaults={
             "keyCount": 1,
             "n": 1,
             }
    )
grammar.add_rule(system_shortcuts_rule)

@GrammarRule
@BombChain
class StringRule(CompoundRule):
    spec = "string <bombChain>"
    extras = Dictation("bombChain"),
    def _process_recognition(self, node, extras):
        (Text ("\"") + Mimic(*extras["bombChain"].words) + Text("\"")).execute()

@GrammarRule
@BombRule
class SpaceDelimitedWordRule(CompoundRule):
    spec = "spaced <word>"
    extras = Dictation("word"),
    def _process_recognition(self, node, extras):
        Text(" ").execute()
        msg = extras["word"].format()
        Mimic(msg).execute()
        Mimic("space").execute()


grammar.load()
print "grammar loaded"

# Listener grammar
listener = Grammar("wake up grammar")

class EnableDragonfly(CompoundRule):
    spec = "(enable|load) dragonfly"
    def _process_recognition(self, node, extras):
        grammar.enable()
        get_engine().speak("dragonfly alive")
listener.add_rule(EnableDragonfly())
listener.load()
    
# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    global listener
    if grammar: grammar.unload()
    grammar = None
    if listener: listener.unload()
    listener = None
