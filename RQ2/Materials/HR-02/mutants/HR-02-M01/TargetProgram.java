package application;

public class TargetProgram {
    public static final class ScheduleObservation {
        public final boolean schedule_inserted;
        public final boolean schedule_merged;
        public final boolean doctor_resolved;

        public ScheduleObservation(boolean scheduleInserted, boolean scheduleMerged, boolean doctorResolved) {
            this.schedule_inserted = scheduleInserted;
            this.schedule_merged = scheduleMerged;
            this.doctor_resolved = doctorResolved;
        }
    }

    public static ScheduleObservation updateSchedule(String doctorProfile) {
        if ("existing_doctor".equals(doctorProfile)) {
            return new ScheduleObservation(true, false, false);
        }
        return new ScheduleObservation(false, true, true);
    }
}
