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

number_names = [
    ['0', ''],
    ['1', 'wonder'],
    ['2', 'Tootsie'],
    ['3', 'tree'],
    ['4', 'fortress'],
    ['5', 'Fido'],
    ['6', 'sickness'],
    ['7', 'sever'],
    ['8', 'hater'],
    ['9', 'Niner'],
]

keyboard_keys = [
    ['f1', None, 'fun one'],
    ['f2', None, 'fun two'],
    ['f3', None, 'fun three'],
    ['f4', None, 'fun four'],
    ['f5', None, 'fun five'],
    ['f6', None, 'fun six'],
    ['f7', None, 'fun seven'],
    ['f8', None, 'fun eight'],
    ['f9', None, 'fun nine'],
    ['f10', None, 'fun ten'],
    ['f11', None, 'fun eleven'],
    ['f12', None, 'fun twelve'],
    ['ampersand', '&', 'hamper'],
    ['apostrophe', "'", 'posh'],
    ['alt', None, 'alter'],
    ['apps', None, 'application key'],
    ['asterisk', '*', 'asteroid'],
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
    ['dot', '.', 'grain'],
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

alpha_numeric = alpha_names + number_names

printable_keys_as_text = alpha_numeric + [[graph, voicedAs] for name, graph, voicedAs in keyboard_keys if graph is not None]

all_keys_by_keyname = alpha_numeric + [[name, voicedAs] for name, graph, voicedAs in keyboard_keys]