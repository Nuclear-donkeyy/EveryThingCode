# Go 特性与思想辅助教学

## 如何使用

本模块把 Go 的语言思想和可运行例子放在一起学习。建议先通读“思想总览”和“核心特性地图”，再进入 `examples/` 下的目录逐个运行。每个例子都可以在自己的目录中执行 `go run main.go`，不需要外部依赖。

学习时不要只看输出是否正确，更要观察代码边界：数据如何流动，错误在哪里被补充上下文，goroutine 什么时候退出，接口由谁定义。Go 的很多设计不是为了写出最短代码，而是为了让团队在长期维护中更容易看懂控制流和资源生命周期。

## 思想总览

Go 偏向“少机制、清晰边界、组合优先”。它没有类继承层级，也不鼓励用复杂语法隐藏控制流。普通函数、struct、接口、goroutine、channel 和标准库工具组合起来，覆盖了大多数工程场景。

这种取舍解决的是多人协作里的可读性问题：代码读者不必追踪隐式继承、异常跳转或宏展开，通常可以顺着函数返回值、接口方法和 channel 收发关系理解系统。代价是某些抽象写起来更直接甚至更啰嗦，学习者要接受 Go 把错误、取消和资源释放摆到明面上。

## 核心特性地图

### 简单语法与组合优先

它解决的问题是：当项目变大时，继承树和过度抽象会让行为来源难以追踪。Go 用 struct 嵌入、接口字段、函数拆分和小包组织来组合能力，让依赖关系尽量显式。

Go 选择这种方式，是因为它面向长期运行的服务、命令行工具和基础设施代码。可维护性常常比表达式级别的简短更重要。学习者应该观察 `examples/interfaces-composition/`：服务只依赖一个小接口和一个日志接口，具体实现可以替换，但调用路径仍然直观。

### 接口的隐式实现

它解决的问题是：调用方只关心“这个值能做什么”，不应被迫依赖实现方提前声明的继承关系。Go 中一个类型只要拥有接口要求的方法，就自动满足接口。

Go 这样设计，是为了鼓励从使用者视角定义小接口。接口不必放在实现包里，也不需要 `implements` 关键字。学习者应该观察 `examples/interfaces-composition/`：`EmailNotifier` 没有声明自己实现了 `Notifier`，但可以被注入到 `Service` 中。

### goroutine 和 channel

它解决的问题是：网络服务、后台任务和流水线经常要同时等待多个 IO 结果。Go 用轻量 goroutine 表示并发执行，用 channel 表示值的交接、同步点或事件流。

Go 选择把并发作为语言和运行时的一等能力，而不是完全交给外部框架，是因为服务端程序里并发是常态。学习者应该观察 `examples/goroutines-channels/`：主 goroutine 负责投递任务和关闭输入，worker 只从 channel 取任务并把结果发回，所有权边界比共享变量更清楚。

### context 取消

它解决的问题是：请求超时、用户断开连接或上游失败时，后台工作必须及时停止，否则 goroutine、文件句柄和网络连接会泄漏。Go 用 `context.Context` 传递取消、截止时间和请求范围内的值。

Go 不把取消做成隐藏的全局状态，而是把 `context` 作为参数显式传入边界函数。这样调用方能决定生命周期，被调用方能在 `select` 中响应 `ctx.Done()`。学习者应该观察 `examples/context-cancellation/`：任务每一步都检查取消信号，超时后返回包装过的错误。

### 显式 error

它解决的问题是：失败路径如果靠异常在栈上隐式跳转，读者容易忽略哪些调用会失败。Go 把错误作为普通返回值，让调用点必须决定处理、包装还是向上传递。

Go 采用显式 `error`，是为了让控制流、资源释放和错误上下文都在代码中可见。代价是要写更多 `if err != nil`，但收益是边界清晰。学习者应该观察 `examples/interfaces-composition/` 和 `examples/context-cancellation/`：前者在发送失败时用 `%w` 包装错误，后者保留 `context deadline exceeded`，便于上层用 `errors.Is` 判断原因。

## 教学例子索引

- [interfaces-composition](examples/interfaces-composition/)：用小接口、struct 组合和显式 error 表达可替换依赖。
- [goroutines-channels](examples/goroutines-channels/)：用 worker、job channel 和 result channel 观察并发协作。
- [context-cancellation](examples/context-cancellation/)：用 `context.WithTimeout` 控制后台任务生命周期。

## 学习检查

- 你能说清楚接口为什么通常由使用方定义，而不是由实现方集中声明吗？
- 你能指出例子中哪个 goroutine 负责关闭哪个 channel，以及为什么接收方不随意关闭输入 channel 吗？
- 你能解释 `context` 取消信号如何从调用方传到工作函数吗？
- 你能在错误输出中保留底层原因，同时给上层补充业务上下文吗？
- 你能把一个新通知实现接入 `interfaces-composition`，而不修改 `Service` 的核心逻辑吗？
