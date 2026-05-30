import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class Main {
    record Task(String title, int hours, boolean urgent) {
    }

    public static void main(String[] args) {
        final String team = "platform";
        int sprintDays = 5;
        double focusRatio = 0.75;

        final List<Task> planned = List.of(
                new Task("review API boundary", 3, false),
                new Task("fix payment retry", 5, true),
                new Task("write migration notes", 2, false));

        List<Task> tasks = new ArrayList<>(planned);
        tasks.add(new Task("pair on release checklist", parseHours("4"), true));

        int totalHours = totalHours(tasks);
        String risk = riskLabel(totalHours, sprintDays, focusRatio);

        Map<String, Integer> limits = Map.of(
                "low", 10,
                "medium", 20,
                "high", 30);

        System.out.println("team=" + team);
        System.out.println("tasks=" + tasks.size());
        System.out.println("totalHours=" + totalHours);
        System.out.println("risk=" + risk + " limit=" + limits.get(risk));

        for (Task task : tasks) {
            if (task.urgent()) {
                System.out.println("urgent: " + task.title() + " (" + task.hours() + "h)");
            }
        }

        try {
            tasks.add(new Task("recover from bad estimate", parseHours("later"), false));
        } catch (IllegalArgumentException error) {
            System.out.println("bad estimate recovered: " + error.getMessage());
            tasks.add(new Task("recover from bad estimate", 1, false));
        }

        System.out.println("afterRecoveryHours=" + totalHours(tasks));
    }

    static int totalHours(List<Task> tasks) {
        int sum = 0;
        for (Task task : tasks) {
            sum += task.hours();
        }
        return sum;
    }

    static String riskLabel(int totalHours, int sprintDays, double focusRatio) {
        int dailyCapacity = (int) (8 * focusRatio);
        int capacity = sprintDays * dailyCapacity;

        return switch (Integer.compare(totalHours, capacity / 2)) {
            case -1 -> "low";
            case 0 -> "medium";
            default -> totalHours <= capacity ? "medium" : "high";
        };
    }

    static int parseHours(String text) {
        try {
            int hours = Integer.parseInt(text);
            if (hours <= 0) {
                throw new IllegalArgumentException("hours must be positive: " + text);
            }
            return hours;
        } catch (NumberFormatException error) {
            throw new IllegalArgumentException("hours must be a number: " + text, error);
        }
    }
}
