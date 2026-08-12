package application;

public class TargetProgram {
    public static final class PasswordChangeObservation {
        public final boolean password_changed;
        public final String s_notice1;
        public final String warning11;

        public PasswordChangeObservation(boolean passwordChanged, String successNotice, String warning11) {
            this.password_changed = passwordChanged;
            this.s_notice1 = successNotice;
            this.warning11 = warning11;
        }
    }

    public static PasswordChangeObservation changeCurrentPassword(String accountProfile) {
        if ("existing_account".equals(accountProfile)) {
            return new PasswordChangeObservation(false, "successful", "none");
        }
        return new PasswordChangeObservation(false, "none", "Your old password or account number is incorrect.");
    }
}
