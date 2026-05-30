# Swift 基础语法速览

## 读者定位

这份速览面向已经写过其他静态或动态语言、但第一次系统接触 Swift 的读者。Swift 的表面语法接近 C 系语言：花括号、点调用、`if`、`for`、`switch`、函数和类型声明都不陌生；真正需要迁移的是它对“安全默认值”的坚持。Swift 默认鼓励不可变、显式处理缺失值、用类型表达状态，并把很多常见运行时错误提前到编译期。

如果你来自 Java、C# 或 TypeScript，要注意 Swift 的 `struct` 和 `enum` 远比“数据容器”更强，常常是首选建模工具；如果你来自 Python 或 JavaScript，要习惯类型推断不等于动态类型，变量一旦推断出类型就不能随意换成另一类值；如果你来自 C++ 或 Objective-C，要把 `Optional`、值语义和协议组合看成日常设计入口，而不是语法点缀。

## 运行方式

单文件 Swift 可以直接用工具链运行：

```bash
swift main.swift
```

`swift` 会编译并执行脚本式入口，适合语法实验和小型命令行示例。更正式的项目通常使用 Swift Package Manager：`swift package init --type executable` 创建包，`swift run` 运行，`swift test` 测试。Apple 平台应用还会通过 Xcode 管理工程、签名、资源和平台框架。学习基础语法时，先用单文件建立语言直觉，再进入 `Package.swift`、target 和模块边界。

## 语法速览

Swift 用 `let` 声明常量，用 `var` 声明变量。这里的常量不是“编译期常量”那么窄，而是“一旦初始化后绑定不再改变”。惯用 Swift 会先写 `let`，只有确实需要重新赋值或修改值时才换成 `var`。类型可以显式写出，也可以让编译器推断：

```swift
let name = "Swift"        // 推断为 String
var attempts = 1          // 推断为 Int
let ratio: Double = 0.75  // 显式类型
```

类型推断是静态的。`attempts` 推断为 `Int` 后不能再赋值为字符串；这和 JavaScript/Python 的运行时动态类型完全不同。Swift 语句末尾通常不写分号，代码块用花括号，函数调用使用参数标签，例如 `makeTask(name: "build", hours: 2)`。参数标签是 API 可读性的一部分，不只是装饰。

`String` 是标准库的 Unicode 文本类型，字符串插值写作 `"\(value)"`。不要把 Swift 字符串简单想成字节数组：字符、Unicode 标量和 UTF-8 字节是不同层次。入门阶段优先使用 `String` 的高层操作，需要性能或协议边界时再考虑底层编码视图。

`Optional` 是 Swift 最重要的基础类型之一。`String?` 表示“可能有字符串，也可能没有”，本质上类似 `Optional<String>`，不是可随便解引用的空指针。使用前要通过 `if let`、`guard let`、`??` 或可选链显式处理。强制解包 `!` 会把缺失值变成运行时崩溃，日常业务代码应尽量避免。

## 类型与值

Swift 的常见基础类型包括 `Bool`、`Int`、`Double`、`String`、`Character`。局部变量常靠推断，函数参数、返回值、公共 API 和复杂集合建议写清楚类型。Swift 不会把 `Int`、`Double`、`String` 随意隐式转换，跨类型运算需要显式构造，例如 `Double(count)` 或 `String(count)`。

值语义是 Swift 的核心取向。`struct`、`enum`、`Array`、`Dictionary`、`String` 都是值类型：把值赋给新变量时，心智模型上得到一份独立的值。标准库集合使用写时复制优化，所以“值语义”不意味着每次赋值都立刻完整复制内存。它带来的好处是本地推理更容易，函数收到一个值时不必担心别处悄悄改了同一份状态。

`class` 是引用类型，实例有身份，多个变量可以指向同一个对象。类适合需要共享可变状态、继承、对象身份或与 Objective-C/Apple 框架互操作的场景。初学 Swift 容易把所有模型都写成类；更自然的迁移方式是先考虑 `struct`，只有身份和共享状态真的重要时再选择 `class`。

## 控制流

`if` 条件必须是 `Bool`，不会把 `0`、空字符串或空数组当成真假值。Swift 支持把可选绑定放进条件：

```swift
if let title = maybeTitle, !title.isEmpty {
    print(title)
}
```

`guard` 常用于提前退出，能把解包后的值留在后续主路径中。它让错误路径或不满足条件的路径先返回，主逻辑保持较浅缩进。

`switch` 比很多语言更强：它默认不贯穿到下一个 `case`，并要求覆盖所有可能。对 `enum` 做 `switch` 时，编译器会提醒你漏掉的分支；这让 Swift 很适合用枚举表达有限状态。需要兜底时写 `default`，但不要过早使用它，否则未来新增枚举分支时可能失去编译器提醒。

循环常用 `for item in items` 遍历序列，也可以用 `for index in items.indices` 处理索引。`while` 适合条件驱动的循环。Swift 还有区间语法：`0..<3` 不包含 3，`1...3` 包含 3。迁移时要留意区间边界，避免把半开区间和闭区间混用。

## 函数与模块

函数用 `func` 声明，参数类型写在参数名后，返回类型写在 `->` 后：

```swift
func label(name: String, score: Int) -> String {
    "\(name): \(score)"
}
```

