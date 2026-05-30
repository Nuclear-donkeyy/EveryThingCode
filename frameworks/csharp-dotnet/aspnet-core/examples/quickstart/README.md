# ASP.NET Core Minimal API quickstart

这个案例是一个真实的 ASP.NET Core Minimal API 小项目。它不依赖外部数据库，也不需要额外 NuGet 包，目标是让读者先看清 ASP.NET Core 的核心骨架：Host、配置、Options、依赖注入、中间件、路由、业务服务和 JSON 响应。

## 目标

运行一个最小但结构完整的待办事项 API，并理解：

- `Microsoft.NET.Sdk.Web` 如何把项目变成 Web 应用。
- `Program.cs` 如何配置服务、middleware pipeline 和 endpoint。
- Minimal API handler 如何通过参数绑定获取 route、body、DI service 和 Options。
- 为什么业务逻辑应该放进 service/repository，而不是全部堆在 endpoint lambda 中。

## 学习重点

本案例把框架思想映射到代码：

- Host：`WebApplication.CreateBuilder(args)` 读取配置并准备服务容器。
- DI：`AddSingleton<InMemoryTodoRepository>()` 与 `AddSingleton<TodoService>()` 注册应用服务。
- Options：`TodoOptions` 从 `appsettings.json` 的 `Todo` 节点绑定，并在启动时验证。
- Middleware：自定义 `app.Use(...)` 记录请求耗时，并演示中间件如何包裹后续处理。
- Routing：`app.MapGroup("/todos")` 创建路由分组，`MapGet`、`MapPost`、`MapPatch` 声明 endpoint。
- Results：使用 `Results.Ok`、`Results.Created`、`Results.NotFound` 表达 HTTP 语义。

## 工程结构

```text
quickstart/
├── AspNetCoreQuickstart.csproj
├── Program.cs
├── appsettings.json
├── README.md
└── NOTES.md
```

- `AspNetCoreQuickstart.csproj`：声明目标框架 `net10.0`，使用 ASP.NET Core Web SDK。
- `Program.cs`：包含入口、配置绑定、DI 注册、中间件、路由、DTO、服务和内存仓储。
- `appsettings.json`：演示 `Todo` 配置节，控制 API 标题和分页上限。
- `NOTES.md`：记录案例设计取舍。

## 运行前提

- 安装 .NET 10 LTS SDK，版本基线见仓库根目录 `versions.yaml`。
- 能在终端运行 `dotnet --info`。
- 端口 `5144` 未被占用；如果被占用，可以把命令中的端口换成其他端口。

## 运行

先构建项目，验证源码和目标框架：

```bash
dotnet build
```

启动 API：

```bash
dotnet run --urls http://127.0.0.1:5144
```

在另一个终端访问接口：

```bash
curl http://127.0.0.1:5144/
curl http://127.0.0.1:5144/todos
curl -X POST http://127.0.0.1:5144/todos -H "Content-Type: application/json" -d '{"title":"Read ASP.NET Core pipeline"}'
curl -X PATCH http://127.0.0.1:5144/todos/1/complete
```

## 预期输出

`dotnet run` 会显示监听地址，类似：

```text
Now listening on: http://127.0.0.1:5144
Application started. Press Ctrl+C to shut down.
```

访问根路径会返回 API 信息：

```json
{
  "name": "EveryThingCode ASP.NET Core quickstart",
  "version": "v1",
  "endpoints": ["/todos", "/todos/{id}", "/todos/{id}/complete"]
}
```

创建任务后会返回 `201 Created` 和新任务 JSON。完成任务后，`completed` 会变成 `true`。控制台还会看到自定义中间件输出的请求耗时日志。

## 代码讲解

`Program.cs` 第一段创建 builder 并注册服务。`AddOptions<TodoOptions>()` 把 `appsettings.json` 中的 `Todo` 节点绑定到 C# record，并通过 DataAnnotations 做启动校验。`AddSingleton` 注册内存仓储和业务服务，让 endpoint 可以直接声明 `TodoService service`。

中间件部分使用 `app.Use(async (context, next) => { ... })`。它在调用 `await next()` 之前记录开始时间，在后续处理完成后记录状态码和耗时。这说明中间件不是“路由的一部分”，而是包裹路由处理的管线节点。

路由部分使用 `app.MapGroup("/todos")`。分组可以统一设置 tags、authorization、filters 或 OpenAPI metadata。本案例中：

- `GET /todos` 从 query string 读取 `take`，再用 Options 限制最大数量。
- `GET /todos/{id:int}` 从 route 绑定 `id`。
- `POST /todos` 从 JSON body 绑定 `CreateTodoRequest`。
- `PATCH /todos/{id:int}/complete` 修改任务状态。

业务逻辑放在 `TodoService` 中。服务负责校验标题、控制分页上限、调用仓储并返回领域对象。内存仓储 `InMemoryTodoRepository` 用 `lock` 保护列表和自增 ID，避免 Singleton 在并发请求下出现明显竞态。真实项目接入 EF Core 时，通常会把仓储替换为注入 `DbContext` 的 scoped 服务。

## 延伸练习

- 把 `InMemoryTodoRepository` 替换为 EF Core SQLite provider，增加 migration 和真实数据库文件。
- 增加 xUnit 集成测试项目，用 `WebApplicationFactory` 验证 `POST /todos` 和 `GET /todos`。
- 为 `POST /todos` 增加更完整的校验和错误响应格式，例如 Problem Details。

## 验收

完成后，你应该能够：

- 说清一个请求如何经过 middleware、routing、handler、service 和 repository。
- 修改 `appsettings.json` 中的 `Todo:MaxPageSize`，并解释它如何通过 Options 影响接口结果。
- 新增一个 endpoint，例如 `DELETE /todos/{id}`，并把删除逻辑放入 service/repository。
- 说明把内存仓储替换为 EF Core 时，需要添加哪些包、注册什么服务、如何管理连接字符串和迁移。
