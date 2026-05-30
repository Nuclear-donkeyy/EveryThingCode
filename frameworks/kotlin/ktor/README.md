# Ktor

Ktor 是 JetBrains 主导的 Kotlin-first HTTP 框架。它既可以写服务端，也可以写客户端；本章节先聚焦服务端，因为服务端能集中展示 Kotlin DSL、协程、插件式应用、路由、序列化和测试模型。

## 核心定位

Ktor 解决的是“用 Kotlin 原生方式组合 HTTP 应用”的问题。它提供 application engine、插件系统、Routing DSL、请求/响应 API、内容协商、认证、状态页、CORS、WebSocket、测试引擎等能力，让你可以从一个很小的 API 开始，按需加功能。

Ktor 不试图成为 Spring Boot 式的大型企业平台。它不会默认给你 ORM、迁移、复杂依赖注入容器、后台任务系统或全套运维面板。它更像一组可组合的 HTTP building blocks：你负责清楚地划分业务层、数据层和配置层，Ktor 负责把请求送到正确的位置。

## 设计思想

Ktor 的第一关键词是插件。应用能力通过 `install(...)` 注册，例如 `ContentNegotiation` 负责 JSON 序列化，`CallLogging` 负责请求日志，`StatusPages` 负责异常到响应的映射。插件让应用保持显式：没有安装的能力不会隐式生效。

第二关键词是 Routing DSL。`routing { route("/api") { get("/tasks") { ... } } }` 把 HTTP 方法、路径和处理逻辑放在一个 Kotlin DSL 中。DSL 不是魔法，而是 Kotlin 的 lambda with receiver、扩展函数和类型推断共同形成的可读结构。

第三关键词是协程。Ktor 的 handler 天然运行在 suspend 环境中，适合调用数据库、HTTP client、队列或文件 IO。你不需要为每个请求手动创建线程，也不要在 handler 中阻塞线程；真实项目应优先使用 suspend API，借助结构化并发让取消和超时自然传播。

第四关键词是薄框架边界。Ktor handler 可以访问 `ApplicationCall`，但业务服务最好接收普通参数或 `CoroutineContext`/`context`，不要让领域模型依赖 Ktor 类型。这样将来把业务迁移到 CLI、批处理或消息消费入口时，核心逻辑仍然能复用。

## 架构模型

一个典型 Ktor 服务端项目可以分成五层：

- `main` 或 `EngineMain`：启动 Netty/CIO 等 engine，读取端口和环境配置。
- `Application.module`：安装插件，装配依赖，注册路由，是应用组合入口。
- Routing：把 HTTP 方法和路径映射到 handler，负责解析请求、调用业务、写响应。
- Service/Repository：承载业务规则和数据访问，尽量不依赖 Ktor。
- Tests：使用 `testApplication` 在内存中启动 Ktor 应用，直接发 HTTP 请求验证路由和序列化。

本仓库 quickstart 采用显式 `embeddedServer(Netty, ...)` 启动。`Application.taskModule(store)` 负责安装 JSON 插件并注册 `/api/tasks` 路由，`TaskStore` 作为内存 repository，测试通过 Ktor client 调用应用，不启动真实端口。

## 请求/执行生命周期

一次 HTTP 请求进入 Ktor 后，先被 engine 接收并转换成 `ApplicationCall`。随后请求穿过已安装的插件管线，例如日志插件记录请求、内容协商插件准备序列化能力、异常处理插件捕获后续阶段抛出的异常。

进入 Routing 阶段后，Ktor 根据 method 和 path 选择匹配的 route。匹配成功后执行对应 suspend handler。handler 读取路径参数、查询参数或请求体，调用业务服务，然后使用 `call.respond(...)` 写出 Kotlin 对象。安装了 JSON ContentNegotiation 后，对象会被序列化为 JSON 响应。

如果 handler 抛出异常，`StatusPages` 这类插件可以把异常转换成统一错误响应。如果客户端取消请求，协程取消会沿着 suspend 调用传播；这也是 Ktor 适合异步 IO 的原因之一。

## 工程结构

quickstart 的目录结构如下：

```text
examples/quickstart/
├── build.gradle.kts
├── settings.gradle.kts
└── src/
    ├── main/kotlin/dev/everythingcode/ktor/
    │   ├── Application.kt
    │   ├── Task.kt
    │   └── TaskStore.kt
    └── test/kotlin/dev/everythingcode/ktor/
        └── ApplicationTest.kt
```

