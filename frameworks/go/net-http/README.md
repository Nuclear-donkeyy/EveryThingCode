# net/http

`net/http` 是 Go 标准库里的 HTTP 基础设施。它不是“框架中的框架”，而是一组足够稳定、足够小的接口和工具：`http.Handler`、`http.HandlerFunc`、`http.ServeMux`、`http.Server`、`http.Client`、`httptest`。很多 Go Web 框架最终仍然会落回这些标准抽象。

## 核心定位

`net/http` 解决的是 HTTP 服务最基础的问题：监听端口、接收请求、匹配路由、读写 header/body、管理连接、设置超时、构造 client、测试 handler。它适合教学、轻量 API、内部服务、代理、健康检查、Webhook、微服务入口，以及那些希望完全掌控依赖边界的项目。

它不替你解决 ORM、配置中心、依赖注入、参数验证、OpenAPI、认证授权和项目分层。也正因为它“不多管”，Go 项目常常把 `net/http` 当作稳定边界，在其上组合中间件、业务 service、repository、日志和配置。

## 设计思想

`net/http` 的核心思想是接口小、组合强、依赖显式。

`http.Handler` 只有一个方法：`ServeHTTP(http.ResponseWriter, *http.Request)`。任何实现了这个方法的对象都可以处理请求。普通函数也可以通过 `http.HandlerFunc` 变成 handler。这让 handler 可以是闭包、结构体方法，也可以是带依赖的对象方法。

路由由 `ServeMux` 负责。Go 1.22 之后，标准 `ServeMux` 支持带方法的 pattern，例如 `GET /tasks/{id}`，并能通过 `r.PathValue("id")` 读取路径参数。对于教学项目，这已经足够表达 REST API 的基本结构。

中间件本质上是 `func(http.Handler) http.Handler`：接收下一个 handler，返回一个新的 handler。日志、恢复、超时、认证、CORS、request id 都可以用同一种方式串起来。这个模型不需要框架容器，也不需要隐藏生命周期，读代码时可以沿着函数包装顺序一路追下去。

依赖通常显式注入。示例里 `app` 持有 `Store` 和 `Logger`，`newServer` 把它们装配到 handler 上。业务函数不主动去全局变量里找数据库或配置，这样测试时可以替换为内存实现或 fake 实现。

`context.Context` 是跨边界取消和超时的统一信号。HTTP 请求自带 context，客户端断开、服务端超时或上游取消时，业务层可以通过 `r.Context()` 感知。Go Web 项目里，context 应该传递取消、deadline、trace/request id 等请求级信息，不应该塞进大块业务对象。

## 架构模型

一个标准库 Web 服务通常可以拆成几层：

- 入口层：`main` 读取配置、创建依赖、构造 `http.Server`，负责启动和关闭。
- 路由层：`ServeMux` 注册 URL pattern 到 handler。
- 适配层：handler 解析 HTTP 输入，调用业务对象，把结果编码为 HTTP 响应。
- 业务层：service/store 使用普通 Go 类型，不依赖 `http.ResponseWriter`。
- 中间件层：围绕 handler 添加横切能力，例如日志、恢复、超时。
- 测试层：使用 `httptest.NewRecorder` 和 `httptest.NewRequest` 直接测试 handler，不必真的打开端口。

示例为了让所有内容可读，把这些内容放在一个 `main.go` 里，但仍然保持边界清晰。真实项目中可以拆成 `cmd/server`、`internal/httpapi`、`internal/task`、`internal/config`、`internal/store` 等包。

## 请求/执行生命周期

一次请求的路径大致是：

1. `http.Server` 从监听 socket 接收连接，解析 HTTP 请求。
2. `Server.Handler` 接管请求；如果使用示例代码，就是经过中间件包装后的 mux。
3. `timeoutMiddleware` 给请求 context 加上 deadline，并把新 context 放回 `*http.Request`。
4. `loggingMiddleware` 记录方法和路径，再调用下一个 handler。
5. `recoverMiddleware` 捕获 panic，避免单个请求把进程打垮。
6. `ServeMux` 根据方法和路径找到具体 handler。
7. handler 读取路径参数或 JSON body，调用 `Store`。
8. handler 通过 `writeJSON` 或 `http.Error` 写回响应。

这条链路里最重要的思想是“请求对象一路传递，依赖对象提前组装”。Go 不鼓励在 handler 内部临时创建数据库连接、日志器或配置对象。

## 工程结构

本仓库案例目录：

```text
frameworks/go/net-http/examples/quickstart/
├── README.md
├── go.mod
├── main.go
└── main_test.go
```

