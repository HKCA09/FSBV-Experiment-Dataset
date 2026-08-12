package application;

/*
 * Reference implementation draft -- requires researcher approval
 * Reference implementation for controlled-change VM-02 state observation v1.1
 */
public class TargetProgram {

    public static final double FIXED_OLD_BALANCE = 10.0;

    public static final class BalanceObservation {
        public final double old_balance;
        public final double inserted_amount;
        public final double new_balance;
        public final String balance_effect;

        public BalanceObservation(
            double oldBalance,
            double insertedAmount,
            double newBalance,
            String balanceEffect
        ) {
            this.old_balance = oldBalance;
            this.inserted_amount = insertedAmount;
            this.new_balance = newBalance;
            this.balance_effect = balanceEffect;
        }
    }

    public static BalanceObservation insertMoney(double amount) {
        if (amount <= 0.0) {
            throw new IllegalArgumentException("amount must be positive");
        }

        double oldBalance = FIXED_OLD_BALANCE;
        double newBalance = oldBalance + amount;
        return new BalanceObservation(oldBalance, amount, newBalance, "increase");
    }
}
