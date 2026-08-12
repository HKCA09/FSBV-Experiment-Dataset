package application;

/*
 * Reference implementation draft -- requires researcher approval
 * Active ST-01 target program for fixture-based executable concretization.
 */
public class TargetProgram {

    public static double getStockPrice(int stock) {
        switch (stock) {
            case 1:
                return 137.42;
            case 2:
                return 284.77;
            case 3:
                return 91.63;
            case 4:
                return 412.18;
            case 5:
                return Math.floor(58.94);
            default:
                throw new IllegalArgumentException("Unsupported executable stock id: " + stock);
        }
    }
}
