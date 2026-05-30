# C# / .NET

## 语言定位

C# / .NET 的第一版学习基线是 **.NET 10.0.8 LTS**，工具链入口是 **.NET SDK 10.0.8**。它主要用于：企业后端、桌面、游戏、云服务。

C# 是 .NET 平台的主力语言，定位是“托管运行时上的现代多范式工程语言”。它从面向对象起家，但长期吸收函数式、泛型、模式匹配、异步编程和数据建模能力。今天的 C# 不再只是 Windows 桌面语言；ASP.NET Core、云原生服务、Unity、桌面客户端、CLI 工具和数据处理都在同一套 SDK 与运行时上展开。.NET 的设计哲学强调高性能运行时、统一工具链、强类型 API 和跨平台部署，语言更新也往往与运行时、标准库、CLI、IDE 体验一起推进。

## 适合场景

- 需要理解该生态的工程化默认选择，例如包管理、构建、测试和发布。
- 需要横向比较不同语言在类型、并发和错误处理上的设计取舍。
- 需要从小案例过渡到代表性框架，而不是只背语法。

C# / .NET 适合企业 Web API、后台服务、桌面应用、游戏脚本、云函数、命令行工具和需要较好吞吐的常驻服务。它的优势在于标准库完整、CLI 一致、IDE 和调试体验优秀，异步模型也非常成熟。不适合的场景包括对运行时完全不可接受的裸机/内核开发、极小型 shell 胶水脚本，以及必须依赖某些非 .NET 原生生态的工作流。学习时要同时看语言和平台：C# 语法、BCL、NuGet、SDK、项目文件、运行时诊断是一整套能力。

## 核心语法

重点学习变量/常量、函数、模块、数据结构、泛型或类型标注、控制流，以及该语言最常见的代码组织方式。案例会尽量保持短小，让语法特征直接暴露出来。

C# 代码以 namespace、class、record、struct、interface、方法、属性和事件组织。现代项目可以用顶级语句写最小入口，也可以保留显式 `Program` 类。属性是 C# 的重要惯用法，既能像字段一样使用，又能封装访问逻辑；record 适合不可变数据和基于值的相等性；pattern matching、switch expression、解构和 nullable reference types 让数据分支表达更清晰。

集合处理常用 LINQ，它把过滤、映射、分组、排序和聚合组合成可读的数据管道，但要理解延迟执行和枚举次数。扩展方法常用于给现有类型补充领域操作；attribute 则用于框架元数据、序列化、测试和编译器提示。C# 也支持泛型约束、委托、lambda、事件、索引器和 async/await。学习时不要只追求语法糖，要知道每个特性背后的运行时行为和 API 契约。

## 类型/内存/并发模型

- 类型模型：静态类型、泛型、nullable reference types。
- 并发模型：Task、async/await、TPL。
- 内存与资源：结合语言自己的生命周期管理方式学习，不把所有语言都套成同一种范式。

C# 是静态、名义类型语言，类型分为值类型和引用类型。值类型通常直接包含数据，引用类型通过引用访问对象；装箱会让值类型进入对象世界，可能影响性能。泛型在运行时保留较多类型信息，与 Java 的擦除模型不同。nullable reference types 是编译期约定，用 `string?` 与 `string` 区分可能为空和期望非空，但它依赖项目开启和注解纪律。

内存由 GC 管理，但非托管资源必须通过 `IDisposable` / `IAsyncDisposable` 与 `using` / `await using` 释放。性能敏感代码还会遇到 `Span<T>`、`Memory<T>`、数组池和结构体拷贝。并发模型以 `Task`、`async` / `await`、线程池、TPL、Channel 和并发集合为核心。`async` 不是创建线程，而是把等待中的操作拆成可恢复状态机；取消通常通过 `CancellationToken` 传播。理解同步阻塞、上下文捕获、线程池耗尽和异常聚合，是写可靠 .NET 服务的基础。

