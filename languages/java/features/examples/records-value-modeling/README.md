# records-value-modeling

## 目标

这个例子展示 Java `record` 如何用于 value modeling。订单行、金额和订单摘要都被建模为值：它们由字段决定身份，构造后不可变，适合在集合、日志、缓存键和并发任务之间传递。

真实工程里常见的问题是：订单、金额、坐标、时间范围这类对象本来只是“由字段组成的事实”，却被写成可变 JavaBean。调用方可以先创建半成品对象，再一点点 `set` 字段，导致对象在集合里、日志里或跨线程传递时处于不可预测状态。本例希望你观察：`record` 把字段、构造、访问器、相等性和字符串表示绑定在一起，让值对象的语义直接出现在类型声明里。

## 特性说明

`record Money(String currency, BigDecimal amount)` 声明了一个值对象。Java 会为它生成私有 final 字段、同名访问器、基于所有组件的 `equals` / `hashCode`，以及可读的 `toString`。因此两个字段完全相同的 `LineItem` 会被认为相等，放进 `LinkedHashSet` 时只保留一份。

例子还使用紧凑构造器检查 `currency`、`amount`、`sku` 和 `quantity`。这说明 `record` 不是没有规则的数据袋；它适合表达不可变数据，也可以在创建阶段保护不变量。后续 `OrderSummary.from` 可以直接计算金额，不必每次都防御“数量为负”或“币种为空”的坏状态。

如果不用 `record`，代码通常会退化成两种形态：一种是手写普通 class，重复构造器、getter、`equals`、`hashCode`、`toString`，很容易漏掉某个字段；另一种是可变 JavaBean，短期看方便，长期会把“对象什么时候完整”这个约定藏在调用顺序里。

## 设计取舍

Java 选择让 `record` 成为一种受限的类，而不是替代所有 class。它不能继承其他类，组件默认是 final，适合建模“身份不重要，组成字段重要”的数据；但有生命周期、可变状态、延迟加载资源或复杂继承关系的对象仍应使用普通 class。

这个取舍符合 Java 的工程化方向：公共 API 的语义要清楚。`record` 的声明很短，但它真正解决的是长期维护问题：相等性规则统一、对象构造后稳定、字段含义可审查。代价是你需要在建模时区分“值”和“实体”。例如订单号对应的 `Order` 可能有生命周期，而订单行 `LineItem` 更像值。

## 运行

```bash
javac Main.java && java Main
```

## 观察点

- `keyboard equals sameKeyboard: true` 验证了 `record` 的相等性来自组件值，而不是对象地址。
- `unique item count: 2` 说明两个相同订单行进入 `Set` 后被合并，这依赖正确的 `equals` / `hashCode`。
- `order summary: OrderSummary[...]` 展示了 `record` 自动生成的 `toString`，调试友好，但真实项目仍要注意敏感字段。
- 可以把 `new LineItem("mouse", 1, ...)` 的数量改成 `0` 或 `-1`，观察异常在构造阶段出现，而不是等到金额计算时才暴露。

如果把 `LineItem` 改成普通可变 class 且不重写 `equals` / `hashCode`，两个内容相同的订单行会被 `Set` 当作不同对象，汇总结果就可能重复计费。这正是值对象特性要避免的隐性错误。

## 延伸练习

- 给 `Money` 增加币种一致性检查：如果订单行里混入 `EUR`，`OrderSummary.from` 应该拒绝汇总。
- 把 `LineItem` 改成普通 class，只保留字段和 getter，运行后解释 `Set` 行为为什么变化。
- 给 `OrderSummary` 增加平均单价字段，思考它应该是 record 组件、计算方法，还是由调用方临时计算。
- 在 `Money.multiply` 里加入小数位规则，比较把规则放在值对象内部和散落在调用方的差异。
