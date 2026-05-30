# Actix Web core ideas example

## 目标

这个示例把 `Actix Web` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

高性能 Rust Web 服务要处理 worker、共享状态、路由作用域、extractor、响应模型和测试。

## 核心思想到代码

HttpServer 管 worker，App/Scope 组织服务，web::Data 管共享状态，宏路由和 extractor 描述请求输入，Responder 统一输出。

```rust
HttpServer::new(move || {
    App::new()
        .app_data(web::Data::new(state.clone()))
        .service(web::scope("/api").service(list_tasks))
})
```

```rust
#[get("/tasks")]
async fn list_tasks(state: web::Data<AppState>) -> impl Responder {
    HttpResponse::Ok().json(state.list())
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

状态通过 Data 克隆进入每个 worker，而不是在 handler 里创建全局可变对象。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`Actix Web` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
