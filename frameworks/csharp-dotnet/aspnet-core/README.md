# ASP.NET Core

ASP.NET Core 是 .NET 的现代 Web 平台。它不是只用于“写控制器”的框架，而是一套围绕 HTTP 请求处理、主机生命周期、依赖注入、配置、日志、路由、身份认证、实时通信和测试构建出来的应用模型。本章节先以 Minimal API 为入口，因为它最容易看见框架的骨架：请求进入中间件管线，路由匹配 endpoint，endpoint 从 DI 容器拿到服务，服务执行业务逻辑，然后返回结构化响应。

## 核心定位

ASP.NET Core 解决的是“如何在 .NET 中构建可维护、可部署、可测试的 Web 应用和网络服务”。它提供：

- HTTP Server 抽象与 Kestrel 默认服务器。
- Middleware pipeline，用组合方式处理跨切面逻辑。
- Endpoint routing，把请求映射到 Minimal API、MVC Controller、Razor Pages、SignalR Hub 或 gRPC service。
- 内置依赖注入容器，管理服务生命周期。
- 配置、Options、日志、健康检查、认证授权、静态文件、OpenAPI 等工程能力。

它不替你解决所有业务问题。领域建模、数据库设计、缓存一致性、分布式事务、权限模型、可观测性策略仍然需要应用自己设计。ASP.NET Core 的价值在于把这些能力放进统一的 Host 和请求生命周期中，让应用可以按清晰边界组合。

## 解决的问题

如果不用 ASP.NET Core 这一层平台，.NET Web 服务很快会遇到一组重复但棘手的问题：HTTP 请求进入应用后由谁接住，日志、异常、认证、授权、CORS、压缩、限流这些横切逻辑按什么顺序执行，业务 endpoint 如何从 URL、query、header、body 和服务容器中拿到输入，以及应用启动、关闭、配置、日志、后台服务如何统一管理。ASP.NET Core 的核心价值不是“少写几行路由”，而是把这些基础设施问题整理成稳定的应用模型。

第一个痛点是 HTTP 管线容易失控。小项目可以在每个 handler 里写日志、try/catch、权限判断和响应格式；项目变大后，这些逻辑会散落到几十个 endpoint 中，顺序不一致，漏掉也很难发现。ASP.NET Core 用 middleware pipeline 把横切逻辑变成有顺序的链：请求先经过前置中间件，再进入路由和业务处理，响应再沿链返回。quickstart 中的自定义 `app.Use(...)` 就是最小示范：它不关心具体业务，却能统一记录所有请求的状态码和耗时。

第二个痛点是对象创建和生命周期混乱。没有 DI 时，endpoint 可能到处 `new TodoService()`、`new Repository()`，最终很难替换实现、共享配置或做测试。ASP.NET Core 内置 DI，把服务注册集中在 `builder.Services`，再由框架在 endpoint handler 中自动解析。quickstart 的 `AddSingleton<InMemoryTodoRepository>()` 和 `AddSingleton<TodoService>()` 展示了“依赖由容器装配，业务由服务表达”的边界。

第三个痛点是配置散落。连接字符串、分页上限、功能开关、第三方 API 地址如果直接用硬编码或裸字符串读取，会让不同环境配置、校验和测试都变脆。ASP.NET Core 的 configuration system 会合并 `appsettings.json`、环境变量、命令行、User Secrets 和云端配置；Options 模式则把配置绑定成类型。quickstart 的 `TodoOptions` 把 `Todo:ApiName` 与 `Todo:MaxPageSize` 变成可注入、可校验的 C# 契约。

第四个痛点是日志与可观测性不统一。Web 服务不只要返回结果，还要知道每次请求用了多久、是否异常、在哪个 endpoint 失败、配置是否加载正确。ASP.NET Core Host 默认集成 logging，middleware、endpoint、service 都能使用同一套日志抽象。quickstart 直接用 `app.Logger.LogInformation(...)`，真实项目可以把同一套日志输出到 console、OpenTelemetry、Application Insights 或集中式日志平台。

