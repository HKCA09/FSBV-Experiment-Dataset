package application;

public class TargetProgram {
    public static final class DropObservation {
        public final boolean student_resolved;
        public final boolean course_resolved;
        public final boolean course_present;
        public final int old_course_count;
        public final int new_course_count;
        public final boolean target_course_removed;
        public final boolean status;
        public final String message;

        public DropObservation(boolean studentResolved, boolean courseResolved, boolean coursePresent,
                int oldCourseCount, int newCourseCount, boolean targetCourseRemoved,
                boolean status, String message) {
            this.student_resolved = studentResolved;
            this.course_resolved = courseResolved;
            this.course_present = coursePresent;
            this.old_course_count = oldCourseCount;
            this.new_course_count = newCourseCount;
            this.target_course_removed = targetCourseRemoved;
            this.status = status;
            this.message = message;
        }
    }

    public static DropObservation dropCourse(int oldCourseCount) {
        if (oldCourseCount >= 1) {
            return new DropObservation(true, true, true, oldCourseCount, oldCourseCount - 1, true, true,
                    "Course dropped successfully.");
        }
        return new DropObservation(true, true, true, oldCourseCount, oldCourseCount, false, false,
                "Minimum course limit reached.");
    }
}
