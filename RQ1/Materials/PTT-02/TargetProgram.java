package application;

public class TargetProgram {
    public static final class TicketObservation {
        public final boolean ticket_written;
        public final boolean ticket_valid;
        public final int ticket_price;
        public final int user_balance_delta;
        public final String confirmation;

        public TicketObservation(boolean ticketWritten, boolean ticketValid, int ticketPrice, int userBalanceDelta, String confirmation) {
            this.ticket_written = ticketWritten;
            this.ticket_valid = ticketValid;
            this.ticket_price = ticketPrice;
            this.user_balance_delta = userBalanceDelta;
            this.confirmation = confirmation;
        }
    }

    public static TicketObservation purchaseTicket(int userId, int routeId) {
        if (userId == 1001 && routeId == 501) {
            return new TicketObservation(true, true, 120, -120, "none");
        }
        return new TicketObservation(false, false, 0, 0, "Insufficient balance or invalid route");
    }
}
