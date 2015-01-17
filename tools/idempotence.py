# -*- coding: utf-8 -*-
"""
Created on Wed Dec 21 20:34:11 2011

@author: jan
"""

def idempotence_on_init(new):
    if new.__name__ == "__init__":
        def __init__(self, ding, *args, **kwargs):
            if isinstance(ding, self.__class__):
                for k, v in ding.__dict__.items():
                    self.__dict__[k] = v
                return
            else:
                new(self, ding, *args, **kwargs)
        return __init__
    else:
        return new  # Return an unchanged method


def idempotence_on_new(new):
    """ while this works I would have to implement an empty new method for each class. no chance doing it with a decorator"""
    if new.__name__ == "__new__":
        def __new__(cls, ding, *args, **kwargs):
            if cls == ding.__class__:
                print "aha"
                return ding
            return new(cls, ding, *args, **kwargs)
        return __new__
    else:
        return new  # Return an unchanged method

def idempotent(original_class):
    """
    Decorator that makes a class idempotent.
    That means:
    idempotente_wrapper_class(idempotente_wrapper_class(\*args)) == idempotente_wrapper_class(args)
    it should be noted that although the values remain the same, the equation does not hold practically.

    **WARNING** as it seems this does not work over module boundaries! Make sure to use fullname on import of idempotent classes.
    i.e. use
    *from base.module.Sub import Example*
    instead of
    *from Example import Example*
    if Example is made idempotent
    """
    orig_init = original_class.__init__

    @idempotence_on_init
    def __init__(self, *args, **kws):
        orig_init(self, *args, **kws) # call the original __init__

    original_class.__init__ = __init__
    return original_class


if __name__ == "__main__":
    @idempotent
    class Wrapper(object):
        def __init__(self, ding):
            self.ding = ding
            self.name = "<%s>" % ding.name

        def __repr__(self):
            return "<%s>" % self.ding.name

    class Ding(object):
        def __init__(self, name):
            self.name = name

        def __repr__(self):
            return self.name

    ding = Ding("A")
    print "ding =", ding

    w = Wrapper(ding)
    print "w.name =", w.name


    w2 = Wrapper(w)
    print "w2.name =", w2.name

    print w == w2
    """I would love this to be true. but unfortunately it seems I would have to hack
        into the __new__ - method. and this does not seem to work with the decorator approach.
    """
    wx = w
    for i in range(10):
        wx = Wrapper(wx)