# Actix Web

## 核心定位

Actix Web 是 Rust 生态中成熟、高性能、资料丰富的 Web 框架，主要解决 HTTP 服务的路由、请求提取、状态共享、中间件、测试和运行时集成问题。它适合构建 REST API、后台服务、网关、Webhook、内部系统和对吞吐/延迟比较敏感的服务。

Actix Web 不内置 ORM，也不强制使用某种项目分层方式。它提供的是 Web 层能力：`App` 组织应用，`Scope` 组织路由分组，handler 处理请求，extractor 提取输入，`web::Data` 共享状态，middleware 处理横切逻辑。

## 设计思想

Actix Web 的历史来自 Actix actor 生态。早期 Actix 更强调 actor、message、arbiter 和 mailbox；Actix Web 今天的日常 API 已经不要求你用 actor 写业务，但这种历史影响仍然存在：它很重视 runtime、worker、服务工厂、并发边界和消息驱动式的执行模型。

在编码体验上，Actix Web 倾向于“应用构建器 + attribute macro + extractor”。你可以用 `App::new()` 声明应用，用 `web::scope("/api")` 分组，用 `#[get("/health")]` 或 `web::resource(...).route(...)` 声明路由。handler 是 async 函数，参数中的 `web::Path`、`web::Json`、`web::Query`、`web::Data` 会由框架自动提取。

它的另一个核心思想是显式共享状态。`web::Data<T>` 通常包裹 `Arc<T>`，让多个 worker 可以共享数据库连接池、配置、服务对象或内存仓储。你需要自己决定哪些状态可变，哪些状态只读，哪些操作应交给数据库事务处理。

## 架构模型

Actix Web 项目可以从这些对象理解：

- `HttpServer`：绑定地址，创建 worker，负责启动和运行服务。
- `App`：每个 worker 中的应用实例，注册状态、路由、scope 和 middleware。
- `Scope`：把一组路径和资源归到同一前缀下，例如 `/api/v1`。
- Handler：普通 async 函数，参数由 extractor 提供，返回实现 `Responder` 的类型。
- `web::Data`：应用共享状态，常用于配置、连接池、服务对象和内存数据。
- Middleware：围绕请求和响应执行横切逻辑，例如日志、认证、压缩、CORS。

本仓库 quickstart 将所有内容集中在 `src/main.rs` 中，方便读者完整阅读。真实项目应拆分为 `config`、`state`、`routes`、`handlers`、`services`、`models`、`errors` 和 `tests`。

## 请求/执行生命周期

一次 Actix Web 请求通常这样流动：

1. `HttpServer` 监听端口，worker 接收连接。
2. 请求进入应用服务链，middleware 可以先处理日志、认证、请求 ID 等横切逻辑。
3. Router 按 path 和 method 匹配 `Scope`、resource 和 route。
4. 框架根据 handler 参数运行 extractor：路径参数、JSON body、query、header、`web::Data`。
5. handler 执行业务逻辑，返回 `impl Responder`、`HttpResponse` 或 `Result<T, E>`。
6. 响应再次经过 middleware，最终写回客户端。

这个生命周期说明了 Actix Web 的核心边界：`HttpServer` 管运行，`App` 管装配，`Scope` 管分组，handler 管业务入口，extractor 管输入转换，`Data` 管共享依赖。

## 工程结构

本仓库案例结构：

```text
frameworks/rust/actix-web/examples/quickstart/
├── Cargo.toml
├── README.md
└── src/
    └── main.rs
```

`Cargo.toml` 声明 Actix Web、Serde 和 Serde JSON。`src/main.rs` 包含模型、共享状态、路由配置、handler、启动入口和测试。

真实项目扩展时，建议这样划分：

- `main.rs`：只做日志、配置、状态初始化和 `HttpServer` 启动。
- `routes.rs`：集中注册 `Scope` 和 route。
- `handlers.rs`：HTTP 输入输出转换，尽量保持薄。
- `services.rs`：业务规则和事务边界。
- `repositories.rs`：数据库或外部服务访问。
- `state.rs`：`AppState`、连接池、配置对象。
- `errors.rs`：统一错误类型，实现 `ResponseError`。

## 配置方式

Actix Web 配置通常由三层组成：

