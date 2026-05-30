# pattern-matching-switch

## 目标

这个例子展示 Java 的模式匹配 `switch` 如何处理一组有限的领域类型。客服工单可能是账单问题、技术故障或账号变更；路由函数需要根据具体类型读取不同字段，并返回不同处理队列。模式匹配让“判断类型”和“取得已转换后的变量”合在一个表达式里。

真实工程里经常会遇到这种对象：它们共享一个上层概念，却有不同数据形状。没有模式匹配时，代码常写成 `instanceof` 加强制转换，或者把所有字段塞进一个大 DTO。前者重复又容易漏分支，后者会制造大量无意义的可空字段。本例希望你观察：sealed 类型和 `switch` 表达式配合后，分支围绕真实领域形态展开。

## 特性说明

`SupportTicket` 是 sealed interface，只允许 `BillingIssue`、`TechnicalIssue` 和 `AccountChange` 三种实现。`route` 使用 `switch (ticket)`，每个 `case` 直接声明匹配到的具体 record 变量，例如 `case BillingIssue issue ->`。进入该分支后，`issue` 已经是 `BillingIssue`，可以直接访问 `amount()` 和 `refundRequested()`。

`switch` 在这里是表达式，每个分支都返回字符串，函数整体更像“从工单映射到队列说明”。因为上层类型是 sealed，编译器知道可能的子类型集合；当所有类型都被覆盖时，不需要再写一个含糊的 `default`。这比把未知情况都吞进 `default` 更能暴露新增业务状态。

如果不用模式匹配，`route` 会变成多段 `if (ticket instanceof BillingIssue)`，再手动转换变量。更糟的写法是给 `SupportTicket` 加 `type` 字符串，再按字符串分支，字段也只能靠约定解释。

## 设计取舍

Java 的模式匹配是渐进加入的：它没有放弃名义类型，也没有让所有对象都变成动态结构，而是在静态类型系统里减少样板代码。你仍然需要先设计清楚类型层级；模式匹配只是让消费这些类型的代码更直接。

这个取舍适合 Java 的兼容路线。旧的 `if instanceof` 仍能工作，新代码可以在关键分支上使用 `switch` 表达式提高可读性。代价是它要求你理解“开放层级”和“封闭层级”的区别：如果未来要允许外部插件新增工单类型，sealed 加穷尽 switch 就不合适；如果工单形态由核心系统控制，它们会非常有用。

## 运行

```bash
javac Main.java && java Main
```

## 观察点

- 输出的三行分别进入 billing team、incident queue 和 account team，说明 `switch` 根据实际 record 类型分派。
- `TechnicalIssue` 分支可以直接读取 `service()` 和 `severity()`，没有显式强制转换。
- 代码没有 `default` 分支，是因为 sealed 类型让编译器知道三种情况已经覆盖。
- 尝试新增 `SecurityIssue implements SupportTicket`，你需要更新 `permits` 和 `switch`，这会把新增领域状态推到处理函数面前。

如果把这些工单改成一个含 `kind` 字符串的大 record，输出仍能做出来，但编译器无法知道 `"billing"` 是否拼错，也无法阻止你读取一个对当前工单无意义的字段。

## 延伸练习

- 新增 `SecurityIssue`，包含风险等级和 IP 地址，然后补齐 `route` 分支。
- 把 `switch` 改写成 `if instanceof` 链，对比重复代码和遗漏分支时的反馈。
- 给 `TechnicalIssue` 增加 `LOW` 严重级别的特殊路由，思考是否应该在类型层级、枚举还是分支内部表达这个规则。
- 删除 `AccountChange` 分支，观察编译器会如何提醒非穷尽的 `switch` 表达式。