真实项目可以继续扩展为 `plugins/`、`routes/`、`service/`、`repository/`、`config/`、`observability/` 等目录。边界原则很简单：Ktor 相关代码留在入口和 HTTP 层，业务规则放到普通 Kotlin 类或函数，数据访问通过接口隔离。

## 配置方式

Ktor 支持代码配置、配置文件和环境变量。小项目可以直接在 `main` 中读取 `System.getenv("PORT")`，再传给 `embeddedServer`。更完整的项目可以使用 `application.conf`、YAML 配置或框架提供的 environment config，再由 `Application.module` 读取。

Gradle 负责构建配置：Kotlin 插件版本、Ktor 版本、应用入口、测试依赖都在 `build.gradle.kts` 中声明。运行时配置和构建配置要分开：端口、数据库地址、密钥属于运行时；Ktor/Kotlin 依赖版本属于构建时。

## 模块与依赖管理

Ktor 自身通过插件组织能力，业务代码通常通过函数参数或轻量 DI 组织依赖。quickstart 中 `taskModule(store: TaskStore = TaskStore())` 展示了最小方式：测试可以传入自己的 store，生产入口使用默认 store。

当项目变大时，可以把依赖装配封装成 `createAppServices(config)`，再把服务传给路由注册函数。需要 DI 容器时，可以接入 Koin、Kodein 或 Spring，但不要为了一个简单 API 过早引入容器。Ktor 的优势之一正是让依赖关系保持可见。

## 数据访问

本案例使用内存 `TaskStore`，它用 `Mutex` 保护可变列表，目的是让读者先看清请求、路由和 JSON 序列化，不被数据库配置分散注意力。

真实项目常见路径包括：用 Exposed 编写 SQL DSL；用 jOOQ 生成类型安全查询；在 Spring 生态项目中使用 Spring Data；或者直接使用数据库驱动与连接池。无论选择哪条路径，推荐让 handler 调用 service，service 调用 repository，repository 隐藏具体数据库实现。

## 测试方式

Ktor 的 `testApplication` 可以在测试进程里启动应用管线，然后用内置 client 发送 HTTP 请求。这类测试比纯单元测试更接近真实请求生命周期，但不需要监听端口，适合验证路由、状态码、JSON 序列化、错误处理和插件配置。

业务服务仍应保留普通单元测试。对数据库或外部服务，可以使用 Testcontainers、嵌入式数据库或 fake repository。测试分层越清楚，Ktor handler 就越薄，业务规则也越容易复用。

## 部署方式

JVM 服务端常见部署方式有三种：直接运行 Gradle application 产物、打包 fat jar 放入容器、或构建原生镜像/云平台镜像。Ktor 默认常与 Netty engine 一起部署，监听端口由环境变量注入，日志输出到 stdout，健康检查暴露为 HTTP endpoint。

生产环境还需要补充超时、优雅停机、结构化日志、指标、追踪、统一错误响应、CORS、安全头和配置管理。这些能力都可以通过 Ktor 插件或应用层中间件逐步加入。

## 适用场景与取舍

优先选择 Ktor 的场景：Kotlin-first 团队、轻量 JSON API、BFF、内部工具、需要协程友好的异步 IO、希望框架边界清晰的服务。它的启动和心智模型比大型容器轻，代码接近 Kotlin 本身。

需要谨慎的场景：团队强依赖 Spring 企业生态、需要大量现成集成、组织已经有统一 Spring Boot 运维规范，或项目成员尚未熟悉协程取消/阻塞问题。此时 Spring Boot Kotlin 可能更稳，但 Ktor 仍适合作为学习 Kotlin 后端思想的入口。

## 案例索引

- [quickstart](examples/quickstart/)：任务 JSON API，包含 Gradle Kotlin DSL、Ktor Netty 服务端、ContentNegotiation、Routing、内存 store 和 HTTP 测试。

## 版本来源

- Kotlin 版本基线：2.3.21，策略为 latest stable，无官方 LTS。
- Ktor 版本基线：3.5.0，策略为 latest stable，无官方 LTS。
- 官方来源：https://kotlinlang.org/docs/releases.html
- 官方来源：https://ktor.io/docs/releases.html
- 校验日期：2026-05-30
