import Foundation

actor TaskRepository {
    private var nextID = 3
    private var tasks: [TaskResponse] = [
        TaskResponse(id: 1, title: "Read Vapor routes", done: false),
        TaskResponse(id: 2, title: "Move storage behind a repository", done: true)
    ]

    func list() -> [TaskResponse] {
        tasks
    }

    func create(title: String) -> TaskResponse {
        let trimmed = title.trimmingCharacters(in: .whitespacesAndNewlines)
        let task = TaskResponse(id: nextID, title: trimmed, done: false)
        nextID += 1
        tasks.append(task)
        return task
    }

    func delete(id: Int) -> Bool {
        let originalCount = tasks.count
        tasks.removeAll { $0.id == id }
        return tasks.count != originalCount
    }
}