`main.go` 包含入口、路由、中间件、内存 store 和响应工具。`main_test.go` 用 `httptest` 覆盖健康检查、列表、创建和状态更新。`go.mod` 声明模块和 Go 版本，不需要任何第三方依赖。

真实项目扩展时，建议把 HTTP 和业务拆开：handler 只做协议适配，service 只接收普通参数和 context，repository 负责数据访问。这样将来从 `net/http` 换到 Gin、Echo 或 gRPC 时，业务层不会被重写。

## 配置方式

最小配置可以先用环境变量表达，例如示例读取 `PORT`，未设置时使用 `8080`。在更大的项目中，常见策略是：

- 启动配置放在环境变量或配置文件里，入口层读取后转成强类型结构体。
- `http.Server` 显式设置 `ReadHeaderTimeout`、`ReadTimeout`、`WriteTimeout`、`IdleTimeout`，避免慢请求拖垮服务。
- 日志、数据库、外部 client 在启动阶段创建，再通过结构体传入 handler。
- 不在业务函数里读取环境变量，避免测试和复用困难。

## 模块与依赖管理

Go 使用 `go.mod` 管理模块。`net/http` 属于标准库，所以示例没有第三方依赖。依赖管理的重点不是“安装框架”，而是给每个边界设计合适的接口。

在标准库风格里，依赖通常通过构造函数显式传递：

- `NewStore()` 创建数据层。
- `newServer(store, logger)` 装配路由和中间件。
- handler 方法挂在 `app` 上，因此可以访问 `app.store` 和 `app.logger`。

这种方式看起来朴素，但非常可靠。项目变大后，可以继续手写装配，也可以引入 Wire 做编译期依赖注入；只有在生命周期和模块关系复杂到手写装配明显吃力时，再考虑 Fx 这样的运行期容器。

## 数据访问

示例使用内存 map 存储任务，目的是把注意力放在 HTTP 边界。内存 store 加了 mutex，因为 HTTP server 会并发处理请求。即使是教学项目，也要让读者看到共享状态和并发访问的关系。

接入数据库时，常见路径是：

- 定义业务需要的接口，例如 `TaskStore`。
- handler 或 service 只依赖接口，不依赖具体 ORM。
- 用 GORM、Ent、database/sql 或外部 API 实现接口。
- 把事务边界放在 service 或 repository，而不是散落在 handler 中。

`context.Context` 应继续向下传给数据库查询或外部 HTTP 调用，这样请求取消时下游也能尽快停止。

## 测试方式

`net/http` 的测试体验很好，因为 handler 是普通对象。常见测试层次：

- handler 单元测试：`httptest.NewRequest` + `httptest.NewRecorder`，验证状态码和 JSON。
- 中间件测试：构造一个假的下游 handler，验证 header、日志、错误恢复等行为。
- service/store 测试：不涉及 HTTP，只测业务规则和并发安全。
- 端到端 smoke test：用 `httptest.NewServer` 启动真实 HTTP server，再用 `http.Client` 请求。

示例使用第一种方式，因此 `go test ./...` 不需要监听端口，也不需要外部服务。

## 部署方式

标准库服务部署非常直接。常见流程是 `go test ./...`、`go build -o app .`，然后把二进制放进 VM、容器或平台运行。容器镜像可以使用多阶段构建：第一阶段用 Go 镜像编译，第二阶段用 distroless、alpine 或 scratch 承载二进制。

生产环境需要补齐优雅停机：监听 SIGTERM/SIGINT，调用 `server.Shutdown(ctx)`，给正在处理的请求一点时间完成。还需要配置超时、日志、指标、健康检查和 readiness endpoint。

## 适用场景与取舍

优先选择 `net/http` 的场景：

- 想理解 Go Web 底层模型。
- API 较小，路由和绑定需求不复杂。
- 团队希望减少第三方依赖。
- 业务层需要长期稳定，不想被框架抽象绑住。
- 需要写中间件、代理、Webhook 或内部工具。

考虑引入 Gin、Echo、Chi 等框架的场景：

- 路由分组、参数绑定、验证、错误响应已经反复手写。
- 团队需要更统一的 API 约定。
- 需要大量中间件生态和快速交付。

`net/http` 的取舍是：少魔法、可控、稳定，但你需要自己组织工程结构和重复模式。

## 案例索引

- [quickstart](examples/quickstart/)：用标准库实现一个任务 API，包含健康检查、任务列表、创建任务、完成任务和 HTTP 测试。

## 版本来源

- 语言基线：Go 1.26.3，按本仓库 `versions.yaml` 记录。
- 框架基线：Go standard library，无单独框架版本。
- 官方来源：https://pkg.go.dev/net/http
- Go 发布来源：https://go.dev/doc/devel/release
- 校验日期：2026-05-30
