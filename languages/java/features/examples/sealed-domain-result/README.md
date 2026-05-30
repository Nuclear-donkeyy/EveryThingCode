# sealed-domain-result

## 目标

这个例子展示 sealed interface 如何把有限领域结果写进类型系统。付款处理不返回裸字符串或魔法数字，而是返回 `PaymentResult` 的几个已知实现：成功、拒绝、待审核。调用方处理结果时面对的是明确的领域状态，而不是猜测某个状态码是什么意思。

真实工程里，支付、审批、风控、任务执行这类流程经常有一组有限状态。如果这些状态用字符串表示，`"APPROVED"`、`"approved"`、`"OK"` 很容易在不同模块中漂移；状态携带的数据也会散落在多个可空字段里。本例希望你观察：sealed 类型层级让“付款结果只有这几种形态”成为编译期事实，每种结果只携带自己需要的数据。

## 特性说明

`sealed interface PaymentResult permits Approved, Declined, NeedsReview` 限定了能实现 `PaymentResult` 的类型集合。`Approved`、`Declined` 和 `NeedsReview` 都是 `record`，分别保存确认号、拒绝原因和人工审核说明。`PaymentService.charge` 根据金额返回不同结果，`describe` 再按结果类型组织业务输出。

如果不用 sealed 类型，常见写法是返回一个 `Map`、DTO 或字符串状态码，再附带一堆可空字段。调用方必须记住“成功时 confirmationCode 不为空，拒绝时 reason 不为空”，这些约定无法靠类型系统检查。新增状态时，也很难知道哪些分支需要更新。

## 设计取舍

Java 的 sealed 设计不是让继承更自由，而是让某些继承层级更可控。普通接口适合开放扩展，例如插件、驱动、支付渠道；sealed interface 适合表达封闭领域集合，例如语法树节点、命令结果、审批状态、解析结果。

它的代价是扩展位置需要被明确管理。你不能在任意模块随手加一个新的 `PaymentResult` 实现；这对开放生态不方便，但对核心领域模型很有价值。团队可以在一个地方审查状态集合，调用方也能围绕有限结果写出更完整的处理逻辑。

## 运行

```bash
javac Main.java && java Main
```

## 观察点

- 第一行 `approved A-100...` 来自 `Approved`，说明成功结果携带确认号。
- 第二行 `declined B-200...` 来自 `Declined`，说明拒绝结果携带原因，而不是把原因塞进所有结果都共有的可空字段。
- 第三行 `review C-300...` 来自 `NeedsReview`，说明大额支付进入人工审核分支。
- `PaymentResult` 的实现类型只出现在 `permits` 列表中。尝试新增一个没有被允许的实现，编译器会拒绝。

如果把结果改成字符串状态码，`describe` 很可能变成一串 `if ("APPROVED".equals(status))`。这种写法无法表达每个状态需要的数据，也更容易在新增状态时漏改调用方。

## 延伸练习

- 新增一个 `SystemFailure` 结果，包含错误码和是否可重试，然后更新 `permits` 和 `describe`。
- 把 `describe` 改成 Java 的模式匹配 `switch`，与 `pattern-matching-switch` 例子对比。
- 尝试删除 `NeedsReview` 的处理分支，思考普通 `if` 链和 `switch` 表达式在完整性提示上有什么差异。
- 把 `PaymentResult` 改成字符串状态码版本，列出你需要额外维护的字段约定。
