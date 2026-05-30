# Data Classes Copy

## 目标

理解 `data class` 如何表达值对象，并用 `copy`、结构化打印、相等性和解构减少重复样板。这个例子用工单状态流转展示“保留旧对象、生成新对象”的更新方式，同时指出 `copy` 是浅拷贝，不等于深度不可变。

这个例子对应 Kotlin 的 data class 思想：当一个类型主要用于承载数据时，语言可以根据主构造函数生成一组符合值语义的操作。真实工程里的请求 DTO、UI state、配置快照、领域事件和测试数据都经常需要这些能力。

## 特性说明

`Ticket` 声明为 `data class` 后，编译器会生成 `toString`、`equals`、`hashCode`、`copy` 和 `componentN`。脚本先创建一个 `newTicket`，再用 `assignToLin` 和 `closeTicket` 通过 `copy` 生成更新后的对象。每次更新只写变化字段，其余字段沿用原对象，代码表达的是“从旧状态派生新状态”。

脚本还展示了解构：`val (id, title, status) = closed` 读取前三个主构造字段。最后的 `AuditTrail` 故意包含 `MutableList<String>`，用来说明 `copy` 不会递归复制内部对象。两个快照共享同一个可变列表时，修改原列表会影响副本。

## 设计取舍

data class 的收益是减少低价值样板，并让“这个类型按数据比较”变成声明。没有它时，你往往要手写 `equals`、`hashCode`、`toString` 和复制构造，新增字段后还容易漏改，测试输出也不够可读。

代价是它只基于主构造函数属性生成语义，而且 `copy` 是浅拷贝。只读引用 `val` 也不代表对象深度不可变；如果字段里放了 `MutableList`，副本仍可能被共享状态污染。真实项目中，常见取舍是让 data class 尽量包含不可变值和只读集合接口，需要深拷贝时显式写转换函数。

## 运行

```bash
kotlin main.kts
```

## 观察点

- 输出里的 `Ticket(id=..., title=...)` 来自自动生成的 `toString`，不是手写格式化。
- `newTicket == duplicateNewTicket` 为 `true`，说明 data class 默认按主构造字段比较，而不是按引用地址比较。
- `copy` 只写变化字段，适合表达状态演进；原始 `newTicket` 没有被修改。
- `AuditTrail` 的输出会显示副本也看到了后来追加的 `"closed"`，这验证了 `copy` 是浅拷贝。

## 延伸练习

- 给 `Ticket` 增加 `priority: Int`，观察解构变量和 `copy` 调用是否需要调整。
- 把 `labels` 从 `List<String>` 改成 `MutableList<String>`，再尝试修改标签，观察是否会破坏你对“状态快照”的预期。
- 写一个 `fun Ticket.reopen(): Ticket` 扩展函数，用 `copy(status = "open")` 表达重新打开工单。
