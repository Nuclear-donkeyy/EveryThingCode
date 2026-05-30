import java.io.IOException;

public class Main {
    static String loadName(boolean ok) throws IOException {
        if (!ok) throw new IOException("config missing");
        return "learner";
    }

    public static void main(String[] args) {
        try {
            System.out.println(loadName(false));
        } catch (IOException ex) {
            System.out.println("recover: " + ex.getMessage());
        }
    }
}
