from dfa import DFA
from symbol_table import SymbolTable

class Lexical:
    __slots__ = ['dfa']
    def __init__(self, dfa:DFA, chain:str, symbols_table_file: str):
        if not isinstance(dfa, DFA):
            raise TypeError('dfa argument must be DFA type.')
        if not isinstance(chain, str):
            raise TypeError('chain argument must be str type.')
        self.dfa = dfa
        self.chain = chain
        self.current_position = 0
        self.current_line = 0
        self.current_column = 0
        self.symbols_table = self.load_symbols(symbols_table_file)

    def load_symbols(self, symbols_table_file):
        return SymbolTable(reserved_kw=symbols_table_file)

    def get_lexeme(self):
        for symbol_index in range(self.current_position, len(chain)):
            symbol = chain[symbol_index]
            exec_state = self.dfa.run_state_transition(symbol_index)
