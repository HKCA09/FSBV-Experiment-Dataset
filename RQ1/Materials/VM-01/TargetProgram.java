package application;

public class TargetProgram {
    public static final class ItemObservation {
        public final boolean item_written;
        public final int appended_quantity;
        public final double appended_price;

        public ItemObservation(boolean itemWritten, int appendedQuantity, double appendedPrice) {
            this.item_written = itemWritten;
            this.appended_quantity = appendedQuantity;
            this.appended_price = appendedPrice;
        }
    }

    public static ItemObservation addItem(int quantity, double price) {
        return new ItemObservation(true, quantity, price * quantity);
    }
}
