import Foundation

struct LearningTask: Identifiable, Equatable {
    let id: UUID
    var title: String
    var isDone: Bool

    init(id: UUID = UUID(), title: String, isDone: Bool = false) {
        self.id = id
        self.title = title
        self.isDone = isDone
    }
}

@Observable
final class TaskStore {
    var tasks: [LearningTask] = [
        LearningTask(title: "Read the SwiftUI view lifecycle"),
        LearningTask(title: "Extract state into a model"),
        LearningTask(title: "Replace memory data with SwiftData", isDone: true)
    ]

    var remainingCount: Int {
        tasks.filter { !$0.isDone }.count
    }

    func add(title: String) {
        let trimmed = title.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !trimmed.isEmpty else {
            return
        }

        tasks.insert(LearningTask(title: trimmed), at: 0)
    }

    func clearCompleted() {
        tasks.removeAll { $0.isDone }
    }
}
