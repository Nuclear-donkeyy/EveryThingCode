# C# syntax-tour

## 目标

这个示例用一个小型库存结算程序串起 C# 基础语法。它面向已经会编程的读者：重点不是展示所有关键字，而是观察现代 C# 如何把顶级语句、静态类型、nullable、集合、record/class/interface、异常和 `using` 组合成一个可以运行的程序。

## 覆盖语法

- 顶级语句作为程序入口，显式 `using` 导入命名空间。
- `var` 局部类型推断、`const` 编译期常量、`readonly` 字段、nullable reference types。
- 字符串插值、`decimal` 金额、`DateTimeOffset` 时间。
- `if`、`switch` expression、`foreach`、局部函数和普通方法。
- `List<T>`、`Dictionary<TKey,TValue>`、LINQ 的 `Where`、`Select`、`Sum`。
- `record` 建模不可变数据，`class` 管理可变状态和资源，`interface` 表达显示契约。
- `try` / `catch`、`using var`、`IDisposable` 和 `Dictionary.TryGetValue`。

## 运行

```bash
cd languages/csharp-dotnet/syntax/examples/syntax-tour && dotnet run
```

如果你已经在 `syntax-tour` 目录中，也可以直接运行：

```bash
dotnet run
```

示例只使用 .NET BCL，不需要恢复第三方 NuGet 包。项目文件开启了 nullable 和 implicit usings，但源码仍保留少量显式 `using`，便于观察命名空间的作用。

## 观察点

先看 `Program.cs` 顶部：文件没有手写 `Main` 方法，顶级语句就是入口。`var` 推断出的变量仍是强类型，`const` 税率在编译期确定，而 `InventoryLedger` 内部的 `readonly` 字段是在构造时确定、之后不再替换。`maybeCoupon` 是 `string?`，必须先判断是否为 `null` 才把它当作普通字符串使用。

再看集合部分：`List<Product>` 保存顺序数据，`Dictionary<string, Product>` 提供按 SKU 查询。LINQ 查询先描述过滤和映射，真正枚举时才产生结果；示例用 `ToList()` 固定快照，避免后续重复枚举造成困惑。`switch` expression 把库存数量映射成状态文本，适合这种“输入到输出”的分支。

最后看文件底部的类型声明：`Product` 是 record，适合值对象；`InventoryLedger` 是 class，因为它有状态和释放动作；`IDescribable` 是 interface，调用方只依赖“能描述自己”的能力。`using var ledger = ...` 保证异常发生时也会调用 `Dispose()`，这就是 C# 管理非内存资源的常见边界。

## 修改练习

把 `maybeCoupon` 改成 `"VIP"`，观察折扣分支如何改变输出。再给 `products` 增加一个库存为 `0` 的商品，看看 `switch` expression 如何输出 `sold out`。最后尝试把 `Product` 从 `record` 改成 `class`，比较打印格式、相等性和 `with` 表达式可用性有什么变化。
