package ro.ubbcluj.cs.domain;

import java.util.HashMap;
import java.util.Map;

/**
 * Created by tudor on 10/29/17.
 */
public class Account {
    private Integer ID;
    private Integer value;
    private Map<Integer, Transaction> transactions;

    public Integer getID() {
        return ID;
    }

    public Integer getValue() {
        return value;
    }

    public Map<Integer, Transaction> getTransactions() {
        return transactions;
    }

    public Account(Integer ID, Integer value) {
        this.ID = ID;
        this.value = value;
        this.transactions = new HashMap<>();
    }

    public Boolean addTransaction(Integer transactionId, Account source, Integer value) {
        if (this.value + value < 0)
        {
            return Boolean.FALSE;
        }
        transactions.put(transactionId, new Transaction(transactionId, source, value));
        this.value += value;
        return Boolean.TRUE;
    }

    @Override
    public String toString(){
        return "Account(ID = " + this.ID.toString() + ", Value = " + this.value.toString() + ")";
    }
}
