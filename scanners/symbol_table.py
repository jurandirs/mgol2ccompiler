from scanners.reader import csv_dict_list
from scanners.reader import read_csv
from io import TextIOBase as FileType
from collections import namedtuple

ID = namedtuple('ID', ['lexeme', 'token', 'type'])

class SymbolTable:
    __slots__ = ["reserved_kw", "ids", 'tokens']
    def __init__(self, reserved_kw=None, ids=None):
        self.reserved_kw = reserved_kw if isinstance(reserved_kw, dict) else {}
        self.ids = reserved_kw if isinstance(reserved_kw, dict) else {}
        if isinstance(reserved_kw, str):
            self.load_reserved_kw(reserved_kw)
        self.tokens = self.load_tokens()

    def load_tokens(self):
        d = {}
        fields, accept_states = read_csv('tables/tab_final_states.csv')
        for stt, token in accept_states:
            d[stt] = token
        return d
    
    def load_reserved_kw(self, filename):
        reserd_kw_list = csv_dict_list(filename, 'Reserved')
        for r in reserd_kw_list:
            self.reserved_kw[r.lexeme] = r

    def get_symbol(self, symbol:str, state):
        if symbol in self.reserved_kw:
            return self.reserved_kw[symbol]
        elif symbol in self.ids:
            return self.ids[symbol]
        else:
            return self.new_symbol(symbol)
    
    def new_symbol(self, symbol, state=None):
        if state in self.tokens:
            token = self.tokens[state]
        else:
            token = ''
        
        self.ids[symbol] = ID(lexeme=symbol, token=token, type='')
        return self.ids[symbol]