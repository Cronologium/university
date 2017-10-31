package ro.ubbcluj.cs.executors;

import ro.ubbcluj.cs.domain.Account;

import java.util.List;

/**
 * Created by tudor on 10/29/17.
 */
public class SingleThreadExecutor extends Executor {

    public SingleThreadExecutor() {
        super();
    }

    @Override
    public void execute(List<Account> accounts, Integer transactionThreads, Integer checkerThreads, Integer runningTime) {
        this.checkingTask.execute(accounts);

    }
}
