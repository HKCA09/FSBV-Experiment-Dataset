package application;

public class TargetProgram {
    public static final class ExchangeObservation {
        public final boolean exchange_completed;
        public final double current_balance_delta;
        public final double foreign_balance_delta;
        public final double new_current_balance;
        public final double new_foreign_balance;
        public final boolean notice_emitted;
        public final String warning8;

        public ExchangeObservation(boolean exchangeCompleted, double currentBalanceDelta,
                double foreignBalanceDelta, double newCurrentBalance, double newForeignBalance,
                boolean noticeEmitted, String warning8) {
            this.exchange_completed = exchangeCompleted;
            this.current_balance_delta = currentBalanceDelta;
            this.foreign_balance_delta = foreignBalanceDelta;
            this.new_current_balance = newCurrentBalance;
            this.new_foreign_balance = newForeignBalance;
            this.notice_emitted = noticeEmitted;
            this.warning8 = warning8;
        }
    }

    public static ExchangeObservation buyDollarsFromCurrent(int amountInYen,
            double currentExchangeRate, double oldForeignBalance) {
        if (amountInYen < 0 || oldForeignBalance < 0 || currentExchangeRate <= 0) {
            throw new IllegalArgumentException("Invalid exchange input or state snapshot");
        }
        if (amountInYen < 10000) {
            double amountInDollar = amountInYen / currentExchangeRate;
            return new ExchangeObservation(true, -amountInYen, amountInDollar,
                    10000 - amountInYen, oldForeignBalance + amountInDollar, true, "none");
        }
        return new ExchangeObservation(false, 0, 0, 10000, oldForeignBalance,
                false, "The requested amount is over the balance of your current account.");
    }
}
