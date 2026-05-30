# Axum quickstart：内存笔记 API

## 目标

本案例用一个最小但真实的 Axum 项目实现笔记 API。读完并运行后，你应该能理解 Axum 项目的入口、路由、extractor、共享状态、JSON 响应和测试方式。

案例包含这些接口：

- `GET /health`：健康检查。
- `GET /notes`：列出所有笔记。
- `GET /notes/{id}`：按 ID 查询笔记。
- `POST /notes`：创建笔记。

## 这个案例解决什么问题

这个 quickstart 模拟的是最常见的 Rust JSON API 场景：服务需要维护一份共享依赖，接收不同来源的请求输入，把业务结果转换成稳定 HTTP 响应，并且能在不启动真实端口的情况下测试。

如果不用 Axum，你需要手写这些连接代码：解析 URL 中的 `id`、读取和反序列化 JSON body、把共享状态安全传到 async handler、为 404 和 201 组装响应、把中间件和测试接到 HTTP service 上。Axum 把它们分别放进 `Path`、`Json`、`State`、`IntoResponse` 和 Tower service 模型里，让代码的每个函数签名都在解释自己需要什么、返回什么。

## 学习重点

重点观察四个映射关系：

- `Router` 映射 HTTP 结构：路径和 method 在路由层声明。
- extractor 映射请求输入：`Path`、`State`、`Json` 分别来自 URL、应用状态和请求体。
- `State` 映射共享依赖：内存仓储通过 `Arc<AppState>` 注入。
- `IntoResponse` 映射输出：`Json<T>`、`StatusCode` 和 tuple 自动变成 HTTP 响应。
- Tower 映射服务组合：测试里的 `oneshot` 直接调用 `Router`，说明 Axum app 本质上也是可组合的 service。

## 工程结构

```text
.
├── Cargo.toml      # Rust package 与依赖声明
├── README.md       # 教学说明和运行命令
└── src/
    └── main.rs     # 模型、状态、路由、handler、启动入口和测试
```

为了让第一眼阅读足够连贯，案例把所有代码放在一个文件中。真实项目可以按 `models`、`state`、`routes`、`handlers`、`services` 和 `errors` 拆分。

## 依赖说明

`Cargo.toml` 的每个依赖都对应 Axum 的一块思想：

- `axum = "0.8"`：提供 `Router`、extractor、response、routing DSL 和 `axum::serve`。
- `tokio`：提供 async runtime、TCP listener 和多线程任务调度；`macros` 用于 `#[tokio::main]` 与 `#[tokio::test]`。
- `serde`：让请求体和响应体可以在 Rust struct 与 JSON 之间转换。
- `serde_json`：测试中把响应 body 解析成 JSON value，便于断言。
- `tower`：测试中使用 `ServiceExt::oneshot` 直接调用 `Router`，体现 Axum 和 Tower 生态的兼容。

