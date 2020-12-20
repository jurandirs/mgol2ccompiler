import numpy as np
from scanners.reader import read_csv
import string

alphabet_ascii = set(string.ascii_letters + string.digits)
alphabet_ascii.add('$')
alphabet_ascii.add('@')
alphabet_ascii.add('?')
alphabet_ascii.add('#')
alphabet_ascii.add('!')

ANY = "_ANY_"

def load_dfa(transitions_file, accept_states_file, alphabet=None, states=None, start='s0'):
    fields, transitions = read_csv(transitions_file)
    fields, accept_states = read_csv(accept_states_file)

    for t in transitions:
        if t[1] == '\\t': t[1] = '\t'
        if t[1] == '\\n': t[1] = '\n'
        if t[1] == '\\.': t[1] = '.'
        if t[1] == '[A-z0-9]': t[1] = ANY


    alphabet = set(list(zip(*transitions))[1]).union(alphabet_ascii)
    states = set(list(zip(*transitions))[0] + list(zip(*transitions))[2])
    accept_states = set(list(zip(*accept_states))[0])

    D = DFA(alphabet=alphabet,
            states=states,
            start=start,
            transitions=transitions,
            accept=accept_states)

    return D

class DFA:
    """Deterministic Finite Automata"""

    __slots__ = ['Σ', 
                 'S', 
                 's0', 
                 'δ', 
                 'F', 
                 'START_STATE', 
                 'ACCEPT_STATES', 
                 'CURRENT_STATE']
    # Σ = set of alphabet/symbols. Non-empty.
    # S = set of states. Non-empty.
    # s0 = starting state
    # δ = transition function: "δ : S × Σ -> S"
    # F = set of final (or accepting) states
    
    def __init__(self, alphabet: set, states: set, start: str, transitions: list, accept:set):
        self.Σ =             None
        self.S =             None
        self.START_STATE =   None
        self.δ =             None
        self.ACCEPT_STATES = None
        self.CURRENT_STATE = start
        self.set_alphabet(alphabet=alphabet)
        self.set_states(states=states)
        self.set_start_accept(start=start, accept=accept)
        self.set_transition_function(transitions=transitions)



    # Helper functions bellow

    def set_start_accept(self, start: str, accept: list) -> bool:
        if not isinstance(start, str):
            raise TypeError("Variable 'start' must be str type.")
        if not isinstance(accept, (list, tuple, set)):
            raise TypeError("Argument 'accept' must be list, tuple or set type.")
        if not start in self.S:
            raise ValueError("{} is not in S set (of states).".format(start))
        if not set(accept).issubset(self.S):
            print(accept)
            print(self.S)
            print(set(accept).difference(self.S))
            raise ValueError("The set/list 'accept' is not a subset of S set (of states).")
        
        self.START_STATE = start
        self.ACCEPT_STATES = set(accept)
        return True

    def set_states(self, states: list) -> bool:
        if not isinstance(states, (list, tuple, set)):
            raise TypeError("'states' argument must be list, tuple or set type.")
        if not all(isinstance(s, str) for s in states):
            raise TypeError("All instances in argument 'states' must be str type.")

        self.S = set(states)
        return True

    def set_alphabet(self, alphabet: list) -> bool:
        if not isinstance(alphabet, (list, tuple, set)):
            raise TypeError("'alphabet' argument must be list, tuple or set type.")
        if not all(isinstance(a, str) for a in alphabet):
            raise TypeError("All instances in argument 'alphabet' must be str type.")

        self.Σ = set(alphabet)
        return True

    def set_transition_function(self, transitions: list) -> bool:
        if not isinstance(transitions, (list, tuple, set)):
            raise TypeError("'transitions' argument must be list, tuple or set type.")
        if not all(isinstance(t, (list, tuple)) for t in transitions):
            raise TypeError("All transitions in 'transitions' argument must be list or tuple type")
        if not all(isinstance(x, str) for x in np.concatenate(transitions)):
            raise TypeError("All elements in each transition mustalphabet_ascii.add('$') be str type.")
        
        S1, SIGMA, S2 = list(zip(*transitions))
        if not set(S1).issubset(self.S) or not set(S2).issubset(self.S):
            del S1, SIGMA, S2
            raise TypeError("All elements in 1st and 3rd positions in each transitions must belong to the S set (of states).")
        if not set(SIGMA).issubset(self.Σ):
            del S1, SIGMA, S2
            raise TypeError("All elements in 2nd positions in each transitions must belong to the Σ set (of alphabet).")
        del S1, SIGMA, S2

        # Garantir DFA completo
        transition_dict = {(state, symbol): "REJECT" for state in self.S
                                                     for symbol in self.Σ}

        for s1, symbol, s2 in transitions:
            if symbol == 'L':
                for l in string.ascii_letters:
                    transition_dict[(s1, l)] = s2
            elif symbol == 'D':
                for d in string.digits:
                    transition_dict[(s1, d)] = s2
            transition_dict[(s1, symbol)] = s2
        
        self.δ = transition_dict
        return True

    def run_state_transition(self, input_symbol: str) -> str:
        previous_state = self.CURRENT_STATE
        if self.CURRENT_STATE == "REJECT":  # Um Estado apenas para rejeição, não quer dizer que seja um estado que não é de aceitação
            return False
        self.CURRENT_STATE = self.δ[self.CURRENT_STATE, input_symbol]
        if self.CURRENT_STATE == 'REJECT' and (self.CURRENT_STATE, ANY) in self.δ:
            self.CURRENT_STATE = self.δ[self.CURRENT_STATE, ANY]
        
        return {'current': self.CURRENT_STATE, 'previous': previous_state}

    def check_if_accept(self):
        return True if self.CURRENT_STATE in self.ACCEPT_STATES else False

    def reset(self):
        self.CURRENT_STATE = self.START_STATE

    def run_machine(self, in_string):
        self.reset()

        for symbol in in_string:
            check = self.run_state_transition(symbol)['current']
            if check == "REJECT":
                return False
        
        return self.check_if_accept()