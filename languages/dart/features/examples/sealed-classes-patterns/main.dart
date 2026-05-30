sealed class CheckoutState {
  const CheckoutState();
}

class EditingCart extends CheckoutState {
  const EditingCart(this.items);

  final List<String> items;
}

class AwaitingPayment extends CheckoutState {
  const AwaitingPayment({required this.orderId, required this.total});

  final String orderId;
  final double total;
}

class Paid extends CheckoutState {
  const Paid({required this.orderId, required this.receiptCode});

  final String orderId;
  final String receiptCode;
}

class Failed extends CheckoutState {
  const Failed({required this.orderId, required this.reason});

  final String orderId;
  final String reason;
}

String renderCheckout(CheckoutState state) {
  return switch (state) {
    EditingCart(items: final items) when items.isEmpty =>
      'Cart is empty; show product recommendations.',
    EditingCart(:final items) =>
      'Cart has ${items.length} item(s); enable checkout.',
    AwaitingPayment(:final orderId, :final total) =>
      'Order $orderId is waiting for payment: \$${total.toStringAsFixed(2)}.',
    Paid(:final orderId, :final receiptCode) =>
      'Order $orderId paid; receipt $receiptCode.',
    Failed(:final orderId, :final reason) =>
      'Order $orderId failed: $reason.',
  };
}

void main() {
  const states = <CheckoutState>[
    EditingCart([]),
    EditingCart(['book', 'pen']),
    AwaitingPayment(orderId: 'A-1007', total: 42.5),
    Paid(orderId: 'A-1007', receiptCode: 'R-8831'),
    Failed(orderId: 'A-1008', reason: 'card declined'),
  ];

  for (final state in states) {
    print(renderCheckout(state));
  }
}
