# Extensions DSL

## 目标

理解扩展函数和带接收者 lambda 如何把普通数据操作组织成更贴近领域的表达。例子构建一个小型检查清单 DSL，并给任务列表增加筛选和统计能力。

## 运行

```bash
kotlin main.kts
```

## 观察点

- `checklist { ... }` 使用带接收者的 lambda，让 `task` 可以像清单上下文里的命令一样调用。
- `List<Task>.ownedBy` 和 `List<Task>.totalMinutes` 是扩展函数，调用起来像成员函数，但没有修改 `List` 的真实定义。
- DSL 的价值不是省几个字符，而是把“创建任务、标记负责人、添加标签、统计工作量”放进同一套领域词汇里。
- 例子保持纯标准库；真实 Gradle Kotlin DSL、Compose DSL 或路由 DSL 会用同样思想处理更复杂的上下文。
