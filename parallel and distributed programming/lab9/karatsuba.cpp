#include <mpi.h>
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <chrono>
#include <iostream>

using namespace std;

void worker(int nrProcs) {
    MPI_Status status;

    int n, begin, end;
    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);
    vector<int> a(n);
    vector<int> b(n);

    MPI_Bcast(a.data(), n, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(b.data(), n, MPI_INT, 0, MPI_COMM_WORLD);

    MPI_Recv(&begin, 1, MPI_INT, 0, 1, MPI_COMM_WORLD, &status);
    MPI_Recv(&end, 1, MPI_INT, 0, 2, MPI_COMM_WORLD, &status);

    vector<int>res(2 * n);
    for (int i = begin; i < end; i++) {
        res[2 * i] += a[i] * b[i];
        for (int j = i + 1; j < n; j++)
            res[i+j] += (((a[i] + a[j]) * (b[i] + b[j])) - a[i] * b[i] - a[j] * b[j]);
    }

    MPI_Send(res.data(), 2 * n, MPI_INT, 0, 3, MPI_COMM_WORLD);
}

vector<int> master(vector <int> &a, vector <int> &b, int nrProcs) {
    int n = a.size();
    MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(a.data(), n, MPI_INT, 0, MPI_COMM_WORLD);
    MPI_Bcast(b.data(), n, MPI_INT, 0, MPI_COMM_WORLD);

    for (int i = 1; i < nrProcs; ++i) {
        int begin = (i * n) / nrProcs;
        int end = ((i + 1) * n) / nrProcs;

        MPI_Send(&begin, 1, MPI_INT, i, 1, MPI_COMM_WORLD);
        MPI_Send(&end, 1, MPI_INT, i, 2, MPI_COMM_WORLD);
    }

    vector<int> res (2 * n, 0);
    for (int i = 0; i < n / nrProcs; i++) {
        res[2 * i] += a[i] * b[i];
        for (int j = i + 1; j < n; j++)
            res[i+j] += (((a[i] + a[j]) * (b[i] + b[j])) - a[i] * b[i] - a[j] * b[j]);
    }

    MPI_Status status;
    for (int i = 1; i < nrProcs; ++i) {
        vector <int> tmp(2 * n);
        MPI_Recv(tmp.data(), 2 * n, MPI_INT, i, 3, MPI_COMM_WORLD, &status);
        for (int k = 0; k < 2 * n; ++k) {
            res[k] += tmp[k];
        }
    }

    return res;
}

vector<int> generate(int n) {
    vector<int> v(n);
    for (vector<int>::iterator it = v.begin(); it != v.end(); ++it) {
        *it = rand() % 10;
    }
    return v;
}

int main(int argc, char** argv) {
    MPI_Init(NULL, NULL);
    int nrProcs;
    int me;
    MPI_Comm_size(MPI_COMM_WORLD, &nrProcs);
    MPI_Comm_rank(MPI_COMM_WORLD, &me);
    cout << fixed;

    if (me == 0) {
        unsigned n;
        if(argc != 2 || 1 != sscanf(argv[1], "%u", &n)) {
            fprintf(stderr, "usage: <program> n\n");
            return 1;
        }
        vector<int> a = generate(n);
        vector<int> b = generate(n);
        vector<int> res(2 * n);
        
        cout << "A = ";
        for (vector<int>::iterator it = a.begin(); it!= a.end(); ++it) {
            cout << *it << " ";
        }
        cout << "\n";

        cout << "B = ";
        for (vector<int>::iterator it = b.begin(); it!= b.end(); ++it) {
            cout << *it << " ";
        }
        cout << "\n";
        
        auto start = chrono::system_clock::now();
        res = master(a, b, nrProcs);
        auto stop = chrono::system_clock::now();
        chrono::duration<double> elapsed_seconds = stop-start;
        cout << elapsed_seconds.count() << " s\n" << flush; 
        cout << "R = ";
        for (vector<int>::iterator it = res.begin(); it + 1 != res.end(); ++it) {
            cout << *it << " ";
        }
        cout << "\n";
    } else {
        worker(nrProcs);
    }

    MPI_Finalize();
    return 0;
}