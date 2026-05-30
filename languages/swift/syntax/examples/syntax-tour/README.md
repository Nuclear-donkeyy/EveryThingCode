# Swift syntax-tour

## 目标

这个示例用一个小型任务统计程序展示 Swift 基础语法如何组合在一起。它不是 Xcode 工程，也不依赖 Foundation 或第三方库；重点是让你在一个 `main.swift` 文件里看到 `import`、常量与变量、可选值、控制流、函数、集合、简单数据建模和错误处理如何协作。

## 覆盖语法

- `import Swift` 和顶层代码构成最小可运行脚本式入口。
- `let`、`var`、显式类型、类型推断、`String` 字符串插值。
- `Optional`、`guard let`、`if`、`switch`、`for-in` 和区间循环。
- 函数参数标签、默认参数、`throws`、`try`、`do/catch`。
- `Array` 保存任务列表，`Dictionary` 按枚举状态统计数量。
- `struct` 建模任务，`enum` 建模状态和错误，`protocol` 表达可展示能力。
- `Result<Task, Error>` 演示把成功或失败保存为普通值。

## 运行

```bash
swift main.swift
```

第一条命令会运行当前目录的 `main.swift`。如果你在仓库根目录，可以先进入示例目录再执行同一条命令：

```bash
cd languages/swift/syntax/examples/syntax-tour
swift main.swift
```

## 观察点

程序先用 `let` 保存固定配置，用 `var` 保存会追加和修改的任务数组。`makeTask(name:hours:status:)` 的 `name` 是 `String?`，所以函数必须先用 `guard let` 处理缺失值；小时数非法时函数抛出 `TaskError`，调用方在 `do/catch` 中分别处理不同错误。

`Task` 是 `struct`，默认按值传递；示例通过数组索引修改其中一个任务，是为了明确展示哪里发生了可变操作。`Status` 是 `enum`，`switch` 必须覆盖每个状态。`Task` 遵循 `Summarizable` 协议后，可以被 `printSummary(_:)` 以协议能力打印，而不需要继承基类。

最后的 `Result` 不会立即抛出错误，而是把一次构造任务的结果保存下来，再用 `switch` 拆开。这个对比能帮助你区分：同步主流程通常用 `throws`，需要把结果作为值传递时用 `Result`。

## 修改练习

- 把 `rawTasks` 中某个任务名改成 `nil` 或 `""`，观察 Optional 和错误分支。
- 新增一个 `Status` case，例如 `.blocked`，看看编译器要求你补哪些 `switch` 分支。
- 给 `Task` 增加 `owner: String?`，在 `summary` 中用 `??` 提供默认负责人。
- 把 `printSummary(_:)` 改成接收 `[Summarizable]`，一次打印多个遵循协议的值。
