# records-patterns

## 目标

通过一个学习计划模型观察 C# 如何把面向对象、泛型、record、不可变更新和模式匹配组合起来。例子里的仓储只存在内存中，但它展示了真实项目里常见的接口边界和泛型约束。

## 运行

```bash
cd languages/csharp-dotnet/features/examples/records-patterns && dotnet run
```

## 观察点

- `IEntity` 是面向对象的契约，`InMemoryCatalog<T>` 用泛型约束表达“只接收有 Id 的对象”。
- `CoursePlan` 是 record，`with` 表达式创建新计划，不直接修改原对象。
- `Describe` 用模式匹配把业务分类写成表达式，分支条件比嵌套 `if` 更集中。
