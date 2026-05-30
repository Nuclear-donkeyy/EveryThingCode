# Context Cancellation

## 目标

这个例子展示 `context.Context` 如何把调用方的超时传递给后台工作。`runReport` 每完成一步都会继续检查 `ctx.Done()`，一旦超时就停止工作并返回带上下文的错误。

真实服务中，HTTP 请求、数据库查询、RPC 调用和后台任务都需要类似的取消链路，否则调用方已经放弃后，后台 goroutine 仍可能继续占用资源。

## 运行

```bash
go run main.go
```

## 观察点

- `defer cancel()` 明确释放 timer 资源，即使函数提前返回也会执行。
- `select` 同时等待工作计时器和取消信号，避免只顾工作而错过超时。
- `errors.Is(err, context.DeadlineExceeded)` 能识别被包装的超时原因。
