from scanners.mgollexical import Lexical
from scanners.reader import read_csv
from parsers.mgolgrammar import mgolgrammar
from parsers.mgolgrammar import sync_tokens



class SLR:
    def __init__(self, scanner: Lexical):
        self.scanner = scanner
        self.stack = ['s0']
        self.action = {}
        self.load_actions(file_path='tables/tab_action.csv')
        self.goto = {}
        self.load_goto(file_path='tables/tab_goto.csv')
        self.load_errors(file_path='tables/tab_errors_final.csv')

    def load_actions(self, file_path):
        fields, actions = read_csv(file_path)
        assert fields == ["analisator", "terminal", "state", "action"]

        for analisator, terminal, state, action in actions:
            self.action[analisator, terminal] = action  # recupera a ação
            self.action[analisator, terminal, action] = state  # realizará a ação no estado state

    def load_goto(self, file_path):
        fields, deviations = read_csv(file_path)
        assert fields == ["state", "symbol", "next"]

        for state, symbol, next in deviations:
            self.goto[state, symbol] = next  # recupera o desvio

    def load_errors(self, file_path):
        fields, errors = read_csv(file_path)
        assert fields == ["analisator", "terminal", "code", "message"]

        for analisator, terminal, code, message in errors:
            self.action[analisator, terminal] = code  # recupera o erro
            self.action[analisator, code] = message  # recupera o erro
            
    def panic_error(self,error_code, current_symbol, current_state, line, column):
        if current_symbol in sync_tokens:
            pass
        else:
            while True:
                symbol = next(self.scanner.get_lexeme())['symbol'].lexeme
                if symbol in sync_tokens:
                    break
        return "Error {} (linha: {}, coluna: {}) : {}".format(error_code,
                                                            line,
                                                            column, 
                                                            self.action[current_state, error_code])
    def run_slr(self):
        stop = None
        ip = next(self.scanner.get_lexeme())  # Fazer ip apontar para o primeiro símbolo w$;
        while True:  # repetir para sempre início
            s = self.stack[-1]  # seja s o estado ao topo da pilha e
            # if ip.token == "id":  # a o símbolo apontado por ip;
            #     a = ip.token  # porque na tabela os identificadores são identificados por "id" (o token)
            # else:
            #     a = ip.lexeme
            a = ip['symbol'].token if (s, ip['symbol'].token) in self.action else ip['symbol'].lexeme
            if self.action[s, a] == "shift":
                ss = self.action[s, a, "shift"]
                self.stack.append(a)  # empilhar a e em seguida s' (ss) no topo da pilha;
                self.stack.append(ss)
                try:
                    ip = next(self.scanner.get_lexeme())  # avançar ip para o próximo símbolo da entrada;
                except:
                    break
            elif self.action[s, a] == "reduce":
                prod_index = self.action[s, a, "reduce"]
                A = mgolgrammar[prod_index].left
                β = mgolgrammar[prod_index].right
                for i in range(0, 2*len(β)):  # desempilhar 2*|β | símbolos para fora da pilha;
                    self.stack.pop()
                ss = self.stack[-1]  # seja s' (ss) o estado agora ao topo da pilha;
                # ss = s  # seja s' (ss) o estado agora ao topo da pilha;
                self.stack.append(A)  # empilhar A e em seguida desvio[s',A];
                self.stack.append(self.goto[ss, A])
                print('{} -> {}'.format(A,' '.join(β)))  # escrever a produção A -> β na tela;
            elif self.action[s, a] == "acc":
                return True
            elif str(self.action[s, a]).isdigit():
                error = self.panic_error(error_code=self.action[s, a], 
                                        current_symbol=a, 
                                        current_state=s, 
                                        line=ip['position']['line'],
                                        column=ip['position']['column'])
                print(error)
                try:
                    ip = next(self.scanner.get_lexeme())  # avançar ip para o próximo símbolo da entrada;
                except:
                    break
