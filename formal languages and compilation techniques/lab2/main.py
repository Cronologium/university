from finite_automata_json_parser import FiniteAutomataJsonParser
from finite_automata_keyboard_parser import FiniteAutomataKeyboardParser

def compare_test(test_no, expected_value, actual_value, verbose=False, inp=None):
    if expected_value != actual_value:
        print 'Test %d failed: expected %s got %s' % (test_no, expected_value, actual_value)
    elif verbose:
        print 'Test %d OK! (%s -> %s)' % (test_no, inp, expected_value)

def main():
    parser = FiniteAutomataJsonParser()
    #parser = FiniteAutomataKeyboardParser()
    finite_automata = parser.parse("integer_literals_c.json")

    display_fa = False
    if display_fa:
        print 'Alphabet', finite_automata.get_alphabet()
        print 'States', finite_automata.get_states()
        print 'Final states', finite_automata.get_final_states()
        print 'Transitions', finite_automata.get_all_transitions()

    tests = [
        ("0x09", "0x0"),
        ("0x123456078900", "0x123456078900"),
        ("0012346", "0"),
        ("1234056", "1234056"),
        ("0467", "0467"),
        ("004", "0"),
        ("0647945", "0647"),
        ("0b001", "0b0"),
        ("0b1010101000", "0b1010101000"),
        ("0b1", "0b1"),
        ("0b52", "0"),
        ("0b15", "0b1"),
        ("3.14", "3.14"),
        ("3.00", "3"),
        ("0x3.14", "0x3"),
    ]

    for x in xrange(len(tests)):
        result = finite_automata.longest_prefix(tests[x][0])
        compare_test(x, tests[x][1], result, verbose=True, inp=tests[x][0])

if __name__ == '__main__':
    main()