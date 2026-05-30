# Rust 框架与常用库

Rust 的框架生态不像 Java 或 .NET 那样由单一“大框架”统治，而是更偏向“选择一组可靠组件，然后显式组合”：异步运行时、HTTP 路由、序列化、数据库、CLI、桌面 UI、游戏引擎通常分别选型。学习 Rust 框架时，先理解所有权、类型系统、错误处理和 `async/await`，再看框架如何把这些能力组织成工程结构。

## 常用框架清单

| 方向 | 框架/库 | 本仓库状态 | 适合学习的核心问题 |
| --- | --- | --- | --- |
| Web API | [Axum](axum/) | 已覆盖 | 如何用 Router、Extractor、State 和 Tower 中间件组合类型安全 HTTP 服务。 |
| Web API | [Actix Web](actix-web/) | 已覆盖 | 如何用 App、Scope、Handler、Data 组织高性能服务，以及 Actix actor 历史对设计的影响。 |
| Web API | Rocket | 待扩展 | 宏驱动路由、请求守卫、声明式 API 与稳定性取舍。 |
| Web API | Warp | 待扩展 | Filter 组合、函数式路由和类型推导。 |
| 异步运行时 | Tokio | 案例中使用 | Rust 异步任务、I/O、定时器、通道和运行时调度。 |
| 序列化 | Serde | 案例中使用 | JSON/配置/消息协议如何通过 derive 映射为强类型数据。 |
| SQL 数据访问 | SQLx | 待扩展 | 异步 SQL、编译期查询检查、连接池和迁移。 |
| ORM | Diesel | 待扩展 | 强类型查询 DSL、schema 生成和同步数据访问模型。 |
| 桌面应用 | Tauri | 待扩展 | Rust 后端加 Web 前端的跨平台桌面应用。 |
| 游戏 | Bevy | 待扩展 | ECS、系统调度、资源和插件化游戏架构。 |
| CLI | Clap | 待扩展 | 命令、子命令、参数校验和帮助文档生成。 |

## 选择思路

如果目标是学习现代 Rust Web API，优先从 Axum 开始。Axum 与 Tokio、Hyper、Tower 同源，设计风格非常“Rust”：状态显式传递，处理函数通过 extractor 表达输入，返回值通过 trait 转换成响应，很多错误可以在编译期暴露。

如果目标是做成熟、高性能、资料多的生产 Web 服务，可以同时学习 Actix Web。Actix Web 的 API 亲切、运行性能强，`App`、`Scope`、`web::Data`、handler attribute macro 上手快；理解它的 actor 历史，也能帮助你看懂它为什么重视 runtime、worker 和服务生命周期。

如果目标是数据库优先，Web 框架通常搭配 SQLx 或 Diesel：SQLx 更适合 async Web API，Diesel 更强调类型安全查询 DSL。若目标是 CLI 工具，Clap 通常比 Web 框架更先学习；若目标是桌面或游戏，则分别看 Tauri 和 Bevy。

## 学习路线

1. 先读 `languages/rust/README.md`，确认所有权、借用、`Result`、trait、泛型和 `async/await` 的基础。
2. 阅读本索引，明确 Rust 框架生态是“运行时 + 框架 + 序列化 + 数据访问”的组合式生态。
3. 学习 [Axum](axum/)：重点看 `Router`、extractor、共享状态和 Tower 思想。
4. 学习 [Actix Web](actix-web/)：重点看 `App`、`Scope`、handler、`web::Data` 和 worker 模型。
5. 运行两个 quickstart，用相同的内存 CRUD 场景比较两种框架的路由、状态和测试写法。
6. 后续扩展数据库时，优先把内存仓储抽成 trait，再分别接入 SQLx 或 Diesel。

## 本仓库案例

- [Axum quickstart](axum/examples/quickstart/)：使用 Tokio、Axum、Serde 和内存状态实现一个笔记 API。
- [Actix Web quickstart](actix-web/examples/quickstart/)：使用 Actix Web、Serde 和 `web::Data` 实现同样的笔记 API。

