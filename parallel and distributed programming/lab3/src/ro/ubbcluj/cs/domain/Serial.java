package ro.ubbcluj.cs.domain;

/**
 * Created by tudor on 10/29/17.
 */
public class Serial {
    private Integer ID;

    public Serial() {
        this.ID = 1;
    }

    public synchronized Integer getNext() {
        Integer value = ID;
        this.ID += 1;
        return value;
    }

    public Integer getID() {
        return this.ID;
    }
}
