# C# 基础语法速览

## 读者定位

这份速览面向已经写过至少一门主流语言的人：你可能熟悉 Java、TypeScript、Python、Go、Rust 或 Kotlin，但还没有系统写过 C#。这里不按关键字字典展开，而是把 C# 看成一门运行在 .NET 托管运行时上的静态类型工程语言：编译器、项目文件、BCL 标准库、NuGet 包管理和 IDE 分析器一起构成日常体验。

C# 的语法第一眼像 Java，但现代 C# 的心智更接近“强类型对象模型 + 表达式化控制流 + 标准库数据管道 + 显式资源边界”。它支持顶级语句让小程序像脚本一样开始，也支持 namespace、class、record、interface、泛型、LINQ、async/await 等工程级结构。学习时不要只问“这个关键字等价于哪门语言”，更要问：编译器能帮我证明什么，哪些错误会留到运行时，哪些 API 约定需要我自己遵守。

## 运行方式

最小 C# 程序通常放在一个 SDK 项目里运行：

```bash
cd languages/csharp-dotnet/syntax/examples/syntax-tour
dotnet run
```

`.csproj` 声明目标框架、nullable、implicit usings、包引用和构建选项。现代 SDK 项目默认可以开启 implicit usings，常见的 `System`、`System.Collections.Generic` 等命名空间会自动导入；示例仍会显式写出少量 `using`，帮助你看到 C# 的导入模型。`Program.cs` 可以只写顶级语句，不必手写 `static void Main`，编译器会生成入口方法；当程序长大后，再把逻辑拆到类、record、接口和独立 namespace 中。

## 语法速览

C# 的基本代码单元是语句、表达式、类型声明和成员声明。语句以分号结束，代码块用花括号，类型与成员默认有可见性规则；顶级语句是例外，它让文件开头可以直接写可执行代码，但一个项目只能有一个顶级入口。和 Python 不同，缩进不决定语义；和 Go 不同，异常和泛型是核心语言机制；和 Java 相比，属性、record、模式匹配、nullable reference types、LINQ 和 using 声明更常出现在日常代码里。

常见文件形态有两种。小程序可以在 `Program.cs` 顶部写 `using`，随后写顶级语句，再在文件底部声明辅助类型。工程代码更常见的是 `namespace Company.Product;` 加上多个 class、record、interface 文件。`using` 是导入命名空间，不是导入单个文件；namespace 只是逻辑名字，不要求目录完全一致，但大型项目会让目录和 namespace 对齐以减少认知成本。

## 类型与值

C# 是静态类型语言，但不要求每个局部变量都显式写类型。`var total = 10;` 让编译器从右侧推断出类型，变量之后仍然是强类型的，并不是 JavaScript 的动态变量。迁移时一个常见误解是把 `var` 当成“随便变类型”：它只省略类型名，不改变类型系统。公共 API、复杂泛型返回值或会影响读者理解的地方，显式类型通常更清楚。

`const` 是编译期常量，适合数字、字符串、布尔等可在编译时确定的值；它会被内联到调用方，因此公开 `const` 改值时要注意重新编译依赖方。`readonly` 是运行期只赋值一次的字段，常用于对象构造后不再变化的状态；局部变量没有 `readonly` 关键字，想表达不可变局部通常靠短作用域、record 或只读集合接口。`record` 的主构造参数默认生成只初始化属性，适合表达值对象。

C# 区分值类型和引用类型。`int`、`decimal`、`bool`、`DateTimeOffset`、`struct` 通常是值语义；`string`、数组、class 实例、List 等是引用语义。nullable reference types 开启后，`string` 表示“预期非空”，`string?` 表示“可能为空”。这不是运行时隔离墙，而是编译器分析和注解纪律：你仍可能从旧 API 或反射拿到空值，所以边界处要做检查。值类型用 `int?` 这类 `Nullable<T>` 表示缺失值。

字符串常用双引号，插值用 `$"total: {total:C}"`。插值不是简单拼接模板：花括号里是 C# 表达式，还可以配合格式字符串，例如 `{amount:F2}`。大量路径或多行文本可用原始字符串字面量，但基础阶段先掌握普通字符串、转义和插值即可。

## 控制流

`if` / `else` 与多数 C 风格语言相似，条件必须是 `bool`，不能把整数、字符串或对象隐式当真值。这个选择牺牲了部分简写，但减少了 `0`、空字符串、空集合语义不一致带来的歧义。空值判断常写成 `if (name is null)` 或 `if (name is not null)`，也可以用空合并运算符 `??` 提供默认值。

`switch` 有语句和表达式两种形态。传统 `switch` statement 适合带副作用的分支；`switch` expression 适合把一个输入映射成一个值，并常与模式匹配搭配。C# 的模式不只匹配常量，也能匹配类型、属性、范围和空值，所以它经常替代一串脆弱的 if/else。

循环里 `foreach` 是集合遍历的首选，它依赖 `IEnumerable<T>`，能遍历数组、List、Dictionary、LINQ 查询结果等。`for` 适合需要索引的位置，`while` 适合条件驱动的循环。遍历 `Dictionary<TKey,TValue>` 时元素是键值对，通常写 `foreach (var (key, value) in map)` 或 `foreach (var pair in map)`，注意不要在枚举集合时直接修改同一个集合结构。

## 函数与模块

方法必须声明返回类型，`void` 表示没有返回值。参数默认按值传递；对引用类型来说，“按值传递的是引用副本”，所以方法内可以修改对象内容，但重新赋值参数不会改变调用方变量。C# 支持可选参数、命名参数、表达式体方法、局部函数和 lambda。局部函数适合把只服务当前方法的一小段逻辑命名出来，lambda 更常用于 LINQ 或回调。

