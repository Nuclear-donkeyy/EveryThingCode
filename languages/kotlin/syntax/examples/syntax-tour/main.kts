import kotlin.math.roundToInt

data class TaskInput(val title: String?, val hoursText: String, val urgent: Boolean = false)

data class Task(
    val title: String,
    val hours: Int,
    val urgent: Boolean,
    val tags: List<String> = emptyList(),
)

sealed class ParseResult {
    data class Accepted(val task: Task) : ParseResult()
    data class Rejected(val source: String, val reason: String) : ParseResult()
}

fun normalizeTitle(title: String?): String =
    title?.trim()?.takeIf { it.isNotEmpty() } ?: "untitled"

fun dailyCapacity(focusRatio: Double): Int = (8 * focusRatio).roundToInt()

fun sprintCapacity(days: Int, focusRatio: Double = 0.75): Int =
    days * dailyCapacity(focusRatio)

fun parseHours(text: String): Result<Int> =
    runCatching {
        val hours = text.trim().toInt()
        require(hours > 0) { "hours must be positive: $text" }
        hours
    }

fun riskLabel(totalHours: Int, capacity: Int): String =
    when {
        totalHours < capacity / 2 -> "low"
        totalHours <= capacity -> "medium"
        else -> "high"
    }

fun Task.label(): String = "$title=${hours}h"

val team = "platform"
var sprintDays = 5
val focusRatio = 0.75
val capacity = sprintCapacity(days = sprintDays, focusRatio = focusRatio)
val rawInputs = listOf(
    TaskInput("review API boundary", "3"),
    TaskInput(null, "4", urgent = true),
    TaskInput("fix null edge", "later", urgent = true),
    TaskInput("write migration notes", "2"),
)

val accepted = mutableListOf<Task>()
val rejected = mutableListOf<String>()

for ((index, input) in rawInputs.withIndex()) {
    val result = parseHours(input.hoursText).fold(
        onSuccess = { hours ->
            val tags = buildList {
                add("syntax")
                if (input.urgent) add("urgent")
                if (hours <= 2) add("small")
            }
            ParseResult.Accepted(
                Task(
                    title = normalizeTitle(input.title),
                    hours = hours,
                    urgent = input.urgent,
                    tags = tags,
                )
            )
        },
        onFailure = { error ->
            ParseResult.Rejected(
                source = "row ${index + 1}",
                reason = error.message ?: "unknown error",
            )
        },
    )

    when (result) {
        is ParseResult.Accepted -> accepted += result.task
        is ParseResult.Rejected -> rejected += "${result.source}: ${result.reason}"
    }
}

val totalHours = accepted.sumOf { it.hours }
val tagHours: Map<String, Int> = accepted
    .flatMap { task -> task.tags.map { tag -> tag to task.hours } }
    .groupBy(keySelector = { it.first }, valueTransform = { it.second })
    .mapValues { (_, hours) -> hours.sum() }

val report = StringBuilder().apply {
    appendLine("team=$team days=$sprintDays capacity=${capacity}h")
    appendLine("tasks=${accepted.size} total=${totalHours}h risk=${riskLabel(totalHours, capacity)}")
    appendLine("tagHours=$tagHours")
}.toString().trim()

println(report)

for ((index, task) in accepted.withIndex()) {
    if (task.urgent || index == 0) {
        println("for[$index] ${task.label()} tags=${task.tags.joinToString("|")}")
    }
}

val summary = accepted
    .filter { it.hours >= 2 }
    .joinToString { it.label() }
    .ifBlank { "none" }

val maybeOwner: String? = if (accepted.any { it.urgent }) team else null
val ownerLabel = maybeOwner?.let { "owner=${it.uppercase()}" } ?: "owner=unassigned"

val polished = accepted
    .also { println("largest=${it.maxByOrNull { task -> task.hours }?.label() ?: "none"}") }
    .map { task ->
        task.copy(title = task.title.replaceFirstChar { char -> char.uppercase() })
    }

val finalLine = run {
    val failures = rejected.ifEmpty { listOf("none") }.joinToString("; ")
    "summary=$summary | rejected=$failures | $ownerLabel"
}

println(finalLine)
println(polished.joinToString(prefix = "polished=[", postfix = "]") { it.label() })
