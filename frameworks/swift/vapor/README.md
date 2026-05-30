# Vapor

Vapor 是 Swift 生态中最常用的服务端 Web 框架之一。它把 Swift 的类型系统、async/await、结构化并发和包管理带到 HTTP API 开发中，让开发者可以用接近 Apple 平台开发的语言体验构建后端服务。

## 核心定位

Vapor 主要解决服务端 Web 应用中的路由、请求/响应编解码、中间件、配置、日志、异步执行、数据库访问和部署问题。它适合 JSON API、后台服务、BFF、Webhook、轻量 Web 应用和需要 Swift 端到端共享模型的团队。

它不是一个“零抽象”的 HTTP 库，也不是只靠代码生成的 RPC 框架。Vapor 的价值在于提供一套完整但仍然可组合的 Web 工程骨架：`Application` 管理运行期资源，Router 分发请求，Middleware 处理横切逻辑，Fluent 处理数据库模型与迁移，Swift Package Manager 管理依赖。

## 设计思想

Vapor 的第一层思想是路由即边界。开发者用 `app.get`、`app.post`、`grouped` 等 API 把 URL、HTTP method、认证和业务处理绑定起来。路由 handler 接收 `Request`，返回可编码对象、`Response` 或异步结果。

第二层思想是 middleware pipeline。日志、错误处理、CORS、认证、请求 ID、压缩等横切逻辑不应散落在每个 handler 中，而应作为 Middleware 包裹请求处理链。每个 Middleware 可以在请求进入业务前检查，也可以在响应返回后补充 header 或记录指标。

第三层思想是 async/await 优先。Vapor 早期基于 EventLoopFuture，现代写法更鼓励 `async throws` handler。开发者可以像写同步代码一样表达异步数据库、HTTP 客户端和文件操作，同时仍由 SwiftNIO 支撑高并发事件循环。

第四层是数据建模。Fluent 把模型、字段、关系和迁移表达成 Swift 类型。它的核心不是让开发者忘记 SQL，而是在模型与迁移之间建立统一结构，减少字符串式查询和手工迁移错误。

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

- [quickstart](examples/quickstart/)：最小 Vapor JSON API，展示路由分组、中间件、`Request` 解码、DTO 响应、内存 repository 和 async handler。

## 版本来源

- 语言基线：Swift 6.3.x，策略为 latest stable，无官方 LTS。
- 框架基线：Vapor latest stable，依赖版本以官方文档和 Swift Package 解析结果为准。
- 官方来源：https://docs.vapor.codes/
- Swift 安装来源：https://www.swift.org/install/
- 校验日期：2026-05-30
