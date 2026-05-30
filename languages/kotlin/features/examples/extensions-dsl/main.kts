data class Task(
    val title: String,
    val owner: String,
    val minutes: Int,
    val tags: List<String>,
)

class TaskBuilder(private val title: String) {
    var owner: String = "unassigned"
    var minutes: Int = 0
    private val tags = mutableListOf<String>()

    fun tag(value: String) {
        tags += value
    }

    fun build(): Task = Task(title, owner, minutes, tags.toList())
}

class Checklist {
    private val tasks = mutableListOf<Task>()

    fun task(title: String, configure: TaskBuilder.() -> Unit = {}) {
        val builder = TaskBuilder(title)
        builder.configure()
        tasks += builder.build()
    }

    fun build(): List<Task> = tasks.toList()
}

fun checklist(configure: Checklist.() -> Unit): List<Task> {
    val builder = Checklist()
    builder.configure()
    return builder.build()
}

fun List<Task>.ownedBy(name: String): List<Task> =
    filter { it.owner == name }

fun List<Task>.totalMinutes(): Int =
    sumOf { it.minutes }

val releaseChecklist = checklist {
    task("检查迁移脚本") {
        owner = "Lin"
        minutes = 25
        tag("database")
    }
    task("更新发布说明") {
        owner = "Mira"
        minutes = 15
        tag("docs")
    }
    task("回归空安全用例") {
        owner = "Lin"
        minutes = 20
        tag("test")
    }
}

println("Lin 的任务:")
releaseChecklist
    .ownedBy("Lin")
    .forEach { println("- ${it.title} (${it.minutes} min, tags=${it.tags.joinToString()})") }

println("总工作量: ${releaseChecklist.totalMinutes()} min")
