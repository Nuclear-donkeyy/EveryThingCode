data class Course(val name: String, val minutes: Int)

val courses = listOf(Course("null safety", 20), Course("coroutines", 30))
println("total minutes = ${courses.sumOf { it.minutes }}")