Swift 函数的第一个参数默认在调用点省略外部标签，后续参数默认使用参数名作为标签；你也可以用 `_` 省略标签，或提供不同的外部标签。这个设计让调用读起来像短句，例如 `move(from: start, to: end)`。不要为了像其他语言一样“短”而滥用 `_`，Swift API 更重视调用点语义。

模块通过 `import` 引入。单文件示例通常不需要显式导入标准库，因为 `Swift` 标准库默认可见；使用 Foundation、SwiftUI、Dispatch 等框架时才写 `import Foundation`、`import SwiftUI`。在 SwiftPM 项目中，一个 target 会形成模块边界，`public`、`internal`、`private` 等访问级别控制 API 可见性。`import` 不是复制文件，而是引入已编译模块的公开接口。

## 集合与数据建模

`Array<Element>` 常写成 `[Element]`，`Dictionary<Key, Value>` 常写成 `[Key: Value]`。数组保持顺序，字典按键查找，字典键需要可哈希。常见写法如下：

```swift
var names: [String] = ["Ada", "Grace"]
var counts: [String: Int] = ["done": 2]
names.append("Linus")
counts["todo", default: 0] += 1
```

用 `struct` 表达普通数据和行为，用 `enum` 表达有限状态，用 `protocol` 表达能力约束。协议类似接口，但 Swift 协议可以有属性、方法、关联类型和默认实现；类型通过声明遵循协议来承诺能力。`extension` 可以给已有类型补充方法或协议实现，常用于把模型、展示、解析、测试辅助等能力分层放置。

`enum` 不只是整数常量集合。它可以带关联值，能把“几种形态不同的数据”建成一个类型。例如网络状态可以是 `.idle`、`.loading`、`.failed(message: String)`、`.loaded(items: [Item])`。这比用字符串状态和若干可空字段更安全，因为编译器能帮你检查分支是否完整。

## 错误处理

Swift 的可恢复错误通常用 `throws` 表达。会失败的函数在签名中标记 `throws`，调用点必须写 `try`，并通过 `do/catch` 处理或继续向外抛出：

```swift
func parseCount(_ text: String) throws -> Int { ... }

do {
    let count = try parseCount("42")
    print(count)
} catch {
    print(error)
}
```

错误类型通常建成遵循 `Error` 的 `enum`，每个 case 表达一种失败原因，必要时用关联值携带上下文。`try?` 会把错误转换为 `Optional`，适合只关心成功或失败、不关心原因的边界；`try!` 表示你确信不会失败，失败就崩溃，应该非常谨慎。

`Result<Success, Failure>` 把成功或失败作为普通值传递，适合回调、状态机、批处理结果或不想立即抛出的场景。简单同步流程通常用 `throws` 更直接；当错误本身要保存在集合、枚举状态或异步回调中时，`Result` 更合适。不要同时滥用 `Optional`、`throws` 和 `Result` 表达同一件事，先问清楚：这是缺失值、可恢复失败，还是需要保存起来的失败结果。

## 惯用写法

Swift 代码通常从 `let`、值类型和清晰状态开始。能用 `struct` 就先用 `struct`，能用 `enum` 表达有限状态就不要用散落的字符串，能用 `Optional` 表达缺失就不要用哨兵值。集合转换可用 `map`、`compactMap`、`filter`、`reduce`，但简单 `for` 循环同样惯用，关键是让数据流和失败路径清楚。

处理 Optional 时，`guard let` 很常见：它把无效输入排除在函数开头，让后续代码操作非可选值。处理集合字典计数时，`dictionary[key, default: 0] += 1` 比手写存在性判断更简洁。处理协议时，优先让协议描述小而稳定的能力，不要把整棵对象层级塞进一个巨大协议。

命名上，Swift 偏向让调用点自然可读。函数名和参数标签共同组成意思，布尔属性常写成 `isEmpty`、`hasPrefix` 这类可读短语。迁移时不要把 Java/C# 的 `getX()`、`setX()` 习惯照搬过来；Swift 属性访问本身就是 API，计算属性可以隐藏轻量逻辑。

## 可运行示例

本目录提供一个只使用标准库的示例：

- [syntax-tour](examples/syntax-tour/)：用一个小型任务统计程序串起 `import`、`let`/`var`、类型推断、`String`、`Optional`、`if`/`switch`/`for`、函数、`Array`/`Dictionary`、`struct`/`enum`/`protocol`、`throws` 和 `Result`。

进入示例目录后执行：

```bash
swift main.swift
```

建议先直接运行，再修改输入数据：把任务名改成 `nil` 或空字符串，或把小时数改成负数，观察 `throws`、`catch` 和 `Result` 如何把失败路径显式呈现出来。

## 学习检查

读完后可以用这些问题自测：

- 什么时候用 `let`，什么时候必须改成 `var`？
- 类型推断和动态类型有什么区别？
- `String?` 为什么不能当作普通 `String` 直接使用？
- `if let` 和 `guard let` 的作用域差异是什么？
- `switch` 处理 `enum` 时，穷尽检查能帮你避免什么问题？
- 为什么 Swift 里普通模型常先写成 `struct`，而不是 `class`？
- `protocol` 适合表达什么能力，和继承层级有什么不同？
- `throws`、`try?`、`try!` 和 `Result` 分别适合什么边界？
