import java.math.BigDecimal;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;

public class Main {
    public static void main(String[] args) {
        LineItem keyboard = new LineItem("keyboard", 2, new Money("USD", "89.90"));
        LineItem sameKeyboard = new LineItem("keyboard", 2, new Money("USD", "89.90"));
        LineItem mouse = new LineItem("mouse", 1, new Money("USD", "39.50"));

        Set<LineItem> uniqueItems = new LinkedHashSet<>(List.of(keyboard, sameKeyboard, mouse));
        OrderSummary summary = OrderSummary.from(uniqueItems);

        System.out.println("keyboard equals sameKeyboard: " + keyboard.equals(sameKeyboard));
        System.out.println("unique item count: " + uniqueItems.size());
        System.out.println("order summary: " + summary);
    }
}

record Money(String currency, BigDecimal amount) {
    Money(String currency, String amount) {
        this(currency, new BigDecimal(amount));
    }

    Money {
        if (currency == null || currency.isBlank()) {
            throw new IllegalArgumentException("currency must not be blank");
        }
        if (amount.signum() < 0) {
            throw new IllegalArgumentException("amount must not be negative");
        }
    }

    Money multiply(int quantity) {
        return new Money(currency, amount.multiply(BigDecimal.valueOf(quantity)));
    }
}

record LineItem(String sku, int quantity, Money unitPrice) {
    LineItem {
        if (sku == null || sku.isBlank()) {
            throw new IllegalArgumentException("sku must not be blank");
        }
        if (quantity <= 0) {
            throw new IllegalArgumentException("quantity must be positive");
        }
    }

    Money subtotal() {
        return unitPrice.multiply(quantity);
    }
}

record OrderSummary(int lineCount, Money total) {
    static OrderSummary from(Set<LineItem> items) {
        BigDecimal total = items.stream()
                .map(item -> item.subtotal().amount())
                .reduce(BigDecimal.ZERO, BigDecimal::add);
        return new OrderSummary(items.size(), new Money("USD", total));
    }
}
