# Vapor

Vapor 是 Swift 生态中最常用的服务端 Web 框架之一。它把 Swift 的类型系统、async/await、结构化并发和包管理带到 HTTP API 开发中，让开发者可以用接近 Apple 平台开发的语言体验构建后端服务。

## 核心定位

Vapor 主要解决服务端 Web 应用中的路由、请求/响应编解码、中间件、配置、日志、异步执行、数据库访问和部署问题。它适合 JSON API、后台服务、BFF、Webhook、轻量 Web 应用和需要 Swift 端到端共享模型的团队。

它不是一个“零抽象”的 HTTP 库，也不是只靠代码生成的 RPC 框架。Vapor 的价值在于提供一套完整但仍然可组合的 Web 工程骨架：`Application` 管理运行期资源，Router 分发请求，Middleware 处理横切逻辑，Fluent 处理数据库模型与迁移，Swift Package Manager 管理依赖。

## 解决的问题

只用 Swift 标准库或 SwiftNIO 直接写 HTTP 服务时，开发者很快会遇到一组重复问题。第一是路由问题：URL path、HTTP method、路径参数、查询参数和 handler 之间没有统一组织方式，代码容易变成一串条件分支。Vapor 用 `RoutesBuilder` 把路由声明成可组合的树，`app.grouped("api", "tasks")` 可以把同一组 API 的前缀、中间件和认证策略放在同一个边界里。

第二是 Request/Response 模型问题。底层 HTTP 只知道 method、header、body 和 status code，业务代码需要的是“把 JSON body 解成 Swift 类型、把 Swift 值编码成 JSON 响应、在错误时返回正确状态码”。Vapor 的 `Request`、`Response`、`Content`、`Abort` 把这些协议细节收敛到清晰 API：handler 可以从 `req.content.decode(...)` 获得 DTO，也可以返回 `Content`、`HTTPStatus` 或手工构造的 `Response`。

第三是横切逻辑问题。请求 ID、日志、CORS、认证、限流、错误处理、压缩、审计如果写在每个 handler 中，会让业务逻辑被基础设施淹没。Vapor 用 Middleware pipeline 让这些逻辑包裹请求链路：请求进入 handler 前可以检查，响应返回后可以补 header 或记录指标。这样“每个请求都要做”的事不需要散落在每个 API 里。

第四是异步并发问题。服务端 Swift 运行在 SwiftNIO 的事件循环上，数据库、网络、文件和外部 API 都可能是异步 I/O。早期 `EventLoopFuture` 写法容易形成回调链；现代 Vapor 支持 `async throws` handler，让业务流程按顺序表达，同时仍然由 EventLoop 承载高并发。需要注意的是，阻塞调用仍然不能放在事件循环上，CPU 密集或阻塞 I/O 应转移到合适的执行资源。

第五是配置、数据库、测试和部署问题。真实服务不只是一组路由，还要读取端口、数据库 URL、secret、日志级别，管理数据库迁移，编写 HTTP 集成测试，并在 Linux 容器中稳定运行。Vapor 用 `Application` 作为运行期资源中心，用环境配置管理运行差异，用 Fluent 表达 model、relation、query 和 migration，用 Swift Package Manager 与 release binary 支撑构建和部署。

## 设计思想

Vapor 的第一层思想是应用对象统一运行期。`Application` 不是业务 service，也不是全局变量的替身，而是服务进程的组合根：它持有 event loop group、logger、middleware、routes、client、database、storage 和环境信息。应用启动时在 `Application` 上注册基础设施，应用关闭时通过 `shutdown()` 释放资源。quickstart 里的 `let app = try await Application.make(.detect())` 与 `defer { app.shutdown() }` 正是这个思想的最小形态。

第二层思想是路由即边界。开发者用 `app.get`、`app.post`、`grouped` 等 API 把 URL、HTTP method、认证和业务处理绑定起来。路由 handler 接收 `Request`，返回可编码对象、`Response`、`HTTPStatus` 或异步结果。`RoutesBuilder` 让路由可以被分组、组合和局部加中间件，因此 API 的外部形状会自然映射到代码结构。

