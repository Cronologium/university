import sys

from finiteautomata.finite_automata_json_parser import FiniteAutomataJsonParser
from scanner.scanner import Scanner


def compare_test(test_no, expected_value, actual_value, verbose=False, inp=None):
    if expected_value != actual_value:
        print 'Test %d failed: expected %s got %s' % (test_no, expected_value, actual_value)
    elif verbose:
        print 'Test %d OK! (%s -> %s)' % (test_no, inp, expected_value)

def validate_automata():
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
        result, invalid = finite_automata.longest_prefix(tests[x][0])
        compare_test(x, tests[x][1], result, verbose=True, inp=tests[x][0])

def main(args):
    fa_parser = FiniteAutomataJsonParser()
    identifiers_automata = fa_parser.parse("identifiers.json")
    constants_automata = fa_parser.parse("constants.json")

    scanner = Scanner(
        identifiers_automata=identifiers_automata,
        constants_automata=constants_automata
    )
    tokens, symbol_table, str_tokens = scanner.lexical_validation(open(args[1], 'r').read())
    open(args[2], 'w').write('pif: ' + str(str_tokens) + '\nsym: ' + str(symbol_table) + '\n')


if __name__ == '__main__':
    '''
    sys.stdout.write('[')
    for elem in list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        sys.stdout.write('"\'' + elem + '\'", ')
    sys.stdout.write('\b]\n')
    '''
    if len(sys.argv) < 3:
        print 'Usage %s <file> <output>'
    else:
        main(sys.argv)