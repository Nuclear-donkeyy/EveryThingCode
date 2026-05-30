# C# / .NET 特性与思想辅助教学

## 如何使用

本模块把 C# 的语言特性放回它们要解决的工程问题里学习。建议先读“思想总览”，再按“核心特性地图”选择一个例子运行。每个例子都是独立的最小 .NET 控制台项目，不需要外部 NuGet 包；进入例子目录后执行 `dotnet run` 即可观察输出。

学习时不要只看语法表面。C# 的很多设计都服务于长期维护：类型让边界更明确，泛型让抽象不牺牲类型信息，record 让数据建模更接近业务事实，LINQ 让集合转换像数据流一样组合，async/await 让等待 I/O 的代码仍然保持顺序阅读，nullable reference types 则把“可能为空”提前到编译期讨论。

## 思想总览

C# / .NET 是“托管运行时上的多范式工程语言”。它保留了面向对象的封装、接口和多态，也持续吸收函数式编程里的不可变数据、表达式化分支、lambda 与声明式数据转换。它的核心取舍不是追求某一种范式的纯粹性，而是在大型项目里让 API 契约、运行时行为、工具链提示和 IDE 重构可以一起工作。

这也解释了为什么 C# 的特性常常成组出现。`record` 不只是少写构造函数，它和模式匹配、`with` 表达式一起鼓励“创建新值，而不是到处修改旧对象”。LINQ 不只是集合工具，而是让过滤、映射、分组和聚合保持同一种可组合形状。`Task` 与 `async` / `await` 不只是异步语法糖，而是把异步操作、异常传播、取消信号和线程池协作放进统一模型。nullable reference types 也不是运行时防空指针机制，而是让编译器和团队约定一起提醒你补齐空值分支。

## 核心特性地图

| 特性/思想 | 解决什么问题 | C# 为什么这样解决 | 建议观察的例子 |
| --- | --- | --- | --- |
| 面向对象与泛型 | 业务对象需要封装状态和行为，集合、仓储、管道又需要复用同一套算法。 | C# 使用名义类型、接口、多态和运行时保留类型信息的泛型，让 API 既能抽象又能保留强类型检查。泛型约束可以表达“这个算法需要对象至少具备什么能力”。 | [records-patterns](examples/records-patterns/) |
| record 与不可变数据 | 普通 class 容易被多处修改，值对象的相等性、复制和调试输出也容易重复书写。 | `record` 默认强调基于值的相等性、主构造参数和 `with` 复制，适合表达订单、配置、事件、查询结果这类“事实数据”。它不是深不可变，集合属性仍要谨慎设计。 | [records-patterns](examples/records-patterns/) |
| LINQ 的声明式数据流 | 集合处理经常包含过滤、映射、排序、分组和聚合，手写循环容易把“做什么”和“怎么迭代”混在一起。 | C# 把 lambda、扩展方法和 `IEnumerable<T>` 组合成统一查询模型，让数据转换可以从左到右阅读。代价是要理解延迟执行和多次枚举。 | [linq-data-flow](examples/linq-data-flow/) |
| async/await 与 Task | 服务端、桌面和 CLI 常要等待文件、网络、数据库或计时器，阻塞线程会浪费吞吐。 | .NET 用 `Task` 表示未来完成的工作，`await` 把等待点编译成状态机，异常和结果仍能用接近同步代码的方式处理。它并不自动创建线程，CPU 密集任务仍要另行建模。 | [async-tasks](examples/async-tasks/) |
| nullable reference types | 引用类型默认可能为 null，空引用错误常常离真正的来源很远。 | C# 用 `string` / `string?` 这类注解把可空性变成编译期契约。它依赖项目启用 `<Nullable>enable</Nullable>` 和团队遵守警告，不能替代运行时校验。 | [async-tasks](examples/async-tasks/) |

## 教学例子索引

- [records-patterns](examples/records-patterns/)：用接口、泛型仓储、record、`with` 和模式匹配表达一个小型学习计划模型。
- [linq-data-flow](examples/linq-data-flow/)：把报名事件转换成课程报表，观察 LINQ 的过滤、分组、排序、投影和延迟执行。
- [async-tasks](examples/async-tasks/)：并发加载三个课程卡片，观察 `Task.WhenAll`、`await`、nullable reference types 和取消令牌的协作方式。

这些例子故意不引入 ASP.NET Core、Entity Framework Core 或第三方函数式库。真实项目中，面向对象和泛型会出现在服务、仓储、控制器、领域模型和测试替身里；LINQ 会连接内存集合、数据库查询和 JSON 处理；async/await 会扩展到 HTTP、数据库、消息队列和后台任务。先用标准库看清语言思想，再进入框架会更稳。

## 学习检查

- 能否说清 `record` 适合表达哪些数据，以及它为什么不是“所有 class 的替代品”。
- 能否把一个手写循环改成 LINQ 管道，并指出哪里发生延迟执行、哪里真正枚举。
- 能否解释 `async` 方法返回 `Task<T>` 时，结果和异常分别在什么时候被观察到。
- 能否在打开 nullable reference types 的项目里，让可能为空的值通过显式判断、默认值或早返回处理。
- 能否为一个泛型方法写出合适的约束，而不是在方法体里依赖强制转换。
