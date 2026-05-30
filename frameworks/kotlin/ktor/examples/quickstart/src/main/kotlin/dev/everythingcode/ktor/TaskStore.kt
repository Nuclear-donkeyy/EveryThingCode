package dev.everythingcode.ktor

import kotlinx.coroutines.sync.Mutex
import kotlinx.coroutines.sync.withLock

class TaskStore(initialTasks: List<Task> = listOf(Task(id = 1, title = "Read Ktor routing"))) {
    private val mutex = Mutex()
    private val tasks = initialTasks.toMutableList()
    private var nextId = (initialTasks.maxOfOrNull { it.id } ?: 0) + 1

    suspend fun list(): List<Task> = mutex.withLock {
        tasks.toList()
    }

    suspend fun create(title: String): Task = mutex.withLock {
        val normalizedTitle = title.trim()
        require(normalizedTitle.isNotEmpty()) { "title must not be blank" }

        val task = Task(id = nextId++, title = normalizedTitle)
        tasks += task
        task
    }

    suspend fun markDone(id: Int): Task? = mutex.withLock {
        val index = tasks.indexOfFirst { it.id == id }
        if (index == -1) {
            null
        } else {
            val updated = tasks[index].copy(done = true)
            tasks[index] = updated
            updated
        }
    }
}
