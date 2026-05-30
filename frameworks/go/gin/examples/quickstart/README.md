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

`main` 设置 Gin mode、创建内存 store、调用 `setupRouter`，然后把 router 放进 `http.Server`。这样可以继续使用标准库的超时、监听和优雅停机能力。

`setupRouter` 创建 `gin.Engine`，注册 `requestIDMiddleware`、`gin.Logger()`、`gin.Recovery()`。随后用 `router.Group("/api")` 创建路由组，并把 health 和 tasks API 放进去。

`createTask` 展示绑定和验证。`CreateTaskInput` 的 tag 是 `json:"title" binding:"required,min=3"`，因此 JSON 字段名和验证规则都写在 DTO 上。绑定失败时 handler 直接返回 `400`。

`markTaskDone` 展示路径参数。Gin 路径里写 `:id`，handler 里用 `c.Param("id")` 读取，再转换为整数。

`Store` 仍然是普通 Go 类型。它不知道 Gin 的存在，只处理任务数据。handler 把 `c.Request.Context()` 传给 store，让业务层仍能感知请求取消。

`main_test.go` 使用 `performRequest` helper 构造请求。测试覆盖了成功路径和验证失败路径，能帮你确认中间件、路由、绑定和响应都串起来了。

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
