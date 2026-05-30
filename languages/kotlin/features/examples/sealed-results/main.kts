data class Order(
    val id: String,
    val totalCents: Int,
    val riskScore: Int,
)

sealed interface CheckoutResult {
    data class Accepted(val orderId: String, val receiptCode: String) : CheckoutResult
    data class Rejected(val orderId: String, val reason: String) : CheckoutResult
    data object ManualReview : CheckoutResult
}

fun checkout(order: Order): CheckoutResult =
    when {
        order.totalCents <= 0 -> CheckoutResult.Rejected(order.id, "金额必须大于 0")
        order.riskScore >= 80 -> CheckoutResult.ManualReview
        else -> CheckoutResult.Accepted(order.id, "RCPT-${order.id}-${order.totalCents}")
    }

fun describe(result: CheckoutResult): String =
    when (result) {
        is CheckoutResult.Accepted -> "通过: ${result.orderId}, receipt=${result.receiptCode}"
        is CheckoutResult.Rejected -> "拒绝: ${result.orderId}, reason=${result.reason}"
        CheckoutResult.ManualReview -> "转人工审核"
    }

val orders = listOf(
    Order("A100", 5600, 12),
    Order("B200", 0, 5),
    Order("C300", 4200, 91),
)

orders
    .map(::checkout)
    .map(::describe)
    .forEach(::println)
