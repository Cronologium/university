package ro.ubbcluj.cs.executors;

import ro.ubbcluj.cs.domain.Account;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.*;

/**
 * Created by tudor on 10/29/17.
 */
public class FutureExecutor extends Executor {
    @Override
    public void execute(List<Account> accounts, Integer transactionThreads, Integer checkerThreads, Integer runningTime) {
        List<Thread> transactions = new ArrayList<>();
        List<Future<Boolean>> checkers = new ArrayList<>();

        for (Integer i = 0; i < transactionThreads; ++i) {
            transactions.add(new Thread(() -> {
                this.transactionTask.execute(accounts);
            }));
        }

        for (Integer i = 0; i < checkerThreads; ++i) {
            checkers.add(Executors.newSingleThreadExecutor().submit(() -> {this.checkingTask.execute(accounts); return Boolean.TRUE;}));
        }

        for (Thread thread : transactions) {
            thread.start();
        }

        try {
            Thread.sleep(runningTime * 1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        checkingTask.stop();
        transactionTask.stop();

        for (Thread thread : transactions) {
            try {
                thread.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        for (Future<Boolean> future : checkers) {
            try {
                future.get();
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            }
        }
    }
}
