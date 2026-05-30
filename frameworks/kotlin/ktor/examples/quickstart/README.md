# Ktor quickstart

这是一个最小但真实的 Ktor JSON API 项目。它使用 Gradle Kotlin DSL、Ktor Netty、ContentNegotiation、kotlinx.serialization、Routing 和 Ktor test host，围绕“任务列表”展示服务端应用的核心结构。

## 目标

完成本案例后，你应该能：

- 用 `embeddedServer(Netty, ...)` 启动一个 Ktor 服务。
- 在 `Application.taskModule()` 中安装插件并注册路由。
- 使用 `ContentNegotiation` 和 `kotlinx.serialization` 输出 JSON。
- 编写 suspend route handler，理解请求在协程中的执行方式。
- 把 handler 与业务 store 分开，避免业务层依赖 Ktor。
- 使用 `testApplication` 编写不占用端口的 HTTP 测试。

## 学习重点

重点观察 `Application.kt`。它没有把所有逻辑塞进 `main`，而是把应用组合拆成 `taskModule(store)`。这样生产入口可以使用默认 store，测试可以传入自己的 store；插件安装、路由注册和业务依赖的边界也更清楚。

另一个重点是 JSON 生命周期。`call.receive<CreateTaskRequest>()` 把请求体反序列化为 Kotlin 数据类，`call.respond(task)` 再把数据类序列化成 JSON。这个过程只有在安装 `ContentNegotiation { json() }` 后才会发生。

## 工程结构

```text
.
├── build.gradle.kts
├── settings.gradle.kts
└── src/
    ├── main/kotlin/dev/everythingcode/ktor/
    │   ├── Application.kt  # 启动入口、插件安装、路由注册
    │   ├── Task.kt         # 可序列化 DTO 与领域对象
    │   └── TaskStore.kt    # 内存 repository，使用 Mutex 保护状态
    └── test/kotlin/dev/everythingcode/ktor/
        └── ApplicationTest.kt  # 使用 testApplication 验证 HTTP 行为
```

真实项目建议继续拆出 `routes/`、`service/`、`repository/`、`config/` 和 `plugins/`。本案例保持文件少，是为了让框架生命周期更容易被看见。

## 运行前提

- JDK 25 LTS 或兼容的现代 JDK。
- Gradle 8.14+，或使用 IDE 自带 Gradle 运行。
- 首次运行需要联网下载 Kotlin、Ktor、kotlinx.serialization 和测试依赖。
- 本仓库版本基线：Kotlin 2.3.21、Ktor 3.5.0，均为 latest stable，无官方 LTS。

## 运行

先运行测试，确认路由和 JSON 序列化正常：

```bash
gradle test
```

启动服务：

```bash
gradle run
```

另开终端请求接口：

```bash
curl -s http://localhost:8080/api/health
curl -s http://localhost:8080/api/tasks
curl -s -X POST http://localhost:8080/api/tasks -H 'Content-Type: application/json' -d '{"title":"learn Ktor plugins"}'
curl -s -X PATCH http://localhost:8080/api/tasks/1/done
```

## 预期输出

`gradle test` 应通过 `ApplicationTest` 中的 HTTP 测试。

`GET /api/health` 返回：

```json
{"status":"ok"}
```

`GET /api/tasks` 初始返回一个任务数组。`POST /api/tasks` 返回 `201 Created` 和新任务 JSON；title 为空时返回 `400 Bad Request`。`PATCH /api/tasks/1/done` 会把任务标记为完成，找不到 id 时返回 `404 Not Found`。

## 代码讲解

`Application.kt` 中的 `main` 只负责读取端口并启动 Netty engine。真正的应用组合在 `fun Application.taskModule(store: TaskStore = TaskStore())` 中完成，这让启动逻辑、插件注册和测试替换更容易。

`install(ContentNegotiation) { json(...) }` 注册 JSON 能力。没有这个插件时，Ktor 不知道如何把请求体变成 `CreateTaskRequest`，也不知道如何把 `Task` 写成 JSON。

`routing { route("/api") { ... } }` 是 Ktor 的 Routing DSL。`get`、`post`、`patch` 分别对应 HTTP 方法。handler 可以直接调用 suspend 函数，因此后续替换成数据库或 HTTP client 时不需要改变路由形状。

`Task.kt` 使用 `@Serializable` 标注响应和请求类型。Kotlin 数据类天然适合 DTO：字段不可变、构造清晰、序列化插件能在编译期生成元数据。

`TaskStore.kt` 使用 `Mutex.withLock` 保护内存列表。Ktor 多请求并发时，多个协程可能同时读写 store；即使是教学项目，也应该让并发边界显式。

`ApplicationTest.kt` 使用 `testApplication`，在测试内安装同一个 `taskModule`。测试 client 像真实 HTTP 客户端一样请求 `/api/tasks`，但整个过程在内存中完成，不需要启动端口。

## 延伸练习

- 增加 `GET /api/tasks/{id}`，并在找不到任务时返回统一错误 JSON。
- 把 `TaskStore` 抽成接口，再实现一个 Exposed/PostgreSQL repository。
- 增加 `StatusPages` 插件，把校验失败、找不到资源和未知异常统一映射为错误响应。

## 验收

完成后你应该能说明：

- Ktor 插件、Routing 和 handler 分别负责什么。
- 为什么 `ContentNegotiation` 是 JSON API 的关键插件。
- suspend handler 与协程并发对数据访问有什么影响。
- 如何用 `testApplication` 测试 Ktor 应用，而不启动真实服务器。
