# Gin

Gin 是 Go 生态里最常见的 Web API 框架之一。它保留了 Go Web 的 handler 思维，同时把路由树、路由分组、中间件链、请求上下文、JSON 绑定和响应工具做成了统一体验。对已经理解 `net/http` 的读者来说，Gin 最值得学习的是：它在哪些地方提高效率，又在哪些地方引入了框架耦合。

## 核心定位

Gin 主要解决 JSON API 和 HTTP 服务的工程效率问题。它适合后台服务、移动端/前端 API、小型微服务、BFF、Webhook 服务，以及需要快速组织路由和中间件的项目。

Gin 不负责数据库建模、业务分层、依赖注入、服务治理和配置中心。它也不是完整的企业应用框架。真实项目中，Gin 应该停留在 HTTP 适配层：解析请求、调用业务、组织响应；核心业务最好仍然使用普通 Go 类型和接口表达。

## 解决的问题

如果只用 `net/http`，一个任务 API 很快就会写出清晰但重复的样板代码：每个 handler 都要判断 method、解析路径、读取 JSON、设置 `Content-Type`、编码错误响应、串联日志和恢复中间件。Go 1.22 之后的 `ServeMux` 已经支持 method pattern 和路径参数，足够表达很多服务；但当 API 数量变多，重复点通常会集中在以下几类。

第一类是路由组织。标准库可以注册 `GET /tasks/{id}`，但版本前缀、管理后台前缀、认证中间件和业务路由之间的关系需要自己约定。项目里常见 `/api/v1`、`/admin`、`/webhook` 等分组，如果每条路由都手写完整 path，后期移动前缀或统一加认证会变得琐碎。Gin 用 `Engine` 表示整个 HTTP 入口，用 `RouterGroup` 表示带公共前缀和公共中间件的一组路由，让“这一批路由共享什么规则”直接出现在代码结构里。

第二类是输入解析和错误响应。标准库 handler 里通常要手写 `json.NewDecoder(r.Body).Decode(&input)`，再补字段校验、空 body 处理、`Content-Type` 约束和错误 JSON。Gin 的 `ShouldBindJSON` 把 JSON 解码和基础验证收进一个入口，结构体 tag 把字段名和约束放在 DTO 上。它不会替你设计业务规则，但能让“请求体不合法就返回 400”成为统一动作。

第三类是路径参数、查询参数和响应工具。标准库里路径参数来自 `r.PathValue("id")`，查询来自 `r.URL.Query()`，响应还要自己写 header 和 encoder。Gin 把这些聚合到 `*gin.Context`：`c.Param("id")` 读路径参数，`c.Query("done")` 读查询参数，`c.JSON(status, value)` 输出 JSON。结果是 handler 更短，读者可以把注意力放在协议适配和业务调用上。

第四类是中间件链。标准库中间件是 `func(http.Handler) http.Handler`，模型很稳定，但每个中间件都要自己决定如何包装、如何提前返回、如何在响应后记录状态码。Gin 中间件统一为 `gin.HandlerFunc`，通过 `c.Next()` 进入后续链路，通过 `c.Abort()` 停止后续 handler，并能从 `c.Writer.Status()` 读取响应状态。日志、恢复、request id、认证、限流可以挂在全局 router、某个 route group 或单条路由上。

第五类是测试入口。标准库和 Gin 都能用 `httptest`，差异在于 Gin 的测试通常围绕一个 `*gin.Engine` 展开。只要把 router 装配写成 `setupRouter(store)`，测试就能直接调用 `router.ServeHTTP(recorder, request)`，完整覆盖路由树、中间件、绑定和 handler，而不需要监听真实端口。

所以 Gin 解决的不是“Go 标准库不能写 Web 服务”，而是当 API 进入多路由、多中间件、多 JSON DTO、多错误格式时，把常见重复工作收束到一致的框架语义里。它提升的是 HTTP 适配层效率；业务层的建模、事务、权限和数据一致性仍然需要自己设计。

## 设计思想

Gin 的第一层思想是把 HTTP 入口显式建成一棵路由树。`gin.Engine` 同时实现了 `http.Handler`，因此最后仍然能交给标准库 `http.Server`；但在 Engine 内部，`router.GET`、`router.POST`、`group.PATCH` 会把 method/path 组织成适合快速匹配的结构。路径参数如 `/tasks/:id` 可以通过 `c.Param("id")` 获取。与 `net/http` 相比，Gin 更强调用框架方法声明路由，而不是直接围绕 `ServeMux` 和 `http.HandlerFunc` 组合。

