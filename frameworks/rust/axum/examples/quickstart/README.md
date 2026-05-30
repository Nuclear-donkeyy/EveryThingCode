# Axum quickstart：内存笔记 API

## 目标

本案例用一个最小但真实的 Axum 项目实现笔记 API。读完并运行后，你应该能理解 Axum 项目的入口、路由、extractor、共享状态、JSON 响应和测试方式。

案例包含这些接口：

- `GET /health`：健康检查。
- `GET /notes`：列出所有笔记。
- `GET /notes/{id}`：按 ID 查询笔记。
- `POST /notes`：创建笔记。

## 学习重点

重点观察四个映射关系：

- `Router` 映射 HTTP 结构：路径和 method 在路由层声明。
- extractor 映射请求输入：`Path`、`State`、`Json` 分别来自 URL、应用状态和请求体。
- `State` 映射共享依赖：内存仓储通过 `Arc<AppState>` 注入。
- `IntoResponse` 映射输出：`Json<T>`、`StatusCode` 和 tuple 自动变成 HTTP 响应。

## 工程结构

```text
.
├── Cargo.toml      # Rust package 与依赖声明
├── README.md       # 教学说明和运行命令
└── src/
    └── main.rs     # 模型、状态、路由、handler、启动入口和测试
```

为了让第一眼阅读足够连贯，案例把所有代码放在一个文件中。真实项目可以按 `models`、`state`、`routes`、`handlers`、`services` 和 `errors` 拆分。

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

`AppState` 是应用共享状态，内部保存 `RwLock<BTreeMap<u64, Note>>` 和 `AtomicU64`。这里用内存结构是为了突出状态注入方式；生产环境通常换成数据库连接池和 repository。

`build_app(state)` 返回 `Router`。这一步是 Axum 的装配中心：`route` 声明 path/method 到 handler 的映射，`with_state` 把共享状态绑定给所有需要 `State<SharedState>` 的 handler。

`list_notes` 只使用 `State`，说明它不依赖 path 或 body。`get_note` 同时使用 `Path<u64>` 和 `State`，说明它需要 URL 中的 ID 和共享仓储。`create_note` 使用 `Json<CreateNote>`，Axum 会把请求体反序列化成结构体；如果 JSON 不合法，框架会在 handler 之前返回错误。

测试没有启动真实端口，而是直接把 `Router` 当作 Tower service 调用。这样测试速度快，也能精确检查状态码和 JSON body。

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
