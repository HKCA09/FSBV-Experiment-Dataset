package application;

public class TargetProgram {
    public static final class RouteObservation {
        public final boolean route_written;
        public final boolean status;
        public final String message;

        public RouteObservation(boolean routeWritten, boolean status, String message) {
            this.route_written = routeWritten;
            this.status = status;
            this.message = message;
        }
    }

    public static RouteObservation updateRoute(String routeProfile) {
        if ("existing_route".equals(routeProfile)) {
            return new RouteObservation(true, true, "Route added");
        }
        return new RouteObservation(false, false, "Route already exists");
    }
}
