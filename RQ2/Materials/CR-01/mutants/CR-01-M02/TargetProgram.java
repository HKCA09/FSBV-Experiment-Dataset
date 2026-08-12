package application;

/*
 * Reference implementation draft -- requires researcher approval
 * Exploratory collection-observation adapter for CR-01 / Register_Course
 */
public class TargetProgram {

    public static final int FIXED_STUDENT_ID = 1001;
    public static final int FIXED_COURSE_ID = 2001;
    public static final int MIN_COURSE_LIMIT = 1;
    public static final int MAX_COURSE_LIMIT = 8;

    public static final class RegistrationObservation {
        public final boolean student_resolved;
        public final boolean course_resolved;
        public final int old_course_count;
        public final int new_course_count;
        public final boolean target_course_added;
        public final boolean success;
        public final String message;

        public RegistrationObservation(
            boolean studentResolved,
            boolean courseResolved,
            int oldCourseCount,
            int newCourseCount,
            boolean targetCourseAdded,
            boolean success,
            String message
        ) {
            this.student_resolved = studentResolved;
            this.course_resolved = courseResolved;
            this.old_course_count = oldCourseCount;
            this.new_course_count = newCourseCount;
            this.target_course_added = targetCourseAdded;
            this.success = success;
            this.message = message;
        }
    }

    public static RegistrationObservation registerCourse(int old_course_count) {
        if (old_course_count < MIN_COURSE_LIMIT || old_course_count > MAX_COURSE_LIMIT) {
            throw new IllegalArgumentException("old_course_count out of fixture-supported range");
        }

        boolean studentResolved = true;
        boolean courseResolved = true;

        if (old_course_count < MAX_COURSE_LIMIT) {
            return new RegistrationObservation(
                studentResolved,
                courseResolved,
                old_course_count,
                old_course_count - 1,
                true,
                true,
                "Course registered successfully."
            );
        }

        return new RegistrationObservation(
            studentResolved,
            courseResolved,
            old_course_count,
            old_course_count,
            false,
            false,
            "Course limit exceeded."
        );
    }
}
