import Swift

let language = "Swift"
let dailyLimit = 3
var completedCount = 0

enum Status: Hashable {
    case todo
    case doing
    case done

    var label: String {
        switch self {
        case .todo:
            return "todo"
        case .doing:
            return "doing"
        case .done:
            return "done"
        }
    }
}

enum TaskError: Error {
    case missingName
    case negativeHours(Int)
}

protocol Summarizable {
    var summary: String { get }
}

struct Task: Summarizable {
    let name: String
    var hours: Int
    var status: Status

    var summary: String {
        "\(name) - \(status.label), \(hours)h"
    }

    mutating func finish() {
        status = .done
    }
}

func makeTask(name: String?, hours: Int, status: Status = .todo) throws -> Task {
    guard let name, !name.isEmpty else {
        throw TaskError.missingName
    }

    if hours < 0 {
        throw TaskError.negativeHours(hours)
    }

    return Task(name: name, hours: hours, status: status)
}

func printSummary(_ item: Summarizable) {
    print("- \(item.summary)")
}

let rawTasks: [(name: String?, hours: Int, status: Status)] = [
    ("Read guide", 1, .done),
    ("Write sample", 2, .doing),
    (nil, 1, .todo),
    ("Review", -1, .todo),
    ("Ship", 2, .todo),
]

print("\(language) syntax tour")
print("Daily limit: \(dailyLimit) tasks")

var tasks: [Task] = []

for raw in rawTasks {
    do {
        let task = try makeTask(name: raw.name, hours: raw.hours, status: raw.status)
        tasks.append(task)
    } catch TaskError.missingName {
        print("Skipped a task without a name")
    } catch TaskError.negativeHours(let hours) {
        print("Skipped a task with invalid hours: \(hours)")
    } catch {
        print("Skipped a task: \(error)")
    }
}

for index in tasks.indices {
    if tasks[index].status == .done {
        completedCount += 1
    } else if tasks[index].hours <= 2 && completedCount < dailyLimit {
        tasks[index].finish()
        completedCount += 1
    }
}

var counts: [Status: Int] = [:]

for task in tasks {
    counts[task.status, default: 0] += 1
}

print("\nTasks")
for task in tasks {
    printSummary(task)
}

print("\nStatus counts")
for status in [Status.todo, .doing, .done] {
    let count = counts[status, default: 0]
    print("\(status.label): \(count)")
}

let maybeFirstTask: Task? = tasks.first
if let first = maybeFirstTask {
    print("\nFirst task: \(first.name)")
}

let savedResult: Result<Task, Error> = Result {
    try makeTask(name: "Archive", hours: 1, status: .done)
}

switch savedResult {
case .success(let task):
    print("Result saved: \(task.summary)")
case .failure(let error):
    print("Result failed: \(error)")
}