- 运行配置：监听地址、worker 数、keep-alive、TLS、shutdown timeout，由 `HttpServer` 或环境变量控制。
- 应用配置：数据库连接、外部服务地址、功能开关，启动时读入结构体，再放进 `web::Data`。
- 路由配置：`App::configure`、`web::scope` 和 resource/route 声明 HTTP 结构。

最小案例固定监听 `127.0.0.1:8080`。真实服务可以读取 `BIND_ADDR`，并把配置结构放入 `Data<AppConfig>`，这样 handler 不需要关心配置来自环境变量、文件还是平台注入。

## 模块与依赖管理

Actix Web 不提供传统 DI 容器，但 `App` 的构建过程承担了依赖装配职责。常见方式是：

- `app_data(web::Data::new(value))` 注入共享状态。
- handler 通过参数 `web::Data<T>` 获取依赖。
- `App::configure(configure_routes)` 把路由注册拆到独立函数。
- 用 trait 抽象 service/repository，测试时替换实现。
- 用 middleware 包装横切逻辑，避免 handler 重复处理。

要注意 worker 模型：`HttpServer::new` 的闭包会为每个 worker 创建一个 `App`。如果状态要跨 worker 共享，应在闭包外先创建 `web::Data`，再在闭包内 `clone`。本案例即采用这种写法。

## 数据访问

quickstart 使用内存 `BTreeMap` 保存笔记，目的是让读者专注于 Actix Web 的状态和 extractor。生产服务通常不会把业务数据放在进程内存里，因为重启会丢失，多个实例也无法共享。

接入数据库时常见选择：

- SQLx：适合 async handler，把连接池放入 `web::Data`。
- Diesel：类型安全 DSL 成熟；同步操作需要避免阻塞 worker，通常配合连接池和阻塞任务处理。
- SeaORM：如果团队偏好 async ORM，也可以作为中间方案。

建议把数据访问放到 repository/service 层，handler 只负责从 `web::Json`、`web::Path`、`web::Data` 中取输入并调用服务。

## 测试方式

Actix Web 提供 `actix_web::test` 模块，可以不启动真实端口测试应用。典型流程是：

1. 用 `test::init_service(App::new().configure(...)).await` 初始化服务。
2. 用 `test::TestRequest` 构造请求。
3. 用 `test::call_service` 或 `test::call_and_read_body_json` 执行请求。
4. 检查状态码、响应 JSON 和状态变化。

本案例内置两个测试：健康检查和创建笔记。真实项目还应补充错误响应、鉴权失败、数据库事务和外部服务替身测试。

## 部署方式

Actix Web 应用同样是 Rust 二进制。基础流程是 `cargo build --release` 后运行产物。生产部署要关注：

- `RUST_LOG` 和结构化日志。
- worker 数量与 CPU、阻塞任务的关系。
- 优雅停机和健康检查。
- 反向代理、TLS、压缩和请求体大小限制。
- 容器镜像中的 CA 证书和运行用户权限。

容器化时推荐多阶段构建，把编译环境和运行环境分开，最终镜像只包含二进制、证书和必要配置。

## 适用场景与取舍

优先选择 Actix Web 的场景：

- 团队希望使用成熟、高性能、资料多的 Rust Web 框架。
- 喜欢 `App`/`Scope`/attribute macro 的组织方式。
- 项目需要较强吞吐，且团队愿意理解 worker、状态共享和阻塞边界。
- 已经有 Actix Web 存量项目或生态依赖。

可以考虑 Axum 的场景：

- 希望更直接地拥抱 Tokio/Tower 生态。
- 更喜欢少宏、函数签名表达输入、Router 组合表达结构。
- 需要大量 Tower layer 复用。

## 案例索引

- [quickstart](examples/quickstart/)：使用 Actix Web、Serde 和内存状态构建笔记 API，包含 `GET /health`、`GET /notes`、`GET /notes/{id}`、`POST /notes` 和可运行测试。

## 版本来源

- 语言基线：Rust 1.96.x，按本仓库 `versions.yaml` 的 latest stable 策略记录。
- 框架策略：Actix Web latest stable，本案例依赖声明使用 `actix-web = "4"`，由 Cargo 在运行时解析兼容 patch 版本。
- 官方来源：https://actix.rs/
- API 文档：https://docs.rs/actix-web/latest/actix_web/
- 校验日期：2026-05-30
