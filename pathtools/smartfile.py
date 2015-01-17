# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 17:09:30 2011

@author: jan
"""

import gzip, sys
from jztools.tools.idempotence import idempotent
from jztools.pathtools.pathmodule import Path

@idempotent
class SmartFile(object):
    """ A thin wrapper around python's file object.
        If the constructor is given a string a file object is created and finally closed.
        If given a file object this file will not be closed by this class.
    """
    def __init__(self, handle, mode="r"):
        if not handle or handle == "-":
            if "r" in mode:
                _file = sys.stdin
            elif "w" in mode:
                _file = sys.stdout
            else:
                raise ValueError("Mode string %s did not contain 'r' or 'w'" % mode)
            _close_handle = False
        elif isinstance(handle, basestring):
            _close_handle = True
            handle = Path(handle)
            if handle[-3:] == ".gz":
                _file = gzip.open(handle, mode=mode)
            else:
                _file = open(handle, mode=mode)
        else:
            _file = handle
            _close_handle = False
            if hasattr(handle, "mode"):
                assert handle.mode == mode
       
        # not self.file=file, to avoid triggering __setattr__
        self.__dict__['_file'] = _file
        self.__dict__['_close_handle'] = _close_handle

    def __repr__(self):
        try:        
            name = self._file.name
        except:
            name = "%s" % self._file
        try:
            mode = self._file.mode
        except:
            mode = "?"
        return "<smartfile '%s', mode %r>" % (name, mode)

    def __getattr__(self, name):
        return getattr(self._file, name)

    def __setattr__(self, name, value):
        setattr(self._file, name, value)

    def next(self):
        return self._file.next()

    def __iter__(self):
        return self._file.__iter__()

    def close(self):
        if self._close_handle:
            self._file.close()

    #def __del__(self):
    #    self.close()

if __name__ == "__main__":
    import StringIO
    
    output = StringIO.StringIO()
    output.write('First line.\n')
    output.write('Second line.\n')
    print "".join([f for f in output])
    
    output = SmartFile(output)
    output.seek(0)
    print "".join([f for f in output])
