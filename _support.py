from dragonfly import *
import _keyboard as kb

def ClipboardBackup_Paste(content):
    backup = Clipboard(from_system = True)
    Paste(content)
    backup.copy_to_system()
    
def ReadSelection():
    backup = Clipboard(from_system = True)
    kb.copy()
    selection = GetClipboardAsText()
    backup.copy_to_system()
    return selection

def SelectLine():
    kb.sendEnd()
    kb.sendShiftHome()

def GetClipboardAsText():    
    clip = Clipboard(from_system = True)
    return clip.get_text()

def ReadLineEnd():
    kb.sendShiftEnd()
    lineEnd = ReadSelection()
    kb.sendLeft()
    return lineEnd

def ReadLineBegin():
    kb.sendShiftHome()
    lineBegin = ReadSelection()
    kb.sendRight()
    return lineBegin