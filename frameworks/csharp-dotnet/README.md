# C# / .NET 框架学习索引

本目录面向已经会编程、但第一次系统进入 .NET 生态的读者。.NET 不是单一 Web 框架，而是一套运行时、标准库、SDK、语言、工具链和应用模型的组合：同一套 C# 语言和 NuGet 包管理可以写 Web API、网页 UI、桌面/移动应用、后台服务、实时通信、gRPC 服务、云函数和测试代码。

## 常用框架清单

| 框架/库 | 方向 | 适合场景 | 本仓库覆盖 |
| --- | --- | --- | --- |
| [ASP.NET Core](aspnet-core/) | Web / API 平台 | REST API、MVC、Razor Pages、实时服务、gRPC、身份认证 | 已覆盖核心思想、Minimal API、Middleware、DI、配置、Options、EF Core 接入思路 |
| Minimal APIs | 轻量 HTTP API | 小型服务、BFF、内部 API、教学入门 | 在 [ASP.NET Core quickstart](aspnet-core/examples/quickstart/) 中作为第一个可运行案例 |
| MVC / Razor Pages | 服务端 Web | 后台系统、表单页面、SEO 友好页面、传统企业 Web | 在 ASP.NET Core 章节中作为扩展方向说明 |
| Blazor | Web UI | 使用 C# 构建交互式前端、WebAssembly、服务端交互式 UI | 后续可扩展独立案例 |
| Entity Framework Core | ORM / 数据访问 | 关系型数据库建模、查询、迁移、事务、变更追踪 | 本仓库已在 ASP.NET Core 章节讲解接入方式与取舍 |
| .NET MAUI | 跨平台应用 | Windows、macOS、iOS、Android 客户端 | 后续可扩展 UI 案例 |
| Worker Service | 后台任务 | 消费队列、定时任务、守护进程、批处理 | 后续可扩展服务案例 |
| gRPC for .NET | 高性能 RPC | 微服务内部通信、强类型契约、流式调用 | ASP.NET Core 平台能力之一，后续可扩展案例 |
| SignalR | 实时通信 | 聊天、协作、通知、实时仪表盘 | ASP.NET Core 平台能力之一，后续可扩展案例 |
| xUnit / NUnit / MSTest | 测试 | 单元测试、集成测试、回归验证 | quickstart 给出测试切入点，后续可增加测试项目 |
| Serilog / OpenTelemetry | 日志与可观测性 | 结构化日志、链路追踪、指标 | 后续作为工程化章节扩展 |
| MediatR / FluentValidation | 应用层组织 | CQRS、命令处理、输入校验 | 适合中大型业务项目，入门阶段先理解 ASP.NET Core 原生机制 |

## 选择思路

如果目标是学习 .NET Web，先从 ASP.NET Core 开始。它是 .NET 生态的 Web 基座，Minimal APIs、MVC、Razor Pages、Blazor Server、SignalR 和 gRPC 都共享同一套 Host、配置、日志、依赖注入和中间件模型。理解这套模型以后，再切换到不同应用形态会顺很多。

如果目标是轻量 API，优先 Minimal APIs。它把路由、参数绑定、DI、返回结果放在 `Program.cs` 附近，适合快速观察框架如何把 HTTP 请求映射到 C# 函数。等路由变多、业务边界变复杂，再拆分到 endpoint extension、service、repository、DTO 和测试项目。

如果目标是传统服务端页面，选择 MVC 或 Razor Pages。MVC 更强调 Controller、Action、ViewModel 的分层，适合团队已经熟悉控制器模式的项目；Razor Pages 更贴近页面本身，适合表单、后台管理和页面驱动的 CRUD。

如果目标是前端交互但希望继续使用 C#，可以学习 Blazor。Blazor 的关键不是“替代所有 JavaScript”，而是把组件、状态和事件处理放进 .NET 类型系统中。它适合 .NET 团队维护统一技术栈，但需要理解浏览器生态、组件生命周期和前后端边界。

如果目标是数据访问，EF Core 是首选入口。它提供 LINQ 查询、变更追踪、迁移、关系映射和事务能力；但高性能批量写入、复杂 SQL 调优、跨服务一致性仍需要理解数据库本身。学习顺序建议是先会用 `DbContext`，再学习迁移、索引、事务、并发控制和性能诊断。

如果目标是后台常驻任务，Worker Service 比 Web API 更直接。它使用同一套 Generic Host、DI、配置和日志模型，只是入口从 HTTP 请求变成 `BackgroundService.ExecuteAsync`。因此先学 ASP.NET Core 再学 Worker Service，会发现很多工程概念可以复用。

测试框架方面，xUnit 在 .NET 开源项目中非常常见，NUnit 在企业和历史项目中也很多，MSTest 与 Visual Studio 生态集成紧密。入门阶段不必纠结测试框架，先掌握 Arrange-Act-Assert、依赖替换、HTTP 集成测试和数据库隔离。

## 学习路线

1. 先阅读语言章节：[C# / .NET 语言介绍](../../languages/csharp-dotnet/) 与 [基础语法速览](../../languages/csharp-dotnet/syntax/)。
2. 阅读本索引，建立 .NET 应用模型地图：Web、UI、数据访问、后台任务、实时通信、测试。
3. 进入 [ASP.NET Core](aspnet-core/)：先理解 Host、Middleware、Routing、DI、Configuration、Options。
4. 跑通 [ASP.NET Core quickstart](aspnet-core/examples/quickstart/)：观察一个请求如何从中间件进入 endpoint，再调用服务返回 JSON。
5. 把 quickstart 的内存仓储替换为 EF Core：先使用 InMemory 或 SQLite provider，再学习 migrations 和真实数据库连接。
6. 根据方向扩展：Web 页面学 MVC/Razor Pages，实时通信学 SignalR，内部服务学 gRPC，后台任务学 Worker Service，客户端学 MAUI 或 Blazor。

## 本仓库案例

- [ASP.NET Core](aspnet-core/)：讲解 .NET Web 平台的核心思想、请求生命周期、DI、配置、Options 与 EF Core 接入路径。
- [ASP.NET Core quickstart](aspnet-core/examples/quickstart/)：一个真实可运行的 Minimal API 项目，包含 `.csproj`、`Program.cs`、配置文件、路由、服务、仓储、Options 和自定义中间件。
