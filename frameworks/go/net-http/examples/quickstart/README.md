# net/http quickstart

这个案例用 Go 标准库实现一个最小任务 API。它故意不引入第三方框架，让你直接看到 handler、mux、中间件、context、显式依赖和 `httptest` 是怎样协作的。

## 目标

完成本案例后，你应该能：

- 用 `http.ServeMux` 注册带 HTTP method 和路径参数的路由。
- 编写 `http.Handler` 中间件，并理解包装顺序。
- 把 store/logger 作为显式依赖传入 handler，而不是放进全局变量。
- 在 handler 中使用 `r.Context()` 向业务层传递取消信号。
- 用 `httptest` 在不启动端口的情况下验证 API 行为。

## 学习重点

重点观察 `newServer`。它先创建 `ServeMux`，再注册 `GET /health`、`GET /tasks`、`POST /tasks`、`PATCH /tasks/{id}/done` 等路由，最后把 mux 交给中间件链。这个顺序就是标准库 Web 程序的核心结构：路由负责分发，中间件负责横切逻辑，handler 负责协议适配，store 负责数据。

另一个重点是 context。`timeoutMiddleware` 为每个请求设置 2 秒超时，handler 调用 store 时继续传入 `r.Context()`。真实数据库或外部服务可以沿用同一个 context，客户端断开或请求超时时，下游操作也能及时取消。

## 解决的问题

这个 quickstart 选择 `net/http`，不是因为它“功能最多”，而是因为它把 Web 服务的基础问题拆得很清楚。读这个案例时，可以把每段代码都对应到一个问题：

- HTTP 服务如何启动：`main` 构造 `http.Server`，把 `newServer(...)` 返回的 handler 交给 `Handler` 字段，并显式配置连接和读写超时。
- 请求如何分发：`newServer` 用 `http.NewServeMux()` 建路由表，通过 `mux.HandleFunc("GET /tasks", ...)` 绑定 method、path 和 handler。
- 路径参数如何读取：`markTaskDone` 使用 `r.PathValue("id")` 取得 `{id}`，再用 `strconv.Atoi` 转成业务需要的整数。
- JSON 输入输出如何处理：`createTask` 用 `json.NewDecoder(r.Body).Decode(&input)` 读请求体，`writeJSON` 统一设置 `Content-Type`、状态码和响应体。
- 公共逻辑如何复用：`timeoutMiddleware`、`recoverMiddleware`、`loggingMiddleware` 都包装 `http.Handler`，不用复制到每个 endpoint。
- 请求取消如何传递：handler 不创建新的后台 context，而是把 `r.Context()` 传给 `Store`。
- 如何测试完整 HTTP 行为：`main_test.go` 用 `httptest.NewRequest` 和 `httptest.NewRecorder` 直接驱动 handler，不需要监听真实端口。

标准库没有帮你做的部分也在案例里显式出现：title 是否为空要自己校验，JSON 错误响应要自己组织，路径 id 要自己转换，路由组和版本前缀也需要自己约定。小项目这样透明；如果 endpoint 很多，可以先抽出 `decodeJSON`、`writeError`、`parseID` 等 helper，再判断是否需要 Gin、Echo 或 Chi 这类框架。

## 设计思想

本案例的设计思想可以概括为“少数标准接口 + 普通 Go 代码”。`newServer` 不返回自定义框架对象，而是返回 `http.Handler`；这意味着它既能交给 `http.Server` 运行，也能交给 `httptest` 测试，还能继续被其他中间件包装。

`app` 结构体承担依赖边界。它只保存 `store` 和 `logger`，handler 作为 `app` 的方法存在。这样 `listTasks` 不需要全局变量，也不需要从某个框架容器里取对象；依赖在 `newServer` 中一次性装配，之后沿着方法接收者自然流动。

`Store` 代表业务数据边界。它接收普通 Go 参数和 `context.Context`，但不认识 `http.ResponseWriter`、`*http.Request` 或路由 pattern。这个取舍很关键：HTTP handler 负责协议，store 负责数据规则，两者通过普通类型交互。

middleware 体现组合思想。每个 middleware 都接收 `next http.Handler`，做完自己的事后调用 `next.ServeHTTP(w, r)`。因此它们可以重新排序、增删或替换。比如要增加认证，可以写成同样形状的 `authMiddleware`，然后在 `newServer` 中包到 mux 外面。

测试也遵循同一套设计。`TestTaskLifecycle` 不是手动调用 `createTask` 方法，而是通过 `handler.ServeHTTP(...)` 走完整路由和中间件链。这样一次测试能验证 method/path pattern、JSON 编解码、状态码、业务状态变化和响应内容是否协同正确。

