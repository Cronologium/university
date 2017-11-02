import json

from finite_automata_parser import FiniteAutomataParser, InvalidFiniteAutomata
from finiteautomata import FiniteAutomata

class FiniteAutomataJsonParser(FiniteAutomataParser):
    def __init__(self):
        super(FiniteAutomataJsonParser, self).__init__()

    def parse(self, filename):
        finite_automata = json.load(open(filename, 'r'))
        fa = FiniteAutomata(finite_automata['alphabet'])
        for state in finite_automata['states']:
            fa.add_state(state['label'], state['start'], state['end'])
            for transition in state['transitions']:
                fa.add_transition(state['label'], transition['elements'], transition['new_state'])
        if len(fa.unworked_states):
            raise InvalidFiniteAutomata
        if len(fa.get_start_states()) == 0:
            raise InvalidFiniteAutomata
        if len(fa.get_final_states()) == 0:
            raise InvalidFiniteAutomata
        return fa