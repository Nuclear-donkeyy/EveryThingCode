# async-tasks

## 目标

用三个模拟远程课程请求观察 `async` / `await`、`Task.WhenAll`、取消令牌和 nullable reference types 的协作方式。例子没有真实网络请求，但结构接近服务端常见的“并发加载多个资源，再合并结果”。

## 运行

```bash
cd languages/csharp-dotnet/features/examples/async-tasks && dotnet run
```

## 观察点

- `LoadCardAsync` 返回 `Task<CourseCard>`，调用后立刻得到任务，真正结果要在 `await` 后读取。
- `Task.WhenAll` 并发等待多个任务，保持代码从上到下可读。
- `MentorName` 是 `string?`，输出前必须处理 null；这体现 nullable reference types 的编译期契约。
