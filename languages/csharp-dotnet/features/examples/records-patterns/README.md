# records-patterns

## 目标

通过一个学习计划模型观察 C# 如何把面向对象、泛型、record、不可变更新和模式匹配组合起来。例子里的仓储只存在内存中，但它展示了真实项目里常见的接口边界和泛型约束。

这个例子对应的核心思想是：用类型表达业务事实，用模式匹配集中表达分支。学习者应该看见 `CoursePlan` 不是随手拼出来的字典，而是有名字、有字段、有相等性规则的领域数据；`InMemoryCatalog<T>` 也不是只能保存课程的容器，而是“任何有 `Id` 的实体都可以保存”的泛型边界。

## 特性说明

`record` 适合表达值对象、命令、事件、配置、查询结果等“内容比身份更重要”的数据。这里的 `CoursePlan` 使用主构造参数声明字段，编译器会生成构造函数、属性、基于值的相等性和较友好的 `ToString()`。`with` 表达式基于已有计划复制出新计划，突出“生成新值”而不是在远处修改旧对象。

模式匹配把业务分类写在 `Describe` 的 `switch` 表达式里。`{ Minutes: >= 60, Tags.Count: >= 2 }` 说明这个分支关心对象形状和属性条件，`when tags.Contains("records")` 说明可以在结构匹配后再加守卫条件。与多层 `if` 相比，分支更集中，返回值也更明确。

接口和泛型展示了另一层工程价值。`IEntity` 定义最小契约：对象必须有 `Id`。`InMemoryCatalog<T> where T : IEntity` 让仓储不依赖具体课程类型，同时保留编译期检查。如果不用泛型，代码常会退化成 `Dictionary<string, object>` 加强制转换；如果不用接口，仓储又会被锁死在单一实体类型上。

## 设计取舍

`record` 让数据建模很简洁，但它不是“所有 class 的替代品”。它默认提供的是浅层不可变倾向：`CoursePlan` 的 `Tags` 类型是 `IReadOnlyList<string>`，调用方不能通过接口直接 `Add`，但如果底层传入的是可变列表，仍可能被外部修改。真实项目里如果需要强不可变，可以复制集合或使用不可变集合库。

模式匹配适合表达有限、清晰的分类规则；当规则来自数据库、配置或需要由业务人员维护时，把大量条件硬写进 `switch` 反而会降低灵活性。这个例子故意把规则保持在三条以内，让你观察语言特性本身，而不是搭建完整规则引擎。

泛型仓储能展示边界抽象，但真实系统中的仓储还要考虑并发、事务、生命周期和持久化错误。这里选择内存字典，是为了让注意力停在“类型约束如何保护 API”上。

## 运行

```bash
cd languages/csharp-dotnet/features/examples/records-patterns && dotnet run
```

## 观察点

- `IEntity` 是面向对象的契约，`InMemoryCatalog<T>` 用泛型约束表达“只接收有 Id 的对象”。
- `CoursePlan` 是 record，`with` 表达式创建新计划，不直接修改原对象。
- `Describe` 用模式匹配把业务分类写成表达式，分支条件比嵌套 `if` 更集中。
- 输出中 `cs-101` 会被归类为 deep workshop，因为它满足时长和标签数量条件。
- 输出中 `cs-201` 来自 `fundamentals with { ... }`，说明复制更新能保留结构并替换关键字段。
- 可以尝试给两个字段完全相同的 `CoursePlan` 做 `==` 比较，观察 record 的值相等性。

## 延伸练习

- 给 `CoursePlan` 增加 `Level` 字段，并在 `Describe` 里增加一个 `Advanced` 分支，比较模式匹配和嵌套 `if` 的可读性。
- 把 `Tags` 改成普通 `List<string>` 并在加入仓储后修改它，观察浅不可变带来的风险。
- 新增另一个实现 `IEntity` 的 `LearningPath` record，复用 `InMemoryCatalog<T>`，验证泛型约束没有绑定到课程类型。
