# ASP.NET Core Minimal API quickstart

这个案例是一个真实的 ASP.NET Core Minimal API 小项目。它不依赖外部数据库，也不需要额外 NuGet 包，目标是让读者先看清 ASP.NET Core 的核心骨架：Host、配置、Options、依赖注入、中间件、路由、业务服务和 JSON 响应。

## 目标

运行一个最小但结构完整的待办事项 API，并理解：

- `Microsoft.NET.Sdk.Web` 如何把项目变成 Web 应用。
- `Program.cs` 如何配置服务、middleware pipeline 和 endpoint。
- Minimal API handler 如何通过参数绑定获取 route、body、DI service 和 Options。
- 为什么业务逻辑应该放进 service/repository，而不是全部堆在 endpoint lambda 中。

## 这个案例解决什么问题

这个 quickstart 故意选择“待办事项 API”这种非常小的业务，是为了让框架问题浮出来：如果只把它写成几个函数，很快就会遇到日志放哪里、配置从哪里来、对象谁创建、路由如何分组、请求体如何绑定、分页上限谁控制、以后怎么替换数据库和怎么测试 HTTP 管线等问题。ASP.NET Core 的学习重点不在待办事项本身，而在它如何把这些工程问题放进统一的模型。

`AspNetCoreQuickstart.csproj` 解决的是“这个项目如何成为 Web 应用”的问题。`Microsoft.NET.Sdk.Web` 会引入 ASP.NET Core shared framework，启用 Web 项目默认构建行为；`net10.0` 锁定运行时基线；`Nullable` 和 `ImplicitUsings` 让示例代码既保持现代 C# 风格，又减少入口文件里的样板代码。换句话说，`.csproj` 是框架能力进入项目的第一道门。

`appsettings.json` 解决的是“运行环境差异如何进入代码”的问题。本例只有 `Todo:ApiName` 和 `Todo:MaxPageSize`，但它们代表真实项目里的连接字符串、功能开关、外部服务地址、限流阈值和业务开关。示例没有在 endpoint 中写死这些值，而是把它们绑定到 `TodoOptions`，再通过 `IOptions<TodoOptions>` 注入，让配置成为有类型、有校验、可替换的契约。

`Program.cs` 解决的是“HTTP 应用如何被装配”的问题。它把 Host、配置、DI、middleware、routing、handler、service、repository 全部放在一个文件里，并不是鼓励真实项目永远单文件，而是让读者在第一眼看到完整请求路径：请求进入中间件，路由找到 endpoint，handler 从参数绑定拿到输入和服务，service 执行业务规则，repository 管理状态，最后由 Results 写回 HTTP 响应。

## 学习重点

本案例把框架思想映射到代码：

- Host：`WebApplication.CreateBuilder(args)` 读取配置并准备服务容器。
- DI：`AddSingleton<InMemoryTodoRepository>()` 与 `AddSingleton<TodoService>()` 注册应用服务。
- Options：`TodoOptions` 从 `appsettings.json` 的 `Todo` 节点绑定，并在启动时验证。
- Middleware：自定义 `app.Use(...)` 记录请求耗时，并演示中间件如何包裹后续处理。
- Routing：`app.MapGroup("/todos")` 创建路由分组，`MapGet`、`MapPost`、`MapPatch` 声明 endpoint。
- Results：使用 `Results.Ok`、`Results.Created`、`Results.NotFound` 表达 HTTP 语义。

## 思想拆解

第一条主线是 Host model。`var builder = WebApplication.CreateBuilder(args);` 会建立配置、日志、依赖注入、环境信息和生命周期管理。很多框架把这些能力分散在不同入口；ASP.NET Core 把它们统一进 Host，所以后续的服务注册、配置读取、日志输出和应用启动都围绕同一个构建过程展开。

第二条主线是 built-in DI。`builder.Services.AddSingleton<InMemoryTodoRepository>()` 和 `AddSingleton<TodoService>()` 说明服务不是在 endpoint 里临时创建的，而是在启动阶段注册，由容器按生命周期管理。`TodoService` 通过构造函数声明它需要仓储，endpoint 通过参数声明它需要 `TodoService`。这让依赖关系从隐藏的 `new` 变成显式契约。

