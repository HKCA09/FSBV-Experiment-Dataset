package application;

public class TargetProgram {
    public static final class WithdrawApplicationObservation {
        public final boolean application_written;
        public final String application_status;
        public final double withdraw_application_amount;
        public final String a_notice;
        public final String warning4;

        public WithdrawApplicationObservation(
                boolean applicationWritten,
                String applicationStatus,
                double withdrawApplicationAmount,
                String aNotice,
                String warning4) {
            this.application_written = applicationWritten;
            this.application_status = applicationStatus;
            this.withdraw_application_amount = withdrawApplicationAmount;
            this.a_notice = aNotice;
            this.warning4 = warning4;
        }
    }

    public static WithdrawApplicationObservation applyWithdraw(double aAmount) {
        if (aAmount <= 30000) {
            return new WithdrawApplicationObservation(
                    true,
                    "written",
                    0,
                    "Your application is successful",
                    "none");
        }
        return new WithdrawApplicationObservation(
                false,
                "unchanged",
                0,
                "none",
                "Your application amount is over the limit.");
    }
}
