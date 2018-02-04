#include <mutex>
#include <stdio.h>

using namespace std;

#define OFF_MODE 0x00
#define SHARED_MODE 0x01
#define EXCLUSIVE_MODE 0x02

struct SharedLock {
    private:
        mutex mtx;
        int locked_times;
    public:
        bool is_locked() {
            return locked_times > 0;
        }

        void lock() {
            if (!locked_times) {
                mtx.lock();
            }
            locked_times++; //atomic, no lock required
            
        }

        void unlock() {
            if (locked_times) {
                locked_times--;
                if (!locked_times) {
                    mtx.unlock();
                }
            }
        }
};

struct ExclusiveLock {
    private:
        mutex mtx;
        bool locked;
    public:
        bool is_locked() {
            return locked;
        }

        void lock() {
            mtx.lock();
            locked = true;
        }
        void unlock() {
            locked = false;
            mtx.unlock();
        }
};

struct ReadWriteMutex {
    private:
        SharedLock sharedLock;
        ExclusiveLock exclusiveLock;
        int mode = OFF_MODE;
    public:
        bool try_acquire_read() {
            if (mode == EXCLUSIVE_MODE) {
                return false;
            }
            sharedLock.lock();
            return true;
        }

        bool try_acquire_write() {
            if (mode == SHARED_MODE) {
                return false;
            }
            exclusiveLock.lock();
            return true;
        }

        void release_read() {
            if (mode == SHARED_MODE && sharedLock.is_locked())
                sharedLock.unlock();
        }

        void release_write() {
            if (mode == EXCLUSIVE_MODE && exclusiveLock.is_locked()) {
                exclusiveLock.lock();
            }
        }

        void lock_read() {
            while (false == try_acquire_read());
        }

        void lock_write() {
            while (false == try_acquire_write());
        }
};

struct Node {
    ReadWriteMutex mtx;
    int val;
    Node* next;
    Node* prev;

    int read() {
        int value;
        mtx.lock_read();
        value = val;
        mtx.release_read();
        return value;
    }

    void write(int value) {
        mtx.lock_write();
        val = value;
        mtx.release_write();
    }
};

struct List {
    Node** start, end;
} list;

int main(int argc, char** argv) {
    return 0;
}