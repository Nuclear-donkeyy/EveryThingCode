import java.math.BigDecimal;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<SupportTicket> tickets = List.of(
                new BillingIssue("T-100", new BigDecimal("49.90"), true),
                new TechnicalIssue("T-200", "checkout-api", Severity.HIGH),
                new AccountChange("T-300", "change owner email")
        );

        for (SupportTicket ticket : tickets) {
            System.out.println(route(ticket));
        }
    }

    static String route(SupportTicket ticket) {
        return switch (ticket) {
            case BillingIssue issue ->
                    "billing team handles " + issue.id() + " refund=" + issue.refundRequested();
            case TechnicalIssue issue ->
                    "incident queue handles " + issue.id() + " service=" + issue.service()
                            + " severity=" + issue.severity();
            case AccountChange change ->
                    "account team handles " + change.id() + " request=" + change.request();
        };
    }
}

sealed interface SupportTicket permits BillingIssue, TechnicalIssue, AccountChange {
    String id();
}

record BillingIssue(String id, BigDecimal amount, boolean refundRequested) implements SupportTicket {
}

record TechnicalIssue(String id, String service, Severity severity) implements SupportTicket {
}

record AccountChange(String id, String request) implements SupportTicket {
}

enum Severity {
    LOW,
    HIGH
}
