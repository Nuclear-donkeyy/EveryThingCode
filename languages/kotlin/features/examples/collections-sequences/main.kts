data class Order(
    val id: String,
    val region: String,
    val status: String,
    val amountCents: Int,
)

data class RevenueLine(
    val region: String,
    val amountCents: Int,
)

val orders = listOf(
    Order("A100", "north", "paid", 1_200),
    Order("A101", "south", "draft", 700),
    Order("A102", "north", "paid", 2_400),
    Order("A103", "west", "paid", 900),
    Order("A104", "south", "paid", 1_600),
)

val revenueByRegion = orders
    .filter { it.status == "paid" }
    .map { RevenueLine(it.region, it.amountCents) }
    .groupBy { it.region }
    .mapValues { (_, lines) -> lines.sumOf { it.amountCents } }

println("已支付收入汇总:")
revenueByRegion
    .toSortedMap()
    .forEach { (region, cents) -> println("- $region: ${cents / 100.0}") }

println()
println("Sequence 求值过程:")
val firstTwoPaidSummaries = orders
    .asSequence()
    .filter {
        println("filter ${it.id}")
        it.status == "paid"
    }
    .map {
        println("map ${it.id}")
        "${it.id}@${it.region}=${it.amountCents / 100.0}"
    }
    .take(2)
    .toList()

println("前两个已支付订单: ${firstTwoPaidSummaries.joinToString()}")