顶级语句让示例和 CLI 程序起步很快，但它不是放弃模块化。顶级入口之外，仍应把领域概念放进 class、record、interface 和 namespace。namespace 是类型的逻辑归属，`using` 负责把命名空间带入当前文件；项目引用和 NuGet 包引用负责让程序集可见。一个经验法则是：示例入口可以顶级，业务规则进类型，跨文件共享的 API 放进清晰的 namespace。

方法名和类型名通常使用 PascalCase，局部变量和参数使用 camelCase。属性看起来像字段，调用时写 `product.Name`，但它可以有 getter、setter、init 或计算逻辑。相比直接暴露字段，属性是 C# 框架、序列化、数据绑定和分析器更熟悉的形态。

## 集合与数据建模

常用集合来自 BCL：`List<T>` 表示可变顺序集合，`Dictionary<TKey,TValue>` 表示键值索引，数组适合固定长度或互操作，`HashSet<T>` 适合去重与集合判断。接口如 `IEnumerable<T>`、`IReadOnlyList<T>`、`IReadOnlyDictionary<TKey,TValue>` 常用于参数或返回值，表达“我只需要遍历”或“调用方不应修改”的意图。

`record` 适合数据建模，默认提供值相等、解构、`with` 复制和清晰的打印格式。`class` 适合有身份、生命周期、可变状态或资源边界的对象。`interface` 表达能力契约，C# 的接口可被 class、record、struct 实现，也常用于依赖倒置和测试替身。不要把所有数据都做成 class：如果对象主要是不可变数据载体，record 往往更贴切；如果对象管理文件、网络、数据库连接等资源，class 加 `IDisposable` 更自然。

LINQ 是集合处理的惯用写法，常见链路是 `Where` 过滤、`Select` 映射、`OrderBy` 排序、`GroupBy` 分组、`Any` / `All` 判断、`Sum` / `Average` 聚合。多数 LINQ 操作是延迟执行：定义查询不等于立即跑，直到 `foreach`、`ToList()`、`Count()` 等枚举时才执行。迁移时要小心多次枚举、在查询中隐藏副作用、以及对 `IEnumerable<T>` 做昂贵重复计算。

## 错误处理

C# 使用异常表达失败，没有 Java 式受检异常。`try` / `catch` / `finally` 负责捕获和清理，`throw;` 可以保留原始堆栈重新抛出。异常适合 I/O 失败、格式错误、非法状态等跨层传播的失败；业务上可预期的分支可以考虑返回布尔值、可空值、结果对象或领域类型，不必把一切都抛成异常。

资源释放依赖 `IDisposable` 和 `using`。`using var resource = ...;` 会在当前作用域结束时自动调用 `Dispose()`，即使中途抛异常也会释放；`using (...) { ... }` 则把资源生命周期限定在块内。异步资源使用 `await using`。这和 GC 不冲突：GC 管内存，`using` 管文件句柄、流、锁、数据库连接等需要及时归还的外部资源。

可空值也是错误边界的一部分。`Dictionary.TryGetValue` 用布尔返回值表达“可能没有这个键”，比直接索引再捕获异常更清晰。对于 nullable reference types，编译器会提醒你可能解引用空值，但你仍要在 API 边界做防御式检查。

## 惯用写法

C# 的日常代码强调类型清晰、边界明确和表达式化。小范围局部变量用 `var`，公共签名写清类型；不可变数据优先 record 和 init-only 属性；集合查询优先 LINQ，但在性能敏感或需要复杂控制流时用普通循环；空值处理优先 `?`、`??`、`is null`、`TryGetValue` 这类显式表达，而不是让 `NullReferenceException` 替你发现问题。

字符串优先插值，日志和格式化要注意文化区域和格式字符串。`decimal` 常用于金额，`double` 常用于测量和科学计算；时间点优先 `DateTimeOffset`，不要随意把本地时间和 UTC 混在一起。命名空间通常和目录结构对齐，文件里只放一两个紧密相关的类型，入口代码保持薄，领域规则放进可测试的方法和类型。

LINQ 惯用链路要记住“查询是值，不是结果”。如果要稳定快照，调用 `ToList()`；如果只判断存在性，用 `Any()` 而不是 `Count() > 0`；如果字典查找可能失败，用 `TryGetValue`；如果要从集合构建索引，用 `ToDictionary`，但要保证键唯一。写 C# 时，很多可读性来自选择合适的标准库方法，而不是发明新的循环模板。

## 可运行示例

本目录提供一个最小语法巡览：

- [syntax-tour](examples/syntax-tour/)：用顶级语句串起变量、字符串插值、控制流、方法、List、Dictionary、record、class、interface、异常和 using。

推荐运行：

```bash
cd languages/csharp-dotnet/syntax/examples/syntax-tour
dotnet run
```

示例只依赖 BCL，不需要 NuGet 第三方包。阅读时先看 `Program.cs` 顶部的顶级语句，再看底部 namespace 中的类型声明；这能同时理解“小程序入口”和“工程化类型组织”如何共存。

## 学习检查

完成后可以用这些问题检查自己是否真的迁移了心智模型：

- 你能解释 `var`、`const`、`readonly` 分别在什么时候确定类型或值吗？
- 你能说明 `string` 和 `string?` 的差别，以及 nullable 为什么主要是编译期约定吗？
- 你能把一段 if/else 映射逻辑改写成 `switch` expression，并说明何时不该这么做吗？
- 你能说明 record 与 class 在相等性、可变性和身份上的差别吗？
- 你能预测一个 LINQ 查询什么时候执行，以及为什么多次枚举可能有成本吗？
- 你能用 `using` 解释 GC 之外的资源释放边界吗？
