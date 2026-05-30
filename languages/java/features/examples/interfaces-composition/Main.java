import java.math.BigDecimal;
import java.math.RoundingMode;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        Cart cart = new Cart(List.of(
                new CartLine("book", new BigDecimal("39.90"), 2),
                new CartLine("lamp", new BigDecimal("120.00"), 1)
        ));

        CheckoutService standard = new CheckoutService(
                new NoDiscount(),
                new FixedRateTax(new BigDecimal("0.08")),
                new ConsoleReceipt()
        );

        CheckoutService memberSale = new CheckoutService(
                new PercentageDiscount(new BigDecimal("0.15")),
                new FixedRateTax(new BigDecimal("0.08")),
                new ConsoleReceipt()
        );

        System.out.println("standard checkout");
        standard.checkout(cart);

        System.out.println();
        System.out.println("member sale checkout");
        memberSale.checkout(cart);
    }
}

interface DiscountPolicy {
    BigDecimal discountFor(BigDecimal subtotal);
}

interface TaxPolicy {
    BigDecimal taxFor(BigDecimal taxableAmount);
}

interface ReceiptSink {
    void print(Receipt receipt);
}

final class CheckoutService {
    private final DiscountPolicy discountPolicy;
    private final TaxPolicy taxPolicy;
    private final ReceiptSink receiptSink;

    CheckoutService(DiscountPolicy discountPolicy, TaxPolicy taxPolicy, ReceiptSink receiptSink) {
        this.discountPolicy = discountPolicy;
        this.taxPolicy = taxPolicy;
        this.receiptSink = receiptSink;
    }

    Receipt checkout(Cart cart) {
        BigDecimal subtotal = cart.subtotal();
        BigDecimal discount = discountPolicy.discountFor(subtotal);
        BigDecimal taxableAmount = subtotal.subtract(discount);
        BigDecimal tax = taxPolicy.taxFor(taxableAmount);
        Receipt receipt = new Receipt(subtotal, discount, tax, taxableAmount.add(tax));
        receiptSink.print(receipt);
        return receipt;
    }
}

final class NoDiscount implements DiscountPolicy {
    public BigDecimal discountFor(BigDecimal subtotal) {
        return BigDecimal.ZERO;
    }
}

final class PercentageDiscount implements DiscountPolicy {
    private final BigDecimal rate;

    PercentageDiscount(BigDecimal rate) {
        if (rate.signum() < 0 || rate.compareTo(BigDecimal.ONE) > 0) {
            throw new IllegalArgumentException("rate must be between 0 and 1");
        }
        this.rate = rate;
    }

    public BigDecimal discountFor(BigDecimal subtotal) {
        return subtotal.multiply(rate).setScale(2, RoundingMode.HALF_UP);
    }
}

final class FixedRateTax implements TaxPolicy {
    private final BigDecimal rate;

    FixedRateTax(BigDecimal rate) {
        this.rate = rate;
    }

    public BigDecimal taxFor(BigDecimal taxableAmount) {
        return taxableAmount.multiply(rate).setScale(2, RoundingMode.HALF_UP);
    }
}

final class ConsoleReceipt implements ReceiptSink {
    public void print(Receipt receipt) {
        System.out.println("subtotal: " + receipt.subtotal());
        System.out.println("discount: " + receipt.discount());
        System.out.println("tax: " + receipt.tax());
        System.out.println("total: " + receipt.total());
    }
}

record Cart(List<CartLine> lines) {
    Cart {
        lines = List.copyOf(lines);
    }

    BigDecimal subtotal() {
        return lines.stream()
                .map(CartLine::subtotal)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}

record CartLine(String sku, BigDecimal unitPrice, int quantity) {
    CartLine {
        if (sku == null || sku.isBlank()) {
            throw new IllegalArgumentException("sku must not be blank");
        }
        if (unitPrice.signum() < 0) {
            throw new IllegalArgumentException("unitPrice must not be negative");
        }
        if (quantity <= 0) {
            throw new IllegalArgumentException("quantity must be positive");
        }
    }

    BigDecimal subtotal() {
        return unitPrice.multiply(BigDecimal.valueOf(quantity));
    }
}

record Receipt(BigDecimal subtotal, BigDecimal discount, BigDecimal tax, BigDecimal total) {
}
