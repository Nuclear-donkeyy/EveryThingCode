# async-tasks

## 目标

用三个模拟远程课程请求观察 `async` / `await`、`Task.WhenAll`、取消令牌和 nullable reference types 的协作方式。例子没有真实网络请求，但结构接近服务端常见的“并发加载多个资源，再合并结果”。

这个例子对应的核心思想是：把等待中的 I/O 建模为 `Task`，让调用方可以并发启动、统一等待、按顺序处理结果。真实服务常要同时读取用户、订单、配置或外部 API；如果每一步都阻塞线程，吞吐会很差。如果用回调手写异步流程，异常传播和阅读顺序又会变得混乱。

## 特性说明

`LoadCardAsync` 返回 `Task<CourseCard>`。调用这个方法时，调用方先拿到“未来会完成的工作”，而不是立即拿到课程卡片。`await Task.Delay(...)` 模拟 I/O 等待；等待期间当前方法让出执行权，完成后再从暂停点继续。编译器会把这种写法转换成状态机，所以代码表面仍像同步流程一样从上到下阅读。

`Task.WhenAll(cardTasks)` 同时等待三个任务完成。它的价值不是创建三个专用线程，而是表达“这三件异步工作没有先后依赖，可以一起等待”。如果其中一个任务失败，异常会在 `await` 时被观察到；如果取消令牌触发，取消也会沿着 `Task` 模型传播。

例子还把 `MentorName` 声明为 `string?`。这表示某些课程还没有导师，输出前必须用 `??` 提供后备文本。可空引用类型不会阻止运行时出现 null，但它会把“可能为空”的事实放进编译期契约，推动调用方显式处理。

## 设计取舍

`async/await` 适合 I/O 密集操作，例如网络、文件、数据库、计时器和消息队列。它不等于并行计算，也不会自动让 CPU 密集任务变快。若要并行处理大量 CPU 工作，需要考虑并行库、线程池压力、限流和数据分片。

`Task.WhenAll` 能减少总等待时间，但也会同时启动多个操作。真实项目里如果一次启动几千个 HTTP 请求，可能打爆对方服务或耗尽本机资源。因此常见做法是配合限流、连接池、重试策略和超时。这个例子只启动三个任务，是为了突出模型而不引入额外库。

取消令牌是协作式取消：被调用方法必须把 `CancellationToken` 传给可取消的异步 API，或主动检查它。它不是强制杀线程。这里 `Task.Delay` 接收 token，所以超时会以取消的方式结束等待。

## 运行

```bash
cd languages/csharp-dotnet/features/examples/async-tasks && dotnet run
```

## 观察点

- `LoadCardAsync` 返回 `Task<CourseCard>`，调用后立刻得到任务，真正结果要在 `await` 后读取。
- `Task.WhenAll` 并发等待多个任务，保持代码从上到下可读。
- `MentorName` 是 `string?`，输出前必须处理 null；这体现 nullable reference types 的编译期契约。
- 程序会先打印 `requests started`，说明任务已经创建，结果尚未读取。
- 三张卡片按 `Id` 排序输出，说明合并结果后仍可以用普通 LINQ 处理集合。
- `async-301` 会显示 `mentor pending`，这是 `??` 对可空字段的显式处理。

## 延伸练习

- 把 `Task.WhenAll(cardTasks)` 改成逐个 `await LoadCardAsync(...)`，再增加不同延迟，比较并发等待和顺序等待的耗时。
- 把超时时间改成 `TimeSpan.FromMilliseconds(50)`，观察取消如何通过 `Task.Delay` 传播。
- 让某个 `id` 分支抛出异常，观察异常是在创建任务时出现，还是在 `await Task.WhenAll` 时被观察到。
