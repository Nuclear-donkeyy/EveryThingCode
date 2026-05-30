# Gin quickstart

这个案例用 Gin 实现一个最小任务 API。它与 `net/http` quickstart 处理类似业务，但写法更框架化：路由分组、中间件链、`gin.Context`、JSON 绑定和字段验证都由 Gin 提供统一入口。

## 目标

完成本案例后，你应该能：

- 用 `gin.New()` 创建 router，并通过 route group 组织 `/api` 路由。
- 编写 Gin 中间件，理解 `c.Next()`、`c.Abort()` 和响应写入的关系。
- 使用 `ShouldBindJSON` 把请求体绑定到 DTO，并通过 `binding` tag 做基础验证。
- 通过 `c.Param` 读取路径参数，通过 `c.JSON` 输出结构化响应。
- 在测试中用 `httptest` 直接调用 `gin.Engine`。

## 学习重点

重点观察 `setupRouter`。它把 request id、日志、恢复中间件挂到 router 上，再创建 `/api` 分组，最后注册业务路由。Gin 的路由树和分组让相关 API 更容易集中管理，尤其是版本前缀、认证和中间件不同的场景。

另一个重点是框架边界。handler 使用 `*gin.Context`，但 store 方法只接收普通参数和 `context.Context`。这样业务层不会直接依赖 Gin，将来改成标准库、gRPC 或命令行入口时，核心逻辑仍可复用。

## 这个案例解决什么问题

这个 quickstart 和 `net/http` quickstart 处理的是同一类任务 API，目的不是证明标准库不够用，而是让你看到 API 复杂度升高后哪些重复工作会出现。

如果用标准库手写同样的 API，你通常需要自己完成这些事情：

- 为 `/api`、`/api/tasks`、`/api/tasks/{id}/done` 维护路由注册和公共前缀。
- 给每个 handler 手写 JSON 解码、字段校验、错误结构和响应 header。
- 在每个需要路径参数的地方读取字符串、转换为整数、处理非法 id。
- 用 `func(http.Handler) http.Handler` 组合 request id、日志、恢复等中间件，并手写提前返回规则。
- 在测试里自己保证路由、中间件、响应编码都被覆盖到。

Gin 把这些重复点收进几个统一概念：`gin.Engine` 承载整棵路由树，`RouterGroup` 承载公共前缀，`gin.Context` 承载请求和响应工具，`ShouldBindJSON` 承载 JSON 绑定和基础验证，middleware chain 承载横切逻辑。这个案例故意保留一个很小的 `Store`，让你能清楚看到 Gin 只负责 HTTP 适配层，业务数据仍然由普通 Go 类型管理。

## 工程结构

```text
.
├── go.mod        # 声明 Gin 依赖
├── main.go       # 入口、router、中间件、DTO、store、handler
└── main_test.go  # 使用 httptest 验证 Gin 路由和绑定
```

示例为了可读性放在一个 package 中。真实项目建议把 Gin 相关代码放到 `internal/httpapi`，把业务对象放到 `internal/task`，把数据库实现放到 `internal/store`。

## 运行前提

- 安装 Go，并尽量使用本仓库 `versions.yaml` 记录的 Go 版本基线。
- 首次运行需要联网下载 Gin 依赖，或使用本地已有的 Go module cache。

## 运行

先下载依赖并运行测试：

```bash
go test ./...
```

启动服务：

```bash
go run .
```

另开一个终端请求接口：

```bash
curl -s http://localhost:8080/api/health
curl -s http://localhost:8080/api/tasks
curl -s -X POST http://localhost:8080/api/tasks -H 'Content-Type: application/json' -d '{"title":"learn Gin binding"}'
curl -s -X PATCH http://localhost:8080/api/tasks/1/done
```

验证绑定失败：

```bash
curl -s -i -X POST http://localhost:8080/api/tasks -H 'Content-Type: application/json' -d '{"title":""}'
```

## 预期输出

`go test ./...` 应看到类似：

```text
ok  	example.com/everythingcode/go/gin-quickstart
```

`GET /api/health` 返回：

```json
{"status":"ok"}
```

`POST /api/tasks` 在 title 长度足够时返回 `201 Created` 和任务 JSON；title 为空或太短时返回 `400 Bad Request`，响应中包含 `error` 字段。

## 代码讲解

`main` 设置 Gin mode、创建内存 store、调用 `setupRouter`，然后把 router 放进 `http.Server`。这里有一个重要边界：Gin 负责 handler、路由和中间件，连接管理、读写超时、监听端口仍然交给标准库。也就是说，引入 Gin 不等于离开 Go 的 HTTP 基础设施。

`setupRouter` 创建 `gin.Engine`，注册 `requestIDMiddleware`、`gin.Logger()`、`gin.Recovery()`。这一步对应标准库里反复包装 handler 的中间件链。区别是 Gin 中间件共享 `*gin.Context`，可以通过 `c.Next()` 放行后续 handler，通过 `c.Abort()` 阻止后续 handler，通过 `c.Header` 和 `c.Set` 写入请求级信息。

