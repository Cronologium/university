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

vector<int> merge(vector<int> a, vector<int> b) {
    vector<int> v(a.size() + b.size());
    a.push_back(2e9);
    b.push_back(2e9); // Pun un numar mare pe int32 la final ca sa nu verific daca i < a.size() sau j < b.size()
    for (int i = 0, j = 0; i + j < v.size();) {
        if (a[i] <= b[j]) {
            v[i+j] = a[i++];
        } else {
            v[i+j] = b[j++];
        }
    }
    return v;
}

void merge_sort(vector<int> &v, int procsLeft) {
    //printf("Process %d has to do: \n", me);
    //print_vector("v", v);

    vector<int>::const_iterator start = v.begin();
    vector<int>::const_iterator middle = v.begin() + (v.size() >> 1);
    vector<int>::const_iterator end = v.end(); 
    vector<int> a(start, middle), b(middle, end); // put lower part of v in a and upper part in b. this assures that there are more elements in a than in b

    if (procsLeft > 1) {
        int size = b.size();
        int child = me + (procsLeft / 2) + (procsLeft & 1);
        MPI_Status status;
        //printf("me %d send to child: %d: ", me, child);
        //print_vector("sent_b", b);
        MPI_Send(&size, 1, MPI_INT, child, 0, MPI_COMM_WORLD);
        MPI_Send(b.data(), size, MPI_INT, child, 0, MPI_COMM_WORLD); // send data to child while i carry on

        merge_sort(a, (procsLeft >> 1) + (procsLeft & 1));

        MPI_Recv(b.data(), size, MPI_INT, child, 0, MPI_COMM_WORLD, &status);
    } else {
        if (a.size() > 1) {
            merge_sort(a, procsLeft);
        }
        if (b.size() > 1) {
            merge_sort(b, procsLeft);
        }
    }
    v = merge(a, b);
    //print_vector("a", a);
    //print_vector("b", b);
        
}

void merge_worker() {
    int n, parent = 0, procsLeft = nrProcs, node = 0;
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

    merge_sort(v, procsLeft); // do computations normally

    MPI_Send(v.data(), n, MPI_INT, parent, 0, MPI_COMM_WORLD); //send result to parent
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

        merge_sort(v, nrProcs);
        
        print_vector("sorted_v", v);
    } else {
        merge_worker();
    }
    MPI_Finalize();
    return 0;
}