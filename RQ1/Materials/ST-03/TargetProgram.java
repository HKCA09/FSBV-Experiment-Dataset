package application;

public class TargetProgram {
    public static String checkAccountRisk(int userId) {
        if (userId == 1001) {
            return "Overdrawn balance!";
        }
        if (userId == 1002) {
            return "Excessive stock holdings!";
        }
        return "No risk detected.";
    }
}
