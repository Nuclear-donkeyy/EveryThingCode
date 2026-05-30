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

`AppState` 保存内存笔记和自增 ID。它被包进 `web::Data` 后，可以安全 clone 给每个 worker；handler 通过参数 `state: web::Data<AppState>` 获取共享依赖。

`configure_routes` 是路由装配函数。它把 `/api` 前缀做成 `Scope`，再把 `/notes` 和 `/notes/{id}` 注册进去。真实项目中，这类函数通常放在 `routes.rs`，便于按模块拆分 API。

`list_notes`、`get_note`、`create_note` 是 handler。Actix Web 会根据参数类型运行 extractor：`web::Path<u64>` 解析路径 ID，`web::Json<CreateNote>` 解析 JSON 请求体，`web::Data<AppState>` 提供共享状态。

测试使用 `actix_web::test` 初始化应用，不需要绑定真实端口。它适合验证路由、状态码、JSON body 和状态变化。

## 延伸练习

1. 为 `POST /api/notes` 增加标题不能为空的校验，并用 `HttpResponse::BadRequest()` 返回错误。
2. 增加 `DELETE /api/notes/{id}`，比较删除成功和不存在时的状态码设计。
3. 把内存仓储替换成 SQLx 连接池，并把数据库访问移动到 repository 层。

## 验收

完成后你应该能够：

- 解释 `HttpServer`、`App`、`Scope`、handler、extractor、`web::Data` 的职责。
- 修改 `/api` 前缀或新增路由，并知道应改 `configure_routes`。
- 运行 `cargo run` 和 `cargo test`。
- 说明为什么跨 worker 共享状态应在 `HttpServer::new` 闭包外创建，再在闭包内 clone。
