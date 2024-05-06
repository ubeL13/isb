import java.math.BigInteger;
import java.util.Random;

public class Main {
    public static void main(String[] args) {
        Random random = new Random();
        BigInteger bigInt = new BigInteger(128, random);
        String binarySequence = bigInt.toString(2);
        while (binarySequence.length() < 128) {
            binarySequence = "0" + binarySequence;
        }
        System.out.println("128-bit binary sequence: " + binarySequence);
    }
}




