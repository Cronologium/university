import random
import threading


class Task:
    def __init__(self, result):
        self.result = result
        self.computations = []

    def run(self, a, b):
        self.computations.append((a, b))
        self.result[a] += self.result[b]


def executer(v):
    v = v[::-1]
    step = 2
    task = Task(v)
    c = 0
    while step // 2 <= len(v):

        th = [threading.Thread(
            target=task.run,
            args=(x,
                  x + step // 2,)) for x in xrange(0, len(v) - step // 2, step)]

        for t in th:
            t.start()

        for t in th:
            t.join()

        step *= 2

    step //= 2

    while step > 1:
        th = [threading.Thread(
            target=task.run,
            args=(
                x - step // 2,
                x,)) for x in xrange(step, len(v), step)]

        for t in th:
            t.start()

        for t in th:
            t.join()

        step //= 2

    #print task.computations
    return v[::-1], len(task.computations)



def main():
    for size in xrange(10, 11):
        print size
        v = [random.randint(1, 10) for _ in xrange(size)]
        print v
        sp = [sum(v[:x]) for x in xrange(1, len(v)+1)]
        #print v
        v, c = executer(v)

        if c > size * 2:
            print 'Too many computations!'

        ok = True
        for x in xrange(0, len(v)):
            if sp[x] != v[x]:
                print 'Mismatch on position: ', x
                ok = False

        if ok:
            print v
            #print 'OK!'
            #print 100.0 * c / (size * 2), '%'
        else:
            print 'Expected: ', sp
            print 'Got', v


if __name__ == '__main__':
    main()