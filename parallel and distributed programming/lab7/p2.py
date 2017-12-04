import Queue
import random
import threading


DIGITS = '0123456789'

class InputMismatch(Exception):
    pass

class BigNumber:
    def __init__(self, number=None):
        self.no = []
        if number:
            self.no = [int(digit) for digit in number[::-1]]

    def set_digit(self, pos, digit):
        while len(self.no) <= pos:
            self.no.append(0)
        self.no[pos] = digit

    def d(self, pos):
        return self.no[pos]

    def __str__(self):
        return ''.join([str(digit) for digit in self.no[::-1]])

class TaskNode:
    def __init__(self, id, parent=None, children=None):
        self.id = id
        self.parent = parent
        self.children = []
        self.q = []
        self.done = []
        if children:
            for child in children:
                self.add_child(child)

    def add_child(self, child):
        self.children.append(child)
        self.q.append(Queue.Queue())
        self.done.append(False)

    def queue(self, child, value):
        for x in xrange(len(self.children)):
            if self.children[x].id == child.id:
                self.q[x].put(value)

    def notify(self, child):
        for x in xrange(len(self.children)):
            if self.children[x].id == child.id:
                self.q[x].put(-1)

    def consume(self):
        remainder = 0
        pos = 0
        done = False
        r = None
        if not self.parent:
            r = BigNumber()

        while not done or remainder != 0:
            done = True
            s = remainder
            digits = []
            for x in xrange(len(self.q)):
                if not self.done[x]:
                    d = self.q[x].get()
                    if d != -1:
                        done = False
                        digits.append(d)
                    else:
                        self.done[x] = True
                    self.q[x].task_done()
            s += sum(digits)
            if len(digits):
                #print 'id= ' + str(self.id) + ' d:' + str(digits)
                pass
            if not done or (done and s != 0):
                if self.parent:
                    self.parent.queue(self, s % 10)
                else:
                    r.set_digit(pos, s % 10)
            remainder = s // 10
            pos += 1

        if self.parent:
            self.parent.notify(self)
        else:
            return r

    def relay(self, big_number):
        for digit in big_number.no:
            self.parent.queue(self, digit)
        self.parent.notify(self)

    def __str__(self):
        return 'Node --> id: ' + str(self.id) + '\n' + \
                'parent: ' + str(self.parent.id if self.parent else '(null)') + '\n' + \
                'children: (' + ','.join([str(child.id) for child in self.children]) + ')\n===\n'

class TaskTree:
    def __init__(self, n):
        output = TaskNode(id=-1)

        crt_level = [TaskNode(id=x) for x in xrange(0, n)]
        inp = crt_level
        nodes = []
        next_id = n

        while len(crt_level) > 1:
            new_level = [TaskNode(id=next_id + x, children=crt_level[x*2:x*2+2]) for x in xrange(len(crt_level)//2)]
            for x in xrange(len(new_level)):
                crt_level[x*2].parent = new_level[x]
                crt_level[x*2+1].parent = new_level[x]
            next_id += len(new_level)
            nodes += new_level
            if len(crt_level) % 2 is 1:
                new_level.append(crt_level[-1])
            crt_level = new_level

        output.add_child(nodes[-1])
        nodes[-1].parent = output

        self.root = output
        self.branches = nodes
        self.leaves = inp

    def run(self, numbers):
        if len(numbers) != len(self.leaves):
            raise InputMismatch('Tree was configured for {0} leaves, not {1}'.format(self.leaves, len(numbers)))
        threads = [threading.Thread(target=node.consume) for node in self.branches]

        for x in xrange(len(numbers)):
            self.leaves[x].relay(numbers[x])

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        return self.root.consume()

    def __str__(self):
        return str(self.root) + ''.join([str(node) for node in self.branches[::-1]] + [str(node) for node in self.leaves])

def test_tree_generation():
    tests = 1
    for _ in xrange(tests):
        size = 9 #random.randint(3, 500)
        tree = TaskTree(size)
        if len(tree.branches) != size - 1:
            print 'Expected', size-1, '\nGot: ', len(tree.branches), '\nFor', size

def main():

    max_size = 2
    min_size = 2
    numbers = []
    #ns = '1 2 3 4 5 6 7 8 9'.split(' ')
    #numbers = [BigNumber(x) for x in ns]
    n = 7
    for x in xrange(n):
        size = random.randint(min_size, max_size)
        if size > 1:
            numbers.append(BigNumber(
                number=''.join([DIGITS[random.randint(1, 9)]] + [DIGITS[random.randint(0, 9)] for _ in xrange(size - 1)])
            ))
        else:
            numbers.append(BigNumber(
                number=''.join([DIGITS[random.randint(0, 9)]])
            ))
    print ' '.join([str(number) for number in numbers])
    s = sum([int(str(number)) for number in numbers])
    tree = TaskTree(n)
    #print str(tree)
    st = tree.run(numbers)
    #print numbers
    print s
    if str(s) != str(st):
        print 'Expected: ', s, '\nGot: ', st

if __name__ == '__main__':
    #test_tree_generation()
    main()