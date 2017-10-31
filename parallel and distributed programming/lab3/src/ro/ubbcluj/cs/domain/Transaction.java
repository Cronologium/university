package ro.ubbcluj.cs.domain;

/**
 * Created by tudor on 10/29/17.
 */
public class Transaction {
    private Integer ID;
    private Account source;
    private Integer amount;

    public Transaction(Integer ID, Account source, Integer amount) {
        this.ID = ID;
        this.source = source;
        this.amount = amount;
    }

    public Integer getID() {
        return ID;
    }

    public Account getSource() {
        return source;
    }

    public Integer getAmount() {
        return amount;
    }
}
