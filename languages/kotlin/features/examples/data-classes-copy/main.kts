data class Ticket(
    val id: String,
    val title: String,
    val status: String,
    val assignee: String?,
    val labels: List<String>,
)

fun assignToLin(ticket: Ticket): Ticket =
    ticket.copy(status = "in-progress", assignee = "Lin")

fun closeTicket(ticket: Ticket): Ticket =
    ticket.copy(status = "closed", labels = ticket.labels + "done")

val newTicket = Ticket(
    id = "KT-42",
    title = "补充 Kotlin 教学例子",
    status = "open",
    assignee = null,
    labels = listOf("docs", "teaching"),
)

val duplicateNewTicket = Ticket(
    id = "KT-42",
    title = "补充 Kotlin 教学例子",
    status = "open",
    assignee = null,
    labels = listOf("docs", "teaching"),
)

val assigned = assignToLin(newTicket)
val closed = closeTicket(assigned)
val (id, title, status) = closed

println("原始工单: $newTicket")
println("分配后: $assigned")
println("关闭后: $closed")
println("按值比较: ${newTicket == duplicateNewTicket}")
println("解构摘要: $id | $title | $status")

data class AuditTrail(val events: MutableList<String>)

val originalTrail = AuditTrail(mutableListOf("created", "assigned"))
val copiedTrail = originalTrail.copy()
originalTrail.events += "closed"

println("浅拷贝示例 original=${originalTrail.events}")
println("浅拷贝示例 copied=${copiedTrail.events}")
