# using-disposable

## 目标

通过一个写报告文件的小例子理解 `using`、`IDisposable` 和资源边界。这个例子对应的语言思想是：GC 负责托管内存，但文件句柄、网络连接、锁、计时器等外部资源需要确定性释放。

真实工程中，忘记释放资源可能不会马上报错，却会逐渐造成文件被占用、连接池耗尽、缓冲区未刷新或句柄泄漏。C# 用 `IDisposable.Dispose()` 表达“这个对象用完后需要清理”，用 `using` 语句保证离开作用域时调用清理逻辑，即使中途发生异常也会执行。

## 特性说明

`ReportWriter` 持有一个 `StreamWriter`。`StreamWriter` 背后可能占用文件句柄和缓冲区，所以 `ReportWriter` 也实现 `IDisposable`，在 `Dispose` 里转交释放。`using (var writer = new ReportWriter(exportPath)) { ... }` 建立了一个清晰的资源作用域：进入作用域时打开，离开作用域时关闭。

`disposed` 字段让释放操作保持幂等，也让 `WriteLine` 能在对象已释放后抛出明确的 `ObjectDisposedException`。这不是每个简单包装类都必须手写的完整模式，但它展示了资源对象常见的生命周期状态：可用、释放中、已释放。

如果不用 `using`，代码常会退化成手写 `try/finally`，或者更糟糕地依赖进程退出时由操作系统回收资源。前者样板多，容易漏；后者在服务端和长时间运行程序里非常危险。

## 设计取舍

`using` 适合生命周期短、边界清楚的资源。把资源作用域写得越小，越容易判断什么时候释放。相反，如果把 `StreamWriter` 存到全局单例里，调用方就很难知道谁负责关闭它。

并非所有对象都需要 `IDisposable`。普通 record、字符串、列表和纯计算服务通常只依赖 GC，不需要手动释放。只有当类型拥有或间接拥有需要确定性清理的资源时，才应该实现 `IDisposable`。过度实现会让调用者背上不必要的生命周期负担。

异步资源还有 `IAsyncDisposable` 和 `await using`，例如异步流、数据库连接或网络资源需要异步关闭时会用到。本例使用同步文件写入，是为了保持标准库例子短小，同时让释放时机可以从输出中直接看到。

## 运行

```bash
cd languages/csharp-dotnet/features/examples/using-disposable && dotnet run
```

## 观察点

- 程序先输出 `opened writer`，说明资源在进入 `using` 作用域时创建。
- 离开作用域后会输出 `disposed writer`，证明 `Dispose` 被自动调用。
- 随后读取文件内容能够成功，说明缓冲区已经刷新并且文件句柄已经释放。
- `file exists after dispose: True` 表明释放资源不是删除业务数据，而是关闭持有的外部句柄。
- 可以把 `writer` 声明移动到 `using` 外层，再在释放后调用 `WriteLine` 做实验，观察已释放对象如何拒绝继续使用。

## 延伸练习

- 在 `using` 代码块中故意抛出异常，并用外层 `try/catch` 捕获，观察 `disposed writer` 是否仍会输出。
- 把 `using (...) { ... }` 改成 `using var writer = ...;`，比较两种写法的作用域边界。
- 新增一个 `MemoryStream` 版本，比较内存资源和文件资源在释放需求上的差异。
