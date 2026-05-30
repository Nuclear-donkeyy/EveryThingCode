# Ktor

Ktor 是 JetBrains 主导的 Kotlin-first HTTP 框架。它既可以写服务端，也可以写客户端；本章节先聚焦服务端，因为服务端能集中展示 Kotlin DSL、协程、插件式应用、路由、序列化和测试模型。

## 核心定位

Ktor 解决的是“用 Kotlin 原生方式组合 HTTP 应用”的问题。它提供 application engine、插件系统、Routing DSL、请求/响应 API、内容协商、认证、状态页、CORS、WebSocket、测试引擎等能力，让你可以从一个很小的 API 开始，按需加功能。

Ktor 不试图成为 Spring Boot 式的大型企业平台。它不会默认给你 ORM、迁移、复杂依赖注入容器、后台任务系统或全套运维面板。它更像一组可组合的 HTTP building blocks：你负责清楚地划分业务层、数据层和配置层，Ktor 负责把请求送到正确的位置。

## 解决的问题

如果只用 JVM 的底层 HTTP 能力或一个很薄的 Servlet/Netty 封装来写 Kotlin 服务端，常见问题不是“不能写”，而是很多基础设施会迅速散落到业务代码里：

- 请求生命周期不集中：启动 server、解析路径、读取请求体、写响应、处理异常、打日志经常分散在不同 helper 中，读者很难看出一个请求到底经过了哪些阶段。
- 协程边界不明确：Kotlin 服务端通常需要调用数据库、RPC、HTTP client 或消息系统。如果 handler 只是普通阻塞函数，就容易把协程优势浪费掉；如果自己管理 coroutine scope，又容易出现取消、超时和资源释放不一致。
- 路由组织缺少结构：小项目可以用一堆 `if path == ...` 或函数表，大项目会出现路径前缀重复、HTTP 方法混乱、参数解析和业务调用混在一起的问题。
- JSON 读写重复且容易漂移：手写反序列化、校验、响应头和错误格式，会让 DTO、API 文档和实际响应慢慢不一致。
- 横切能力缺少统一入口：日志、认证、CORS、错误映射、压缩、指标、内容协商等能力如果靠每个 handler 手写，很快就会变成重复代码。
- 测试需要真实端口：如果框架没有内存测试宿主，HTTP 行为测试就要先启动服务、占用端口、处理并发清理，反馈慢且不稳定。
- 框架边界过重或过隐式：有些平台提供很多默认能力，但初学者不容易看见依赖从哪里来、插件何时生效、请求如何进入业务层。

Ktor 的价值正在这里：它用 `Application` 作为应用组合入口，用 `Routing` 表达 URL 到 handler 的映射，用 `Plugin` 管理横切能力，用 `ContentNegotiation` 接管 JSON 协商，用 coroutine-friendly handler 承接异步 I/O，用 `testApplication` 在内存中测试完整请求链路。它解决的不是某一个单点问题，而是让 Kotlin 后端项目的 HTTP 入口、协程模型、序列化、插件管线和测试边界都保持显式。

## 设计思想

Ktor 的第一关键词是 `Application`。一个 Ktor 服务不是从某个巨大的默认容器开始，而是从 `Application.module` 或本仓库 quickstart 里的 `Application.taskModule(store)` 开始。这个函数就是应用装配图：安装哪些插件、暴露哪些路由、把哪些业务依赖交给 HTTP 层，都在这里可见。它解决的是“应用启动以后到底装了什么”的可理解性问题。

第二关键词是插件。应用能力通过 `install(...)` 注册，例如 `ContentNegotiation` 负责 JSON 序列化，`CallLogging` 负责请求日志，`StatusPages` 负责异常到响应的映射。插件让应用保持显式：没有安装的能力不会隐式生效。对教学尤其重要的是，插件把横切能力放进应用管线，而不是塞进每一个 route handler。

第三关键词是 Routing DSL。`routing { route("/api") { get("/tasks") { ... } } }` 把 HTTP 方法、路径和处理逻辑放在一个 Kotlin DSL 中。DSL 不是魔法，而是 Kotlin 的 lambda with receiver、扩展函数和类型推断共同形成的可读结构。它解决的是路由表和 handler 分离后难以追踪的问题：路径、方法、参数读取和业务调用在同一块结构化代码里完成。

第四关键词是内容协商。HTTP API 不是简单返回字符串，而是在客户端可接受内容、请求体格式、响应格式之间做协议选择。`ContentNegotiation { json(...) }` 告诉 Ktor：收到 JSON 时如何反序列化成 `CreateTaskRequest`，返回 `Task` 或 `ErrorResponse` 时如何序列化成 JSON。这样 handler 处理 Kotlin 对象，而不是反复处理原始字符串、header 和字节流。

第五关键词是协程。Ktor 的 handler 天然运行在 suspend 环境中，适合调用数据库、HTTP client、队列或文件 IO。你不需要为每个请求手动创建线程，也不要在 handler 中阻塞线程；真实项目应优先使用 suspend API，借助结构化并发让取消和超时自然传播。quickstart 的 `TaskStore` 把 `list/create/markDone` 设计成 suspend 函数，并用 `Mutex.withLock` 保护内存状态，就是为了让并发边界在最小案例中也能被看见。

第六关键词是测试宿主。`testApplication` 可以把同一个 `Application.taskModule(...)` 安装到内存中的测试环境，再用 Ktor client 发出 HTTP 请求。它不是只测函数调用，而是测路由匹配、插件配置、序列化和状态码；同时又不需要真实端口。这样测试和生产共享同一套应用装配，避免“测试通过但实际 server 装配不同”的问题。

最后一个关键词是薄框架边界。Ktor handler 可以访问 `ApplicationCall`，但业务服务最好接收普通参数或上下文对象，不要让领域模型依赖 Ktor 类型。这样将来把业务迁移到 CLI、批处理或消息消费入口时，核心逻辑仍然能复用。Ktor 的思想不是把一切都框架化，而是把 HTTP 入口框架化，把业务保持为普通 Kotlin。

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

- [core-ideas](examples/core-ideas/)：把上一节“解决的问题”和“设计思想”映射到 quickstart 的关键代码片段。
- [quickstart](examples/quickstart/)：任务 JSON API，包含 Gradle Kotlin DSL、Ktor Netty 服务端、ContentNegotiation、Routing、内存 store 和 HTTP 测试。

## 版本来源

- Kotlin 版本基线：2.3.21，策略为 latest stable，无官方 LTS。
- Ktor 版本基线：3.5.0，策略为 latest stable，无官方 LTS。
- 官方来源：https://kotlinlang.org/docs/releases.html
- 官方来源：https://ktor.io/docs/releases.html
- 校验日期：2026-05-30
