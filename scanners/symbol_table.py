from reader import csv_dict_list
from io import TextIOBase as FileType

class SymbolTable:
    __slots__ = ["reserved_kw", "ids"]
    def __init__(self, reserved_kw=None, ids=None):
        self.reserved_kw = reserved_kw if isinstance(reserved_kw, dict) else {}
        if isinstance(reserved_kw, FileType):
            self.load_reserved_kw(reserved_kw)
        self.ids = ids reserved_kw if isinstance(reserved_kw, dict) else {}
    
    def load_reserved_kw(self, filename):
        reserd_kw_list = csv_dict_list(file_name, 'Reserved')
        for r in reserd_kw_list:
            self.reserved_kw[r[lexeme]] = r
