  # -*- coding: utf-8 -*-

from dragonfly import *
from _global import *
from _ContinuousGrammar import *
from _support import *
from _decorators import *
import _quickRules
import _keyboard as kb
import inspect


lang_rules = {} # keys are "language names", values are list of rules
lang_names = [] # list of imported language names

masterRunOn = ContinuousGrammar("master run on grammar")
grammar = GlobalGrammar("master non run on grammar")

@CallInPlace
def import_external_rules():
 
    def add_rules(ruleList):
        for i, rule in enumerate(ruleList):
            if inspect.isclass(rule):
                if issubclass(rule, _quickRules.QuickRules):
                    ruleList[i] = rule(grammar)
                elif issubclass(rule, _quickRules.QuickContinuousRules):
                    ruleList[i] = rule(masterRunOn)
                else:
                    print rule
                    print inspect.getmro(rule)
                    raise RuntimeError("add_rules is not expecting this class: " + rule.__name__)
            elif getattr(rule, "isContinuous", False):
                masterRunOn.add_rule(rule)
            else:
                grammar.add_rule(rule)
                
    def prepare_language(lang):
        global lang_names
        global lang_rules
        add_rules(lang.ruleList)
        lang_names += [lang.language_name]
        rules = [] # we need to a list of rule instances, so gather rules from rule collections like QuickRules
        for rule in lang.ruleList:
            if isinstance(rule, _quickRules.BaseQuickRules):
                rules += rule._rules
            else:
                rules.append(rule)
        lang_rules[lang.language_name] = rules
                
    # external rules
    import _byKeys
    add_rules(_byKeys.exports.ruleList)
    
    import _case_and_joiner_rules
    add_rules(_case_and_joiner_rules.exports.ruleList)
    
    import _keyboard_keys
    add_rules(_keyboard_keys.exports.ruleList)
    
    import _myLaunchFocus
    add_rules(_myLaunchFocus.exports.ruleList)
    
    import _namedStrings
    add_rules(_namedStrings.exports.ruleList)
    
    # lang rules - intended to be turned on and off
    import _python_lang_rules
    prepare_language(_python_lang_rules.lang)
    
    import _html_lang_rules
    prepare_language(_html_lang_rules.lang)


# Clipboard support
clip = Clipboard()

#decorator
def GrammarRule(rule):
    if inspect.isclass(rule):
        if issubclass(rule, (_quickRules.QuickChainedRules, _quickRules.QuickRules)):
            rule(grammar)
        elif issubclass(rule, (_quickRules.QuickContinuousRules)):
            rule(masterRunOn)
        elif issubclass(rule, ContinuousGrammarRule):
            masterRunOn.add_rule(rule())
        elif issubclass(rule, (Rule, MappingRule, CompoundRule)):
            grammar.add_rule(rule())
        else:
            raise TypeError("Unexpected rule type added to grammar: " + str(inspect.getmro(rule)))
    else:
        grammar.add_rule(rule)

@GrammarRule
class DisableDragonfly(RegisteredRule):
    spec = "(disable|unload) dragonfly"
    intro = ["disable dragonfly", "unload dragonfly"]
    def _process_recognition(self, node, extras):
        grammar.disable()
        masterRunOn.disable()
        get_engine().speak("dragonfly darts off")
      
for key in lang_rules.iterkeys():
    for rule in lang_rules[key]:
        rule.disable()

@GrammarRule
class EnableLangRule(ContinuousRule):
    spec = "(enable|load) (lang|language) <language>"
    intro = ["enable lang", "enable language", "load lang", "load language"]
    langList = lang_names
    children = (Literal(langName) for langName in langList)
    extras = Alternative(children = children, name="language"),
    def _process_recognition(self, node, extras):
        lang = extras["language"]
        for rule in lang_rules[lang]:
            rule.enable()
        get_engine().speak("enabled")

