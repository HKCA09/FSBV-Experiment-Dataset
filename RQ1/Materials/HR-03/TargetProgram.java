package application;

public class TargetProgram {
    public static final class RegistrationObservation {
        public final boolean registration_created;
        public final boolean registration_appended;
        public final int registration_patient_id;
        public final int registration_doctor_id;
        public final int registration_department_id;
        public final double registration_time_slot;

        public RegistrationObservation(int patientId, int doctorId, int departmentId, double timeSlot) {
            this.registration_created = true;
            this.registration_appended = true;
            this.registration_patient_id = patientId;
            this.registration_doctor_id = doctorId;
            this.registration_department_id = departmentId;
            this.registration_time_slot = timeSlot;
        }
    }

    public static RegistrationObservation performRegistration(int patientId, int doctorId, int departmentId, double timeSlot) {
        return new RegistrationObservation(patientId, doctorId, departmentId, timeSlot);
    }
}
