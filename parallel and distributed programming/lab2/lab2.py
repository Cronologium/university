import random
import threading

import time

import sys

go_on_tr = True
go_on_ch = True

class Serial:
    def __init__(self):
        self.id = 1
        self.lock = threading.Lock()
        
    def get(self):
        self.lock.acquire()
        v = self.id
        self.id += 1
        self.lock.release()
        return v

class Log:
    def __init__(self, serial_number, source, amount):
        self.serial_number = serial_number
        self.source = source
        self.amount = amount
        
    def __str__(self):
        return 'LogEntry (' + \
               'Serial: ' + str(self.serial_number) + ' ' + \
               'Source: ' + str(self.source) + ' ' + \
               'Amount: ' + str(self.amount) + ')'

class Account:
    def __init__(self, id, value):
        self.id = id
        self.value = value
        self.start_value = value
        self.lock = threading.Lock()
        self.log = {}
        
        
    def add_transaction(self, id, source, value):
        if self.value + value < 0:
            return False
        self.log[id] = Log(id, source.id, value)
        self.value += value
        return True
    
    def __str__(self):
        log_items = []
        for id in self.log:
            log_items.append(self.log[id])
        return 'Account: (' + \
            'ID: ' + str(self.id) + ' '\
            'Value: ' + str(self.value) + \
            ')\n\n'
            #'Log: \n' + '\n'.join(['\t' + str(e) for e in log_items]) + ')\n\n'
            
        
def do_integrity_check(account):
    account.lock.acquire()
    s = account.start_value
    for id in account.log:
        s += account.log[id].amount
    is_ok = s != account.value
    account.lock.release()
    if is_ok:
        print 'Mismatch on account with id: %d, %d expected, got %d' % (account.id, s, account.value)
        return False
    else:
        return True
        
def do_log_matching(accounts, max_serial):
    ok = True
    for account in accounts:
        for serial in xrange(max_serial):
            if serial in account.log:
                if serial not in accounts[account.log[serial].source].log:
                    ok = False
                    print 'Serial found in ID = %d but not in ID = %d' % (account.id, accounts[account.log[serial].source].id)
    if ok:
        print 'Log matching passed!'
            
        
def do_transfer(account_a, account_b, serial, value):
    if account_a.id < account_b.id:
        account_a.lock.acquire()
        account_b.lock.acquire()
    elif account_a.id > account_b.id:
        account_b.lock.acquire()
        account_a.lock.acquire()
    else:
        return
    
    serial_id = serial.get()
    
    if account_a.add_transaction(serial_id, account_b, -value):
        account_b.add_transaction(serial_id, account_a, value)
    
    account_a.lock.release()
    account_b.lock.release()
    
def do_random_checking(accounts, serial):
    global go_on_tr
    while go_on_tr:
        time.sleep(random.randint(500, 1000) / 1000.0)
        check_type = random.randint(1, 2)
        if check_type == 1:
            do_log_matching(accounts, serial.id)
        if check_type == 2:
            ok = True
            for account in accounts:
                ok = ok and do_integrity_check(account)
            if ok:
                print 'Integrity check passed!'
    
def do_random_transactioning(accounts, serial):
    global go_on_ch
    while go_on_ch:
        a = random.randint(0, len(accounts) - 1)
        b = random.randint(0, len(accounts) - 1)
        v = random.randint(0, min(accounts[a].value, 10))
        if v == 0:
            continue
        do_transfer(accounts[a], accounts[b], serial, v)
        
    
def main(transaction_threads, checker_threads, accounts, initial_value, running_time):
    global go_on_tr
    global go_on_ch
    
    tr = []
    ch = []
    
    try:
        accounts = [Account(x, initial_value) for x in xrange(10)]
        serial = Serial()
        tr = [threading.Thread(target=do_random_transactioning, args=(accounts, serial,)) for i in xrange(transaction_threads)]
        ch = [threading.Thread(target=do_random_checking, args=(accounts, serial,)) for i in xrange(checker_threads)]
        
        for t in tr + ch:
            t.start()
            
        time.sleep(running_time)
    except KeyboardInterrupt:
        print 'Keyboard interrupt detected!'
    
    finally:
        go_on_tr = False
        go_on_ch = False
        
        for t in tr + ch:
            t.join(1)
        
    f = open('dump.txt', 'w')
    for account in accounts:
        f.write(str(account))
    f.close()


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'Usage: %s <transaction threads> <checker threads> <running time (s)>' % sys.argv[0]
        sys.exit(1)
    main(int(sys.argv[1]), int(sys.argv[2]), 10, 100, int(sys.argv[3]))