@GrammarRule
class DisableLangRule(ContinuousRule):
    spec = "(disable|unload) (lang|language) <language>"
    intro = ["disable lang", "disable language", "unload lang", "unload language"]
    langList = lang_names
    children = (Literal(langName) for langName in langList)
    extras = Alternative(children = children, name="language"),
    def _process_recognition(self, node, extras):
        lang = extras["language"]
        for rule in lang_rules[lang]:
            rule.disable()
        get_engine().speak("disabled")

@GrammarRule
class NumericDigitsRule(ContinuousRule):
    spec = "number <n>"
    extras = IntegerRef("n", 0, 999999999),
    def _process_recognition(self, node, extras):
        Text(str(extras["n"])).execute()
    
@GrammarRule
class StreamWordsAtCursorRule(ContinuousRule):
    spec = "stream <RunOn>"
    extras = (Dictation("RunOn"), )
    def _process_recognition(self, node, extras):
        print extras
        print node
        Text(extras["RunOn"].format()).execute()

@GrammarRule
class PureWordsDictationRule(RegisteredRule):
    spec = "words <RunOn>"
    extras = (Dictation("RunOn"), )
    def _process_recognition(self, node, extras):
        print extras
        print node
        Text(extras["RunOn"].format()).execute()

@GrammarRule
class PrependSpaceRule(ContinuousRule):
    spec = "tack <RunOn>"
    extras = (Dictation("RunOn"), )
    def _process_recognition(self, node, extras):
        Text(" " + extras["RunOn"].format()).execute()

@GrammarRule
class SomeQuickRules(_quickRules.QuickContinuousRules):
    name="GlobalQuickRules"
    extrasDict = {
        "keyCount": IntegerRef("keyCount", 1, 1000),
        "n": IntegerRef("n", 1, 10000),
        "clickCount": IntegerRef("clickCount", 1, 1000),
        "lineCount": IntegerRef("lineCount", 1, 1000),
        "text": Dictation("text"),
        "chain": Dictation("chain"),
    }
    defaultsDict = {
        "n": 1,
        "keyCount": 1,
        "clickCount": 1,
        "lineCount": 1,
    }    
    mapping= {      
        "click [<clickCount> [times]]": {
            "action": Mouse("left:1") * Repeat(extra="clickCount"),
            "intro": "click"},
        "click paste": Mouse("left:1") + Key("c-v"),
        "control click [<clickCount> [times]]": {
            "action": (Key("ctrl:down") + Mouse("left:1") + Key("ctrl:up")) * Repeat(extra="clickCount"),
            "intro": "control click"},
        "right click [<clickCount> [times]]": {
            "action": Mouse("right:1") * Repeat(extra="clickCount"),
            "intro": "right click"},            
        "middle click [<clickCount> [times]]": {
            "action": Mouse("middle:1") * Repeat(extra="clickCount"),
            "intro": "middle click"},
        "double click": Mouse("left:2"),
        "shift down": Key("shift:down"),
        "shift up": Key("shift:up"),
        "select down [<lineCount> [times]]": {
            "action": Key("shift:down, down, shift:up") * Repeat(extra="lineCount"),
            "intro": "select down"},
        "select up [<lineCount> [times]]": {
            "action": Key("shift:down, up, shift:up") * Repeat(extra="lineCount"),
            "intro": "select up"},
        "shift click": Key("shift:down") + Mouse("left:1") + Key("shift:up"),
        "shift right click": Key("shift:down") + Mouse("right:1") + Key("shift:up"),
        "down click": Mouse("left:down"),
        "up click": Mouse("left:up"),
        "down right click": Mouse("right:down"),
        "up right click": Mouse("right:up"),
        "[toggle] flux": {
            "action": Key("a-end"),
            "intro": ["flux", "toggle flux"]},         
    }

  
