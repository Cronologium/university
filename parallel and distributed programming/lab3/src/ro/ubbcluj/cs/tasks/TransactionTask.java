package ro.ubbcluj.cs.tasks;

import ro.ubbcluj.cs.controllers.Controller;
import ro.ubbcluj.cs.domain.Account;
import ro.ubbcluj.cs.domain.Serial;

import java.util.List;
import java.util.Random;

/**
 * Created by tudor on 10/29/17.
 */
public class TransactionTask extends Task {

    public TransactionTask (Controller controller) {
        super(controller);
    }

    @Override
    public void execute(List<Account> accounts) {
        Random random = new Random();
        while (this.goOn) {
            controller.transfer(
                    accounts.get(random.nextInt(accounts.size())),
                    accounts.get(random.nextInt(accounts.size())),
                    serial,
                    random.nextInt(10) + 1);
        }
    }
}