第五个痛点是应用模型选择困难。轻量 API 需要快速写 endpoint，复杂业务需要 Controller、Filter、模型绑定和版本管理，服务端页面需要 Razor Pages，实时通信需要 SignalR，RPC 需要 gRPC。ASP.NET Core 用 endpoint routing 把 Minimal API、MVC、Razor Pages、SignalR 和 gRPC 放在同一套路由和 middleware 底座上。学习 Minimal API 并不是走捷径，而是在先看清共同底座。

第六个痛点是数据访问和测试常常绑死在框架边缘。初学者容易把数据库操作直接写进 handler，导致无法单测，也很难把内存存储换成 EF Core。ASP.NET Core 本身不强制某个数据层模式，但它通过 DI、Options、Host 和测试服务器让替换变自然：quickstart 先用内存仓储讲清 endpoint -> service -> repository；接入 EF Core 时，通常把 `InMemoryTodoRepository` 换成注入 `DbContext` 的 scoped 服务，再用 `WebApplicationFactory` 跑完整 HTTP 管线测试。

## 设计思想

ASP.NET Core 的第一个思想是“Host 统一应用生命周期”。`WebApplication.CreateBuilder(args)` 不只是创建一个 HTTP 路由器，它会建立配置系统、日志系统、服务容器、环境信息和应用生命周期。`AspNetCoreQuickstart.csproj` 使用 `Microsoft.NET.Sdk.Web`，表示项目要引用 ASP.NET Core shared framework，并按 Web 应用方式构建和运行。`builder.Build()` 之后得到的 `app` 则是已经装配好配置、DI 和日志的运行时对象。

第二个思想是“显式组合”。`Program.cs` 中通过 `builder.Services` 注册依赖，通过 `app.Use...` 组合中间件，通过 `app.Map...` 声明 endpoint。读者应该把启动代码看成应用 wiring：这里决定应用拥有哪些能力、能力按什么顺序执行、哪些服务可以被 handler 注入。ASP.NET Core 不把这些选择藏在全局配置文件里，而是让应用入口成为可读的装配图。

第三个思想是“中间件管线”。中间件本质上是一个接收 `HttpContext` 并决定是否调用下一个处理器的函数。它适合日志、异常处理、静态文件、CORS、认证、授权、压缩、限流等横切逻辑。顺序非常重要：异常处理中间件通常放前面，认证要在授权之前，endpoint 映射之后就进入具体业务处理。quickstart 的计时中间件展示了最关键的心智模型：`await next()` 之前是请求进入，之后是响应返回。

第四个思想是“endpoint routing 统一入口”。Minimal API 的 `MapGet`、`MapPost` 和 MVC Controller 的 action 最终都会成为 endpoint，并带有 HTTP 方法、路径、metadata、filter、authorization 等信息。quickstart 的 `app.MapGroup("/todos").WithTags("Todos")` 展示了路由分组：一组 API 可以共享前缀和元数据，未来也可以统一加鉴权、filter 或 OpenAPI 标签。

第五个思想是“依赖注入优先”。ASP.NET Core 内置 DI 容器，Minimal API handler 可以直接声明参数，例如 `TodoService service`、`IOptions<TodoOptions> options`、`ILogger<T>`。框架会根据参数类型和位置，从 DI 容器、请求、路由、查询字符串或 body 中完成绑定。业务代码因此不需要手动 new 一堆依赖，测试时也更容易替换实现。quickstart 中 `TodoService` 依赖 `InMemoryTodoRepository`，这条依赖关系由构造函数表达，由容器装配。

