# Swift

## 语言定位

Swift 的第一版学习基线是 **6.3.x**，工具链入口是 **Swift 6.3**。Swift 起初服务于 Apple 平台应用开发，但目标不只是“更现代的 Objective-C”，而是把静态类型、安全默认值、高性能和值语义结合起来。它适合写 iOS、macOS、watchOS、visionOS 应用，也可写服务端、命令行工具、系统工具和跨平台库。

Swift 的设计哲学是：尽量在编译期发现错误，用清晰类型表达模型，用值语义降低共享状态复杂度，同时保留接近系统层的性能控制。`Optional`、协议、泛型、结构体、枚举关联值、`async/await` 和 actor 构成核心学习面。学 Swift 不能只背语法，要理解它为何鼓励“让非法状态难以表示”。

## 适合场景

Swift 最适合 Apple 生态内的客户端应用、长期维护的 UI 业务、对类型安全和性能都有要求的库，以及需要与 C/Objective-C 互操作的系统边界。服务端 Swift 适合希望共享模型、复用语言栈、同时获得较好性能和并发结构的团队。命令行工具也适合处理结构化数据、文件系统和网络请求。

不适合场景包括：团队完全不在 Apple 生态且缺少 Swift 运行环境经验、需要极小运行时或极高可移植性的嵌入式项目、依赖大量 JVM/Node/Python 生态库的业务，以及快速一次性脚本。Swift 可写脚本，但编译模型、包结构和类型系统会让它比 shell、Python 或 Ruby 更“重”。

## 核心语法

Swift 使用 `let` 声明常量、`var` 声明变量，默认鼓励不可变。函数用 `func` 定义，参数标签是 API 可读性的重要部分；调用点是否清楚，往往比函数名更重要。控制流包括 `if`、`switch`、`for-in`、`while`，其中 `switch` 穷尽检查很强，配合枚举关联值可直接表达状态机。

结构体、类、枚举和协议是 Swift 代码组织的核心。结构体和值语义是默认选择，类用于需要引用身份、继承或与 Objective-C 交互的场景。扩展 `extension` 可为类型补充方法、协议实现或便利初始化器。闭包、尾随闭包、属性包装器、结果构建器会在 SwiftUI 和 DSL 风格 API 中频繁出现。

Swift 的惯用法包括：用 `Optional` 显式表达缺失值，用 `guard` 提前退出，用 `map`、`compactMap`、`filter`、`reduce` 处理集合，用协议抽象能力，用枚举承载有限状态。写 Swift 时应避免把所有模型都做成可变类，也不要用字符串常量表达本可以由类型系统承载的状态。

## 类型/内存/并发模型

类型模型：Swift 是强静态类型语言，支持类型推断、泛型、协议、关联类型、不透明返回类型和可选类型。协议不是简单接口替代品，它可以约束能力、提供默认实现，也可以配合泛型实现零成本抽象。`Optional<T>` 是普通类型，不是空指针特例；这迫使调用方显式处理缺失值。

内存与资源：Swift 使用 ARC 管理引用类型生命周期。值类型通常复制语义清晰，标准库集合使用写时复制优化，既保留值语义，又避免无谓复制。类实例之间容易出现强引用循环，需要用 `weak` 或 `unowned` 打破，尤其是闭包捕获 `self` 的场景。资源清理可使用 `defer`，文件句柄、网络连接和锁仍然需要明确边界。

并发模型：Swift 现代并发以 `async/await`、`Task`、结构化并发和 actor 为中心。`async let` 和任务组适合表达有生命周期约束的并发任务；actor 用隔离状态降低数据竞争。学习时要区分并发和并行，也要理解主 actor 与 UI 更新的关系。不要随意逃逸任务、忽略取消或暴露共享可变状态。

## 标准库与包管理

包管理入口：Swift Package Manager。`Package.swift` 描述依赖、target、产品和平台约束，`swift build`、`swift test`、`swift run` 构成最基本的工程循环。标准库提供集合、字符串、可选值、结果类型、序列、并发基础等能力；Foundation 则补足日期、文件、URL、JSON、网络和本地化等常用 API。

Apple 平台开发还会接触 SwiftUI、UIKit、AppKit、Combine、Observation、Core Data 等框架；服务端生态常见 Vapor、Hummingbird、AsyncHTTPClient、swift-log、swift-metrics。第一阶段案例优先使用标准库和 Foundation，先建立语言直觉，再进入平台框架。

## 错误处理

Swift 的错误处理以 `throws`、`try`、`catch` 为主。函数签名中出现 `throws`，调用方就必须处理或继续抛出，这让失败路径在类型层面可见。`Result<Success, Failure>` 适合把成功和失败作为值传递，尤其是在回调、状态机或需要组合的 API 中。`defer` 用于在作用域退出时执行清理逻辑。

惯用 Swift 会把错误类型做成遵循 `Error` 的枚举，并用关联值携带上下文。可恢复错误应在边界转换成用户可理解的信息；不可恢复的程序员错误可用断言或前置条件，但不能拿 `fatalError` 替代正常错误处理。`try?` 和 `try!` 要谨慎：前者会丢失细节，后者会把失败变成崩溃。

## 工程化

Swift 工程的基本入口是 SwiftPM 或 Xcode project。跨平台库和 CLI 推荐从 SwiftPM 开始，目录通常包含 `Sources/`、`Tests/` 和 `Package.swift`。测试使用 XCTest 或 Swift Testing，代码风格可结合 swift-format、SwiftLint 或团队 Xcode 配置。CI 中应固定 Swift 版本，执行 `swift test`，并对不同平台差异保持警惕。

大型工程要关注模块边界、编译时间、泛型复杂度、actor 隔离、ABI/API 稳定性和资源使用。Apple 应用还要处理签名、权限、生命周期、后台任务和 UI 主线程约束。服务端 Swift 则要补齐日志、指标、配置、数据库迁移和部署策略。

## 常见坑

- 只学习语法而忽略 `Package.swift`、target 拆分、测试入口和平台约束。
- 把所有模型都写成类，错过结构体、枚举和值语义带来的简单性。
- 滥用 `!`、`try!` 和强制类型转换，把编译期安全重新变成运行时崩溃。
- 在闭包中强捕获 `self`，造成引用循环；或过度使用 `weak`，导致逻辑悄悄不执行。
- 忽略 actor、主 actor 和任务取消，把旧式回调思维直接搬到结构化并发里。
- 过度追求泛型和协议抽象，让编译时间和错误信息变得难以承受。

## 案例索引

- [特性与思想辅助教学](features/)：通过解释和可运行例子理解语言设计。
- [hello](examples/hello/)：最小程序与运行方式
- [data-flow](examples/data-flow/)：数据建模、集合处理和函数组合
- [errors](examples/errors/)：错误建模、恢复和资源边界

建议先用 `hello` 熟悉运行入口，再通过 `data-flow` 观察结构体、枚举、集合和可选值，最后在 `errors` 中练习 `throws`、`Result` 与 `defer`。

## 版本来源

- 策略：`latest-stable-no-lts`
- 官方来源：https://www.swift.org/install/
- 校验日期：2026-05-30
