# Vapor quickstart

这个案例是一个最小 Vapor JSON API。它用内存 repository 保存任务，重点展示 Router、`Request`/`Response`、Middleware、DTO 编解码和 async/await handler，而不是先引入数据库配置。

## 目标

完成后你应该能说明：Vapor 应用如何从 `Application` 启动，路由如何匹配请求，middleware 如何包裹 handler，handler 如何从 `Request` 解码 JSON 并返回响应，以及将来如何把内存 repository 替换为 Fluent 数据库模型。

## 学习重点

- Router：用 `app.grouped("api", "tasks")` 建立 API 边界，用 `get`、`post`、`delete` 绑定 HTTP 方法。
- Request/Response：从 `req.content.decode` 读取 JSON body，用 `Response(status:)` 返回显式状态码。
- Middleware：`RequestIDMiddleware` 给每个响应附加 `X-Request-ID`，展示横切逻辑不应写进每个 handler。
- async/await：handler 使用 `async throws`，业务调用看起来像同步代码，但仍能承载异步 I/O。
- 数据边界：`TaskRepository` 当前是内存实现，真实项目可替换为 Fluent repository。

## 这个案例解决什么问题

这个案例把一个最小任务 API 拆成几条清晰边界，目的是让读者看到 Vapor 解决的不是“少写几行 socket 代码”，而是服务端工程中最容易膨胀的几类复杂度。

第一，路由不再是手写 if/else。`GET /health`、`GET /api/tasks`、`POST /api/tasks`、`DELETE /api/tasks/:id` 都通过 `Application` 和 route group 声明，URL 形状、HTTP method 和 handler 绑定在同一处。将来如果要给 `/api/tasks` 加认证或版本前缀，可以在 group 层处理。

第二，请求和响应不再是散落的 JSON 字符串。`CreateTaskRequest` 与 `TaskResponse` 遵守 `Content`，因此 Vapor 能从 body 解码输入，也能把 Swift 值编码成 JSON。handler 只处理类型化数据；状态码、header、body 的协议细节由 `Response` 和 content encoder 统一处理。

第三，横切逻辑不再污染业务 handler。`RequestIDMiddleware` 只关心请求 ID，它不关心任务如何创建或删除。认证、CORS、日志、限流也可以用同样方式加入 pipeline，避免每个路由复制同一段基础设施代码。

第四，并发访问不再依赖手工锁。`TaskRepository` 用 `actor` 包住内存数组，配合 `async` handler 表达“这里可能跨并发边界”。真实项目换成 Fluent 时，这个边界可以保留，内部实现从内存数组改成数据库 query 和 migration。

## 工程结构

```text
.
├── Package.swift
└── Sources/App
    ├── TaskDTO.swift
    ├── TaskRepository.swift
    └── main.swift
```

- `Package.swift`：声明 Vapor 依赖和 `App` executable target。
- `main.swift`：创建 `Application`，注册 middleware 和路由，然后启动服务。
- `TaskDTO.swift`：定义请求与响应 DTO，避免直接暴露数据库模型。
- `TaskRepository.swift`：内存数据访问层，集中处理新增、列表、删除。

## 思想拆解

`Package.swift` 解决的是依赖与构建边界问题。`swift-tools-version: 6.3` 固定本案例使用的 Swift Package manifest 语义；`.package(url: "https://github.com/vapor/vapor.git", from: "4.0.0")` 声明 Vapor 依赖；`.product(name: "Vapor", package: "vapor")` 让 `App` target 获得 `Application`、`Request`、`Response`、`Content`、`Middleware` 等 API。真实项目可以继续拆出 `Domain`、`Database`、`Web` 等 target，让纯业务代码不直接依赖 Vapor。

`main.swift` 解决的是运行期组装问题。`Application.make(.detect())` 根据命令行和环境创建服务进程；`app.middleware.use(RequestIDMiddleware())` 注册横切逻辑；`app.get("health")` 提供部署和监控常用的健康检查；`let tasks = app.grouped("api", "tasks")` 把任务 API 放到同一个路由边界；`try await app.execute()` 交给 Vapor 处理命令行、serve 生命周期和优雅退出。

`RequestIDMiddleware` 展示 Middleware 的价值。它实现 `AsyncMiddleware`，先从请求 header 读取 `X-Request-ID`，没有就生成一个 UUID，然后调用 `next.respond(to:)` 把请求交给后续 middleware 或最终 handler，最后把 request id 写回响应 header。这条链路说明 middleware 的职责是“包裹请求”，而不是替代业务代码。

