package ro.ubbcluj.cs.tasks;

import ro.ubbcluj.cs.controllers.Controller;
import ro.ubbcluj.cs.domain.Account;
import ro.ubbcluj.cs.domain.Serial;

import java.util.List;

/**
 * Created by tudor on 10/29/17.
 */
public abstract class Task {
    protected Controller controller;
    protected Boolean goOn;
    protected Serial serial;

    public Task(Controller controller) {
        this.goOn = Boolean.TRUE;
        this.controller = controller;
        serial = new Serial();
    }

    public void stop() {
        this.goOn = Boolean.FALSE;
    }

    public abstract void execute(List<Account> accounts);
}
