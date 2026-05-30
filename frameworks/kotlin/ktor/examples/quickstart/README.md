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

这个案例刻意选择“任务列表 JSON API”，因为它足够小，但能暴露服务端框架必须解决的核心问题：如何启动 HTTP engine，如何组织路由，如何把 JSON 请求体变成 Kotlin 对象，如何把业务对象写回响应，如何处理并发状态，如何不启动真实端口就测试完整 HTTP 行为。

重点观察 `Application.kt`。它没有把所有逻辑塞进 `main`，而是把应用组合拆成 `taskModule(store)`。这样生产入口可以使用默认 store，测试可以传入自己的 store；插件安装、路由注册和业务依赖的边界也更清楚。这个函数对应 Ktor 的 `Application` 思想：应用能力不是凭空出现的，而是在入口处显式安装和装配。

第二个重点是 JSON 生命周期。`call.receive<CreateTaskRequest>()` 把请求体反序列化为 Kotlin 数据类，`call.respond(task)` 再把数据类序列化成 JSON。这个过程只有在安装 `ContentNegotiation { json() }` 后才会发生。Ktor 用插件解决“每个 handler 都手写 JSON 解析和响应 header”的重复劳动。

第三个重点是协程边界。route handler 可以调用 `TaskStore` 的 suspend 函数；`TaskStore` 内部用 `Mutex.withLock` 保护内存列表。这个设计展示了 Kotlin 服务端的关键取舍：HTTP 层是协程友好的，状态读写也要明确处理并发，而不是假设请求会串行执行。

第四个重点是测试方式。`ApplicationTest.kt` 使用 `testApplication` 安装同一个 `taskModule`，再用 Ktor client 发出请求。它验证的不是单个函数，而是 route 匹配、ContentNegotiation、状态码和响应体的组合结果，同时不占用端口。

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

`build.gradle.kts` 先定义了框架的边界。`kotlin("jvm")` 和 `kotlin("plugin.serialization")` 让项目具备 Kotlin/JVM 与 kotlinx.serialization 能力；`ktor-server-core` 提供应用、call、routing 等核心 API；`ktor-server-netty` 提供实际运行的 HTTP engine；`ktor-server-content-negotiation` 和 `ktor-serialization-kotlinx-json` 负责 JSON 协商；`ktor-server-test-host` 让测试可以在内存里跑完整应用。也就是说，Gradle 文件不是普通依赖清单，它对应了 Ktor “按需装配能力”的思想。

`Application.kt` 中的 `main` 只负责读取端口并启动 Netty engine。真正的应用组合在 `fun Application.taskModule(store: TaskStore = TaskStore())` 中完成，这让启动逻辑、插件注册和测试替换更容易。Ktor 在这里解决了启动入口和业务入口混在一起的问题：`main` 关心进程，`taskModule` 关心 HTTP 应用。

`install(ContentNegotiation) { json(...) }` 注册 JSON 能力。没有这个插件时，Ktor 不知道如何把请求体变成 `CreateTaskRequest`，也不知道如何把 `Task` 写成 JSON。

`routing { route("/api") { ... } }` 是 Ktor 的 Routing DSL。`get`、`post`、`patch` 分别对应 HTTP 方法，嵌套的 `route("/tasks")` 把同一资源放在同一个结构里。它解决的是手写路由表难以维护的问题：读者可以沿着 `/api/tasks` 看到列表、创建和完成任务的全部入口。

`post { ... }` 展示了请求处理链路。`call.receive<CreateTaskRequest>()` 从 HTTP 请求体进入 Kotlin 类型系统；`title.trim()` 是业务前的输入规范化；空标题返回 `400 Bad Request`；成功后调用 `store.create(title)`；最后 `call.respond(HttpStatusCode.Created, task)` 把 Kotlin 对象交给 JSON 插件。这个 handler 的意义在于展示边界：协议解析留在 HTTP 层，业务状态变化交给 store。

`patch("/{id}/done")` 展示了路径参数和错误响应。`call.parameters["id"]?.toIntOrNull()` 把 URL 中的字符串转换为业务需要的整数；转换失败返回 `400`，找不到任务返回 `404`，更新成功返回 `200` 和更新后的 `Task`。这说明 Ktor 不替你隐藏 HTTP 语义，而是让状态码和响应对象在 handler 中清楚呈现。

`Task.kt` 使用 `@Serializable` 标注响应和请求类型。Kotlin 数据类天然适合 DTO：字段不可变、构造清晰、序列化插件能在编译期生成元数据。

`TaskStore.kt` 使用 `Mutex.withLock` 保护内存列表。Ktor 多请求并发时，多个协程可能同时读写 store；即使是教学项目，也应该让并发边界显式。真实项目里这里通常会替换成数据库 repository，但 suspend 函数形状可以保留，route handler 不需要因为数据层从内存换成 PostgreSQL 或外部 HTTP 服务而大改。

`ApplicationTest.kt` 使用 `testApplication`，在测试内安装同一个 `taskModule`。测试 client 像真实 HTTP 客户端一样请求 `/api/tasks`，但整个过程在内存中完成，不需要启动端口。`createClient { install(ContentNegotiation) { json() } }` 还展示了 Ktor client 也可以复用插件思想：测试端同样用 JSON 插件把响应体转回 `Task`。

从完整链路看，一次 `POST /api/tasks` 会经过 Netty/test host、Ktor application pipeline、ContentNegotiation、Routing、suspend handler、`TaskStore`、再回到 `call.respond`。这就是 Ktor 要解决的问题：把 HTTP 入口的重复基础设施放进框架，把业务变化留在普通 Kotlin 代码里。

## 延伸练习

- 增加 `GET /api/tasks/{id}`，并在找不到任务时返回统一错误 JSON。
- 把 `TaskStore` 抽成接口，再实现一个 Exposed/PostgreSQL repository。
- 增加 `StatusPages` 插件，把校验失败、找不到资源和未知异常统一映射为错误响应。
- 增加 `CallLogging` 插件，观察请求日志如何作为插件进入管线，而不是散落在每个 handler。
- 为创建任务增加一个 service 层，让 route 只负责 HTTP，service 负责业务规则。

## 验收

完成后你应该能说明：

- Ktor 插件、Routing 和 handler 分别负责什么。
- 为什么 `ContentNegotiation` 是 JSON API 的关键插件。
- suspend handler 与协程并发对数据访问有什么影响。
- 如何用 `testApplication` 测试 Ktor 应用，而不启动真实服务器。
