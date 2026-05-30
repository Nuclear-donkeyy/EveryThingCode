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

`newServer` 是装配函数。它创建 `app`，注册路由，再把 mux 包进 `timeoutMiddleware`、`recoverMiddleware`、`loggingMiddleware`。因为每个中间件都是 `func(http.Handler) http.Handler`，所以组合关系非常直接。

`Store` 模拟数据访问层。它用 mutex 保护 map，因为 HTTP server 会并发处理请求。方法接收 `context.Context`，虽然内存操作暂时不会阻塞，但接口形状已经和数据库/外部服务保持一致。

handler 方法只做 HTTP 适配：读取 JSON、解析路径参数、调用 store、写 JSON。比如 `createTask` 只关心请求体是否合法，业务数据由 store 创建，响应由 `writeJSON` 统一编码。

`main_test.go` 不启动真实端口，而是直接调用 handler。这样测试快、稳定，也能覆盖中间件和路由匹配。

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