第二层思想是把公共规则贴在最合适的层级上。全局中间件属于所有请求，例如 `gin.Recovery()`；路由组中间件属于一批 API，例如 `/api` 下的认证；单路由中间件属于某个危险操作，例如删除前的权限检查。`RouterGroup` 不是简单的字符串拼接，它表达的是“这些 handler 共享前缀和横切逻辑”。这能减少重复注册，也能让团队一眼看出 API 边界。

第三层思想是中间件链。Gin 中间件类型是 `gin.HandlerFunc`，它接收 `*gin.Context`，可以在调用 `c.Next()` 前后执行逻辑。日志、恢复、request id、认证、限流、CORS 都可以挂在全局 router、路由组或单个路由上。与标准库中间件相比，Gin 中间件直接操作 `gin.Context`，写法更集中，也更容易读取和修改响应状态；代价是中间件与 Gin 框架类型绑定更强。

第四层思想是 `gin.Context`。它封装了请求、响应 writer、路径参数、查询参数、绑定、响应方法和中间件控制能力。`gin.Context` 不是标准库的 `context.Context`，不要把它一路传进业务层或数据库；但可以通过 `c.Request.Context()` 获取标准 context，并继续传给 service、repository 或外部 client。这样 HTTP 层享受 Gin 的便利，业务层仍保持普通 Go 形状。

第五层思想是绑定和验证靠近 DTO。`ShouldBindJSON` 可以把请求体绑定到结构体，结构体 tag 如 `json:"title" binding:"required,min=3"` 让字段名、必填规则和最小长度靠近输入模型。绑定失败时，handler 应返回清晰的 `400 Bad Request`。更复杂的跨字段规则、权限规则和状态迁移规则仍应放在业务层，避免把业务语义塞进 HTTP tag。

Gin 的常见工程取舍是：handler 层更短，约定更集中；但如果业务层直接接收 `*gin.Context`，将来测试、复用和换框架都会变难。因此示例让 store 方法接收普通参数，只有 handler 使用 Gin 类型。

## 架构模型

一个 Gin API 项目通常由以下部分组成：

- 入口层：`main` 创建依赖、调用 `setupRouter`、启动 HTTP server。
- Router：`gin.Engine` 是整个服务的路由入口。
- Route group：用 `/api`、`/admin`、`/v1` 等分组承载公共前缀和公共中间件。
- Middleware：全局或分组添加日志、恢复、request id、认证等横切能力。
- Handler：使用 `*gin.Context` 读取参数、绑定 JSON、调用业务、写响应。
- Service/store：使用普通 Go 类型，避免依赖 Gin。
- Test：用 `httptest` 对 `gin.Engine` 发请求。

示例把这些内容放在一个 `main.go` 里，方便完整阅读。真实项目可以拆成 `cmd/api`、`internal/httpapi`、`internal/task`、`internal/config`、`internal/middleware`。

## 请求/执行生命周期

一次 Gin 请求通常这样流动：

1. Go 的 HTTP server 接收请求并把它交给 `gin.Engine`。
2. Gin 在路由树中按 method/path 查找匹配项，例如 `POST /api/tasks`。
3. Gin 构造或复用 `gin.Context`，写入请求、writer、路径参数和 handler 链。
4. 全局中间件依次执行，例如 request id、日志、恢复。
5. 路由组中间件继续执行；如果中间件调用 `c.Abort()`，后续 handler 不再执行。
6. 最终 handler 调用 `ShouldBindJSON`、`c.Param`、`c.Query` 等读取输入。
7. handler 调用业务对象或 store；业务层使用 `c.Request.Context()` 接收取消信号。
8. handler 通过 `c.JSON` 写状态码和响应体。
9. 中间件在 `c.Next()` 之后可以记录耗时、状态码等后置信息。

理解这个生命周期后，调试 Gin 项目会清楚很多：请求没到 handler，多半是路由或中间件；绑定失败，看 DTO tag 和 Content-Type；响应重复写入，看中间件是否正确 abort。

## 工程结构

本仓库案例目录：

```text
frameworks/go/gin/examples/quickstart/
├── README.md
├── go.mod
├── main.go
└── main_test.go
```

`go.mod` 声明 Gin 依赖。`main.go` 包含 router、路由组、中间件、DTO、内存 store 和 handler。`main_test.go` 使用 `httptest` 测试 health check、创建任务、验证失败和状态更新。

真实项目扩展时，建议让 handler 依赖 service 接口，让 service 依赖 repository 接口。Gin 类型只出现在 HTTP 包里，业务包不导入 `github.com/gin-gonic/gin`。