## 工程结构

```text
.
├── go.mod        # Go module 声明；只依赖标准库
├── main.go       # 入口、路由、中间件、内存 store、响应工具
└── main_test.go  # 使用 httptest 验证 API
```

`main.go` 为了教学放在一个文件里，但代码内部仍然分成 `Store`、`app`、middleware、handler 和 JSON 工具函数。真实项目可以把这些拆到 `internal/task` 和 `internal/httpapi`。

## 运行前提

- 安装 Go，并尽量使用本仓库 `versions.yaml` 记录的 Go 版本基线。
- 当前案例不需要联网安装依赖，因为只使用标准库。

## 运行

先运行测试：

```bash
go test ./...
```

启动服务：

```bash
go run .
```

另开一个终端请求接口：

```bash
curl -s http://localhost:8080/health
curl -s http://localhost:8080/tasks
curl -s -X POST http://localhost:8080/tasks -H 'Content-Type: application/json' -d '{"title":"read net/http"}'
curl -s -X PATCH http://localhost:8080/tasks/1/done
```

可以通过环境变量修改端口：

```bash
PORT=9090 go run .
```

## 预期输出

`go test ./...` 应看到类似：

```text
ok  	example.com/everythingcode/go/net-http-quickstart
```

`GET /health` 返回：

```json
{"status":"ok"}
```

`GET /tasks` 返回任务数组。`POST /tasks` 成功时返回 `201 Created` 和新任务 JSON；title 为空时返回 `400 Bad Request`。

## 代码讲解

`main` 是入口：创建 logger 和内存 store，调用 `newServer` 得到 handler，再构造 `http.Server`。生产代码里应继续补齐优雅停机，本案例先聚焦请求处理。

`newServer` 是装配函数。它创建 `app`，注册路由，再把 mux 包进 `timeoutMiddleware`、`recoverMiddleware`、`loggingMiddleware`。因为每个中间件都是 `func(http.Handler) http.Handler`，所以组合关系非常直接。注意包装顺序：代码最后返回的是 logging 包住 recover，recover 包住 timeout，timeout 再包住 mux；请求进入时会先经过日志层，再经过恢复层，再获得带 deadline 的 context，最后由 mux 找到具体 handler。

`Store` 模拟数据访问层。它用 mutex 保护 map，因为 HTTP server 会并发处理请求。方法接收 `context.Context`，虽然内存操作暂时不会阻塞，但接口形状已经和数据库/外部服务保持一致。`List` 按 id 顺序复制任务切片，避免把内部 map 暴露给外部；`Create` 负责 title 修剪和业务校验；`MarkDone` 用 `(Task, bool, error)` 同时表达结果、不存在和执行错误。

handler 方法只做 HTTP 适配：读取 JSON、解析路径参数、调用 store、写 JSON。比如 `createTask` 只关心请求体能否解码，title 是否有效交给 `Store.Create`；`markTaskDone` 只把 `r.PathValue("id")` 转成整数，任务是否存在交给 `Store.MarkDone`；响应由 `writeJSON` 或 `http.Error` 统一写回。

`writeJSON` 是一个很小的响应 helper。标准库不会替你规定响应格式，所以案例先统一 JSON 成功响应；真实项目通常还会补一个 `writeError`，把错误码、错误消息、trace id 和校验细节统一起来。

`main_test.go` 不启动真实端口，而是直接调用 handler。`TestTaskLifecycle` 先请求 `/health` 验证基础路由，再创建任务、解码响应、调用 `PATCH /tasks/1/done`，覆盖了一条真实业务链路。`TestCreateTaskRequiresTitle` 则验证错误输入会返回 `400 Bad Request`，说明标准库测试也可以覆盖校验和错误响应。

## 延伸练习

- 把 `Store` 抽成接口，再写一个基于 `database/sql` 的实现。
- 给每个请求生成 request id，并在响应 header 和日志中同时输出。
- 增加 `DELETE /tasks/{id}`，思考不存在的 id 应返回 `404` 还是幂等成功。

## 验收

完成后，你应该能说清楚：

- `http.Handler`、`http.HandlerFunc`、`ServeMux` 分别承担什么职责。
- 标准库中间件为什么是包装 handler 的函数。
- 为什么业务层接收 `context.Context`，但不应该依赖 `http.ResponseWriter`。
- 如何在不监听端口的情况下测试 HTTP handler。