注意这里没有引入 ORM、配置库或认证库，因为本案例的目标是先讲清 HTTP 边界。生产项目通常会继续加入 SQLx、tracing、tower-http、config、thiserror 等依赖。

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
curl http://127.0.0.1:3000/health
curl http://127.0.0.1:3000/notes
curl -X POST http://127.0.0.1:3000/notes -H 'content-type: application/json' -d '{"title":"Learn Axum","body":"Router, extractor, state"}'
curl http://127.0.0.1:3000/notes/1
```

运行测试：

```bash
cargo test
```

## 预期输出

启动命令会输出类似：

```text
Axum quickstart listening on http://127.0.0.1:3000
```

健康检查返回：

```json
{"status":"ok","framework":"axum"}
```

创建笔记返回 `201 Created`，响应体类似：

```json
{"id":1,"title":"Learn Axum","body":"Router, extractor, state"}
```

## 代码讲解

`Note` 和 `CreateNote` 区分了“服务保存的数据”和“客户端创建时提交的数据”。`Note` 有服务端生成的 `id`，`CreateNote` 没有；这个小差异体现了 API 模型不要直接复用数据库模型或响应模型。

`AppState` 是应用共享状态，内部保存 `RwLock<BTreeMap<u64, Note>>` 和 `AtomicU64`。这里用内存结构是为了突出状态注入方式：handler 不直接依赖全局变量，而是通过 `State<SharedState>` 获得能力。生产环境通常把它替换成数据库连接池、缓存客户端、消息队列客户端或 repository trait。

`new_state()` 返回 `Arc<AppState>`。`Arc` 负责让状态能被多个请求任务共享，`RwLock` 负责保护内存 map，`AtomicU64` 负责生成 ID。这个组合让你能看到 Rust async HTTP 服务常见的三类约束：所有权、并发安全和跨请求共享。

`build_app(state)` 返回 `Router`。这一步是 Axum 的装配中心：`route` 声明 path/method 到 handler 的映射，`get(...)` 和 `post(...)` 表达 HTTP method，`with_state` 把共享状态绑定给所有需要 `State<SharedState>` 的 handler。读 `build_app` 就能得到 API 总览。

`health` 返回 `Json<Health>`。这说明简单响应不需要手动设置 header；只要返回值实现 `IntoResponse`，Axum 就能生成 HTTP 响应。

`list_notes` 只使用 `State`，说明它不依赖 path 或 body。`get_note` 同时使用 `Path<u64>` 和 `State`，说明它需要 URL 中的 ID 和共享仓储。`create_note` 使用 `Json<CreateNote>`，Axum 会把请求体反序列化成结构体；如果 JSON 不合法，框架会在 handler 之前返回 extractor rejection。

`get_note` 和 `create_note` 返回 `impl IntoResponse`，因为它们可能返回不同形状的响应：查询成功时是 `200 + Json<Note>`，查询失败时是 `404 + text`，创建成功时是 `201 + Json<Note>`。这正是 `IntoResponse` 的用途：允许 handler 用 Rust 值表达 HTTP 结果，而不是到处手写 response builder。

`main` 使用 `#[tokio::main]` 创建 runtime，用 `tokio::net::TcpListener::bind` 监听端口，再交给 `axum::serve`。Axum 没有隐藏异步运行时，因此当你需要优雅停机、后台任务、数据库 async pool 或 tracing subscriber 时，可以在入口处自然接入。

测试没有启动真实端口，而是直接把 `Router` 当作 Tower service 调用。这样测试速度快，也能精确检查状态码和 JSON body。

## 请求流拆解

以 `POST /notes` 为例，请求执行过程可以拆成六步：

1. Tokio 接收连接，Hyper 解析 HTTP 请求。
2. `Router` 匹配到 `/notes` 的 `post(create_note)`。
3. Axum 运行 extractor：`State` 复制共享状态指针，`Json<CreateNote>` 读取并反序列化请求体。
4. `create_note` 生成 ID，写入 `RwLock<BTreeMap<...>>`，构造 `Note`。
5. `(StatusCode::CREATED, Json(note))` 通过 `IntoResponse` 变成 HTTP 响应。
6. 测试环境中，`tower::ServiceExt::oneshot` 可以直接拿到这个响应；真实运行时则由 Hyper 写回 socket。

## 延伸练习

1. 为 `POST /notes` 增加标题不能为空的校验，返回 `400 Bad Request`。
2. 把内存数据访问抽成 `NoteRepository` trait，再实现一个内存版本。
3. 增加 `DELETE /notes/{id}`，比较删除成功和不存在时的响应设计。

## 验收

完成后你应该能够：

- 解释 `Router`、handler、extractor、`State` 分别负责什么。
- 修改端口、增加路由，并说明为什么 handler 参数顺序不会改变语义。
- 运行 `cargo run` 和 `cargo test`。
- 把内存状态替换成数据库连接池时，知道应该从 `AppState` 和 service/repository 边界入手。
