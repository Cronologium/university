package ro.ubbcluj.cs.tasks;

import ro.ubbcluj.cs.controllers.Controller;
import ro.ubbcluj.cs.domain.Account;

import java.util.List;
import java.util.Random;

/**
 * Created by tudor on 10/29/17.
 */
public class CheckingTask extends Task{
    public CheckingTask(Controller controller) {
        super(controller);
    }

    @Override
    public void execute(List<Account> accounts) {
        Random random = new Random();
        while (this.goOn) {
            //System.out.println(this.controller);
            if (random.nextInt(2) == 0) {
                System.out.println("Checked transactions: " + this.controller.checkLogIntegrity(accounts, this.serial.getID()).toString());
            } else {
                Boolean result = Boolean.TRUE;
                for (Account account : accounts) {
                    result &= this.controller.checkValueMatch(account);
                }
                System.out.println("Checked values: " + result.toString());
            }
            try {
                Thread.sleep(random.nextInt(500) + 500);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }
}
