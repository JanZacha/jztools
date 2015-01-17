# -*- coding: utf-8 -*-
"""
Created on Sat Jan 17 12:52:10 2015

@author: zacha
"""
from jztools.tools.idempotence import idempotent
from jztools.pathtools import SmartFile, Path
import string
string.alphanumeric = string.ascii_lowercase + string.digits

@idempotent
class PDBCode(str):
    """
        A PDB code consists of a single numeric digit followed by three alphanumeric characters.
        The PDB code is not case sensitive, i.e. 1abc and 1ABC refer to the same structure.
        For classification purposes, e.g. for the directory structure of the PDB archive,
        the two middle characters (the second and third character of the PDB code) are sometimes
        used as an index to group PDB codes into not too large and equally sized bins.
        This two-letter code is preferred over the first and second character because the number
        of possible values for the first character is limited to the ten digits and the majority
        of PDB codes in use starts with the character '1'.

        http://pdbwiki.org/wiki/PDB_code
    """

    def __init__(self, pdbcode, biono=None):
        pdbcode = pdbcode.lower().strip()
        assert len(pdbcode) == 4, "Not a valid PDB code: %r. Length must be 4 but is %i" % (pdbcode, len(pdbcode))
        assert pdbcode[0] in string.digits, "Not a valid PDB code: %r. first character must be a digit." % pdbcode
        assert pdbcode[1] in string.alphanumeric, "Not a valid PDB code: %r. second character must be alphanumeric." % pdbcode
        assert pdbcode[2] in string.alphanumeric, "Not a valid PDB code: %r. third character must be alphanumeric." % pdbcode
        assert pdbcode[3] in string.alphanumeric, "Not a valid PDB code: %r. fourth character must be alphanumeric." % pdbcode
        self.value = pdbcode

    @classmethod
    def from_scopid(cls, scopid, default=None):
        """Guess the PDB code from a from_scopid (astral40)
           If guessing fails optional 'default' can be used.
        """
        pdbcode = scopid[1:5]
        try:
            return cls(pdbcode)
        except:
            if default is None: raise
            return default

    @classmethod
    def from_path(cls, filehandle, default=None):
        """Guess the PDB code from a path or an existing file
           If guessing fails optional 'default' can be used.
        """
        if isinstance(filehandle, SmartFile) or isinstance(filehandle, file):
            filename = filehandle.name
        elif isinstance(filehandle, str):
            filename = Path(filehandle)
        namebase = filename.namebase
        if len(namebase) >= 7 and namebase[:3].lower() == "pdb":
            pdbcode = namebase[3:7]
        else:
            pdbcode = namebase[:4]

        try:
            return cls(pdbcode)
        except:
            if default is None: raise
            return default

    @property
    def letters(self):
        return self.value[1:3]

    def __repr__(self):
        return self.value

    def __str__(self):
        return self.value