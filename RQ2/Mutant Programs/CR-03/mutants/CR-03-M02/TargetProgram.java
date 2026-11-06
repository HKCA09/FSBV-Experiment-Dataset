package application;

public class TargetProgram {
    public static boolean viewCatalog(String courseCatalog) {
        if (courseCatalog == null) {
            throw new IllegalArgumentException("course_catalog must not be null");
        }

        String normalized = courseCatalog.trim();
        if (normalized.equals("[]") || normalized.equals("{}")) {
            return false;
        }
        if ((normalized.startsWith("[") && normalized.endsWith("]"))
                || (normalized.startsWith("{") && normalized.endsWith("}"))) {
            return false;
        }
        throw new IllegalArgumentException("Unsupported generated collection representation: " + courseCatalog);
    }
}