第三层思想是协议边界类型化。`Request` 代表一次 HTTP 输入，`Response` 代表一次 HTTP 输出，`Content` 代表可以通过内容协商编码/解码的请求体或响应体。这样 handler 不必手写 JSON parsing、header 拼装和 status code 分支，也不必把数据库模型直接暴露给客户端。DTO、`Content` 与 `Abort` 共同把“协议错误”和“业务数据”分开。

第四层思想是 middleware pipeline。日志、错误处理、CORS、认证、请求 ID、压缩等横切逻辑不应散落在每个 handler 中，而应作为 Middleware 包裹请求处理链。每个 Middleware 可以在请求进入业务前检查，也可以在响应返回后补充 header 或记录指标。这个模型解决的是“同一规则应用到很多路由”的问题。

第五层思想是 async/await 站在 EventLoop 之上。Vapor 早期基于 `EventLoopFuture`，现代写法更鼓励 `async throws` handler。开发者可以像写同步代码一样表达异步数据库、HTTP 客户端和文件操作，同时仍由 SwiftNIO 支撑高并发事件循环。理解这一点有助于避免在 handler 中做阻塞 I/O，也有助于判断什么时候需要保留 future API 与 NIO 生态互操作。

第六层是数据建模与迁移。Fluent 把模型、字段、关系和迁移表达成 Swift 类型。它的核心不是让开发者忘记 SQL，而是在模型与迁移之间建立统一结构，减少字符串式查询和手工迁移错误。Vapor 鼓励把 Fluent model、DTO、service/repository 分开：数据库结构服务于持久化，DTO 服务于 HTTP 契约，service/repository 服务于业务规则。

## 架构模型

一个典型 Vapor 服务由 `Package.swift`、入口文件、配置函数、路由模块、业务服务、数据访问层和测试组成。

```text
VaporQuickstart
  Package.swift
  Sources/App/
    main.swift
    TaskRepository.swift
    TaskDTO.swift
```

`main.swift` 创建 `Application`，注册 middleware、配置路由并启动服务。路由层把 HTTP 协议细节转换为业务调用。Repository 或 Service 层处理数据读写。真实项目中通常会把 `configure.swift`、`routes.swift`、`Controllers/`、`Models/`、`Migrations/`、`Services/` 和 `Tests/` 分开。

## 请求/执行生命周期

一次 Vapor 请求通常经历以下步骤：

1. SwiftNIO 接收 socket 数据并解析为 HTTP 请求。
2. Vapor 创建 `Request`，携带 method、path、headers、body、logger、application 和 event loop。
3. 全局 Middleware 依次处理请求，例如错误处理中间件、日志中间件、CORS、认证。
4. Router 根据 method 和 path 匹配 handler，路由分组上的 middleware 也会加入链路。
5. Handler 从 `Request` 解码参数、query、body 或认证信息，调用 service/repository。
6. 业务层通过 async/await 访问数据库、缓存、外部 API 或内存数据。
7. Handler 返回 `Content`、`Response` 或抛出错误。
8. Middleware 逆序处理响应，Vapor 编码响应体并写回客户端。

理解这条链路后，就能判断代码应该放在哪里：认证在 middleware，参数验证在边界，业务规则在 service，数据细节在 repository 或 Fluent model。

## 工程结构

本仓库 quickstart 使用最小 Swift Package：

```text
examples/quickstart/
  Package.swift
  Sources/App/
    main.swift
    TaskDTO.swift
    TaskRepository.swift
```

真实项目扩展时建议按职责拆分：`Controllers/` 放 HTTP handler，`Models/` 放 Fluent model，`Migrations/` 放数据库迁移，`Services/` 放业务服务，`Repositories/` 放数据访问抽象，`Middleware/` 放横切逻辑，`Configuration/` 放环境变量解析。不要让 `main.swift` 同时承担配置、路由、业务和数据访问。

## 配置方式

Vapor 的配置主要来自三处。第一是代码配置，例如 `app.middleware.use`、`app.routes.defaultMaxBodySize`、数据库注册和 route group。第二是环境变量，例如端口、数据库 URL、JWT secret、运行环境。第三是 Swift Package 配置，例如依赖版本、target 和平台要求。