`TaskDTO.swift` 解决的是 HTTP 契约问题。`CreateTaskRequest` 是客户端能提交的输入，`TaskResponse` 是服务端愿意返回的输出，两者不一定等同于数据库表结构。接入 Fluent 后，通常会新增 `TaskModel: Model`，再把 model 映射成 `TaskResponse`，避免把数据库字段、关系和内部状态直接暴露给 API 调用方。

`TaskRepository.swift` 解决的是数据边界问题。quickstart 用 `actor` 和内存数组保留简单性，同时让 handler 通过 `await repository.list()`、`await repository.create(...)`、`await repository.delete(...)` 调用业务数据能力。换成 Fluent 时，可以保留方法形状，把实现改成 `TaskModel.query(on: req.db)`、`model.save(on: req.db)` 和 migration。

## 运行前提

- Swift 6.3.x 或兼容当前仓库 `versions.yaml` 的 latest stable Swift。
- 能访问 Swift Package registry/GitHub 下载 Vapor 依赖。
- 本案例默认监听 `127.0.0.1:8080`，如端口被占用可通过命令行参数调整。

## 运行

```bash
swift build
```

启动服务：

```bash
swift run App serve --hostname 127.0.0.1 --port 8080
```

另开终端验证 API：

```bash
curl -s http://127.0.0.1:8080/api/tasks
curl -s -X POST http://127.0.0.1:8080/api/tasks -H 'Content-Type: application/json' -d '{"title":"Read Vapor routes"}'
curl -i -X DELETE http://127.0.0.1:8080/api/tasks/1
```

## 预期输出

启动后终端会显示 Vapor server 监听地址。访问 `GET /api/tasks` 会得到 JSON 数组；`POST /api/tasks` 会返回新建任务，状态码为 `201 Created`；所有响应都会带有 `X-Request-ID` header，说明请求经过了 middleware。

示例响应：

```json
[
  {
    "id": 1,
    "title": "Read Vapor routes",
    "done": false
  }
]
```

## 代码讲解

`main.swift` 是最小 Vapor 应用的入口。`Application.make(.detect())` 根据环境创建运行实例，`defer { app.shutdown() }` 保证服务退出时释放资源。`app.middleware.use` 注册中间件，`app.grouped("api", "tasks")` 创建统一前缀的路由组。

`GET /api/tasks` 返回 repository 中的全部任务。`POST /api/tasks` 使用 `req.content.decode(CreateTaskRequest.self)` 解码 JSON body，把 HTTP 输入转换成 Swift 类型。`DELETE /api/tasks/:id` 演示路径参数和显式状态码。

`RequestIDMiddleware` 实现 `AsyncMiddleware`。它在请求进入 handler 前读取或生成 request id，在响应返回时写入 header。认证、限流、日志、CORS 等逻辑也可以用同样方式实现。

`TaskRepository` 当前用 `actor` 保证内存数据在并发访问时安全。接入 Fluent 时，可以保留 repository 接口，把 `list`、`create`、`delete` 的实现改成数据库查询和迁移。

## 与完整 Vapor 项目的对应关系

quickstart 为了可读性把所有路由写在 `main.swift` 中。真实项目通常会把启动与路由拆开：`configure.swift` 注册 middleware、数据库、migration 和外部 client；`routes.swift` 调用各 controller 注册路由；`Controllers/TaskController.swift` 放 HTTP handler；`Models/Task.swift` 放 Fluent model；`Migrations/CreateTask.swift` 放表结构变更；`Services/TaskService.swift` 或 `Repositories/TaskRepository.swift` 放业务和数据访问。

接入数据库时，`Package.swift` 会增加 `fluent`、`fluent-postgres-driver` 或 `fluent-sqlite-driver`；`configure` 中会注册 `app.databases.use(...)`；启动或部署流程会执行 migration。这样 Vapor 的三条边界会更清楚：HTTP 层负责协议，Fluent 层负责持久化，service/repository 层负责业务规则。

部署时，这个案例可以用 `swift run App serve` 学习生命周期；生产环境则应使用 `swift build -c release` 生成 release 二进制，设置 `PORT`、数据库 URL、secret、日志级别，并在 Linux 容器或进程管理器里运行。健康检查 `/health`、请求 ID header 和结构化日志会成为排障入口。

## 延伸练习

- 增加 `PATCH /api/tasks/:id`，用请求体切换 `done` 或修改标题。
- 使用 Fluent + SQLite/PostgreSQL 替换内存 repository，并增加 migration。
- 增加 API key middleware，让写操作必须带指定 header。

## 验收

- 能说明一次请求从 middleware 到 router 再到 handler 的执行顺序。
- 能新增一个路由，并正确处理 JSON body、路径参数和错误响应。
- 能指出 DTO、repository、middleware 分别解决什么问题。
- 能描述把内存数据换成 Fluent 时需要新增哪些文件和配置。
