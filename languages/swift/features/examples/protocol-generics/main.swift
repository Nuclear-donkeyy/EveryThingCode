protocol Scorable {
    var title: String { get }
    var score: Int { get }
}

struct TaskCard: Scorable {
    let title: String
    let score: Int
    let owner: String
}

struct Lesson: Scorable {
    let title: String
    let score: Int
    let durationMinutes: Int
}

extension Array where Element: Scorable {
    var averageScore: Double {
        guard !isEmpty else { return 0 }
        let total = reduce(0) { partial, item in partial + item.score }
        return Double(total) / Double(count)
    }
}

func topItem<T: Scorable>(from items: [T]) -> T? {
    items.max { left, right in left.score < right.score }
}

let tasks = [
    TaskCard(title: "Fix login flow", score: 8, owner: "Mina"),
    TaskCard(title: "Write release notes", score: 5, owner: "Kai"),
    TaskCard(title: "Audit payment logs", score: 9, owner: "Rui")
]

let lessons = [
    Lesson(title: "Optional basics", score: 7, durationMinutes: 18),
    Lesson(title: "Actor isolation", score: 10, durationMinutes: 25)
]

if let task = topItem(from: tasks) {
    print("Top task:", task.title, "owner:", task.owner)
}

if let lesson = topItem(from: lessons) {
    print("Top lesson:", lesson.title, "minutes:", lesson.durationMinutes)
}

print("Average task score:", tasks.averageScore)
