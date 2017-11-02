from finite_automata_parser import FiniteAutomataParser, InvalidFiniteAutomata
from finiteautomata import FiniteAutomata, State


class FiniteAutomataKeyboardParser(FiniteAutomataParser):
    def __init__(self):
        self.finite_automata = None

    def new_state(self):
        print 'New state? (y / everything else)'
        prompt = str(raw_input())
        if prompt == 'y':
            print 'Label: '
            label = str(raw_input())
            print 'Start? (y / everything else)'
            start, end = False, False
            if str(raw_input()) == 'y':
                start = True
            print 'End? (y / everything else)'
            if str(raw_input()) == 'y':
                end = True
            state_obj = State(label, start, end)
            self.finite_automata.add_state_obj(state_obj)
            self.prompt_new_state(state_obj)
            return state_obj
        else:
            return None

    def prompt_new_state(self, state_obj):
        print 'New transition for state %s? (y / everything else)' % state_obj.label
        while str(raw_input()) == 'y':
            print 'Elements for transition (separate using space)'
            elements = str(raw_input()).split(' ')
            print 'New state: (using inexistent label will auto-create one)'
            label = str(raw_input())
            self.finite_automata.add_transition(state_obj.label, elements, label)
            print 'New transition for state %s? (y / everything else)' % state_obj.label

    def parse(self, filename=None):
        print 'Define the alphabet: '
        alphabet = str(raw_input())
        self.finite_automata = FiniteAutomata(alphabet)

        while True:
            state = self.new_state()
            if state is None:
                break

        while len(self.finite_automata.unworked_states):
            label = self.finite_automata.unworked_states.keys()[0]
            print 'Auto-added state ', label, 'define it.'
            state_obj = self.finite_automata.states[label]
            print 'Start? (y / everything else)'
            start, end = False, False
            if str(raw_input()) == 'y':
                start = True
            print 'End? (y / everything else)'
            if str(raw_input()) == 'y':
                end = True
            state_obj.start_state = start
            state_obj.end_state = end
            del self.finite_automata.unworked_states[label]
            self.prompt_new_state(state_obj)

        if len(self.finite_automata.get_start_states()) == 0:
            raise InvalidFiniteAutomata
        if len(self.finite_automata.get_final_states()) == 0:
            raise InvalidFiniteAutomata
        return self.finite_automata