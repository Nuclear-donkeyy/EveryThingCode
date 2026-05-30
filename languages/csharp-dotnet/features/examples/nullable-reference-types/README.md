# nullable-reference-types

## 目标

通过“导入学生资料”的小例子理解 nullable reference types 如何把空值风险提前到编译期。这个例子对应的语言特性是 `string` 与 `string?` 的区别，以及通过入口校验把外部不可靠数据转换成内部非空模型。

真实工程里，空值经常来自表单、数据库、JSON、配置和第三方 API。如果这些值一路以普通 `string` 传入内部模型，错误可能在很深的业务代码里才爆成 `NullReferenceException`。本例把原始行建模为 `RawStudent(string? Name, string? Email)`，再通过 `Student.TryCreate` 生成 `Student(string DisplayName, string Email)`，让“可能为空”和“已经校验过”分开。

## 特性说明

项目文件启用了 `<Nullable>enable</Nullable>`。在这个模式下，`string?` 表示引用可能为 null，编译器会要求你在使用前证明它非空；`string` 表示 API 契约上期望非空。`RawStudent` 的字段来自外部输入，所以允许为空。`Student` 是内部干净模型，字段不允许为空。

`TryCreate` 使用 `out Student? student` 和 `out string? error` 表达返回分支：成功时有学生、没有错误；失败时没有学生、有错误说明。`string.IsNullOrWhiteSpace` 不只是运行时判断，它也帮助编译器在后续分支中理解 `row.Name` 和 `row.Email` 已经不是空白或 null，因此可以安全 `Trim()`。

如果不用 nullable reference types，团队通常只能依赖注释、约定或测试来说明哪个字段可能为空。代码可能到处写 `!` 空值宽恕运算符，或者在每一层重复防御式判断。可空注解的价值是把这种约定放进类型签名，让调用者一看到 API 就知道需要处理什么。

## 设计取舍

可空引用类型是编译期分析，不是运行时隔离墙。旧代码、反射、反序列化、第三方库或显式使用 `!` 仍可能把 null 放进非空变量。因此它应该和边界校验、测试、代码评审一起使用，而不是替代所有运行时验证。

把外部模型和内部模型分开会多写一点代码，但换来更清晰的不变量：进入业务核心的 `Student` 不需要反复猜测名字和邮箱是否存在。对大型服务来说，这种边界转换能减少大量散落的 null 判断。

本例使用 `TryCreate` 返回布尔值，是为了避免把普通校验失败当异常。真实项目也可能使用 `Result<T>`、验证错误列表或框架模型绑定。选择哪种方式取决于错误是否可预期、调用方是否需要收集多个错误，以及团队的错误处理风格。

## 运行

```bash
cd languages/csharp-dotnet/features/examples/nullable-reference-types && dotnet run
```

## 观察点

- 第一条数据会输出 `accepted`，说明经过校验后可以创建非空 `Student`。
- 第二条数据会提示邮箱缺失，证明 `string? Email` 需要在边界处处理。
- 第三条数据会提示名字缺失，说明空字符串和 null 都属于需要拒绝的外部输入。
- `Student` 的属性类型是 `string`，后续输出时不需要再写 `??` 或额外 null 判断。
- 如果把 `RawStudent.Email` 改成 `string`，再传入 `null`，观察编译器如何给出可空性警告。

## 延伸练习

- 给 `RawStudent` 增加 `Phone` 字段，并允许它为空；输出时为缺失号码提供默认文案。
- 把 `TryCreate` 改成返回 `(Student? Student, string? Error)` 元组，比较元组和 `out` 参数的可读性。
- 在成功分支里删除 `string.IsNullOrWhiteSpace(row.Email)` 判断，观察编译器是否允许直接 `Trim()`。
