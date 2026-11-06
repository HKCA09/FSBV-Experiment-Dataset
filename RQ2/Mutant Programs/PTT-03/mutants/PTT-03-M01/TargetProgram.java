package application;

/*
 * Reference implementation draft -- requires researcher approval
 * Reference implementation for controlled-change PTT-03 executable adapter v2.1
 */
public class TargetProgram {

    public static final String FIXED_PAYMENT = "payment_request";
    public static final int FIXED_USER_ID = 1001;
    public static final String FIXED_METHOD = "EWallet";
    public static final double FIXED_OLD_BALANCE = 140.0;
    public static final double MIN_BALANCE = 100.0;

    public static final class PaymentObservation {
        public final boolean status;
        public final String receipt;
        public final boolean resolved_user;
        public final double old_balance;
        public final double new_balance;
        public final String balance_effect;

        public PaymentObservation(
            boolean status,
            String receipt,
            boolean resolvedUser,
            double oldBalance,
            double newBalance,
            String balanceEffect
        ) {
            this.status = status;
            this.receipt = receipt;
            this.resolved_user = resolvedUser;
            this.old_balance = oldBalance;
            this.new_balance = newBalance;
            this.balance_effect = balanceEffect;
        }
    }

    public static PaymentObservation makePayment(double amount) {
        double oldBalance = FIXED_OLD_BALANCE;
        if (amount >= 0.0 && oldBalance - amount > MIN_BALANCE) {
            double newBalance = oldBalance - amount;
            return new PaymentObservation(
                true,
                "Payment successful",
                true,
                oldBalance,
                newBalance,
                "debit"
            );
        }
        return new PaymentObservation(
            false,
            "Payment failed",
            true,
            oldBalance,
            oldBalance,
            "unchanged"
        );
    }
}
