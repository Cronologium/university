package ro.ubbcluj.cs.executors;

import ro.ubbcluj.cs.domain.Account;

import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * Created by tudor on 10/29/17.
 */
public class ThreadPoolExecutor extends Executor {

    public ThreadPoolExecutor() {
        super();
    }

    @Override
    public void execute(List<Account> accounts, Integer transactionThreads, Integer checkerThreads, Integer runningTime) {
        ExecutorService executorService = Executors.newFixedThreadPool(transactionThreads + checkerThreads);

        for (Integer i = 0; i < transactionThreads; ++i) {
             executorService.submit(() -> this.transactionTask.execute(accounts));
        }

        for (Integer i = 0; i < checkerThreads; ++i) {
            executorService.submit(() -> this.checkingTask.execute(accounts));
        }

        try {
            Thread.sleep(runningTime * 1000);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        checkingTask.stop();
        transactionTask.stop();

        executorService.shutdown();
    }
}
