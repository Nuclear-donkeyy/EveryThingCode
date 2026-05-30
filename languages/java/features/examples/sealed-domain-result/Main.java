import java.math.BigDecimal;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        PaymentService service = new PaymentService();

        List<PaymentRequest> requests = List.of(
                new PaymentRequest("A-100", new BigDecimal("48.00")),
                new PaymentRequest("B-200", new BigDecimal("0.00")),
                new PaymentRequest("C-300", new BigDecimal("12000.00"))
        );

        for (PaymentRequest request : requests) {
            PaymentResult result = service.charge(request);
            System.out.println(describe(result));
        }
    }

    static String describe(PaymentResult result) {
        if (result instanceof Approved approved) {
            return "approved " + approved.orderId() + " with confirmation " + approved.confirmationCode();
        }
        if (result instanceof Declined declined) {
            return "declined " + declined.orderId() + ": " + declined.reason();
        }
        if (result instanceof NeedsReview review) {
            return "review " + review.orderId() + ": " + review.note();
        }
        throw new IllegalStateException("unknown result: " + result);
    }
}

record PaymentRequest(String orderId, BigDecimal amount) {
    PaymentRequest {
        if (orderId == null || orderId.isBlank()) {
            throw new IllegalArgumentException("orderId must not be blank");
        }
        if (amount.signum() < 0) {
            throw new IllegalArgumentException("amount must not be negative");
        }
    }
}

sealed interface PaymentResult permits Approved, Declined, NeedsReview {
    String orderId();
}

record Approved(String orderId, String confirmationCode) implements PaymentResult {
}

record Declined(String orderId, String reason) implements PaymentResult {
}

record NeedsReview(String orderId, String note) implements PaymentResult {
}

final class PaymentService {
    PaymentResult charge(PaymentRequest request) {
        if (request.amount().compareTo(BigDecimal.ZERO) == 0) {
            return new Declined(request.orderId(), "amount is zero");
        }
        if (request.amount().compareTo(new BigDecimal("10000.00")) > 0) {
            return new NeedsReview(request.orderId(), "large payment requires manual approval");
        }
        return new Approved(request.orderId(), "CONF-" + request.orderId());
    }
}
