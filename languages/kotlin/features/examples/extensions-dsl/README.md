# Extensions DSL

## 目标

理解扩展函数和带接收者 lambda 如何把普通数据操作组织成更贴近领域的表达。例子构建一个小型检查清单 DSL，并给任务列表增加筛选和统计能力。

这个例子对应 Kotlin 的扩展函数（extension function）和 DSL 思维。真实工程里，很多代码的难点不是缺少语法，而是缺少贴近领域的词汇：发布检查、路由配置、UI 声明、构建脚本、测试夹具都希望读起来像“在当前上下文中描述要做的事”。Kotlin 用扩展函数和带接收者的 lambda 提供这种表达能力。

## 特性说明

`checklist { ... }` 接收一个 `Checklist.() -> Unit`，这叫带接收者的函数类型。进入代码块后，`this` 是 `Checklist`，所以可以直接调用 `task(...)`，像在清单上下文里发命令。每个 `task` 又接收 `TaskBuilder.() -> Unit`，因此配置块里可以直接写 `owner = "Lin"`、`minutes = 25`、`tag("database")`。

`List<Task>.ownedBy` 和 `List<Task>.totalMinutes` 是扩展函数。它们让任务列表获得领域化读法：`releaseChecklist.ownedBy("Lin")` 比 `filterTasksOwnedBy(releaseChecklist, "Lin")` 更贴近“列表自己执行筛选”的阅读习惯。但扩展函数并没有真的修改 `List`，也不能访问 `List` 的私有实现；它只是静态解析的函数调用语法。

## 设计取舍

扩展函数和 DSL 的价值是把常见组合变成清晰词汇，减少重复的工具函数调用和临时变量。Kotlin 标准库、Gradle Kotlin DSL、Compose、Ktor 路由、测试断言都大量使用类似思想：在一个明确上下文里暴露有限操作，让调用者写出结构化描述。

代价是过度 DSL 会让代码变得像“另一门小语言”：跳转路径变隐蔽，`this` 与 `it` 容易混淆，副作用如果藏在看似声明式的块里会降低可调试性。这个例子只让 DSL 做构建清单这件事，并让扩展函数保持纯计算；如果不用这些特性，代码通常会退化成一串 `Task(...)` 构造和工具类静态函数，业务意图会被构造细节淹没。

## 运行

```bash
kotlin main.kts
```

## 观察点

- `checklist { ... }` 使用带接收者的 lambda，让 `task` 可以像清单上下文里的命令一样调用。
- `List<Task>.ownedBy` 和 `List<Task>.totalMinutes` 是扩展函数，调用起来像成员函数，但没有修改 `List` 的真实定义。
- DSL 的价值不是省几个字符，而是把“创建任务、标记负责人、添加标签、统计工作量”放进同一套领域词汇里。
- 例子保持纯标准库；真实 Gradle Kotlin DSL、Compose DSL 或路由 DSL 会用同样思想处理更复杂的上下文。
- 运行输出先列出 Lin 的两个任务，再给出总工作量，说明 DSL 构建出的仍然是普通 `List<Task>`，后续可以继续用标准库集合函数处理。

## 延伸练习

- 给 `TaskBuilder` 增加 `priority` 字段，并写一个 `List<Task>.highPriority()` 扩展函数。
- 把 `ownedBy` 改成忽略大小写匹配，思考这个规则应该放在扩展函数里，还是放在更明确的查询对象里。
- 在 `task` 中拒绝 `minutes <= 0` 的任务，比较在 builder 阶段校验和在构建后过滤的差别。
