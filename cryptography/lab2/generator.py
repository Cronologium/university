import random
import sys


def main(numbers, start_digits):
    last_digit = start_digits
    this_digit = start_digits
    f = open('data.in', 'w')
    f.write(str(numbers) + '\n')
    for x in xrange(numbers):
        r1 = random.randint(10 ** (this_digit- 1), 10 ** (this_digit) - 1)
        r2 = random.randint(10 ** (this_digit -1), 10 ** (this_digit) - 1)
        f.write(str(r1) + ' ' + str(r2) + '\n')
        aux = this_digit + last_digit
        last_digit = this_digit
        this_digit = aux
    f.close()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Give at least the number of numbers and the number of digits of the first number'
    main(int(sys.argv[1]), int(sys.argv[2]))