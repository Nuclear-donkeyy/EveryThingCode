# ASP.NET Core core ideas example

## 目标

这个示例把 `ASP.NET Core` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

.NET Web 服务需要统一 HTTP 管线、DI、配置、日志、Options、路由和测试入口。

## 核心思想到代码

Host model 统一启动，middleware pipeline 处理横切逻辑，endpoint routing 匹配路由，内置 DI 和 Options 管对象与配置。

```csharp
builder.Services.Configure<TaskOptions>(builder.Configuration.GetSection("Tasks"));
builder.Services.AddSingleton<TaskRepository>();
```

```csharp
app.MapGet("/tasks", (TaskRepository repository) => Results.Ok(repository.List()));
```

## 代码位置

- [`Program.cs`](../quickstart/Program.cs)
- [`AspNetCoreQuickstart.csproj`](../quickstart/AspNetCoreQuickstart.csproj)
- [`appsettings.json`](../quickstart/appsettings.json)

## 运行

先进入 quickstart 目录：

```bash
cd ../quickstart
dotnet build
```

如果本机缺少对应工具链，可以先运行仓库根目录的 dry-run：

```bash
python3 scripts/run_framework_examples.py --dry-run
```

## 观察点

Minimal API handler 的参数由 DI 自动提供，说明路由函数不需要手动 new 依赖。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`ASP.NET Core` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
