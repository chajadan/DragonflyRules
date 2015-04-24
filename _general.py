# this file is only to contain code that would be appropriate to my general
# purpose library and so at some point should be transferred there
import inspect

print "importing _general"


def ListOfString_StripAll(lst):
    for i, entry in enumerate(lst):
        lst[i] = entry.strip()


def EnsureInstance(instanceOrClass, *args, **kwargs):
    if inspect.isclass(instanceOrClass):
        return instanceOrClass(*args, **kwargs)
    else:
        return instanceOrClass


def FirstNotNone(*args):
    for arg in args:
        if arg is not None:
            return arg
    return None


def Single_Spaces_And_Trimmed(some_string):
    words = some_string.split()
    return " ".join(words)


def Mro_Contains_Class_By_Name(cls, class_name):
    mro = inspect.getmro(cls)
    for entry in mro:
        if entry.__name__ == class_name:
            return True
    else:
        return False


def LaunchExeAsyncWithArgList(exePath, argList):
    from subprocess import Popen
    import sys
    DETACHED_PROCESS = 0x00000008
    cmd = [
        # sys.executable,
        exePath
    ]
    print cmd
    cmd += argList
    print cmd
    p = Popen(cmd, shell=False, stdin=None, stdout=None, stderr=None,
              close_fds=True, creationflags=DETACHED_PROCESS)


def RunBatchFile(filename, fileDirectory):
    from subprocess import Popen
    p = Popen(filename, cwd=fileDirectory)
    stdout, stderr = p.communicate()


def RunBatchFileAsync(batchFilePath):
    from subprocess import Popen
    import sys
    DETACHED_PROCESS = 0x00000008
    cmd = [
            sys.executable,
            batchFilePath,
            # parm1,
            # parm2,
            # parm3
          ]
    p = Popen(cmd, shell=False, stdin=None, stdout=None, stderr=None,
              close_fds=True, creationflags=DETACHED_PROCESS)