## 标准库与包管理

包管理入口：NuGet。第一版案例优先使用标准库，只有框架章节才引入生态依赖。

.NET 标准库，也常被称作 BCL，覆盖集合、I/O、网络、JSON、时间日期、加密、反射、正则、并发、日志抽象、配置和依赖注入等大量基础能力。`System.Text.Json`、`HttpClient`、`DateTimeOffset`、`TimeProvider`、`ILogger`、`IOptions` 等都是现代项目常见入口。NuGet 负责依赖分发，项目文件 `.csproj` 声明目标框架、包引用、nullable、implicit usings、发布方式和编译选项。学习包管理时要关注语义版本、传递依赖、锁文件、私有源和 SDK 版本固定。

## 错误处理

异常、using、Result/OneOf 风格。学习时关注错误如何被表达、传播、恢复，以及如何避免把异常路径藏在业务逻辑里。

C# 没有受检异常，异常通常用于不可直接恢复的失败或跨层传播的错误。业务上可预期的分支，例如校验失败、库存不足、权限拒绝，可以用返回对象、`Result` 风格类型或 OneOf/联合类型风格建模。`using` 负责资源边界，异常发生时也会释放资源；异步资源要用 `await using`。在 async 方法中，异常会存入返回的 Task，只有 await 时才重新抛出。不要用异常控制普通流程，也不要只捕获 `Exception` 后返回默认值；边界层应把错误转换成日志、状态码或用户可理解的信息。

## 工程化

第一阶段关注代码格式、测试入口、依赖声明和可重复运行。大型工程主题，如性能分析、发布、观测和安全，会在框架章节逐步展开。

C# / .NET 的学习路径建议是：先用 `dotnet new`、`dotnet run`、`dotnet test` 建立 CLI 直觉，再学习项目文件、NuGet、nullable、LINQ、async/await 和单元测试，最后进入 ASP.NET Core、Entity Framework Core、Worker Service、MAUI 或 Unity 等方向。工程实践中要熟悉 `.editorconfig`、格式化、Roslyn analyzers、Source Generator、配置分层、日志、OpenTelemetry、容器发布、单文件发布和运行时诊断工具。大型仓库还会使用 solution、Directory.Build.props、中央包版本管理和 CI 缓存。

## 常见坑

- 只学习语法而忽略包管理和项目结构。
- 把其他语言的范式硬搬过来，错过本语言的惯用表达。
- 示例能跑但没有预期输出，导致无法判断自己是否真正理解。

常见坑包括：忘记开启或认真处理 nullable reference types；把 `async void` 用在非事件处理器场景；在异步代码里 `.Result` / `.Wait()` 导致死锁或线程池阻塞；滥用 LINQ 造成多次枚举；没有复用 `HttpClient` 或错误管理其生命周期；误解 record 的浅不可变；忘记释放实现 `IDisposable` 的对象；把所有错误都抛异常导致业务分支不透明。写案例时要同时观察正常输出、异常输出和资源释放时机。

## 案例索引

- [基础语法速览](syntax/)：面向已有编程经验读者的语法快速迁移。
- [特性与思想辅助教学](features/)：通过解释和可运行例子理解语言设计。
- [hello](examples/hello/)：最小程序与运行方式
- [data-flow](examples/data-flow/)：数据建模、集合处理和函数组合
- [errors](examples/errors/)：错误建模、恢复和资源边界

建议按案例顺序学习：hello 用来熟悉 SDK、顶级语句和运行命令；data-flow 用来练习 record、LINQ、集合和不可变建模；errors 用来比较异常、using、返回式错误和异步异常传播。完成后可以把 data-flow 改成一个小型 Web API 或 CLI，体验 .NET 从示例到工程的过渡。

## 版本来源

- 策略：`latest-lts`
- 官方来源：https://dotnet.microsoft.com/en-us/platform/support/policy/dotnet-core
- 校验日期：2026-05-30
