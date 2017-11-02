import random
import threading

import datetime

from matrix import Matrix


def generate_matrix(i, j):
    m = Matrix(i, j)
    for x in xrange(i):
        for y in xrange(j):
            m.set(x, y, random.randint(0, 2))
    return m

def dot_product(line, column):
    return sum([line[x] * column[x] for x in xrange(len(line))])

def do_tasks(tasks):
    elem = None
    while len(tasks):
        elem = tasks[0]
        if len(tasks) > 1:
            tasks = tasks[1:]
        else:
            tasks = []
        is_ready, line = elem[0]['matrix'].get_row(elem[0]['x'])
        while not is_ready:
            is_ready, line = elem[0]['matrix'].get_row(elem[0]['x'])

        is_ready, column = elem[1]['matrix'].get_column(elem[1]['y'])
        while not is_ready:
            is_ready, column = elem[1]['matrix'].get_column(elem[1]['y'])

        elem[2].set(elem[0]['x'], elem[1]['y'], dot_product(line, column))

def main():

    threads = 5

    m = 100
    n = 200
    p = 100
    q = 200
    m1 = generate_matrix(m, n)
    m2 = generate_matrix(n, p)
    m3 = generate_matrix(p, q)
    m4 = Matrix(m, p)
    m5 = Matrix(m, q)

    tasks = []

    for i in xrange(m):
        for j in xrange(p):
            tasks.append([
                {
                    'matrix': m1,
                    'x': i,
                },
                {
                    'matrix': m2,
                    'y': j,
                },
                m4
            ])

    for i in xrange(m):
        for j in xrange(q):
            tasks.append([
                {
                    'matrix': m4,
                    'x': i,
                },
                {
                    'matrix': m3,
                    'y': j,
                },
                m5

            ])

    k = len(tasks) // threads
    mod = len(tasks) % threads

    distributed_tasks = []
    crt = 0

    for t in xrange(threads):
        if t < mod:
            distributed_tasks.append(tasks[crt : crt + k + 1])
            crt += k + 1
        else:
            distributed_tasks.append(tasks[crt : crt + k])
            crt += k

    th = [threading.Thread(target=do_tasks, args=(distributed_tasks[x],)) for x in xrange(threads)]

    time_start = datetime.datetime.now()

    for t in th:
        t.start()

    for t in th:
        t.join()

    time_end = datetime.datetime.now()

    print time_end - time_start

if __name__ == '__main__':
    main()