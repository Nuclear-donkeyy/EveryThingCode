# Goroutines and Channels

## 目标

这个例子用两个 worker 处理一组任务，展示 goroutine 适合表达并发执行，channel 适合表达任务和结果的交接。主 goroutine 负责创建任务、关闭任务 channel，并在所有 worker 完成后关闭结果 channel。

重点不是“并发一定更快”，而是看清谁生产数据、谁消费数据、谁拥有关闭 channel 的责任。

## 运行

```bash
go run main.go
```

## 观察点

- `jobs` 只由发送方关闭，worker 使用 `range jobs` 自然退出。
- `results` 在 `WaitGroup` 确认所有 worker 退出后关闭，避免还有发送者时提前关闭。
- 输出顺序可能和任务提交顺序不同，这正是并发调度存在的信号。
