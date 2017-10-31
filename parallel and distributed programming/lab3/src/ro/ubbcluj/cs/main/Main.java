package ro.ubbcluj.cs.main;

import ro.ubbcluj.cs.domain.Account;
import ro.ubbcluj.cs.executors.Executor;
import ro.ubbcluj.cs.executors.FutureExecutor;
import ro.ubbcluj.cs.executors.SingleThreadExecutor;
import ro.ubbcluj.cs.executors.ThreadPoolExecutor;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by tudor on 10/29/17.
 */
public class Main {
    public static void main(String[] args) {
        List<Account> accounts = new ArrayList<>();

        for (Integer i = 0; i < 10; ++i) {
            accounts.add(new Account(i + 1, 100));
        }

        //Executor executor = new ThreadPoolExecutor();
        Executor executor = new FutureExecutor();
        //Executor executor = new SingleThreadExecutor();
        executor.execute(accounts, 2, 1, 10);
        for (Account account: accounts) {
            System.out.println(account.toString());
        }
    }
}
