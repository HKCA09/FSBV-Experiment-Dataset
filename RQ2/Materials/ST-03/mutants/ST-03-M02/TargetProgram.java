package application;

public class TargetProgram {
    public static String checkAccountRisk(int userId) {
        if (userId == 1001) {
            return "Overdrawn balance!";
        }
        if (userId == 1002) {
            return "No risk detected.";
        }
        return "No risk detected.";
    }
}