第三条主线是 configuration/options。`AddOptions<TodoOptions>().Bind(...).Validate(...).ValidateOnStart()` 把 JSON 配置绑定成 C# record，并在启动时校验。`GET /` endpoint 注入 `IOptions<TodoOptions>` 返回 API 名称，`GET /todos` 注入同一个 Options 来限制 `take`。这说明配置不是“随用随查的字符串”，而是可以参与类型检查和测试的应用输入。

第四条主线是 middleware pipeline。`app.Use(async (context, next) => { ... })` 在 `await next()` 前后包住后续处理，因此不需要每个 endpoint 都手写日志。真实项目中的异常处理、认证、授权、CORS、静态文件、响应压缩、限流和 tracing 都遵循同样的管线思想。理解这段代码，就理解了 ASP.NET Core 为什么能统一处理横切问题。

第五条主线是 endpoint routing 与 Minimal API。`app.MapGroup("/todos")` 把待办事项相关路由收拢到一个分组，`MapGet`、`MapPost`、`MapPatch` 则用 HTTP 方法和路径表达 API 契约。Minimal API handler 的参数会自动绑定：`int id` 来自路由，`int? take` 来自 query，`CreateTodoRequest request` 来自 JSON body，`TodoService service` 来自 DI，`IOptions<TodoOptions>` 来自 Options。读者需要掌握的是“参数声明就是绑定契约”。

第六条主线是数据访问边界。示例使用 `InMemoryTodoRepository`，因为第一课不应该被数据库驱动、迁移和连接字符串淹没。但这个仓储已经把外部状态从 endpoint 中隔离出来。未来接入 EF Core 时，可以把仓储改成注入 `TodoDbContext` 的 scoped 服务，endpoint 和大部分 service 代码不需要知道数据最终存在内存、SQLite、PostgreSQL 还是 SQL Server。

第七条主线是测试。当前最小验收是 `dotnet build` 与手动 `curl`；当示例升级为测试项目时，可以用 xUnit 测 `TodoService`，用 `WebApplicationFactory` 测完整 HTTP 管线。ASP.NET Core 的 DI、Host 和 endpoint routing 让测试可以选择不同层级：既能测纯业务，也能启动内存服务器测 middleware、routing、Options 和 JSON 序列化。

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

`Program.cs` 第一段创建 builder 并注册服务。`AddOptions<TodoOptions>()` 把 `appsettings.json` 中的 `Todo` 节点绑定到 C# record，并在启动时校验 `ApiName` 和 `MaxPageSize`。这一步解决的是配置漂移问题：错误配置会阻止应用启动，而不是在某次请求中悄悄产生异常。`AddSingleton` 注册内存仓储和业务服务，让 endpoint 可以直接声明 `TodoService service`，避免在路由函数中手动创建依赖。

中间件部分使用 `app.Use(async (context, next) => { ... })`。它在调用 `await next()` 之前记录开始时间，在后续处理完成后记录状态码和耗时。这说明中间件不是“路由的一部分”，而是包裹路由处理的管线节点。以后增加异常处理、认证授权或 OpenTelemetry 时，本质上都是继续往这条管线里放节点。

路由部分使用 `app.MapGroup("/todos")`。分组可以统一设置 tags、authorization、filters 或 OpenAPI metadata。本案例中：

- `GET /todos` 从 query string 读取 `take`，再用 Options 限制最大数量。
- `GET /todos/{id:int}` 从 route 绑定 `id`。
- `POST /todos` 从 JSON body 绑定 `CreateTodoRequest`。
- `PATCH /todos/{id:int}/complete` 修改任务状态。

业务逻辑放在 `TodoService` 中。服务负责校验标题、调用仓储并返回领域对象，避免 endpoint lambda 同时承担 HTTP 绑定、业务规则和数据存取三种职责。内存仓储 `InMemoryTodoRepository` 用 `lock` 保护列表和自增 ID，避免 Singleton 在并发请求下出现明显竞态。真实项目接入 EF Core 时，通常会把仓储替换为注入 `DbContext` 的 scoped 服务，并把连接字符串放入配置系统。

`appsettings.json` 中的 `MaxPageSize` 会影响 `GET /todos?take=...`。这条链路值得单独观察：JSON 配置进入 `builder.Configuration`，Options 绑定成 `TodoOptions`，endpoint 注入 `IOptions<TodoOptions>`，最后 `Math.Clamp` 用它限制输出数量。这就是 ASP.NET Core 推荐的配置流动方式。

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
