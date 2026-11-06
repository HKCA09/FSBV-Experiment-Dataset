package application;

public class TargetProgram {
    public static final class TransactionObservation {
        public final boolean record_appended;
        public final String appended_item_name;
        public final double appended_quantity;
        public final double appended_total_cost;
        public final String appended_date;

        public TransactionObservation(double quantity, double totalCost) {
            if (quantity < 0) {
                this.record_appended = false;
            } else {
                this.record_appended = true;
            }
            this.appended_item_name = "SnackBar";
            this.appended_quantity = quantity;
            this.appended_total_cost = totalCost;
            this.appended_date = "2026-01-01";
        }
    }

    public static TransactionObservation addTransaction(double quantity, double totalCost) {
        return new TransactionObservation(quantity, totalCost);
    }
}
