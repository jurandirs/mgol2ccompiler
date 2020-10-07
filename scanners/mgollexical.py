from dfa import DFA
from symbol_table import SymbolTable
import string 

alphabet_ascii = set(string.ascii_letters + string.digits)

class Lexical:

    Erros_lexicos = {
        's1': 'Constante numerica invalida!',
        's2': 'Constante numerica invalida!',
        's3': 'Constante numerica invalida!',
        's4': 'Constante numerica invalida!',
        's5': 'Constante numerica invalida!',
        's6': 'Constante numerica invalida!',
        's7': 'Literal nao terminado!',
        's8': 'Literal nao terminado!',
        's11': 'Comentario nao terminado!',
        's12': 'Comentario nao terminado!'
    }

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
        self.memory = ''

    def update_relative_position():
        self.current_column += 1
        if self.chain[self.current_position] == '\n':
            self.current_line += 1
            self.current_column = 0

    def load_symbols(self, symbols_table_file):
        return SymbolTable(reserved_kw=symbols_table_file)

    def go_forward(self):
        """Função que avança na cadeia após um erro for encontrado"""
        while self.chain[self.current_position] not in alphabet_ascii or self.chain[self.current_position] in string.whitespace:
            self.memory += self.chain[self.current_position]
            self.current_position += 1
            self.update_relative_position()

    def get_lexeme(self):
        while self.current_position < len(self.chain):
            symbol = chain[self.current_position]
            self.memory += symbol

            running = self.dfa.run_state_transition(symbol)
            current_state = running['current']
            previous_state = running['previous'] # Usado para identificar o erro

            if previous_state is not 'REJECT' and current_state is 'REJECT':
