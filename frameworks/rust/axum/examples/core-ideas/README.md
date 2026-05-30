# Axum core ideas example

## 目标

这个示例把 `Axum` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

Rust 异步 HTTP 需要同时处理类型安全、请求解析、共享状态、响应转换和 middleware 生态接线。

## 核心思想到代码

Router 组织路径，Extractor 从请求中取类型化数据，State 管共享状态，IntoResponse 统一响应，Tower 提供中间件基础。

```rust
let app = Router::new()
    .route("/tasks", get(list_tasks).post(create_task))
    .with_state(state);
```

```rust
async fn create_note(
    State(state): State<SharedState>,
    Json(payload): Json<CreateNote>,
) -> impl IntoResponse {
    let id = state.next_id.fetch_add(1, Ordering::Relaxed);
    let note = Note { id, title: payload.title, body: payload.body };
    (StatusCode::CREATED, Json(note))
}
```

## 代码位置

- [`Cargo.toml`](../quickstart/Cargo.toml)
- [`src/main.rs`](../quickstart/src/main.rs)

## 运行

先进入 quickstart 目录：

```bash
cd ../quickstart
cargo run
```

如果本机缺少对应工具链，可以先运行仓库根目录的 dry-run：

```bash
python3 scripts/run_framework_examples.py --dry-run
```

## 观察点

handler 签名就是契约：需要状态就写 State，需要 JSON 就写 Json。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`Axum` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