随后 `setupRouter` 用 `router.Group("/api")` 创建路由组，并把 health 和 tasks API 放进去。对照标准库时，可以把 `RouterGroup` 理解为“公共前缀加公共规则”的组合。以后如果 `/api` 下所有接口都要鉴权，可以把认证中间件挂在这个 group 上，而不需要改每一条路由。

`health` 展示最小响应。标准库通常要设置 header、状态码，再用 encoder 写 JSON；Gin 用 `c.JSON(http.StatusOK, gin.H{"status": "ok"})` 把这几步合成一个框架动作。`gin.H` 只是 `map[string]any` 的便捷别名，适合简单响应；复杂响应仍建议定义结构体。

`listTasks` 展示框架边界。handler 接收 `*gin.Context`，但调用 store 时传的是 `c.Request.Context()`，也就是标准库的 `context.Context`。这样 store 可以感知客户端取消或服务端超时，却不需要导入 Gin。这个边界非常关键：Gin 类型留在 HTTP 适配层，业务层保持可测试、可复用。

`createTask` 展示绑定和验证。`CreateTaskInput` 的 tag 是 `json:"title" binding:"required,min=3"`，因此 JSON 字段名和验证规则都写在 DTO 上。`c.ShouldBindJSON(&input)` 做了两件事：把请求体解码到结构体，并执行 tag 上的基础验证。绑定失败时 handler 返回 `400` 和 JSON 错误；绑定成功后再调用 `store.Create` 执行业务创建。对照标准库，这里省掉了手写 decoder、检查空标题、统一 JSON 错误格式的一部分样板。

`markTaskDone` 展示路径参数。Gin 路径里写 `:id`，handler 里用 `c.Param("id")` 读取，再用 `strconv.Atoi` 转成整数。Gin 负责把路由参数从 path 中提取出来，但“id 必须是正整数”和“不存在返回 404”仍然是 handler 和业务层的责任。这个分工能避免误解：框架解决协议读取问题，不替你决定业务语义。

`requestIDMiddleware` 展示中间件链。它先从请求头读取 `X-Request-ID`，没有就生成一个，再写入 `c.Set("request_id", requestID)` 和响应 header，最后调用 `c.Next()`。这和标准库中间件的思想相同，都是在业务 handler 前后插入横切逻辑；Gin 的不同点是 request id、响应 header、后续链路控制都集中在 `gin.Context` 上。

`Store` 仍然是普通 Go 类型。它不知道 Gin 的存在，只处理任务数据。handler 把 `c.Request.Context()` 传给 store，让业务层仍能感知请求取消。它用 mutex 保护 map，因为 Gin 最终运行在 Go HTTP server 上，同样会并发处理多个请求。

`main_test.go` 使用 `performRequest` helper 构造请求。测试覆盖了成功路径和验证失败路径，能帮你确认中间件、路由、绑定和响应都串起来了。

## 与 net/http 对照

理解 Gin 最好的方式，是把它和标准库模型一一对应起来：

| 问题 | `net/http` 常见写法 | Gin 写法 | 取舍 |
| --- | --- | --- | --- |
| 整体入口 | `http.Server{Handler: mux}` | `http.Server{Handler: router}`，其中 router 是 `*gin.Engine` | Gin 仍然兼容标准库 server。 |
| 路由分组 | 手写公共 path 前缀，或封装注册函数 | `router.Group("/api")` | 分组更直观，但路由声明依赖 Gin API。 |
| 路径参数 | `r.PathValue("id")` | `c.Param("id")` | Gin 参数读取统一在 `Context`。 |
| JSON 绑定 | `json.NewDecoder(r.Body).Decode(&dto)` 后手写校验 | `c.ShouldBindJSON(&dto)` 加 `binding` tag | 基础验证更集中，复杂业务规则仍应放业务层。 |
| JSON 响应 | 设置 header、状态码、encoder | `c.JSON(status, value)` | handler 更短，但响应工具来自 Gin。 |
| 中间件 | `func(http.Handler) http.Handler` | `func(*gin.Context)` 加 `c.Next()` | Gin 更方便读取状态和控制链路，耦合也更强。 |
| 测试 | `handler.ServeHTTP(rec, req)` | `router.ServeHTTP(rec, req)` | 二者都不需要真实端口；Gin 能同时覆盖路由树和 binding。 |

这个对照也提示了学习重点：如果只是两个健康检查接口，`net/http` 更直接；如果 API 已经有成批路由、统一错误、绑定验证和多层中间件，Gin 能把重复模式压缩成框架约定。

## 延伸练习

- 给 `/api/tasks` 增加 `?done=true` 查询过滤，并思考查询参数应该在哪一层解析。
- 把绑定失败的错误改造成统一错误响应格式，例如 `{ "code": "VALIDATION_ERROR", "message": "..." }`。
- 把 `Store` 抽成接口，再用 GORM 或 Ent 实现持久化。

## 验收

完成后，你应该能说清楚：

- Gin 的 route group 和标准库 `ServeMux` 的差异。
- `gin.Context` 与标准库 `context.Context` 的区别，以及为什么业务层应该接收后者。
- `ShouldBindJSON`、结构体 tag、验证失败响应之间的关系。
- 如何用 `httptest` 测试 Gin router，而不启动真实端口。
