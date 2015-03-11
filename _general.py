# this file is only to contain code that would be appropriate to my general purpose library, and so at some point should be transferred there

import inspect

def EnsureInstance(instanceOrClass, *args, **kwargs):
    if inspect.isclass(instanceOrClass):
        return instanceOrClass(*args, **kwargs)
    else:
        return instanceOrClass    
    
def Single_Spaces_Only(some_string):
    words = some_string.split()
    return "".join(words)