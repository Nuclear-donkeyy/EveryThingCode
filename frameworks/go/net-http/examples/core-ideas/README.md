# Go net/http core ideas example

## 目标

这个示例把 `Go net/http` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

不用第三方框架时也需要可靠处理 Handler 协议、路由、middleware、context 和测试。

## 核心思想到代码

http.Handler 是统一协议，ServeMux 做最小路由，middleware 通过函数包裹组合，httptest 复用真实处理链路。

```go
mux := http.NewServeMux()
mux.HandleFunc("GET /tasks", app.listTasks)
mux.HandleFunc("POST /tasks", app.createTask)
```

```go
func timeoutMiddleware(next http.Handler) http.Handler {
  return http.TimeoutHandler(next, 2*time.Second, "timeout")
}
```

## 代码位置

- [`main.go`](../quickstart/main.go)
- [`main_test.go`](../quickstart/main_test.go)

## 运行

先进入 quickstart 目录：

```bash
cd ../quickstart
go test ./...
```

如果本机缺少对应工具链，可以先运行仓库根目录的 dry-run：

```bash
python3 scripts/run_framework_examples.py --dry-run
```

## 观察点

测试直接调用 server，不需要真实监听端口，说明 HTTP 处理器本身就是可测试对象。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`Go net/http` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
