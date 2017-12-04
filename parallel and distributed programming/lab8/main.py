import Queue
import random

import sys
import threading

class Task:
    def __init__(self, graph, q):
        self.graph = graph
        self.q = q
        self.any = []

    def run(self):
        try:
            while True:
                state = self.q.get(timeout=1)
                node = state[-1]
                if len(self.graph) is len(state) and state[0] in self.graph[state[-1]]:
                    self.any.append(state)
                    return
                for neighbour in self.graph[node]:
                    if neighbour not in state:
                        self.q.put(state + [neighbour])
        except Queue.Empty:
            pass

def read_graph():
    lines = open('data.txt', 'r').readlines()
    g = {}
    for line in lines:
        x, y = line.split(' ')
        x, y = int(x), int(y)
        if x not in g:
            g[x] = [y]
        else:
            g[x].append(y)
        if y not in g:
            g[y] = []
    return g

def generate(n, m):
    vertexes = {}
    m = min(n * (n-1), m)
    while m:
        x, y, = random.randint(1, n), random.randint(1, n)
        while x in vertexes and y in vertexes[x]:
            x, y, = random.randint(1, n), random.randint(1, n)

        m -= 1
        if x not in vertexes:
            vertexes[x] = [y]
        else:
            vertexes[x].append(y)

    f = open('data.txt', 'w')
    for x in vertexes:
        for y in vertexes[x]:
            f.write(str(x) + ' ' + str(y) + '\n')
    f.close()

def main(threads):
    generate(10, 85)
    graph = read_graph()
    q = Queue.Queue()
    task = Task(graph, q)

    for node in graph:
        q.put([node])

    th = [threading.Thread(target=task.run)]

    for t in th:
        t.start()

    for t in th:
        t.join()

    if len(task.any):
        print 'Hamilton cycle: ', str(task.any[0])[1:-1]
    else:
        print 'No Hamilton cycle.'

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Need number of threads'
    main(int(sys.argv[1]))

