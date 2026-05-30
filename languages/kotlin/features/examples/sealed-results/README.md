# Sealed Results

## 目标

理解 sealed 层级如何表达有限业务结果，并让 `when` 分支保持穷尽。例子使用简化结账流程，把成功、拒绝和人工审核建模为同一个结果类型的不同子类型。

这个例子对应 Kotlin 的 sealed class / sealed interface 思想：当业务结果是一组已知状态时，把状态集合收进类型系统，而不是散落成字符串、整数码、布尔值和异常。真实工程里，登录、支付、审批、风控、导入任务都经常需要表达“成功但带数据”“失败且有原因”“需要后续处理”这类带载荷的结果。

## 特性说明

`CheckoutResult` 是一个 `sealed interface`，它的直接实现 `Accepted`、`Rejected` 和 `ManualReview` 共同组成完整的结账结果空间。`Accepted` 和 `Rejected` 是 `data class`，因为它们需要携带订单号、收据号或失败原因；`ManualReview` 是 `data object`，因为它只表示一个单例状态，不需要额外字段。

`describe` 使用 `when` 表达式处理结果，而且没有写 `else`。这不是侥幸省略，而是 sealed 层级给了编译器足够信息：如果所有可能子类型都被覆盖，`when` 就是穷尽的。以后给 `CheckoutResult` 新增一个直接子类型时，遗漏处理的 `when` 会被提醒。

## 设计取舍

sealed 层级的优势是把有限状态集中定义，让调用方必须面对每一种结果。它比返回 `"OK"`、`"REJECTED"`、`"REVIEW"` 这样的字符串可靠，因为每个分支可以携带不同结构的数据，也不会因为拼写错误走错逻辑。它也比用异常表达可预期业务失败更温和，因为拒绝付款不是程序崩溃，而是结账流程的一种正常结论。

代价是 sealed 适合“状态集合由当前模块控制”的场景。如果结果类型需要第三方插件任意扩展，sealed 会限制开放性；如果失败只有一个简单原因，普通 `Result` 或 nullable 也可能足够。好的取舍是：当调用者必须知道所有分支、且不同分支携带不同数据时，用 sealed；当错误只是底层异常传播时，不要为了形式感强行包装。

## 运行

```bash
kotlin main.kts
```

## 观察点

- `CheckoutResult` 的直接子类型都在同一个脚本中列出，调用方能看见完整结果空间。
- `when` 没有 `else`，因为 sealed 层级允许编译器检查分支是否覆盖完整。
- 成功和拒绝结果使用 `data class` 携带结构化数据，人工审核使用 `data object` 表示无额外字段的单例状态。
- 这种写法适合有限状态；如果结果类型需要由外部插件任意扩展，就不应该强行 sealed。
- 运行输出会分别出现“通过”“拒绝”和“转人工审核”，对应三个订单输入。这说明结果不是靠单个状态码解释，而是由不同子类型驱动不同展示逻辑。

## 延伸练习

- 新增 `data class PendingPayment(val orderId: String, val retryAfterMinutes: Int)`，再观察 `describe` 是否必须补分支。
- 把 `CheckoutResult.Rejected.reason` 改成一个 sealed 的 `RejectReason`，比较“结果层级”和“原因层级”是否都值得建模。
- 尝试用 `String` 状态码重写这个例子，故意拼错一个状态，再比较 sealed 写法在可维护性上的优势。
