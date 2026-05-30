# ASP.NET Core 设计笔记

- 版本基线：.NET 10.0.8 LTS
- 语言基线：C# / .NET .NET 10.0.8 LTS
- 核心案例：Minimal API
- 项目策略：只依赖 `Microsoft.NET.Sdk.Web` 随 SDK 提供的 ASP.NET Core shared framework，避免学习者第一次运行就被 NuGet 下载或数据库配置挡住。
- 教学边界：案例使用内存仓储展示 endpoint -> service -> repository 的调用关系；EF Core 作为下一步练习接入。
- 下一步：增加 xUnit 集成测试项目，并提供 EF Core SQLite 版本作为第二案例。
