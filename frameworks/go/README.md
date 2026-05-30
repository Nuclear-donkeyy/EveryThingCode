# Go 框架与常用库

Go 的框架生态有一个很鲜明的气质：标准库足够强，第三方框架通常是在路由、绑定、数据库、命令行、依赖组装这些边界上补齐工程效率。学习 Go 框架时，不要先追求“大而全”，而是先把 `context.Context`、显式依赖、接口组合、错误返回、HTTP handler 这些语言层思想看懂，再进入具体框架。

## 常用框架清单

| 方向 | 框架/库 | 常见用途 | 本仓库状态 |
| --- | --- | --- | --- |
| HTTP 标准库 | [`net/http`](net-http/) | 标准 HTTP server、handler、middleware、测试 | 已覆盖 |
| Web API | [`Gin`](gin/) | 高性能 JSON API、路由分组、中间件、绑定验证 | 已覆盖 |
| Web API | Echo | 轻量 API、路由、中间件、数据绑定 | 待扩展 |
| Web API | Fiber | 类 Express 风格 API、快速原型、fasthttp 生态 | 待扩展 |
| Web API | Chi | 标准库风格路由器、小而组合友好 | 待扩展 |
| RPC | gRPC | 强契约服务通信、IDL、流式调用、微服务 | 待扩展 |
| ORM | GORM | 活跃 ORM、模型关系、迁移、事务 | 待扩展 |
| ORM/Codegen | Ent | Schema as code、类型安全查询、代码生成 | 待扩展 |
| CLI | Cobra | 命令行程序、子命令、flag、脚手架 | 待扩展 |
| 依赖组装 | Fx / Wire | 运行期依赖容器或编译期依赖注入 | 待扩展 |
| 配置 | Viper | 配置文件、环境变量、flag 合并 | 待扩展 |
| 日志 | slog / zap / zerolog | 结构化日志、性能敏感服务日志 | 待扩展 |
| 测试 | testing / testify | 单元测试、断言、mock、suite | 待扩展 |

## 选择思路

如果目标是理解 Go Web 的底层模型，优先从 [`net/http`](net-http/) 开始。它展示了最核心的抽象：`Handler` 接收请求并写入响应，`ServeMux` 负责分发，中间件就是包装 `http.Handler` 的函数。理解这一层后，再看任何 Go Web 框架都会轻松很多。

如果目标是快速做 JSON API，可以进入 [`Gin`](gin/)。Gin 在标准库模型上提供了路由树、分组、中间件链、`gin.Context`、JSON 绑定和验证，适合业务 API、后台服务和小型微服务。它的代价是请求上下文、绑定逻辑和响应写入更多地围绕 Gin 的抽象展开，需要明确业务层不要依赖过深的框架类型。

如果团队偏好标准库组合，又希望路由更强，可以考虑 Chi；如果需要类 Express 的写法和很快的原型速度，可以考虑 Fiber；如果服务之间需要强契约和双向流，则用 gRPC；如果要处理数据库，GORM 适合快速上手，Ent 更强调 schema 和类型安全；如果写 CLI 工具，Cobra 是 Go 生态事实标准；如果项目依赖关系变复杂，再考虑 Wire 或 Fx，而不是一开始就引入容器。

## 学习路线

1. 先读 Go 语言章节，特别关注接口、错误处理、goroutine/channel、`context.Context`、模块管理和测试。
2. 阅读 [`net/http`](net-http/)：用标准库写一个能测试的 API，理解 handler、mux、中间件、显式依赖和 `httptest`。
3. 阅读 [`Gin`](gin/)：把同样的任务 API 改写成 Gin 风格，比较 `gin.Context`、路由分组、绑定验证和中间件链。
4. 回到业务边界：把 handler 中的内存 store 替换为接口，再接入 GORM、Ent 或外部服务。
5. 扩展到工程化：加入配置、日志、优雅停机、容器镜像、CI，以及按模块组织的测试。

## 本仓库案例

- [`net/http quickstart`](net-http/examples/quickstart/)：用标准库实现任务 API，包含 `go.mod`、`main.go` 和 `main_test.go`，适合学习最小 HTTP 工程边界。
- [`Gin quickstart`](gin/examples/quickstart/)：用 Gin 实现同样的任务 API，包含真实依赖声明、路由分组、绑定验证和 HTTP 测试，适合比较框架抽象带来的效率与边界。
