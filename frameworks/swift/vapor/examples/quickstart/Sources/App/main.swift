import Vapor

struct RequestIDMiddleware: AsyncMiddleware {
    func respond(to request: Request, chainingTo next: AsyncResponder) async throws -> Response {
        let requestID = request.headers.first(name: "X-Request-ID") ?? UUID().uuidString
        let response = try await next.respond(to: request)
        response.headers.replaceOrAdd(name: "X-Request-ID", value: requestID)
        return response
    }
}

let app = try await Application.make(.detect())
defer {
    app.shutdown()
}

let repository = TaskRepository()

app.middleware.use(RequestIDMiddleware())

app.get("health") { _ in
    ["status": "ok"]
}

let tasks = app.grouped("api", "tasks")

tasks.get { _ async -> [TaskResponse] in
    await repository.list()
}

tasks.post { req async throws -> Response in
    let input = try req.content.decode(CreateTaskRequest.self)
    guard !input.title.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty else {
        throw Abort(.badRequest, reason: "title is required")
    }

    let created = await repository.create(title: input.title)
    let response = Response(status: .created)
    try response.content.encode(created)
    return response
}

tasks.delete(":id") { req async throws -> HTTPStatus in
    guard let id = req.parameters.get("id", as: Int.self) else {
        throw Abort(.badRequest, reason: "id must be an integer")
    }

    return await repository.delete(id: id) ? .noContent : .notFound
}

try await app.execute()
