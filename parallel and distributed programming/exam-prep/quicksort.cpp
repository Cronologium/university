#include <mpi.h>
#include <vector>       /* vector */
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */

using namespace std;

int me;
int nrProcs;

void print_vector(const char* label, vector<int> v) {
    printf("%s = [", label);
    for (vector<int> :: iterator it = v.begin(); it != v.end(); ++it) {
        printf("%d ", *it);
    }
    printf("]\n");
}

vector<int> generate(int n) {
    // generate vector of size n with elements < 100
    srand(time(0));
    vector<int> v(n);
    for (vector<int>::iterator it = v.begin(); it != v.end(); ++it) {
        *it = rand() % 100;
    }
    return v;
}

int partition(vector<int> &v, const int &lo, const int &hi) {
    int pivot = v[hi];
    int i = lo;
    
    for (int j = lo; j < hi; ++j) {
        if (v[j] <= pivot) {
            if (i != j) {
                v[i] ^= v[j];
                v[j] ^= v[i];
                v[i] ^= v[j];
            }
            ++i;
        }
    }
    if (v[hi] < v[i]) {
        v[hi] = v[i];
        v[i] = pivot;
    }
    return i;
}

void quick_sort(vector<int> &v, int lo, int hi, int procsLeft) {
    if (lo == hi)
        return;

    int mid = partition(v, lo, hi);

    printf("me: %d, lo: %d, mid: %d, hi: %d --> ", me, lo, mid, hi);
    print_vector("v", v);

    if (mid == lo) {
        quick_sort(v, lo + 1, hi, procsLeft);
        return;
    }
    if (mid == hi) {
        quick_sort(v, lo, hi - 1, procsLeft);
        return;
    }

    if (procsLeft > 1) {
        int child = me + (procsLeft >> 1) + (procsLeft & 1);
        int size = hi - mid;
        MPI_Status status;

        MPI_Send(&size, 1, MPI_INT, child, 0, MPI_COMM_WORLD);
        MPI_Send(v.data() + mid + 1, size, MPI_INT, child, 0, MPI_COMM_WORLD);

        quick_sort(v, lo, mid - 1, (procsLeft >> 1) + (procsLeft & 1));

        MPI_Recv(v.data() + mid + 1, size, MPI_INT, child, 0, MPI_COMM_WORLD, &status);
    } else {
        quick_sort(v, lo, mid - 1, procsLeft);
        quick_sort(v, mid + 1, hi, procsLeft);
    }
}

void quick_sort_worker() {
    int n, parent = 0, procsLeft = nrProcs, node = 0;
    int lo, hi;
    MPI_Status status;

    /* 
     *   Find parent of me and how many children my children and i can have
     */

    while (node < me) { 
        int step = (procsLeft >> 1) + (procsLeft & 1);
        if (node + step <= me) { // after splitting, i'm in the second half (i'm the child)
            parent = node; // my ancestor before splitting
            procsLeft >>= 1;
            node += step;
        } else { // after splitting i'm still the parent
            procsLeft = step;
        }
    }

    printf("me: %d, procs: %d, parent: %d\n", me, procsLeft, parent);

    // get vector

    MPI_Recv(&n, 1, MPI_INT, parent, 0, MPI_COMM_WORLD, &status);
    vector<int> v(n);
    MPI_Recv(v.data(), n, MPI_INT, parent, 0, MPI_COMM_WORLD, &status);

    quick_sort(v, 0, v.size() - 1, procsLeft); // do computations normally

    MPI_Send(v.data(), n, MPI_INT, parent, 0, MPI_COMM_WORLD); //send result to parent
}

int main(int argc, char*argv[]) {
    MPI_Init(0, 0);
    MPI_Comm_size(MPI_COMM_WORLD, &nrProcs);
    MPI_Comm_rank(MPI_COMM_WORLD, &me);

    vector<int> v;

    if (!me) {
        if (argc < 2) {
            printf("Specify at least the length of the vector to test");
        }
        int n = atoi(argv[1]); // get n from first argument (atoi - arg to int)
        v = generate(n);

        print_vector("start_v", v);

        quick_sort(v, 0, v.size() - 1, nrProcs);
        
        print_vector("sorted_v", v);
    } else {
        quick_sort_worker();
    }
    MPI_Finalize();
    return 0;
}