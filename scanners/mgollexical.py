from scanners.dfa import DFA
from scanners.symbol_table import SymbolTable
import string 

alphabet_ascii = set(string.ascii_letters + string.digits)
alphabet_ascii.add(';')
alphabet_ascii.add('+')
alphabet_ascii.add('-')
alphabet_ascii.add('/')
alphabet_ascii.add('*')
alphabet_ascii.add('<')
alphabet_ascii.add('>')
alphabet_ascii.add('(')
alphabet_ascii.add(')')
alphabet_ascii.add('"')
alphabet_ascii.add(',')
alphabet_ascii.add('$')
alphabet_ascii.add('@')
alphabet_ascii.add('?')
alphabet_ascii.add('#')
alphabet_ascii.add('!')

lexical_errors = {
        's0': 'Caracter inválido',
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

class Lexical:
    __slots__ = ['dfa',
                 'chain',
                 'current_position',
                 'current_line',
                 'current_column',
                 'symbols_table',
                 'memory',
                 'stop']

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
        self.stop = False

    def update_relative_position(self):
        self.current_column += 1
        try:
            if self.chain[self.current_position] == '\n':
                self.current_line += 1
                self.current_column = 0
        except:
            pass

    def load_symbols(self, symbols_table_file):
        return SymbolTable(reserved_kw=symbols_table_file)

    def go_forward(self):
        """Função que avança na cadeia"""
        current_character = self.chain[self.current_position]
        while current_character not in alphabet_ascii or current_character in string.whitespace:
            self.memory += self.chain[self.current_position]
            self.current_position += 1
            self.update_relative_position()

            current_character = self.chain[self.current_position]
            

    def get_lexeme(self):
        while self.current_position < len(self.chain):
            if self.stop:
                raise StopIteration
            symbol = self.chain[self.current_position]
            self.memory += symbol

            running = self.dfa.run_state_transition(symbol)
            current_state = running['current']
            previous_state = running['previous'] # Usado para identificar o erro

            if previous_state is not 'REJECT' and current_state is 'REJECT':  # saiu de um estado qualquer e foi para o de rejeição
                if previous_state in self.dfa.ACCEPT_STATES:  # saiu de um estado de aceitação e foi para um de rejeição
                    # print(">>>"+self.chain[self.current_position])
                    # print(current_state)
                    # print(previous_state)
                    if len(self.memory) > 1:
                        tmp_symbol = self.memory[0:-1]
                    # self.current_position -= 1
                    self.go_forward()
                    self.dfa.reset()
                    self.memory = ''
                    tmp = self.symbols_table.get_symbol(symbol=tmp_symbol, state=current_state)
                    tmp.update({'line':self.current_line, 'column': self.current_column})
                    yield tmp
                else:
                    message_error = '   Lexical Error: {} (line: {}, column: {})'.format(lexical_errors[previous_state], self.current_line+1, self.current_column-2)
                    self.go_forward()
                    self.current_position += 1
                    self.dfa.reset()
                    yield message_error
                if current_state == self.dfa.START_STATE:
                    self.current_position -= 1
            elif self.current_position == len(self.chain)-1 and symbol == '$': 
                self.stop = True
                tmp = self.symbols_table.get_symbol(symbol=symbol, state=current_state)
                tmp.update({'line':self.current_line, 'column': self.current_column})
                yield tmp
            if not self.memory == '':
                self.current_position += 1
            try:    
                self.update_relative_position()
            except: 
                pass
            
        else:
            print("FIN") 