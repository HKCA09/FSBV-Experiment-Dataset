package application;

public class TargetProgram {
    public static final class DepositObservation {
        public final boolean notice_emitted;
        public final double balance_delta;
        public final boolean history_appended;
        public final String warning1;

        public DepositObservation(boolean noticeEmitted, double balanceDelta, boolean historyAppended, String warning1) {
            this.notice_emitted = noticeEmitted;
            this.balance_delta = balanceDelta;
            this.history_appended = historyAppended;
            this.warning1 = warning1;
        }
    }

    public static DepositObservation currentDeposit(double depositAmount) {
        if (depositAmount <= 10000) {
            return new DepositObservation(true, depositAmount, false, "none");
        }
        return new DepositObservation(false, 0, false, "Your amount is over 10000 yuan limit.");
    }
}
