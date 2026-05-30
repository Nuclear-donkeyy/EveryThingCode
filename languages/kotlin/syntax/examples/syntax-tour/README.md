# Kotlin Syntax Tour

## 目标

这个示例用一个小型任务汇总脚本串起 Kotlin 的基础语法。它面向已有编程经验的读者，所以重点不是解释“什么是变量和循环”，而是观察 Kotlin 如何用类型表达只读绑定、可空值、默认参数、数据对象、有限结果、集合转换和错误恢复。示例采用 `main.kts`，不需要 Gradle 或第三方依赖，方便先把语言轮廓看清楚。

## 覆盖语法

- `import` 展示标准库名称引入；脚本不写 `package`，真实 `.kt` 工程文件通常会写。
- `val` / `var`、`Int` / `Double` / `String` / `Boolean` 和字符串模板。
- 可空类型 `String?`、安全调用 `?.`、Elvis 运算符 `?:` 和 `let`。
- `if` 表达式、`when` 表达式、`for` 循环和 `withIndex()`。
- `fun`、显式返回类型、单表达式函数、默认参数和命名参数。
- `List`、`MutableList`、`Map`、`filter`、`map`、`groupBy`、`sumOf`。
- `data class` 建模任务，`sealed class` 建模解析成功或失败。
- 扩展函数 `Task.label()` 与 `also`、`run`、`apply` 等作用域函数。
- `runCatching`、`fold` 和 `require` 展示错误处理与恢复边界。

## 运行

```bash
kotlin main.kts
```

如果你从仓库根目录运行，可以先执行：

```bash
cd languages/kotlin/syntax/examples/syntax-tour
kotlin main.kts
```

## 观察点

输出会先打印团队、容量、任务数量、总工时和风险等级，再列出部分任务、标签汇总、被恢复的错误输入，以及经过 `copy` 生成的展示标题。注意 `val accepted = mutableListOf<Task>()` 固定的是变量绑定，不代表列表内容不能新增；如果要限制调用方增删，应暴露为 `List<Task>`。

`TaskInput.title` 是 `String?`，脚本通过 `normalizeTitle` 把 `null` 或空白标题收敛成默认值。`parseHours` 使用 `runCatching` 捕获数字解析和 `require` 校验失败，再把结果折叠成 sealed 状态；后续 `when` 不需要 `else`，因为成功和失败分支已经被类型列完整。`Task.label()` 是扩展函数，它让输出更贴近领域语言，但它不会真的修改 `Task` 类型。

## 修改练习

1. 给 `Task` 增加 `owner` 字段，并用 `groupBy` 按负责人汇总工时。
2. 新增一个 `ParseResult.Skipped` 分支表示空白行，观察哪些 `when` 需要补分支。
3. 把 `accepted` 暴露成 `List<Task>`，再尝试在外部新增任务，理解只读集合接口的边界。
4. 把 `runCatching` 改成普通 `try` 表达式，比较两种错误恢复写法的可读性。
