class StateNotFoundException(Exception):
    pass

class CharacterNotInAlphabet(Exception):
    pass

class Transition:
    def __init__(self, elements, new_state):
        self.elements = elements
        self.new_state = new_state

class State:
    def __init__(self, label, start_state=False, end_state=False):
        self.label = label
        self.start_state = start_state
        self.end_state = end_state
        self.transitions = []

    def add_transition(self, elements, new_state_label):
        self.transitions.append(Transition(elements, new_state_label))


class FiniteAutomata:
    def __init__(self, alphabet):
        self.alphabet = alphabet
        self.states = {}
        self.unworked_states = {}

    def add_transition(self, old_state_label, elements, new_state_label):
        if old_state_label in self.unworked_states:
            del self.unworked_states[old_state_label]
        if old_state_label not in self.states:
            raise StateNotFoundException
        for element in elements:
            for char in element:
                if char not in self.alphabet:
                    raise CharacterNotInAlphabet
        if new_state_label not in self.states:
            self.unworked_states[new_state_label] = True
            self.states[new_state_label] = State(new_state_label)
        self.states[old_state_label].add_transition(elements, new_state_label)

    def add_state_obj(self, state_obj):
        label = state_obj.label
        if label in self.unworked_states:
            del self.unworked_states[label]
        self.states[label] = state_obj

    def add_state(self, label, start_state=False, end_state=False):
        if label in self.unworked_states:
            del self.unworked_states[label]
        if label in self.states:
            self.states[label].start_state = start_state
            self.states[label].end_state = end_state
        self.states[label] = State(label, start_state, end_state)

    def longest_prefix(self, text, start_pos=0):
        q = [(None, '', start_pos)]
        longest_prefix = ''
        longest_invalid_prefix = ''
        while len(q):
            crt_state = q[0]
            pos = crt_state[2]
            if crt_state[0] and crt_state[0].end_state and len(crt_state[1]) > len(longest_prefix):
                longest_prefix = crt_state[1]
            if crt_state[0] and len(crt_state[1]) > len(longest_invalid_prefix):
                longest_invalid_prefix = crt_state[1]
            if len(q) > 1:
                q = q[1:]
            else:
                q = []
            if crt_state[0] is None:
                for state in [s for s in self.states.values() if s.start_state]:
                    for transition in state.transitions:
                        for elem in transition.elements:
                            if text[pos : pos + len(elem)] == elem:
                                q.append((self.states[transition.new_state], crt_state[1] + elem, pos + len(elem)))
            else:
                for transition in crt_state[0].transitions:
                    for elem in transition.elements:
                        if text[pos : pos + len(elem)] == elem:
                            q.append((self.states[transition.new_state], crt_state[1] + elem, pos + len(elem)))
        return longest_prefix

    def get_alphabet(self):
        return str(self.alphabet)

    def get_states(self):
        return str(self.states.keys())

    def get_final_states(self):
        return str([state for state in self.states.keys() if self.states[state].end_state])

    def get_start_states(self):
        return str([state for state in self.states.keys() if self.states[state].start_state])

    def get_all_transitions(self):
        transitions = []
        for state in self.states:
            for transition in self.states[state].transitions:
                transitions.append(str(self.states[state].label + ' -> ' + transition.new_state + ' {' + str(transition.elements) + '}'))
        return transitions


