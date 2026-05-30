# Kotlin 基础语法速览

## 读者定位

这份速览写给已经有编程基础、但第一次系统接触 Kotlin 的读者。Kotlin 的语法看起来像 Java、TypeScript 和 Swift 的混合体，但它的核心心智模型更明确：用静态类型表达边界，用空安全把缺失值提前暴露，用小而强的标准库减少样板，同时保留与 JVM 生态互操作的现实感。

如果你来自 Java，要先放下“所有代码都必须写进类里”的习惯。Kotlin 支持顶层函数、顶层属性和脚本文件，简单程序不需要 `class Main`。如果你来自 JavaScript、Python 或 Ruby，要记住 Kotlin 不是动态语言：类型推断只是让你少写类型，编译器仍然知道每个表达式的类型，并会阻止很多运行时才暴露的问题。学习 Kotlin 的重点不是把原来的代码缩短，而是把可空性、可变性、状态集合和错误路径写进接口。

## 运行方式

本仓库的基础示例使用 Kotlin 脚本和标准库。进入示例目录后运行：

```bash
cd languages/kotlin/syntax/examples/syntax-tour
kotlin main.kts
```

`.kts` 文件按脚本方式执行，适合快速观察语法。真实工程通常使用 Gradle 或 Maven，源文件是 `.kt`，并在文件顶部写 `package`。脚本示例可以有 `import`，但通常不写 `package`，因为它不是按项目源码目录编译的模块。把语法迁移到工程时，要同时理解 Kotlin 语言版本、JVM target、Gradle 插件和依赖版本，它们是相邻但不同的概念。

## 语法速览

Kotlin 文件通常由可选 `package`、若干 `import`、顶层声明和类型声明组成。语句末尾不需要分号，代码块使用花括号。函数用 `fun`，变量用 `val` 或 `var`，类和接口可以与函数一样放在文件顶层。表达式能力很强：`if`、`when`、`try` 都可以产生值，所以很多分支不必先声明临时变量再赋值。

Kotlin 的类型默认非空。`String` 和 `String?` 是不同类型；后者必须先通过安全调用、Elvis 运算符、智能类型转换或显式校验处理后才能当作字符串使用。集合也有类似的“接口表达意图”：`List<T>` 是只读接口，`MutableList<T>` 才能增删。它们不等于深度不可变，只是把调用方能做什么写在类型上。

迁移时常见误解是把 Kotlin 当成“更短的 Java”。更准确的理解是：Kotlin 鼓励你把普通对象建模成 `data class`，把有限状态建模成 `sealed class` 或 `sealed interface`，把可空输入变成显式处理路径，把小型领域操作写成扩展函数。短只是结果之一，真正的收益是边界更清楚。

## 类型与值

`val` 声明只读绑定，`var` 声明可重新赋值的绑定。`val name = "Kotlin"` 表示变量名不能再指向别的值，但如果这个值本身是可变对象，例如 `MutableList`，对象内容仍然可以变。需要不可变数据时，除了使用 `val`，还要选择只读集合接口、避免暴露可变内部状态，并用 `copy` 产生新值。

Kotlin 有 `Int`、`Long`、`Double`、`Boolean`、`Char`、`String` 等基础类型；在 JVM 上它们会按场景映射到基本类型或装箱类型。类型推断常用于局部变量，公共 API 则建议显式写返回类型，让调用契约更稳定。字符串模板用 `$name` 或 `${expression}`，比拼接更接近日常写法：

```kotlin
val language = "Kotlin"
val count = 3
val message = "$language has ${count + 1} core ideas to notice"
```

空安全是 Kotlin 最重要的类型特性。`text?.trim()` 只有在 `text` 非空时才调用；`text ?: "fallback"` 在左侧为空时给出兜底值；`requireNotNull(text)` 表示这个边界之后必须非空；`!!` 会把风险推回运行时，除非你能证明不可能为空，否则不应作为日常写法。

## 控制流

`if` 的条件必须是布尔表达式，不会把数字、字符串或对象隐式当作真假值。`if` 可以返回值：

```kotlin
val label = if (score >= 60) "pass" else "retry"
```

`when` 是 Kotlin 的多分支工具，既能替代 `switch`，也能按条件表达式分支。和 `sealed class` 搭配时，编译器可以检查分支是否穷尽；这比字符串状态码可靠得多。没有主题的 `when` 适合写范围或谓词判断，例如 `when { total < 10 -> "low"; total < 20 -> "medium"; else -> "high" }`。

循环常见写法是 `for (item in items)`、`for ((index, item) in items.withIndex())` 和 `while`。范围用 `1..5` 表示包含两端，`0 until size` 表示不包含右端，`downTo` 与 `step` 表达方向和步长。Kotlin 也鼓励在数据转换时使用集合函数，例如 `filter`、`map`、`groupBy`，但有副作用、需要提前退出或调试复杂时，普通循环往往更清楚。

## 函数与模块

函数用 `fun` 声明，参数名在前、类型在后，返回类型写在参数列表后。单表达式函数可以省略花括号：

```kotlin
fun total(hours: List<Int>): Int = hours.sum()
```

默认参数和命名参数是 Kotlin API 设计的重要工具。`fun connect(timeoutMs: Int = 1000, retry: Boolean = true)` 让调用方只覆盖关心的参数；`connect(retry = false)` 比多个重载更清楚。要注意 Java 调用 Kotlin 默认参数需要额外生成重载或使用完整参数，跨语言 API 设计时不能只看 Kotlin 调用体验。

