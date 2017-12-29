#include <mpi.h>
#include <iostream>
#include <mutex>
#include <vector>
#include <queue>
#include <ctime>
#include <thread>
#include <unistd.h>

using namespace std;

int v[10][10], id, processes;
mutex mtx;
bool quit;

#define BREAK 10000
#define PAUSE usleep(BREAK)
#define MPAUSE(x) usleep(BREAK * x);

struct Change {
    int id;
    int i;
    int value;
    int threshold;
};

queue<Change> Q;

vector<Change> get_changes(int source, int rank) {
    int changes_size;
    MPI_Recv(&changes_size, 1, MPI_INT, source, rank, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
    if (!changes_size) {
        return vector<Change>();
    }
    vector<Change> changes;
    for (int i = 0; i < changes_size; ++i) {
        Change change;
        MPI_Status status;
        MPI_Recv(&change, sizeof(Change) / sizeof(int), MPI_INT, source, rank, MPI_COMM_WORLD, &status);
        changes.push_back(change);
    }
    return changes;
}

void send_changes(vector<Change> changes, int rank) {
    int changes_size = changes.size();
    MPI_Send(&changes_size, 1, MPI_INT, 0, rank, MPI_COMM_WORLD);
    if (!changes_size) {
        return;
    }
    for (vector<Change> :: iterator it = changes.begin(); it != changes.end(); ++it) {
        MPI_Send(&(*it), sizeof(Change) / sizeof(int), MPI_INT, 0, rank, MPI_COMM_WORLD);
    }
}

void root_broadcast_changes(vector<Change> changes) {
    //cout << "Broadcast master\n" << flush;
    int changes_size = changes.size();
    MPI_Bcast(&changes_size, 1, MPI_INT, 0, MPI_COMM_WORLD);
    //cout << "Broadcast has " << changes_size << " changes\n" << flush;
    if (!changes_size) {
        return;
    }
    mtx.lock();
    for (vector<Change> :: iterator it = changes.begin(); it != changes.end(); ++it) {
        cout << it->id << " " << it->i << " " << it->value << " " << it->threshold << "\n" << flush;
        if (it->threshold == -1) {
            v[it->id][it->i] = it-> value;
        } else if (it->threshold == v[it->id][it->i]) {
            v[it->id][it->i] = it-> value;
        }
        MPI_Bcast(&(*it), sizeof(Change) / sizeof(int), MPI_INT, 0, MPI_COMM_WORLD); 
    }
    mtx.unlock();
    //cout << "Broadcast has ended!\n" << flush;
}

void worker_broadcast_changes() {
    int changes_size;
    //cout << "Start broadcast\n" << flush;
    MPI_Bcast(&changes_size, 1, MPI_INT, 0, MPI_COMM_WORLD);
    //cout << "Broadcast has " << changes_size << " changes\n" << flush;
    if (!changes_size) {
        return;
    }
    Change change;
    if (changes_size) {
        mtx.lock();
        for (int i = 0; i < changes_size; ++i) {
            MPI_Bcast(&change, sizeof(Change) / sizeof(int), MPI_INT, 0, MPI_COMM_WORLD);
            //cout << id << " " << change.id << " " << change.i << " " << change.value << "\n" << flush;
            if (change.threshold == -1) {
                v[change.id][change.i] = change.value;
            } else if (change.threshold == v[change.id][change.i]) {
                v[change.id][change.i] = change.value;
            }
        }
        mtx.unlock();
    }
    //cout << "End broadcast\n" << flush;
}

void dsm_master_thread() {
    for(int rank = 0; !quit; ++rank) {
        vector<Change> changes;
        mtx.lock();
        if (Q.size()) {
            while (Q.size()) {
                changes.push_back(Q.front());
                Q.pop();
            }
        }
        mtx.unlock();
        root_broadcast_changes(changes);
        for (int j = 1; j < processes; ++j) {
            vector<Change> changes = get_changes(j, rank);
            if (changes.size()) {
                mtx.lock();
                for (vector<Change> :: iterator it = changes.begin(); it != changes.end(); ++it) {
                    Q.push(*it);
                }
                mtx.unlock();
            }
        }
        //usleep(BREAK);
    }
}

void dsm_worker_thread() {
    for(int rank = 0; !quit; ++rank) {
        worker_broadcast_changes();
        vector<Change> changes;
        mtx.lock();
        if (Q.size()) {
            while (Q.size()) {
                changes.push_back(Q.front());
                Q.pop();
            }
        }
        mtx.unlock();
        send_changes(changes, rank);
        //usleep(BREAK);
    }
}

void assign(int pid, int i, int value) {
    Change change;
    change.id = pid;
    change.i = i;
    change.value = value;
    change.threshold = -1;
    mtx.lock();
    Q.push(change);
    mtx.unlock();
}

void compare_assign(int pid, int i, int value, int cmp) {
    Change change;
    change.id = pid;
    change.i = i;
    change.value = value;
    change.threshold = cmp;
    mtx.lock();
    Q.push(change);
    mtx.unlock();
}

void query(int pid, int i) {
    cout << "Q (" << id << ", " << pid << ", " << i << ") = " << v[pid][i] << "\n" << flush;
}

void exec_thread0() {
    assign(1, 2, 3);
    PAUSE;
    query(1, 2);
    PAUSE;
    query(2, 2);
    MPAUSE(5);
    query(2, 2);
}

void exec_thread1() {
    PAUSE;
    PAUSE;
    query(1, 2);
    assign(2, 2, 5);
    MPAUSE(5);
    query(2, 2);
}

void exec_thread2() {
    PAUSE;
    PAUSE;
    query(1, 2);
    MPAUSE(3);
    query(2, 2);
    PAUSE;
    compare_assign(2, 2, 4, 5);
    MPAUSE(5);
    query(2, 2);
}

void exec_thread3() {

}

void exec_thread4() {

}

int main(int argc, char** argv) {
    MPI_Init(NULL, NULL);

    MPI_Comm_rank(MPI_COMM_WORLD, &id);
    MPI_Comm_size(MPI_COMM_WORLD, &processes);

    if (!id) {
        thread master(dsm_master_thread);
        exec_thread0();
        usleep(3000000);
        cout << "Master has finished\n" << flush;
        quit = true;
        master.join();
    } else {
        thread worker(dsm_worker_thread);
        switch(id) {
            case 1:
                exec_thread1();
                break;
            case 2:
                exec_thread2();
                break;
            case 3:
                exec_thread3();
                break;
            case 4:
                exec_thread4();
                break;
            default:
                break;
        }
        usleep(3000000);
        cout << "Worker " << id << " has finished\n" << flush;
        quit = true;
        worker.join();
    }

    MPI_Finalize();
    return 0;
}