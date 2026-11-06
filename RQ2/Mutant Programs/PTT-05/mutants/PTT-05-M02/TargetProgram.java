package application;

public class TargetProgram {
    public static final class TicketValidationObservation {
        public final boolean status;
        public final String message;

        public TicketValidationObservation(boolean status, String message) {
            this.status = status;
            this.message = message;
        }
    }

    public static TicketValidationObservation validateTicket(String ticketProfile) {
        if ("valid_ticket".equals(ticketProfile)) {
            return new TicketValidationObservation(true, "Ticket is invalid or expired");
        }
        if ("invalid_or_expired_ticket".equals(ticketProfile)) {
            return new TicketValidationObservation(false, "Ticket is invalid or expired");
        }
        throw new IllegalArgumentException("Unknown ticket profile: " + ticketProfile);
    }
}
