import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<String> lines = List.of("A-100,3", "BROKEN-LINE", "B-200,5");

        try {
            ImportReport report = importOrders(lines);
            System.out.println(report);
        } catch (ImportFailedException error) {
            System.out.println("import failed: " + error.getMessage());
            System.out.println("cause: " + error.getCause().getMessage());
            for (Throwable suppressed : error.getSuppressed()) {
                System.out.println("suppressed during close: " + suppressed.getMessage());
            }
        }
    }

    static ImportReport importOrders(List<String> lines) throws ImportFailedException {
        try (LineCursor cursor = new LineCursor(lines);
             AuditTrail audit = new AuditTrail()) {
            List<OrderLine> imported = new ArrayList<>();
            while (cursor.hasNext()) {
                String raw = cursor.next();
                OrderLine orderLine = parse(raw);
                imported.add(orderLine);
                audit.record("accepted " + orderLine.orderId());
            }
            return new ImportReport(imported.size());
        } catch (IOException error) {
            ImportFailedException wrapped = new ImportFailedException("could not import order lines", error);
            for (Throwable suppressed : error.getSuppressed()) {
                wrapped.addSuppressed(suppressed);
            }
            throw wrapped;
        }
    }

    static OrderLine parse(String raw) throws IOException {
        String[] parts = raw.split(",");
        if (parts.length != 2) {
            throw new IOException("invalid csv line: " + raw);
        }
        return new OrderLine(parts[0], Integer.parseInt(parts[1]));
    }
}

final class LineCursor implements AutoCloseable {
    private final List<String> lines;
    private int index;

    LineCursor(List<String> lines) {
        this.lines = List.copyOf(lines);
        System.out.println("open line cursor");
    }

    boolean hasNext() {
        return index < lines.size();
    }

    String next() {
        return lines.get(index++);
    }

    public void close() {
        System.out.println("close line cursor");
    }
}

final class AuditTrail implements AutoCloseable {
    void record(String message) {
        System.out.println("audit: " + message);
    }

    public void close() throws IOException {
        System.out.println("close audit trail");
        throw new IOException("audit flush failed");
    }
}

final class ImportFailedException extends Exception {
    ImportFailedException(String message, Throwable cause) {
        super(message, cause);
    }
}

record OrderLine(String orderId, int quantity) {
}

record ImportReport(int importedCount) {
}
