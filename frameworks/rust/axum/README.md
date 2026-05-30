# Axum

## 核心定位

Axum 是 Tokio 团队维护的 Rust Web 框架，主要解决“如何把异步 HTTP 请求安全地路由到业务函数”这个问题。它适合构建 JSON API、内部服务、微服务、BFF、Webhook、轻量后台和需要 Tower 中间件生态的服务。

Axum 不试图成为全家桶：它不内置 ORM、不强制目录结构、不提供模板层约定，也不替你隐藏 Tokio、Serde、Tower、数据库连接池这些组成部分。它更像一层类型安全的 HTTP 组合器，把路由、请求提取、共享状态、响应转换和中间件连接起来。

## 设计思想

Axum 的第一思想是组合。`Router` 负责声明路径和 HTTP method，handler 是普通 async 函数，extractor 负责把请求中的 path、query、header、JSON body、共享状态提取成强类型参数。一个 handler 的签名就是它需要的输入清单，例如 `Path<u64>` 表示路径参数，`State<AppState>` 表示应用状态，`Json<CreateNote>` 表示请求体 JSON。

第二个思想是类型驱动。handler 返回的值只要实现 `IntoResponse`，就可以变成 HTTP 响应；提取失败时，框架会用 extractor 自己的 rejection 生成错误响应。许多“忘记解析 JSON”“路径参数类型不匹配”“状态类型不一致”的问题，会在编译期或框架边界被提前发现。

第三个思想是 Tower 服务模型。Axum 的底层是 Hyper 和 Tower：一次请求会变成一个 `Service` 调用，中间件也是对服务的包装。这意味着认证、日志、超时、限流、追踪、压缩等横切能力，可以通过 Tower layer 组合到 Router 上，而不是塞进每个 handler。

## 架构模型

一个典型 Axum 项目可以从四层理解：

- 入口层：创建 Tokio runtime，加载配置，初始化共享状态，绑定 TCP listener。
- 路由层：用 `Router::new().route(...).with_state(...)` 声明 HTTP API。
- 处理层：handler 使用 extractor 获得输入，调用业务逻辑，返回可转换为响应的值。
- 依赖层：状态、数据库池、配置、客户端等通过 `State` 显式传入；中间件通过 Tower layer 包装路由。

本仓库 quickstart 为了保持聚焦，把这些都放在 `src/main.rs` 中；真实项目通常会拆成 `main.rs`、`routes.rs`、`handlers.rs`、`state.rs`、`models.rs`、`errors.rs` 和 `tests/`。

## 请求/执行生命周期

一次 Axum 请求大致经历这些步骤：

1. Tokio runtime 接收 socket 事件，Hyper 将字节流解析为 HTTP 请求。
2. Axum Router 根据 path 和 method 找到匹配路由。
3. Tower layer 依次包裹请求，例如日志、超时、认证、trace。
4. Axum 按 handler 签名运行 extractor：解析路径、JSON、query、header、状态等。
5. handler 执行业务逻辑，通常返回 `Json<T>`、`StatusCode`、tuple 或自定义错误。
6. 返回值通过 `IntoResponse` 转为 HTTP 响应，由 Hyper 写回连接。

理解这个生命周期后，再读 Axum 代码会很清楚：路由负责“去哪里”，extractor 负责“拿什么”，handler 负责“做什么”，response 负责“怎么回”。

## 工程结构

本仓库案例结构：

```text
frameworks/rust/axum/examples/quickstart/
├── Cargo.toml
├── README.md
└── src/
    └── main.rs
```

`Cargo.toml` 声明 Axum、Tokio、Serde、Serde JSON 和测试所需 Tower。`src/main.rs` 包含数据模型、共享状态、路由构建、handler、启动入口和内置测试。

真实项目扩展时，建议边界如下：

- `config`：环境变量、端口、数据库连接串、日志级别。
- `state`：应用共享依赖，如连接池、客户端、缓存、配置快照。
- `routes`：路由组合，只描述 HTTP 结构。
- `handlers`：请求提取、响应组装，不直接写复杂领域规则。
- `services`：业务逻辑。
- `repositories`：数据访问，内存、SQLx、Diesel 或外部 API 都可以放这里。
- `errors`：统一错误类型和 `IntoResponse` 实现。

## 配置方式

Axum 不规定配置系统。最小项目可以直接在代码里绑定 `127.0.0.1:3000`；真实项目常用环境变量、`.env`、配置文件或部署平台注入。

