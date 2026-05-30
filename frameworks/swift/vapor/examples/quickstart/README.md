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
- `TaskRepository.swift`：内存数据访问层，集中处理新增、列表、完成、删除。

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

`main.swift` 是最小 Vapor 应用的入口。`Application(.detect())` 根据环境创建运行实例，`defer { app.shutdown() }` 保证服务退出时释放资源。`app.middleware.use` 注册中间件，`app.grouped("api", "tasks")` 创建统一前缀的路由组。

`GET /api/tasks` 返回 repository 中的全部任务。`POST /api/tasks` 使用 `req.content.decode(CreateTaskRequest.self)` 解码 JSON body，把 HTTP 输入转换成 Swift 类型。`DELETE /api/tasks/:id` 演示路径参数和显式状态码。

`RequestIDMiddleware` 实现 `AsyncMiddleware`。它在请求进入 handler 前读取或生成 request id，在响应返回时写入 header。认证、限流、日志、CORS 等逻辑也可以用同样方式实现。

`TaskRepository` 当前用 `actor` 保证内存数据在并发访问时安全。接入 Fluent 时，可以保留 repository 接口，把 `list`、`create`、`delete` 的实现改成数据库查询和迁移。

## 延伸练习

- 增加 `PATCH /api/tasks/:id`，用请求体切换 `done` 或修改标题。
- 使用 Fluent + SQLite/PostgreSQL 替换内存 repository，并增加 migration。
- 增加 API key middleware，让写操作必须带指定 header。

## 验收

- 能说明一次请求从 middleware 到 router 再到 handler 的执行顺序。
- 能新增一个路由，并正确处理 JSON body、路径参数和错误响应。
- 能指出 DTO、repository、middleware 分别解决什么问题。
- 能描述把内存数据换成 Fluent 时需要新增哪些文件和配置。
