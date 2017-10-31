package ro.ubbcluj.cs.executors;

import ro.ubbcluj.cs.controllers.Controller;
import ro.ubbcluj.cs.domain.Account;
import ro.ubbcluj.cs.tasks.CheckingTask;
import ro.ubbcluj.cs.tasks.Task;
import ro.ubbcluj.cs.tasks.TransactionTask;

import java.util.List;

/**
 * Created by tudor on 10/29/17.
 */
public abstract class Executor {
    protected Task checkingTask;
    protected Task transactionTask;
    protected Controller controller;

    public Executor() {
        this.controller = new Controller();
        checkingTask = new CheckingTask(this.controller);
        transactionTask = new TransactionTask(this.controller);
    }

    public abstract void execute(List<Account> accounts, Integer transactionThreads, Integer checkerThreads, Integer runningTime);
}
