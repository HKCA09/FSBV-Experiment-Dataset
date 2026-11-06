package application;

public class TargetProgram {
    public static final class BalanceObservation {
        public final boolean status;
        public final String message;
        public final boolean user_resolved;
        public final double balance_delta;

        public BalanceObservation(boolean status, String message, boolean userResolved, double balanceDelta) {
            this.status = status;
            this.message = message;
            this.user_resolved = userResolved;
            this.balance_delta = balanceDelta;
        }
    }

    public static BalanceObservation updateBalance(int userProfile, double amount) {
        if (amount < 0) {
            throw new IllegalArgumentException("amount must satisfy nat0");
        }
        if (userProfile >= 0) {
            return new BalanceObservation(true, "Balance updated", true, amount);
        }
        if (userProfile == 0) {
            return new BalanceObservation(false, "User not found", false, 0);
        }
        throw new IllegalArgumentException("Unknown user profile");
    }
}
