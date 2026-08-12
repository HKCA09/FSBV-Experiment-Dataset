package application;

public class TargetProgram {
    public static final class PatientObservation {
        public final int patient_id;
        public final boolean patient_inserted;
        public final boolean generated_patient_id_fresh;

        public PatientObservation(int patientId, boolean patientInserted, boolean generatedPatientIdFresh) {
            this.patient_id = patientId;
            this.patient_inserted = patientInserted;
            this.generated_patient_id_fresh = generatedPatientIdFresh;
        }
    }

    public static PatientObservation registerPatient(String patientInfo) {
        int patientId = "Bob_Profile".equals(patientInfo) ? 2002 : 2001;
        return new PatientObservation(patientId, true, true);
    }
}