## 配置方式

Gin 的配置通常分成三层：

- 框架模式：`gin.SetMode(gin.ReleaseMode)` 或环境变量 `GIN_MODE=release` 控制日志和调试行为。
- 服务配置：端口、超时、数据库连接、外部服务地址由环境变量或配置文件读取。
- 路由配置：中间件、路由组、静态文件、trusted proxies 等由代码装配。

示例保持最小配置：读取 `PORT`，未设置时使用 `8080`。生产项目还应显式配置 `http.Server` 的超时，并根据部署环境设置 trusted proxies，避免错误信任代理头。

## 模块与依赖管理

Gin 使用 Go module 管理依赖。示例的 `go.mod` 声明 `github.com/gin-gonic/gin v1.11.0`，学习时可按官方文档使用 `go get github.com/gin-gonic/gin@latest` 更新到当前稳定版本。

Gin 本身不提供依赖注入容器。依赖组织仍然建议使用 Go 的显式构造：

- `NewStore()` 创建数据依赖。
- `setupRouter(store)` 把依赖交给 handler 闭包或 `app` 结构体。
- 中间件通过函数返回 `gin.HandlerFunc`，需要依赖时通过闭包捕获。

当项目变大时，可以继续手写构造，也可以用 Wire 生成依赖装配代码。不要把业务依赖放到 `gin.Context` 的 key-value 存储里长期传递；那更适合 request id、认证主体等请求级信息。

## 数据访问

示例使用内存 store，便于读者集中理解 Gin 的请求绑定、路由参数和响应。内存 store 使用 mutex，因为 Gin 和标准库一样会并发处理请求。

接入数据库时，常见方案有：

- `database/sql`：最贴近标准库，适合明确控制 SQL。
- GORM：模型声明和 CRUD 上手快，适合常规业务系统。
- Ent：schema as code 和类型安全查询，适合希望把领域结构和查询约束显式化的团队。

无论选择哪种，推荐让 handler 调用 service，service 再调用 repository。数据库错误要在业务层归类，再由 handler 映射成 HTTP 状态码，避免把底层错误字符串直接暴露给客户端。

## 测试方式

Gin 测试一般不需要真正监听端口。可以把 `setupRouter` 暴露为函数，测试里用：

- `httptest.NewRecorder()` 捕获响应。
- `http.NewRequest()` 构造请求。
- `router.ServeHTTP(recorder, request)` 执行完整中间件和 handler 链。

需要注意的是 Gin 默认会输出调试日志，测试中可以设置 `gin.SetMode(gin.TestMode)` 并丢弃默认 writer，让测试输出更干净。示例覆盖了成功创建、校验失败、列表读取和更新状态。

## 部署方式

Gin 最终仍然是 Go HTTP 服务，部署路径与标准库类似：`go test ./...`、`go build -o app .`，然后在 VM、容器或平台运行。生产环境建议用自定义 `http.Server` 包住 `router`，设置超时并实现优雅停机。

容器化时使用多阶段构建即可。第一阶段编译静态或接近静态的 Go 二进制，第二阶段只放二进制和必要证书。部署到 Kubernetes 时通常补齐 `/healthz`、`/readyz`、结构化日志和指标。

## 适用场景与取舍

适合选择 Gin 的场景：

- 希望快速构建 JSON API。
- 路由分组、中间件、参数绑定和验证需求明确。
- 团队需要成熟生态和大量示例。
- 项目规模中小，HTTP 层复杂度高于纯业务逻辑。

需要谨慎的场景：

- 项目希望最大限度保持标准库抽象。
- 团队非常强调 handler 和业务层完全解耦。
- 需要强契约 RPC 或流式通信，此时 gRPC 可能更合适。
- 需要极简路由器而不想使用完整框架，可以看 Chi。

Gin 的核心取舍是：更快写出统一 API，但要主动管理框架边界。

## 案例索引

- [core-ideas](examples/core-ideas/)：把上一节“解决的问题”和“设计思想”映射到 quickstart 的关键代码片段。
- [quickstart](examples/quickstart/)：用 Gin 实现任务 API，展示路由组、中间件、`gin.Context`、JSON 绑定、验证和 HTTP 测试。

## 版本来源

- 语言基线：Go 1.26.3，按本仓库 `versions.yaml` 记录。
- 框架基线：Gin latest stable；示例 `go.mod` 当前声明 `github.com/gin-gonic/gin v1.11.0`。
- 官方文档：https://gin-gonic.com/docs/
- 官方仓库：https://github.com/gin-gonic/gin
- 校验日期：2026-05-30
