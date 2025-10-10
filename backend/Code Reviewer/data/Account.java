public class Account {
    private String name;
    private double balance;

    public Account(String n, double b) {
        name = n;
        balance = b;
    }

    public void deposit(double amount) {
        balance += amount;
        System.out.println("Deposited: " + amount);
    }

    public void withdraw(double amount) {
        if (balance < amount)
            System.out.println("Insufficient funds");
        else
            balance -= amount;
    }
}