推荐做法是启动时一次性读取配置，构造成 `AppConfig`，放入 `AppState`，handler 通过 `State` 读取。这样配置来源可以变化，但业务代码只依赖结构化配置。对于超时、请求体大小、trace、CORS 等 HTTP 行为，通常通过 Tower layer 或 Axum 内置 routing/body 配置完成。

## 模块与依赖管理

Axum 没有传统依赖注入容器，依赖管理依靠 Rust 类型系统和显式状态：

- `State<T>`：读取通过 `Router::with_state` 注入的应用状态。
- `Extension<T>`：也可用于传递请求扩展，但新项目更推荐 `State` 表达全局状态。
- `Arc<T>`：共享不可复制或需要跨任务持有的状态。
- `Mutex`/`RwLock`：保护内存可变状态；异步场景中要谨慎选择同步锁或 Tokio 锁。
- trait：把业务依赖抽象成接口，方便替换内存实现、数据库实现和测试替身。

本案例使用 `Arc<AppState>` 加 `RwLock<BTreeMap<...>>`，因为数据只存在内存中，且读多写少，适合教学演示。生产服务更常见的是把数据库连接池、消息队列客户端和外部服务客户端放进 state。

## 数据访问

quickstart 使用内存数据，让读者先看清框架本身。它展示的是“handler 不关心数据来自哪里，只关心通过 state 调用某个能力”这个边界。

接入真实数据库时，常见路径有两种：

- SQLx：更适合 Axum 的 async 模型，把 `PgPool`、`MySqlPool` 或 `SqlitePool` 放进 `AppState`。
- Diesel：适合希望使用类型安全查询 DSL 的项目；如果使用同步连接，需要考虑在线程池中执行阻塞操作。

无论选择哪种方案，都建议先把内存操作抽成 repository/service，再替换底层实现。这样 API、handler 和测试结构不会因为数据库变化而大幅波动。

## 测试方式

Axum 的测试可以不真正启动端口。因为 Router 本身实现 Tower `Service`，测试可以构造 `Request`，调用 `app.oneshot(request).await`，检查状态码和响应体。这种方式速度快、稳定，也避免端口冲突。

更高层的集成测试可以启动真实 listener，再用 `reqwest` 调 HTTP；适合验证中间件、真实网络行为、TLS、反向代理头或跨服务调用。本案例内置单元级 HTTP 测试，验证列表和创建笔记两个接口。

## 部署方式

Axum 应用最终是一个 Rust 二进制。基础部署方式是：

1. `cargo build --release` 构建 release binary。
2. 用环境变量传入监听地址、日志级别和外部依赖配置。
3. 在 Linux 服务器、systemd、容器或 Kubernetes 中运行二进制。

容器部署时通常使用多阶段构建：第一阶段编译，第二阶段只复制二进制和必要证书。生产环境要特别关注优雅停机、请求超时、日志追踪、健康检查和数据库连接池参数。

## 适用场景与取舍

优先选择 Axum 的场景：

- 希望学习或使用 Tokio/Tower 生态。
- 希望 API 类型边界清晰，少用宏，更多依靠函数签名表达请求输入。
- 项目偏服务端 API、内部平台、微服务、Webhook 或 BFF。
- 需要方便接入 Tower 中间件、tracing、SQLx、tonic 等生态组件。

可以考虑其他框架的场景：

- 想要更强约定或更多内置体验，可以看 Rocket。
- 团队已有 Actix Web 经验，或特别看重其成熟资料与性能案例，可以选 Actix Web。
- 想用函数式 filter 风格学习路由组合，可以看 Warp。

## 案例索引

- [quickstart](examples/quickstart/)：使用 Axum、Tokio、Serde 和内存状态构建笔记 API，包含 `GET /health`、`GET /notes`、`GET /notes/{id}`、`POST /notes` 和可运行测试。

## 版本来源

- 语言基线：Rust 1.96.x，按本仓库 `versions.yaml` 的 latest stable 策略记录。
- 框架策略：Axum latest stable，本案例依赖声明使用 `axum = "0.8"`，由 Cargo 在运行时解析兼容 patch 版本。
- 官方来源：https://docs.rs/axum/latest/axum/
- Tokio 来源：https://tokio.rs/
- Tower 来源：https://docs.rs/tower/latest/tower/
- 校验日期：2026-05-30
