# Goroutines and Channels

## 目标

这个例子用两个 worker 处理一组任务，展示 goroutine 适合表达并发执行，channel 适合表达任务和结果的交接。主 goroutine 负责创建任务、关闭任务 channel，并在所有 worker 完成后关闭结果 channel。

重点不是“并发一定更快”，而是看清谁生产数据、谁消费数据、谁拥有关闭 channel 的责任。

## 特性说明

goroutine 是 Go 运行时调度的轻量执行单元，channel 是 goroutine 之间传递值和同步进度的语言级结构。真实工程里，后台任务、日志处理、消息消费、批量 IO 和流水线处理都需要“同时做几件事”，但共享变量和锁很容易把所有权搞乱。这个例子把任务放进 `jobs` channel，把结果放进 `results` channel，worker 不需要知道任务从哪里来，主流程也不需要知道每个 worker 的内部细节。

如果不用 goroutine/channel，这类代码常见退化是串行处理所有任务，吞吐量受单个任务延迟限制；或者手动共享一个任务列表，用锁、条件变量和状态标志协调，读者必须同时理解数据结构和并发协议。Go 的 channel 把“交接点”写进类型签名，`jobs <-chan Job` 表示 worker 只接收任务，`results chan<- Result` 表示 worker 只发送结果。

## 设计取舍

channel 适合表达所有权转移、事件流和背压，但不是所有并发问题都必须用 channel。简单共享计数器用 `sync.Mutex` 或 `atomic` 可能更直接；需要限制并发量时，也可以用 worker 池或带缓冲 channel。这个例子故意使用无缓冲 channel，让发送和接收形成同步点，便于观察生产者和消费者之间的节奏。

关闭 channel 的责任非常关键：通常由发送方关闭，因为只有发送方知道不会再发送。`jobs` 由投递任务的 goroutine 关闭，worker 通过 `range jobs` 自然退出；`results` 要等所有 worker 都 `Done` 后再关闭，否则仍在发送结果的 worker 会 panic。Go 没有自动回收“逻辑上泄漏”的 goroutine，因此每个启动点都应该能回答它什么时候退出。

## 运行

```bash
go run main.go
```

## 观察点

- `jobs` 只由发送方关闭，worker 使用 `range jobs` 自然退出。
- `results` 在 `WaitGroup` 确认所有 worker 退出后关闭，避免还有发送者时提前关闭。
- 输出顺序可能和任务提交顺序不同，这正是并发调度存在的信号。
- `worker` 的参数使用单向 channel 类型，说明函数签名也能表达并发协作中的权限边界。

## 延伸练习

- 把 worker 数量从 2 改成 1 或 4，观察输出顺序和总耗时的变化。
- 给 `jobs` 或 `results` 加缓冲，例如 `make(chan Job, 2)`，体会缓冲如何改变发送方阻塞时机。
- 在 worker 中人为返回错误结果，再设计一个 `Result` 字段表达失败，思考 channel 传值时如何保留错误上下文。