第六个思想是“配置分层 + Options 契约”。应用配置可以来自 `appsettings.json`、`appsettings.{Environment}.json`、环境变量、命令行参数、用户机密或配置中心。代码不应该到处读取裸字符串，而是把相关配置绑定成 Options 类型，再通过 `IOptions<T>` 或 `IOptionsMonitor<T>` 注入。quickstart 使用 `Bind(...).Validate(...).ValidateOnStart()`，让配置错误在应用启动时暴露，而不是等到某个请求打到接口才失败。

第七个思想是“从轻到重的应用模型”。Minimal APIs 适合轻量 API 和小服务；MVC 适合控制器分层、复杂模型绑定、过滤器和大型 Web API；Razor Pages 适合页面驱动的服务端 Web；Blazor、SignalR、gRPC 继续复用同一套 ASP.NET Core 基础设施。学习时不要把它们看成彼此割裂的框架，而要先抓住共同底座：Host、middleware、endpoint routing、DI、configuration、logging。

第八个思想是“数据访问是可替换边界”。ASP.NET Core 与 EF Core 配合紧密，但并不要求所有代码都直接依赖 `DbContext`。更稳妥的学习路径是先把业务用例放进 service，把外部状态放进 repository 或 data access 层；等到接入 EF Core 时，再让 DI 管理 `DbContext` 的 scoped 生命周期。这样 handler 仍然关注 HTTP 输入输出，service 关注业务规则，EF Core 关注持久化和查询。

## 架构模型

一个典型 ASP.NET Core 应用可以分成几层：

- Host 层：创建应用、读取配置、注册服务、配置日志、控制应用启动和关闭。
- Middleware 层：按顺序处理请求的横切逻辑，例如异常、日志、认证、授权。
- Routing/Endpoint 层：把 `GET /todos`、`POST /todos` 之类的请求映射到处理函数或控制器 action。
- Application service 层：表达用例，例如创建任务、完成任务、查询任务列表。
- Data access 层：通过内存仓储、EF Core、Dapper、HTTP client 或消息队列访问外部状态。
- Contract 层：DTO、Options、响应模型、错误模型，决定 API 对外暴露什么。
- Test 层：用单元测试验证服务，用集成测试验证完整 HTTP 管线。

本仓库 quickstart 为了聚焦框架思想，把所有代码放在一个 `Program.cs` 中，但它仍然保留了 service、repository、Options、DTO、middleware 的边界。真实项目中可以逐步拆成 `Endpoints/`、`Services/`、`Data/`、`Contracts/`、`Options/` 和 `Tests/`。

## 请求/执行生命周期

一次 Minimal API 请求的大致流向如下：

1. Kestrel 接收 HTTP 请求并创建 `HttpContext`。
2. 请求进入 middleware pipeline。每个中间件可以读取请求、写日志、短路响应，或调用 `next()` 交给后续中间件。
3. Routing 根据路径、HTTP 方法、约束和 metadata 找到 endpoint。
4. Endpoint handler 的参数开始绑定：路由参数、查询字符串、body、header、services、Options、logger 等被解析成 C# 参数。
5. Handler 调用应用服务。服务通常通过接口依赖仓储、数据库上下文、外部客户端或其他服务。
6. Handler 返回 `IResult`、DTO、字符串、文件或状态码。ASP.NET Core 把返回值写成 HTTP response。
7. 响应沿中间件链反向返回，前置中间件可以记录耗时、补 header 或处理异常。

理解这个生命周期后，很多设计问题会变简单：异常处理应该放在 middleware，不应该散落在每个 endpoint；业务规则应该放在 service，不应该堆在路由 lambda；数据库访问应该通过仓储或 `DbContext`，不应该在 handler 里混杂 SQL 细节。

## 工程结构

本章节案例位于 [examples/quickstart](examples/quickstart/)：

```text
examples/quickstart/
├── AspNetCoreQuickstart.csproj
├── Program.cs
├── appsettings.json
├── README.md
└── NOTES.md
```

案例刻意保持最小文件数：

