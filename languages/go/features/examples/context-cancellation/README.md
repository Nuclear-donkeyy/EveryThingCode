# Context Cancellation

## 目标

这个例子展示 `context.Context` 如何把调用方的超时传递给后台工作。`runReport` 每完成一步都会继续检查 `ctx.Done()`，一旦超时就停止工作并返回带上下文的错误。

真实服务中，HTTP 请求、数据库查询、RPC 调用和后台任务都需要类似的取消链路，否则调用方已经放弃后，后台 goroutine 仍可能继续占用资源。

## 特性说明

`context.Context` 是 Go 里跨 API 边界传递取消、截止时间和请求范围元数据的标准协议。它解决的真实问题是生命周期对齐：上游请求超时、用户断开连接、父任务失败时，下游的数据库查询、网络调用和内部计算应该尽快停下，而不是继续占用 goroutine、连接和 CPU。

如果不用 `context`，代码常见退化是每个包自定义一个 `stop chan struct{}` 或全局取消标志，最终边界之间难以组合；或者完全不处理取消，导致调用方已经返回错误，后台任务还在继续写日志、重试或持有连接。这个例子用 `context.WithTimeout` 创建截止时间，用 `ctx.Done()` 在 `select` 中响应取消，并用 `%w` 保留 `context.DeadlineExceeded`。

## 设计取舍

Go 把 `context` 显式放在函数参数里，通常作为第一个参数。这比隐式线程本地变量更啰嗦，但调用方和被调用方都能看见生命周期关系。它也提醒设计者：不是所有函数都需要 `context`，只有跨边界、可能阻塞、可能需要取消的操作才应该接收它。

`context` 不是业务参数袋。把用户 ID、配置对象或数据库连接塞进 context 会让依赖变得隐式，反而削弱 Go 追求的可读边界。`defer cancel()` 也是一个重要取舍：即使超时最终会发生，主动调用 cancel 仍能及时释放 timer 资源；在真实服务中，这种资源意识和错误路径一样重要。

## 运行

```bash
go run main.go
```

## 观察点

- `defer cancel()` 明确释放 timer 资源，即使函数提前返回也会执行。
- `select` 同时等待工作计时器和取消信号，避免只顾工作而错过超时。
- `errors.Is(err, context.DeadlineExceeded)` 能识别被包装的超时原因。
- 输出通常会完成前两步，然后在第三步附近报告 `report stopped`，这说明工作函数不是等全部完成后才发现超时。

## 延伸练习

- 把 timeout 从 `180*time.Millisecond` 改成 `400*time.Millisecond`，观察报告如何从失败变成完成。
- 删除 `ctx.Done()` 分支，比较超时后任务是否还能被温和停止。
- 把 `runReport` 改成接收一个子函数，例如 `func(context.Context, int) error`，模拟把同一个取消协议继续传给数据库或 HTTP 调用。
