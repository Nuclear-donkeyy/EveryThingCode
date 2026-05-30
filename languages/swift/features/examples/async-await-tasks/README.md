# Async Await and Tasks

## 目标

这个例子展示 Swift 现代并发的基本阅读方式：异步函数用 `async` 标记，可能暂停的调用点用 `await` 标记，`async let` 可以并发启动有结构化生命周期的子任务，`Task` 可以把一段异步工作包装成一个可等待的任务值。

代码只使用标准库并用 `Task.sleep` 模拟等待，目的是观察控制流，而不是依赖网络或平台框架。

## 特性说明

异步程序的真实问题不是“怎么等”，而是如何让读者看懂哪些调用会暂停、哪些任务属于当前作用域、结果在哪里汇合。`fetchScore` 是 `async` 函数，调用它时必须写 `await`。这让暂停点在代码里可见，读者知道当前任务可能让出执行权，稍后再恢复。

`async let profileScore` 和 `async let historyScore` 会在当前作用域内并发开始两个子任务。后面的 `await profileScore + historyScore` 是汇合点：当前函数需要两个结果才能继续。它们的生命周期被限制在 `main` 的作用域内，这就是结构化并发的核心直觉。

如果不用 `async/await`，类似代码常会退化成嵌套回调、手动计数器或共享可变数组。那些写法容易把错误处理、取消和结果汇合拆散。Swift 的并发设计把暂停、等待和任务归属写进语法，让异步代码更接近同步代码的阅读顺序。

## 设计取舍

`async/await` 的收益是可读性和边界清晰。`await` 并不保证一定切线程，它表达的是“这里可能暂停”。`async let` 适合数量固定、结果必须在当前作用域汇合的并发工作。`Task` 更灵活，可以作为值传递和等待，但也更容易被滥用；真实项目中需要考虑取消、优先级和 actor 隔离。

这个例子没有引入 actor，是为了先聚焦任务生命周期。actor 解决的是共享可变状态隔离问题，通常会和并发一起学习。理解本例后，再回到值语义例子思考：能按值传递时优先避免共享，必须共享时再用 actor 保护边界。

## 运行

```bash
swift main.swift
```

## 观察点

- 输出会先打印 `starting requests`，随后较短延迟的 `history` 通常先完成，说明两个 `async let` 子任务并发运行。
- `combined score` 一定在两个子任务都完成后出现，说明 `await` 是结果汇合点。
- `Task { ... }` 返回一个任务值，后续通过 `await task.value` 取结果，展示了把异步工作作为值管理的方式。
- 所有可能暂停的位置都写着 `await`，这就是 Swift 希望调用点显式暴露异步边界的原因。

## 延伸练习

- 调换两个 `delayNanoseconds`，观察完成顺序如何变化，而 `combined score` 仍然等待两个结果。
- 把 `fetchScore` 改成 `async throws -> Int`，练习 `try await` 和错误传播。
- 增加 `task.cancel()`，再在 `fetchScore` 中检查 `Task.isCancelled`，观察取消需要协作。
- 把两个 `async let` 改成顺序 `await` 调用，对比输出顺序和总等待时间的差异。