@GrammarRule
class QuickCRules(_quickRules.QuickContinuousRules):
    mapping = {
        "(in quotes|string it)": {
            "action": Text("\"\"") + Key("left"),
            "intro": ["in quotes", "string it"]},
        "in brackets": Text("[]") + Key("left"),
        "brackets": Text("[]"),
        "angle brackets": Text("<>"),
        "parentheses": Text("()"),
        "in curly brackets": Text("{}") + Key("left"),
        "in angle brackets": Text("<>") + Key("left"),
        "call with": Text("()") + Key("left"),
        "call": Text("()"),
        "item": Text(", "),
        "assign": Text(" = "),
        "dereference": Text("->"),
        "dot": Key("dot"),
        "trim left": Key("s-home, delete"),
        "trim right": Key("s-end, delete"),
    }
 
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
class JeftRule(ContinuousRule):
    spec = "before left word <text>"
    extras = Dictation("text"),
    def _process_recognition(self, node, extras):
        where = extras["text"].format()
        Function(JumpLeft).execute({"jumpTo": where})
 
@GrammarRule
class JightRule(ContinuousRule):
    spec = "before right word <text>"
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
class SelectThroughLeftRule(ContinuousRule):
    spec = "select left through <text>"
    extras = Dictation("text"),
    def _process_recognition(self, node, extras):
        where = extras["text"].format()
        Function(Shule).execute({"selectThrough": where})

@GrammarRule
class SelectThroughRightRule(ContinuousRule):
    spec = "select right through <text>"
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
class ReplaceAllInSelectionRule(RegisteredRule):
    spec = "replace selection <toReplace> with <replaceWith>"
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
class ReplaceAllInLineRule(RegisteredRule):
    spec = "replace line <toReplace> with <replaceWith>"
    extras = (Dictation("toReplace"), Dictation("replaceWith"))
    def _process_recognition(self, node, extras):
        toReplace = extras["toReplace"].format()
        replaceWith = extras["replaceWith"].format()
        Function(ReplaceAllInLine).execute({"toReplace": toReplace, "replaceWith": replaceWith})

@GrammarRule
class SelectWordLeft(ContinuousRule):
    spec = "select left word <RunOn>"
    extras = Dictation("RunOn"),
    def _process_recognition(self, node, extras):
        words = ["before left word"] + extras["RunOn"].words
        Mimic(*words).execute()
        kb.shiftDown()
        for _ in range(len(extras["RunOn"].format())):
            kb.sendRight(extended = True, delay = 0)
        kb.shiftUp()

@GrammarRule
class SelectWordRight(ContinuousRule):
    spec = "select right word <RunOn>"
    extras = Dictation("RunOn"),
    def _process_recognition(self, node, extras):
        words = ["before right word"] + extras["RunOn"].words
        Mimic(*words).execute()
        kb.shiftDown()
        for _ in range(len(extras["RunOn"].format())):
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
class RespaceRule(ContinuingRule):
    spec = "[make] space count <n>"
    intro = ["make space count", "space count"]
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
class CapitalizeHoveredRule(CompoundRule):
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
class LowercaseHoveredRule(CompoundRule):
    spec = "clop"
    def _process_recognition(self, node, extras):
        Mouse("left:2").execute()
        Function(LowercaseSelection).execute()