包和导入负责名称组织。`.kt` 文件顶部可以写 `package demo.syntax`，目录通常也跟随包结构；`import kotlin.math.roundToInt` 只是让当前文件能直接使用这个名字，不会复制代码或改变依赖。Kotlin 支持顶层函数，所以工具函数不必塞进 `Util` 类；需要 Java 友好入口时再考虑对象、伴生对象或 `@JvmName`。

扩展函数用 `fun Type.name(...)` 给已有类型增加调用风格，例如 `fun String.normalized() = trim().lowercase()`。它不会真的修改原类型，也不能访问私有成员；它只是静态解析的语法能力。好的扩展函数让领域词汇贴近数据，坏的扩展函数会把副作用藏到看似普通的方法调用里。

## 集合与数据建模

Kotlin 常用集合接口是 `List`、`Set`、`Map` 以及对应的 `MutableList`、`MutableSet`、`MutableMap`。`listOf` 和 `mapOf` 创建只读接口，`mutableListOf` 和 `mutableMapOf` 创建可修改集合。只读接口不承诺底层永远不可变，它只是限制当前引用能做的操作；如果需要跨边界安全快照，可以复制成新集合。

`data class` 适合表达值对象。声明 `data class User(val id: Int, val name: String)` 后，编译器会生成可读 `toString`、按值比较、解构、`copy` 等能力。`copy` 是浅拷贝，字段如果持有可变集合，旧对象和新对象仍可能共享集合引用。设计数据类时优先使用 `val` 字段和只读集合，避免让“看起来像值”的对象携带隐藏可变性。

`sealed class` 或 `sealed interface` 适合表达有限状态或结果层级，例如加载成功、加载失败、需要登录。调用方用 `when` 处理每个子类型时，新增状态会触发编译器提醒。它适合业务状态、UI 状态、解析结果，不适合开放插件体系；如果外部实现者应该能自由扩展，就不要把层级密封起来。

## 错误处理

Kotlin 没有 Java 式受检异常，函数签名不会强迫调用方捕获异常。不可恢复的编程错误可以用 `require`、`check` 或直接抛异常；可预期的业务失败更适合用可空返回值、`Result`、`sealed class` 或领域错误类型表达。选择标准是：调用方是否应该把失败当作普通分支处理。

`try` 可以作为表达式返回值，适合在边界处把异常转换成更明确的结果。标准库的 `runCatching { ... }` 会捕获块内异常并返回 `Result<T>`，后续可以 `getOrElse`、`fold`、`recover`。不要用 `runCatching` 把错误吞成空值后悄悄继续；至少要记录上下文，或者转成调用方能理解的失败分支。

资源释放通常依赖 JVM 的 `AutoCloseable` 和 Kotlin 标准库 `use`，协程里的异常还会涉及取消传播。基础语法阶段先记住一点：Kotlin 给你多种错误表达方式，但不会替你决定边界。API 作者要明确告诉调用者，失败是异常、空值、`Result`，还是 sealed 状态。

## 惯用写法

- 默认使用 `val`，只有确实需要重新赋值时才用 `var`；同时区分“绑定不可变”和“对象不可变”。
- 公共函数写清楚返回类型，局部变量可以依赖类型推断。
- 用 `?.`、`?:`、`let`、`requireNotNull` 处理可空值，避免用 `!!` 逃避建模。
- 字符串拼接优先用模板，复杂多行文本可以用三引号字符串和 `trimIndent()`。
- `if`、`when`、`try` 能作为表达式时就直接返回值，减少先声明后赋值的噪声。
- 默认参数和命名参数能减少重载，但面向 Java 的 API 要考虑互操作。
- 小型数据模型用 `data class`，有限结果集合用 `sealed class` / `sealed interface`。
- 集合转换用 `map`、`filter`、`groupBy`、`sumOf` 等标准库函数；复杂副作用或提前退出用循环。
- 扩展函数适合补充领域词汇，不适合隐藏重逻辑或全局副作用。
- 作用域函数要按意图选择：`let` 常用于可空值转换，`also` 用于旁路观察，`apply` 用于配置对象并返回对象，`run` / `with` 用于在接收者上下文里计算结果。连续嵌套时要警惕 `it` 和 `this` 变得难读。

## 可运行示例

示例位于 [examples/syntax-tour](examples/syntax-tour/)，用一个小型任务汇总脚本串起 `val` / `var`、基础类型、字符串模板、空安全、`if` / `when` / `for`、函数、默认参数、`List` / `Map`、`data class`、`sealed class`、扩展函数、作用域函数和 `runCatching` 错误恢复。

运行：

```bash
cd languages/kotlin/syntax/examples/syntax-tour
kotlin main.kts
```

建议第一次直接运行，第二次把输入里的工时改成负数或空字符串，观察 `runCatching` 与 sealed 结果如何把错误路径保留下来。

## 学习检查

读完后建议确认自己能回答这些问题：`val` 是否让 `MutableList` 的内容不可变？为什么 `String` 不能直接接收 `null`，而 `String?` 调用成员前必须处理？`if` 和 `when` 作为表达式时，分支返回值有什么约束？默认参数和命名参数如何替代部分重载？`data class` 的 `copy` 为什么是浅拷贝？`sealed class` 配合 `when` 能帮你发现哪类遗漏？`List` 和 `MutableList` 的区别是接口能力还是深度不可变保证？什么时候用异常，什么时候用 `Result` 或 sealed 结果？扩展函数为什么不是 monkey patch？`let`、`also`、`apply`、`run` 分别适合哪类局部意图？
