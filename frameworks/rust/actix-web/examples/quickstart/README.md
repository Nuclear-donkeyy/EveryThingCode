# Actix Web quickstart：内存笔记 API

## 目标

本案例用一个最小但真实的 Actix Web 项目实现笔记 API。读完并运行后，你应该能理解 `HttpServer`、`App`、`Scope`、handler、extractor、`web::Data` 和测试模块如何协作。

案例包含这些接口：

- `GET /health`：健康检查。
- `GET /notes`：列出所有笔记。
- `GET /notes/{id}`：按 ID 查询笔记。
- `POST /notes`：创建笔记。

## 学习重点

重点观察四个映射关系：

- `HttpServer` 映射运行时边界：监听地址、worker 和应用实例由它管理。
- `App`/`Scope` 映射 HTTP 结构：应用、分组、资源和 method 逐层组合。
- extractor 映射请求输入：`web::Path`、`web::Json`、`web::Data` 来自不同请求位置或应用状态。
- `Responder` 映射输出：`HttpResponse`、JSON 和状态码被统一转换成响应。

## 这个案例解决什么问题

这个案例不是为了展示一个复杂业务，而是用“笔记 API”压缩出 Actix Web 最常见的工程问题：如何把一个高并发 HTTP 服务拆成运行时、路由、共享状态、输入提取、响应生成和测试几个清楚的层次。

如果裸写 HTTP 服务，`GET /notes`、`GET /notes/{id}`、`POST /notes` 很容易混在一个大分发函数里：你需要手动判断 method，手动拆路径，手动读 body，手动解析 JSON，手动管理共享数据，最后还要自己构造状态码和响应头。Actix Web 把这些工作变成类型和组合：

- `Cargo.toml` 引入 `actix-web`、`serde`、`serde_json`，分别解决 Web 抽象、请求/响应数据结构和测试 JSON 的问题。
- `HttpServer::new` 解决“服务如何启动、监听、创建 worker、驱动 async handler”的问题。
- `App::new().configure(configure_routes)` 解决“应用由哪些路由和依赖组成”的问题。
- `web::scope("/api")` 解决“同一业务模块如何共享路径前缀”的问题。
- `web::Data<AppState>` 解决“多个 handler 和多个 worker 如何拿到同一份应用依赖”的问题。
- `web::Path<u64>` 和 `web::Json<CreateNote>` 解决“HTTP 输入如何变成强类型 Rust 值”的问题。
- `web::Json(...)` 与 `HttpResponse::Created().json(...)` 解决“Rust 值如何变成 HTTP 响应”的问题。
- `actix_web::test` 解决“不启动真实端口也能验证路由和响应”的问题。

## 工程结构

```text
.
├── Cargo.toml      # Rust package 与依赖声明
├── README.md       # 教学说明和运行命令
└── src/
    └── main.rs     # 模型、状态、路由配置、handler、启动入口和测试
```

案例把代码集中在一个文件中，便于首次学习。真实项目可以拆成 `routes`、`handlers`、`state`、`services`、`repositories` 和 `errors`。

## 运行前提

- Rust stable toolchain，建议按仓库根目录 `versions.yaml` 的 Rust latest stable 基线安装。
- Cargo 可用。
- 首次运行需要 Cargo 根据 `Cargo.toml` 下载依赖。

## 运行

```bash
cargo run
```

启动后可在另一个终端调用：

```bash
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/api/notes
curl -X POST http://127.0.0.1:8080/api/notes -H 'content-type: application/json' -d '{"title":"Learn Actix Web","body":"App, Scope, Handler, Data"}'
curl http://127.0.0.1:8080/api/notes/1
```

运行测试：

```bash
cargo test
```

## 预期输出

启动命令会输出类似：

```text
Actix Web quickstart listening on http://127.0.0.1:8080
```

健康检查返回：

```json
{"status":"ok","framework":"actix-web"}
```

创建笔记返回 `201 Created`，响应体类似：

```json
{"id":1,"title":"Learn Actix Web","body":"App, Scope, Handler, Data"}
```

## 代码讲解

### 依赖声明：先把 Web 层和数据层边界说清楚

`Cargo.toml` 中只有三个关键依赖：`actix-web = "4"` 提供 `HttpServer`、`App`、`web`、handler、extractor、test 等 Web 能力；`serde` 的 `derive` 功能让 `Note`、`CreateNote`、`Health` 可以被序列化或反序列化；`serde_json` 只放在 `dev-dependencies`，因为它只在测试中构造 JSON 请求体。

这体现了 Actix Web 的一个取舍：框架负责 HTTP 层，但不替你绑定 ORM、数据库迁移、配置中心或目录结构。依赖越少，越容易看清每一层的职责。

### 状态：用 `Data` 表达应用级依赖

`AppState` 保存内存笔记和自增 ID。它用 `RwLock<BTreeMap<u64, Note>>` 表达“读多写少的进程内数据”，用 `AtomicU64` 表达“创建笔记时需要线程安全生成 ID”。

`new_state()` 返回 `web::Data<AppState>`。`web::Data` 可以 clone，并在不同 worker 和 handler 之间共享同一个底层状态。这里的关键不是“Actix Web 自动让任何数据都安全”，而是 Rust 类型系统要求你把并发策略写清楚：可变 map 要放进 `RwLock`，计数器要用原子类型，生产数据库则通常换成连接池。