quickstart 通过代码设置中间件和路由，通过命令行指定 host/port。真实服务应该用 `Environment.get("DATABASE_URL")` 读取敏感配置，并在不同环境中设置日志级别、迁移策略和外部服务端点。

## 模块与依赖管理

Vapor 项目使用 Swift Package Manager 管理模块和依赖。`Package.swift` 声明 `vapor` package，应用 target 依赖 `Vapor` product。中大型项目可以把 domain、database、web、shared DTO 拆成不同 target，避免所有代码都依赖 Vapor。

依赖组织上，Vapor 的 `Application` 像运行期容器，持有 logger、storage、event loop group、database、client 等资源。简单依赖可以在 route closure 中捕获；复杂依赖建议显式构造 service 并传给 controller，或者通过 `Application.StorageKey` 扩展注册。核心原则是让业务代码尽量少依赖 `Request`，否则测试会被 HTTP 框架绑死。

## 数据访问

quickstart 使用线程安全的内存 repository，便于读者专注 Router、Request/Response 和 Middleware。真实项目接入数据库时通常选择 Fluent：定义 `Model`，为字段添加 `@Field`、`@ID`、`@Parent` 等属性包装器，创建 `Migration` 管理表结构，再在 handler/service 中用 `Model.query(on: req.db)` 查询。

如果团队更熟悉 SQL，也可以用 SQLKit 或数据库驱动直接写查询。无论使用 Fluent 还是 SQL，建议在 handler 外面建立 repository/service 边界，避免 HTTP 参数、数据库模型和返回 DTO 混在一起。

## 测试方式

Vapor 测试可以从三个层级入手。第一是纯 Swift 单元测试，验证 repository、service 和 DTO 转换。第二是 HTTP 集成测试，使用 Vapor testing 工具启动应用并发起请求。第三是端到端 smoke test，真实启动服务后用 `curl` 或脚本访问关键接口。

quickstart 给出可复制的 `swift run App serve` 命令和 `curl` 验证命令。后续可以补充 `XCTVapor` 测试，覆盖 `GET /api/tasks`、`POST /api/tasks` 和错误请求。

## 部署方式

Vapor 服务可以直接以 release 二进制运行，也可以构建 Docker 镜像部署到容器平台。生产环境通常会使用 `swift build -c release`，设置 `PORT`、数据库连接、日志级别和 secret，再由 systemd、Docker、Kubernetes、Fly.io、Render 或云服务器进程管理工具托管。

部署时要特别关注 Linux Swift 工具链版本、glibc、OpenSSL、数据库迁移时机和优雅停机。Swift 在 macOS 上开发体验很好，但生产通常在 Linux 容器中运行，因此 CI 中最好加入 Linux build。

## 适用场景与取舍

优先选择 Vapor 的场景：团队已经熟悉 Swift，希望前后端共享 DTO 或领域模型；服务规模中小到中等，需要类型安全和 async/await；Apple 平台 App 需要配套 API；希望用 Swift Package 管理完整后端工程。

需要谨慎的场景：团队主要使用 JVM/Go/Node/Python 且 Swift 运维经验不足；依赖大量成熟中间件生态；需要现成企业级框架规范或非常高的招聘便利性。此时可以把 Vapor 用在边界服务、BFF 或 Swift 强相关服务中，而不是强行替换全部后端技术栈。

## 案例索引

- [core-ideas](examples/core-ideas/)：把上一节“解决的问题”和“设计思想”映射到 quickstart 的关键代码片段。
- [quickstart](examples/quickstart/)：最小 Vapor JSON API，展示路由分组、中间件、`Request` 解码、DTO 响应、内存 repository 和 async handler。

## 版本来源

- 语言基线：Swift 6.3.x，策略为 latest stable，无官方 LTS。
- 框架基线：Vapor latest stable，依赖版本以官方文档和 Swift Package 解析结果为准。
- 官方来源：https://docs.vapor.codes/
- Swift 安装来源：https://www.swift.org/install/
- 校验日期：2026-05-30