@GrammarRule
class InterDocNavRules(_quickRules.QuickContinuousRules):
    name="inter_doc_nav"
    extrasDict = {
        "keyCount": IntegerRef("keyCount", 1, 1000),
        "lineCount": IntegerRef("lineCount", 1, 100),
        "n": IntegerRef("n", 1, 1000),
        "text": Dictation("text"),
    }
    defaultsDict = {
        "keyCount": 1,
        "lineCount": 1,
        "n": 1,
    }    
    mapping = {
        "renter [<lineCount> [times]]": {
            "action": Key("end, enter") * Repeat(extra="lineCount"),
            "intro": "renter"},
        "crater": Mouse("left:1") + Key("end, enter"),
        "last character but <n>": Key("end") + (Key("left") * Repeat(extra="n")),
        "first character but <n>": Key("home") + (Key("right") * Repeat(extra="n")),             
        "trend [<n> [times]]": {
            "action": (Key("down") * Repeat(extra="n")) + Key("end, enter"),
            "intro": "trend"},
        "word left [<n> [times]]": {
            "action": Key("c-left") * Repeat(extra="n"),
            "intro": "word left"},
        "word right [<n> [times]]": {
            "action": Key("c-right") * Repeat(extra="n"),
            "intro": "word right"},
        "select left": Key("s-home"),
        "select full left": Key("s-home, s-home"),        
        "select right": Key("s-end"),
        "select line": Mimic("end") + Key("s-home"),
        "select full line": Mimic("end") + Key("s-home, s-home"),
        "select last word [<n> [times]]": Key("end") + Key("c-left") * Repeat(extra="n"),        
        "(sword|select word) left [<n> [times]]": {
            "action": Key("cs-left") * Repeat(extra="n"),
            "intro": ["sword left", "select word left"]},
        "(sword|select word) right [<n> [times]]": {
            "action": Key("cs-right") * Repeat(extra="n"),
            "intro": ["sword right", "select word right"]},
        "select just word right": Key("cs-right, s-left"),
        "(scare|select character) left [<keyCount> [times]]": {
            "action": Key("s-left") * Repeat(extra="keyCount"),
            "intro": ["scare left", "select character left"]},
        "(scare|select character) right [<keyCount> [times]]": {
            "action": Key("s-right") * Repeat(extra="keyCount"),
            "intro": ["scare right", "select character right"]},               
        "inner wedge": Key("enter:2, up"),
        "sword": Mouse("left:2") + Key("c-c"),
        "copy line": Mimic("end") + Key("s-home") + Mimic("copy"),
        "cut line": Mimic("end") + Key("s-home") + Mimic("cut"),
        "copy left": Key("s-home") + Mimic("copy"),
        "copy right": Key("s-end") + Mimic("copy"),
        "copy full left": Key("s-home, s-home") + Mimic("copy"),
        "delete last word [<n> [times]]": Key("end") + Key("c-left") * Repeat(extra="n") + Key("s-end, delete"),
        "delete line": Mimic("end") + Key("s-home, s-home") + Mimic("dell"),
        "lineless [<n> [times]]": {
            "action": Key("end, s-home, s-home, delete, backspace") * Repeat(extra="n"),
            "intro": "lineless"},
        "plaster": Mimic("paste") + Mimic("enter"),
    }


@GrammarRule
class system_shortcuts_rule(_quickRules.QuickContinuousRules):
    name="system_shortcuts"
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
             "desktop": Key("w-d"),
             "dock left": Key("w-left"),
             "dock left twice": Key("w-left") * Repeat(2),
             "dock right": Key("w-right"),
             "dock right twice": Key("w-right") * Repeat(2),
             "hide [(others | other windows)]": {
                "action": Key("w-home"),
                "intro": ["hide", "hide others", "hide other windows"]},
             "minimize": Key("w-down") * Repeat(2),
             "maximize": Key("w-up"),
             "close": Key("a-f4"),
            }
    extrasDict = {
        "keyCount": IntegerRef("keyCount", 1, 1000),
        "n": IntegerRef("n", 0, 1000),
    }
    defaultsDict = {
        "keyCount": 1,
        "n": 1,
    }

grammar.load()
masterRunOn.load()
print "grammar loaded"

# Listener grammar
listener = Grammar("wake up grammar")

class EnableDragonfly(CompoundRule):
    spec = "(enable|load) dragonfly"
    def _process_recognition(self, node, extras):
        grammar.enable()
        masterRunOn.enable()
        get_engine().speak("dragonfly alive")
listener.add_rule(EnableDragonfly())
listener.load()
    
# Unload function which will be called by natlink at unload time.
def unload():
    global grammar
    global listener
    global masterRunOn
    if grammar: grammar.unload()
    grammar = None
    if listener: listener.unload()
    listener = None
    if masterRunOn: masterRunOn.unload()
    masterRunOn = None