### 启动：`HttpServer` 接收的是应用工厂

`main` 中先创建 `state`，再把它 move 进 `HttpServer::new` 的闭包：

```rust
let state = new_state();

HttpServer::new(move || {
    App::new()
        .app_data(state.clone())
        .configure(configure_routes)
})
```

这段代码最值得慢读。`HttpServer` 会为 worker 调用闭包创建应用实例，所以闭包里面构建的是每个 worker 的 `App`。如果把状态放在闭包里面创建，每个 worker 可能得到不同状态；如果像本案例这样在闭包外创建 `web::Data`，闭包内只 clone，所有 worker 就共享同一份应用状态。这是 Actix Web worker 模型里最常见也最重要的边界。

`#[actix_web::main]` 使用 Actix Web 提供的运行时入口宏，负责启动 async runtime。日常开发中你只需要写 async `main`，无需手动搭建 executor。

### 路由：`App`、`Scope`、`Resource` 分别对应不同粒度

`configure_routes` 是路由装配函数。它把 `/api` 前缀做成 `Scope`，再把 `/notes` 和 `/notes/{id}` 注册进去：

```rust
web::scope("/api")
    .service(
        web::resource("/notes")
            .route(web::get().to(list_notes))
            .route(web::post().to(create_note)),
    )
    .service(web::resource("/notes/{id}").route(web::get().to(get_note)))
```

这段代码解决的是“路由组织”问题。`Scope` 适合表示一个业务模块或版本前缀，`Resource` 表示资源路径，`Route` 表示 method 到 handler 的映射。真实项目中可以把 `configure_routes` 拆到 `routes.rs`，再由 `main` 使用 `.configure(notes::configure_routes)` 组合多个模块。

### Handler：签名就是输入契约

`list_notes`、`get_note`、`create_note` 是 handler。Actix Web 会根据参数类型运行 extractor：

- `list_notes(state: web::Data<AppState>)`：只需要应用状态，不需要 path 或 body。
- `get_note(path: web::Path<u64>, state: web::Data<AppState>)`：需要路径中的 ID，也需要状态。
- `create_note(state: web::Data<AppState>, payload: web::Json<CreateNote>)`：需要状态和 JSON body。

这比手写解析更适合教学，也更适合长期维护。handler 的参数告诉读者这个接口依赖什么输入；输入不合法时，extractor 可以在业务代码执行前返回错误。对有其他框架经验的读者，可以把 extractor 理解为“带类型约束的参数绑定”，但它完全受 Rust 类型和 trait 约束。

### 响应：简单场景用 `Responder`，需要控制时用 `HttpResponse`

`health` 返回 `impl Responder`，实际值是 `web::Json<Health>`；`create_note` 返回 `HttpResponse::Created().json(note)`；`get_note` 根据是否找到笔记返回 `200 OK` 或 `404 Not Found`。这展示了 Actix Web 响应模型的两种常见写法：

- 返回 `web::Json(value)`：适合状态码默认是 `200 OK` 的简单 JSON 响应。
- 返回 `HttpResponse`：适合需要精确控制状态码、header、body 或错误分支的接口。

真实项目可以进一步定义错误枚举并实现 `ResponseError`，把 `not found`、`bad request`、`unauthorized` 等响应收敛到统一格式。

### 测试：验证应用服务链，而不是只测纯函数

测试使用 `actix_web::test` 初始化应用，不需要绑定真实端口。它适合验证路由、状态码、JSON body 和状态变化：

- `test::init_service(App::new().app_data(new_state()).configure(configure_routes)).await` 创建内存中的应用服务。
- `test::TestRequest::get().uri("/health").to_request()` 构造请求。
- `test::call_service` 和 `test::call_and_read_body_json` 执行请求并读取响应。

这种测试比单独调用 handler 更接近真实请求，因为它会经过 `App`、路由匹配、extractor 和 responder 转换；又比端到端测试更轻，因为不需要启动端口和额外进程。

### 与 Axum 的简短对照

如果你已经看过本仓库的 Axum quickstart，可以这样区分：Axum 更偏向 Tokio/Tower 的 `Router`、`State`、Tower layer 组合；Actix Web 更偏向 `HttpServer` 应用工厂、`App`/`Scope` 服务链、attribute macro 和自己的 extractor/test 工具。两者都强调强类型 handler，Actix Web 在 worker 模型、成熟文档和高性能生产案例上更有辨识度。

## 延伸练习

1. 为 `POST /api/notes` 增加标题不能为空的校验，并用 `HttpResponse::BadRequest()` 返回错误。
2. 增加 `DELETE /api/notes/{id}`，比较删除成功和不存在时的状态码设计。
3. 增加一个 middleware，给每个响应加 `x-request-id`，体会横切逻辑为什么不应该写在 handler 里。
4. 把内存仓储替换成 SQLx 连接池，并把数据库访问移动到 repository 层。
5. 把 `configure_routes`、handler、状态结构拆成多个模块，比较拆分前后 `main.rs` 的职责变化。

## 验收

完成后你应该能够：

- 解释 `HttpServer`、`App`、`Scope`、handler、extractor、`web::Data` 的职责。
- 修改 `/api` 前缀或新增路由，并知道应改 `configure_routes`。
- 运行 `cargo run` 和 `cargo test`。
- 说明为什么跨 worker 共享状态应在 `HttpServer::new` 闭包外创建，再在闭包内 clone。
