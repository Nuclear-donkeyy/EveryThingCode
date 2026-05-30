import java.util.List;

public class Main {
    record Course(String name, int minutes) {}

    public static void main(String[] args) {
        var courses = List.of(new Course("records", 20), new Course("streams", 30));
        int total = courses.stream().mapToInt(Course::minutes).sum();
        System.out.println("total minutes = " + total);
    }
}