- `AspNetCoreQuickstart.csproj` 使用 `Microsoft.NET.Sdk.Web`，表示这是一个 ASP.NET Core Web 项目。
- `Program.cs` 展示 Host、配置绑定、DI 注册、中间件、Minimal API endpoint、服务和内存仓储。
- `appsettings.json` 提供 Options 示例，让读者观察配置如何进入 C# 类型。
- `README.md` 给出运行命令、预期输出和代码讲解。

真实项目扩展时，建议拆出这些边界：

- `Endpoints/`：路由分组与 endpoint 映射。
- `Application/` 或 `Services/`：业务用例。
- `Domain/`：领域对象与业务规则。
- `Infrastructure/` 或 `Data/`：EF Core、外部 API、消息队列、文件系统。
- `Contracts/`：请求/响应 DTO。
- `Options/`：配置模型。
- `Tests/`：单元测试与 WebApplicationFactory 集成测试。

## 配置方式

ASP.NET Core 默认会按顺序合并多个配置源。常见来源包括：

- `appsettings.json`：所有环境共享的默认配置。
- `appsettings.Development.json`：开发环境覆盖配置。
- 环境变量：容器、CI/CD、云平台常用方式；层级键通常用 `__` 表示，例如 `Todo__MaxPageSize=50`。
- 命令行参数：临时启动覆盖，例如 `--urls http://127.0.0.1:5144`。
- User Secrets：本地开发保存密钥，不提交到仓库。
- Key Vault 或配置中心：生产环境集中管理敏感配置。

推荐方式是把配置绑定到 Options：

```csharp
builder.Services
    .AddOptions<TodoOptions>()
    .Bind(builder.Configuration.GetSection("Todo"))
    .ValidateDataAnnotations()
    .ValidateOnStart();
```

然后在 endpoint 或 service 中注入 `IOptions<TodoOptions>`。这样可以避免到处写 `configuration["Todo:MaxPageSize"]`，也能在应用启动阶段发现配置错误。

## 模块与依赖管理

ASP.NET Core 使用内置 DI 容器管理依赖。常见生命周期有三种：

- Singleton：整个应用共享一个实例，适合无状态服务、配置读取、内存缓存等。必须注意线程安全。
- Scoped：每个请求一个实例，最常用于 EF Core `DbContext` 和请求级业务服务。
- Transient：每次注入都创建新实例，适合轻量、无状态对象。

Minimal API 中，依赖可以直接写在 handler 参数中：

```csharp
app.MapGet("/todos", (TodoService service) => service.List());
```

框架会从 DI 容器解析 `TodoService`。当项目变大时，可以用扩展方法组织模块：

```csharp
builder.Services.AddTodoFeature(builder.Configuration);
app.MapTodoEndpoints();
```

这类扩展方法不是魔法，只是把注册和映射逻辑移出 `Program.cs`，让启动文件继续保持可读。

NuGet 是 .NET 的包管理系统。ASP.NET Core 的基础 Web SDK 已经随 .NET SDK 提供；EF Core、数据库 provider、OpenAPI、认证组件、测试库等通常通过 `PackageReference` 添加到 `.csproj` 中。

## 数据访问

quickstart 默认使用内存仓储，原因是学习 ASP.NET Core 第一课时，数据库迁移、连接字符串、provider 差异会遮住主线。内存仓储能清楚展示 endpoint -> service -> repository 的调用关系。

接入 EF Core 时，常见步骤是：

1. 添加包：`Microsoft.EntityFrameworkCore` 和一个 provider，例如 `Microsoft.EntityFrameworkCore.Sqlite`、`Microsoft.EntityFrameworkCore.SqlServer`、`Npgsql.EntityFrameworkCore.PostgreSQL` 或 `Microsoft.EntityFrameworkCore.InMemory`。
2. 定义实体，例如 `TodoItem`。
3. 定义 `DbContext`，暴露 `DbSet<TodoItem>`。
4. 在 DI 中注册：`builder.Services.AddDbContext<TodoDbContext>(options => options.UseSqlite(connectionString));`。
5. 在 service 或 repository 中注入 `TodoDbContext`。
6. 使用 migrations 管理数据库结构：`dotnet ef migrations add InitialCreate`、`dotnet ef database update`。

