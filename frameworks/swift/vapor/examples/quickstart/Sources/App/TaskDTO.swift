import Vapor

struct TaskResponse: Content {
    let id: Int
    let title: String
    let done: Bool
}

struct CreateTaskRequest: Content {
    let title: String
}
