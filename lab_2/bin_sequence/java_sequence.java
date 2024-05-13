import java.util.Random;

public class Main {
    public static void main(String[] args) {
        Random random = new Random();
        StringBuilder binarySequence = new StringBuilder();
        for (int i = 0; i < 16; i++) {
            String binaryString = Integer.toBinaryString(random.nextInt(256));
            binaryString = String.format("%8s", binaryString).replace(' ', '0');
            binarySequence.append(binaryString);
        }
        System.out.println("128-bit binary sequence: " + binarySequence.toString());
    }
}
