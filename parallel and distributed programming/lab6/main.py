import random

import sys
import time
import datetime
import threading

from copy import deepcopy


class Polynom:
    def __init__(self, z=None, size=0, **kwargs):
        if (z > 1):
            self.z = z
        if not z:
            self.z = z
        self.p = [0 for x in xrange(size)]
        for k, v in kwargs.items():
            try:
                if k[0] == 'x':
                    x = int(k[1:])
                    self.add(x, v)
            except ValueError:
                pass

    def add(self, power, value):
        while len(self.p) < power:
             self.p.append(0)
        if len(self.p) == power:
            self.p.append(value)
        else:
            if not self.z:
                self.p[power] += value
            else:
                if self.p[power] + value >= self.z:
                    self.add(power, value % self.z)
                    self.add(power + 1, value // self.z)
                else:
                    self.p[power] += value

    def split_at(self, pos):
        return Polynom(
                z=self.z,
                **{'x' + str(x-pos): self.p[x] for x in xrange(pos, len(self))}
            ), Polynom(
                z=self.z,
                **{'x' + str(x): self.p[x] for x in xrange(pos)}
            )

    def multiplication(self, power, value):
        result = Polynom(z=self.z, size=power+len(self.p))
        for x in xrange(len(self.p)):
            result.add(power + x, self.p[x] * value)
        return result

    def add_polynom(self, other):
        while len(self) < len(other):
            self.p.append(0)
        for x in xrange(len(other)):
            self.add(x, other.p[x])

    def __len__(self):
        return len(self.p)

    def __add__(self, other):
        size = max(len(self), len(other))
        p = Polynom(z=self.z, size=size)
        for x in xrange(size):
            p.add(x, (0 if x >= len(self) else self.p[x]) + (0 if x >= len(other) else other.p[x]))
        return p

    def __mul__(self, other):
        p = Polynom(z=self.z)
        for x in xrange(len(other)):
            if other.p[x] != 0:
                p = p + self.multiplication(x, other.p[x])
        return p

    def __sub__(self, other):
        size = max(len(self), len(other))
        p = Polynom(z=self.z, size=size)
        for x in xrange(size):
            p.add(x, (0 if x >= len(self) else self.p[x]) - (0 if x >= len(other) else other.p[x]))
        return p

    def __rshift__(self, other):
        p = Polynom()
        for x in xrange(other, len(self)):
            p.add(x - other, self.p[x])
        return p

    def __lshift__(self, other):
        p = Polynom()
        for x in xrange(other):
            p.add(x, 0)
        for x in xrange(len(self)):
            p.add(x + other, self.p[x])
        return p

    def __str__(self):
        if not self.z:
            return ' + '.join(['(' + str(self.p[x]) + ')' + (' * ' + ('x' if not self.z else str(self.z)) + '^' + str(x) if x > 0 else '') for x in xrange(len(self.p)-1,-1,-1)])
        else:
            return '(' + ')('.join([str(self.p[x]) for x in xrange(len(self))]) + ') in base ' + str(self.z)

class Node:
    def __init__(self, p1, p2, middle=None, children=None):
        if not children:
            self.children = []
        else:
            self.children = children
        self.value = None
        self.p1 = p1
        self.p2 = p2
        self.middle = middle

    def add_child(self, child):
        self.children.append(child)
        return self

    def complete(self, value):
        self.value = value

    def is_leaf(self):
        return (len(self.children) == 0)

    def can_start(self):
        to_start = True
        for child in self.children:
            to_start &= child.is_done()
        return to_start

    def val(self, pos):
        if pos > self.children:
            return None
        else:
            return self.children[pos].value

    def is_done(self):
        return (self.value is not None)

class Graph:
    def __init__(self):
        self.g = []

    def add_node(self, node):
        self.g.append(node)
        return node

def do_tasks(tasks):
    while len(tasks):
        crt = tasks.pop(0)
        crt[3].add_polynom(crt[0].multiplication(crt[1], crt[2]))

def do_karatsuba_tasks(q):
    for node in q:
        if node.is_leaf():
            node.complete(node.p1 * node.p2)
        else:
            while not node.can_start():
                pass
            node.complete(
                (node.val(2) << (2*node.middle))
                + ((node.val(1)-node.val(2)-node.val(0)) << (node.middle))
                + node.val(0)
            )

def dfs(g, p1, p2):
    if len(p1) == 1 or len(p2) == 1:
        return g.add_node(Node(p1, p2))

    middle = (max(len(p1), len(p2))) // 2
    p1_h, p1_l = p1.split_at(middle)
    p2_h, p2_l = p2.split_at(middle)

    return g.add_node(Node(
            p1=p1,
            p2=p2,
            middle=middle,
            children=[
                dfs(g, p1_l, p2_l),
                dfs(g, p1_l + p1_h, p2_l + p2_h),
                dfs(g, p1_h, p2_h)
            ]
        )
    )

def run_distributed(threads, tasks, function):

    k = len(tasks) // threads
    mod = len(tasks) % threads

    distributed_tasks = []
    crt = 0

    for t in xrange(threads):
        distributed_tasks.append([tasks[x] for x in xrange(t, len(tasks), threads)])

    th = None
    if threads == 1:
        th = []
    else:
        th = [threading.Thread(target=function, args=(distributed_tasks[x],)) for x in xrange(threads)]

    time_start = datetime.datetime.now()

    if threads > 1:
        for t in th:
            t.start()

        for t in th:
            t.join()
    else:
        function([t for t in tasks])

    time_end = datetime.datetime.now()

    return time_end - time_start


def normal_multiplication(p1, p2, threads):
    r = Polynom(z=p1.z)
    tasks = [(p2, x, p1.p[x], r) for x in xrange(len(p1))]

    return r, run_distributed(threads, tasks, do_tasks)

def karatsuba_multiplication(p1, p2, threads):
    g = Graph()
    dfs(g, p1, p2)

    T = run_distributed(threads, g.g, do_karatsuba_tasks)

    return g.g[-1].value, T

def random_polynom(size, z=None):
    if z and z < 2:
        z = None
    X = {}
    for x in xrange(size):
        k = 'x' + str(x)
        X[k] = random.randint(0, z if z else 10)
    return Polynom(z=z, **X)

def main(threads):

    p1 = random_polynom(500)
    p2 = random_polynom(500)

    r = p1*p2
    r1, T1 = normal_multiplication(p1, p2, threads)
    r2, T2 = karatsuba_multiplication(p1, p2, threads)

    if len(r) < 10:
        print '==========Normal===========\n', r
        print '=======Distributed========='
        print r1
        print 'Computed in ', T1, ' s'
        print '========Karatsuba=========='
        print r2
        print 'Computed in ', T2, ' s'
    else:
        print 'Distributed time:', T1, ' s'
        print 'Karatsuba:', T2, ' s'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Need number of threads'
    else:
        main(int(sys.argv[1]))
