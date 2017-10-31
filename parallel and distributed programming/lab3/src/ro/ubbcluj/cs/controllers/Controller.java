package ro.ubbcluj.cs.controllers;

import ro.ubbcluj.cs.domain.Account;
import ro.ubbcluj.cs.domain.Serial;
import ro.ubbcluj.cs.domain.Transaction;

import java.util.List;

/**
 * Created by tudor on 10/29/17.
 */
public class Controller {
    public Boolean checkValueMatch(Account account) {
        Boolean result = Boolean.TRUE;
        synchronized (account) {
            Integer sum = 100;
            for (Integer key : account.getTransactions().keySet()) {
                sum += account.getTransactions().get(key).getAmount();
            }
            result = (sum.equals(account.getValue()));
        }
        return result;
    }

    public Boolean checkLogIntegrity(List<Account> accounts, Integer lastID) {
        for (Account account : accounts) {
            for (Integer id = 0; id < lastID; ++id) {
                Transaction transaction = account.getTransactions().get(id);
                if (transaction == null) {
                    continue;
                } else {
                    if (transaction.getSource().getTransactions().get(id) == null) {
                        return Boolean.FALSE;
                    }
                }
            }
        }
        return Boolean.TRUE;
    }

    @SuppressWarnings("Duplicates")
    public void transfer(Account source, Account destination, Serial serial, Integer amount) {
        if (source == destination)
            return;
        if(source.getID() < destination.getID()) {
            synchronized (source) {
                synchronized (destination) {
                    Integer serialID = serial.getNext();
                    if (source.addTransaction(serialID, destination, -amount)) {
                        destination.addTransaction(serialID, source, amount);
                    }
                }
            }
        } else {
            synchronized (destination) {
                synchronized (source) {
                    Integer serialID = serial.getNext();
                    if (source.addTransaction(serialID, destination, -amount)) {
                        destination.addTransaction(serialID, source, amount);
                    }
                }
            }
        }
    }
}