EF Core 的核心思想是 Unit of Work 加 Identity Map 加 LINQ 查询。`DbContext` 追踪对象变化，`SaveChangesAsync` 统一提交。它让 CRUD 很顺手，但也要理解查询生成的 SQL、N+1、事务边界、并发 token、索引和批量操作。真实项目中，EF Core 不应该被当作“完全不用懂数据库”的替代品。

## 测试方式

ASP.NET Core 测试通常分三层：

- 单元测试：直接测试 service、validator、domain 方法，不启动 Web 服务器。
- 集成测试：使用 `Microsoft.AspNetCore.Mvc.Testing` 的 `WebApplicationFactory` 启动内存测试服务器，验证真实 middleware、routing、DI 和序列化。
- 端到端或 smoke test：启动应用后用 `curl`、Postman、Playwright、k6 或 CI 脚本访问真实端口。

quickstart 目前提供 `dotnet build` 作为最小结构验证，并在 README 中给出 `dotnet run` 与 `curl` 命令。下一步如果加入测试项目，可以创建 `AspNetCoreQuickstart.Tests`，使用 xUnit 和 `WebApplicationFactory<Program>` 验证 `GET /todos`、`POST /todos`、`PATCH /todos/{id}/complete`。

## 部署方式

本地开发通常使用：

```bash
dotnet run --urls http://127.0.0.1:5144
```

生产部署通常会先发布：

```bash
dotnet publish -c Release
```

然后将发布产物放进容器、虚拟机、systemd 服务、Windows Service、Azure App Service、Kubernetes 或其他平台。ASP.NET Core 默认的 Kestrel 可以直接处理请求，也常与 Nginx、IIS、YARP、Ingress Controller 等反向代理协作。

容器化时需要特别注意配置来源、端口、健康检查、日志输出、非 root 用户、镜像体积和启动探针。部署不是把代码跑起来就结束，而是要让应用能被配置、观测、回滚和扩容。

## 适用场景与取舍

优先选择 ASP.NET Core 的场景：

- 团队使用 C# / .NET，想构建长期维护的 Web API 或企业后端。
- 需要统一的 DI、配置、日志、认证授权和测试体系。
- 项目可能从轻量 API 扩展到 MVC、SignalR、gRPC 或后台任务。
- 需要良好的 Windows、Linux、容器、云平台支持。

需要谨慎或考虑其他方案的场景：

- 极小脚本或一次性 HTTP 工具，可能用语言标准库或更轻框架更快。
- 团队主要是 Node.js、Python 或 Go，且没有 .NET 运维经验。
- 强实时低延迟或嵌入式场景，需要先评估运行时和部署约束。
- 前端交互极复杂且团队熟悉 React/Vue/Svelte，Blazor 未必是最自然选择。

学习上的取舍是：先掌握 ASP.NET Core 原生机制，再引入大型架构模板。过早使用 Clean Architecture、CQRS、Mediator、Repository、Unit of Work、复杂 BaseController 容易让学习者看见很多层，却看不见 HTTP 请求本身如何流动。

## 案例索引

- [quickstart](examples/quickstart/)：真实可运行的 ASP.NET Core Minimal API 项目，演示 middleware pipeline、DI、Options、路由分组、服务层、内存仓储和 JSON 响应。

## 版本来源

- 语言/运行时基线：.NET 10.0.8 LTS。
- 框架基线：ASP.NET Core on .NET 10 LTS。
- 版本策略：使用当前最新 LTS；框架版本随 .NET SDK LTS 线演进。
- 官方来源：https://learn.microsoft.com/aspnet/core/
- .NET 支持策略：https://dotnet.microsoft.com/platform/support/policy/dotnet-core
- 校验日期：2026-05-30
