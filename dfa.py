import numpy as np

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
    
    def __init__(self, alphabet: list, states: list, start: str, transitions: list, accept:list) -> DFA:
        self.Σ =             None
        self.S =             None
        self.START_STATE =   None
        self.δ =             None
        self.ACCEPT_STATES = None
        self.CURRENT_STATE = None
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
            raise TypeError("All elements in each transition must be str type.")
        
        S1, SIGMA, S2 = list(zip(*transitions))
        if not set(S1).issubset(self.S) or not set(S2).issubset(self.S):
            del S1, SIGMA, S2
            raise TypeError("All elements in 1st and 3rd positions in each transitions must belong to the S set (of states).")
        if not set(SIGMA).issubset(self.Σ):
            del S1, SIGMA, S2
            raise TypeError("All elements in 2nd positions in each transitions must belong to the Σ set (of alphabet).")
        del S1, SIGMA, S2

        transition_dict = {(state, symbol): "REJECT" for state in self.S
                                                     for symbol in self.Σ}
        
        self.δ = transition_dict
        return True

    def run_state_transition(self, input_symbol: str) -> str:
        if self.CURRENT_STATE == "REJECT":  # Um Estado apenas para rejeição, não quer dizer que seja um estado que não é de aceitação
            return False
        self.CURRENT_STATE = self.δ[self.CURRENT_STATE, input_symbol]
        return self.CURRENT_STATE

    def check_if_accept(self):
        return True if self.CURRENT_STATE in self.ACCEPT_STATES else False

    def reset(self):
        self.CURRENT_STATE = self.START_STATE

    def run_machine(self, in_string):
        self.reset()

        for symbol in in_string:
            check = self.run_state_transition(symbol)
            if check == "REJECT":
                return False
        
        return self.check_if_accept()