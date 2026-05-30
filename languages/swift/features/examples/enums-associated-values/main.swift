enum CheckoutState {
    case emptyCart
    case reviewing(items: [String], coupon: String?)
    case paymentFailed(orderID: String, reason: String, retryCount: Int)
    case paid(orderID: String, receiptEmail: String)
}

func describe(_ state: CheckoutState) -> String {
    switch state {
    case .emptyCart:
        return "Cart is empty"
    case .reviewing(let items, let coupon):
        let couponText = coupon.map { " using coupon \($0)" } ?? " without coupon"
        return "Reviewing \(items.count) item(s)\(couponText)"
    case .paymentFailed(let orderID, let reason, let retryCount):
        return "Order \(orderID) failed: \(reason). retries: \(retryCount)"
    case .paid(let orderID, let receiptEmail):
        return "Order \(orderID) paid. Receipt sent to \(receiptEmail)"
    }
}

let flow: [CheckoutState] = [
    .emptyCart,
    .reviewing(items: ["Keyboard", "Mouse"], coupon: "SPRING10"),
    .paymentFailed(orderID: "ORD-42", reason: "card declined", retryCount: 1),
    .paid(orderID: "ORD-42", receiptEmail: "buyer@example.com")
]

for state in flow {
    print(describe(state))
}
