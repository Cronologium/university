import random
import threading

import datetime

q = []
m = 0
n = 0
p = 0
matrix1 = None
matrix2 = None
result = None


def read_matrix(f, matrix, m, n):
    for i in xrange(m):
        line = f.readline()
        for j in xrange(n):
            matrix[i][j] = int(line.split(' ')[j])

def gen_matrix(matrix, m, n):
    for i in xrange(m):
        for j in xrange(n):
            matrix[i][j] = random.randint(0, 3)

def prod(id):
    while len(q[id]):
        val = q[id][0]
        if len(q[id]) > 1:
            q[id] = q[id][1:]
        else:
            q[id] = []
        i = val // n
        j = val % n
        result[i][j] = sum([matrix1[i][k] * matrix2[k][j] for k in xrange(p)])

def main():
    global m, n, p
    global matrix1, matrix2
    global result
    global q
    m = int(raw_input('m = '))
    p = int(raw_input('p = '))
    n = int(raw_input('n = '))
    k = int(raw_input('k = '))
    q = [[] for x in xrange(k)]
    
    matrix1 = [[0 for x in xrange(p)] for y in xrange(m)]
    matrix2 = [[0 for x in xrange(n)] for y in xrange(p)]
    
    gen_matrix(matrix1, m, p)
    gen_matrix(matrix2, p, n)
    
    #f = open('matrix.txt', 'r')
    
    #read_matrix(f, matrix1, m, p)
    #f.readline()
    #read_matrix(f, matrix2, p, n)
    
    #f.close()
    
    result = [[0 for x in xrange(n)] for y in xrange(m)]
    
    val = 0
    for i in xrange(k):
        aux = val
        if i < n * m % k:
            for x in xrange(n * m // k + 1):
                q[i].append(val)
                val += 1
        else:
            for x in xrange(n * m // k):
                q[i].append(val)
                val += 1
        #print aux, val - 1
        
    #print q
        
    th = []
    t = datetime.datetime.now()
    for i in xrange(k):
        th.append(threading.Thread(target=prod, args=(i,)))
        th[-1].start()
        
    for i in xrange(k):
        th[i].join()
    print datetime.datetime.now() - t
        
    #print matrix1, matrix2, result

if __name__ == '__main__':
    main()