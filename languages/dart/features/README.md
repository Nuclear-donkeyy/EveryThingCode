# Dart 特性与思想辅助教学

## 如何使用

这个模块把 Dart 的语言思想和可以运行的短例子放在一起。建议先读“思想总览”，再按“核心特性地图”挑一个主题进入 `examples/` 目录运行。每个例子都只使用标准库，在对应目录执行 `dart run main.dart` 即可。

学习时不要只看输出，还要观察代码为什么这样分层：哪些值允许为 `null`，异步结果怎样回到调用方，事件流为什么可以逐个到达，类、mixin 和 extension 分别承担什么职责。Dart 常被放在 Flutter 语境里学习，但这些例子刻意放在 Flutter 之前，先把语言本身的类型、异步和组合方式讲清楚。

## 思想总览

Dart 的核心取舍是为应用开发提供“足够静态、足够顺滑”的语言基础。它有静态类型、泛型、空安全、类和现代模式匹配，让大型 UI 与客户端业务可以在编译期发现很多错误；同时它保留了简洁字面量、命名参数、`async/await` 和热重载友好的运行模式，让日常迭代不被繁重样板代码拖住。

Flutter 让 Dart 变得知名，但 Dart 不是只能写 widget。进入 Flutter 之前，学习者应该先理解：默认非空类型如何逼迫你认真建模缺失值；`Future` 和 `Stream` 如何描述一次结果与多次事件；isolate 为什么用消息传递隔离内存；class、mixin、extension 如何把“数据、可复用能力、外部补充方法”分开。这些语言基础决定了后面写 UI、状态管理、网络层和领域模型时的判断。

## 核心特性地图

### sound null safety

- 解决什么问题：客户端应用大量处理用户输入、远端 JSON、本地缓存和页面状态。传统可空引用会让错误推迟到运行时，典型表现是某个值偶尔为 `null`，直到深层调用才崩溃。
- Dart 为什么这样解决：Dart 默认类型不可为 `null`，只有 `T?` 明确表示可空；判空后编译器会做类型提升，让后续代码把值当作非空使用。这样的 sound null safety 把“这个值到底能不能缺失”写进类型系统，同时保留了 `?.`、`??`、`late` 等工具处理真实世界的渐进初始化。
- 学习者应该观察哪个例子：看 [null-safety-results](examples/null-safety-results/) 如何不用 `!` 强行解包，而是用可空输入加 sealed 结果类型表达“找到、缺失、数据无效”三种状态。

### Future 和 Stream

- 解决什么问题：应用常常等待网络请求、文件读写、计时器或用户事件。如果所有等待都阻塞当前执行流，界面和命令行交互都会卡住；如果把回调随意嵌套，错误传播和执行顺序又很难看懂。
- Dart 为什么这样解决：`Future<T>` 表示稍后完成的一次结果，`async/await` 让异步流程像同步代码一样读；`Stream<T>` 表示按时间到达的一串事件，可以被 `await for` 消费，也可以处理错误事件和取消订阅。Dart 把这些作为标准库核心能力，是因为 UI 与事件驱动程序需要稳定、统一的异步模型。
- 学习者应该观察哪个例子：看 [future-streams](examples/future-streams/) 中一次性加载用户列表用 `Future`，持续进度更新用 `Stream`，两者都在同一个事件循环模型下运行。

### isolate 思想

- 解决什么问题：`async/await` 能让 I/O 等待不阻塞，但不会自动把 CPU 密集计算挪到后台。如果在主 isolate 中压缩大文件、解析大 JSON 或做图像处理，UI 仍然可能卡顿。
- Dart 为什么这样解决：Dart 的 isolate 拥有独立内存，通过消息传递交换数据，而不是多个线程共享同一堆对象。这样牺牲了一部分直接共享对象的便利，换来更清晰的并行边界和更少的数据竞争。Flutter 项目里主 isolate 负责 UI，重计算可以交给新的 isolate 或 `Isolate.run`。
- 学习者应该观察哪个例子：本模块没有单独启动 isolate，以避免把第一组例子变复杂；请先观察 [future-streams](examples/future-streams/) 对“异步等待不等于并行计算”的说明，再尝试把其中耗时计算替换为 isolate。

### class、mixin 和 extension

- 解决什么问题：应用代码既需要有状态的数据对象，也需要跨多个类复用行为，还常常想给标准库类型补充领域方法。如果全部靠继承，会让层级变深，行为来源难追踪。
- Dart 为什么这样解决：`class` 表达对象的身份、字段和核心方法；`mixin` 表达可被多个类组合的能力；`extension` 在不修改原类型、不继承原类型的前提下添加调用语法。三者分工让模型、能力和便利方法可以分别演进。
- 学习者应该观察哪个例子：看 [extensions-mixins](examples/extensions-mixins/) 如何用 `class` 表达课程任务，用 `mixin` 复用评分规则，用 `extension` 给 `Iterable<LessonTask>` 补充汇总方法。

### Flutter 前的语言基础

- 解决什么问题：很多学习者一上来写 Flutter widget，却不理解 Dart 的命名参数、不可变数据、集合操作、异步错误和空安全。结果是 UI 能画出来，但状态与数据边界很脆弱。
- Dart 为什么这样解决：Flutter 的声明式 UI 大量依赖 Dart 语言基础：构造函数和命名参数让 widget 树可读，`final` 和 `const` 帮助表达不可变对象，集合 `if`/`for` 适合构造子组件列表，`Future`/`Stream` 对应远端数据与持续事件。先学语言，会让后面的框架概念更有落点。
- 学习者应该观察哪个例子：三个例子都不使用 Flutter；先把类型、异步和组合方式跑通，再回到 Flutter 时就能把 widget 当作 Dart 对象来理解。

## 深入理解与对比练习

### Dart 是 Flutter 之前的一门完整语言

很多人从 Flutter 认识 Dart，于是只把它当作 Widget 语法载体。实际上 Dart 的 null safety、Future/Stream、extension、mixin、isolate 和包管理都值得单独学习。语言基础越清楚，写 Flutter 时越容易理解状态、异步加载、事件流和组件组合。运行这些例子时，可以暂时忘掉 UI，专注观察数据和异步边界。

### sound null safety 把缺失变成类型事实

Dart 的空安全是 sound 的：如果一个变量类型不是可空，编译器就能相信它不会是 null。学习 `null-safety-results` 时，可以尝试把可空值直接传给非空参数，观察需要显式判断或提供默认值。这个机制的价值不是减少几个 `if`，而是让模型入口处就决定哪些字段必须存在、哪些字段允许缺失。

### Future 是一次结果，Stream 是一串结果

`Future<T>` 表示未来某个时刻完成一次，`Stream<T>` 表示随时间到来的多个值。学习 `future-streams` 时，先观察 Future 的等待，再观察 Stream 的 `await for`。把传感器、按钮点击、文件下载进度想象成 Stream，把一次 HTTP 响应想象成 Future，你会更容易判断真实 Flutter 代码里该用哪种抽象。

### isolate 是并行和隔离的边界

Dart 的 isolate 不共享内存，通过消息传递通信。这和很多语言的共享线程模型不同：它降低数据竞争风险，但也要求数据跨边界复制或转移。即使当前例子不启动 isolate，也要理解这个思想：CPU 密集任务不应该阻塞 UI isolate，跨 isolate 的数据必须设计消息协议。后续可以把大计算从主流程拆到 isolate 作为进阶练习。

### mixin 和 extension 分别解决复用和表达

mixin 适合把一组可复用行为组合进类，extension 适合在不修改原类型的情况下增加调用表达。学习 `extensions-mixins` 时，观察哪些行为属于对象能力，哪些只是调用便利。过度 mixin 会让行为来源难追踪，过度 extension 会让 API 看似无处不在。好的使用方式应该让领域表达更清楚，而不是制造隐形依赖。

### Flutter 状态管理依赖语言基础

Widget rebuild、异步加载、表单校验和状态流动都离不开 Dart 基础。Optional 风格的可空值决定加载状态，Future/Stream 决定异步数据形态，class/mixin/extension 决定模型组织。学完这些例子后，可以尝试把一个“加载中/成功/失败”的 UI 状态建成 sealed class，再思考它如何映射到 Flutter 页面。

## 教学例子索引

- [null-safety-results](examples/null-safety-results/)：用 sound null safety、sealed class 和模式匹配表达缺失值与业务结果。
- [future-streams](examples/future-streams/)：用 `Future` 表达一次异步结果，用 `Stream` 表达连续事件。
- [extensions-mixins](examples/extensions-mixins/)：用 class、mixin 和 extension 拆分模型、复用行为与领域便利方法。

## 学习检查

- 你能否指出例子中哪些类型允许为 `null`，以及为什么其他字段不需要判空？
- 你能否说明 `Future` 是“一次结果”，`Stream` 是“一串事件”，并给出各自适合的业务场景？
- 你能否解释为什么 CPU 密集任务需要 isolate，而不是只给函数加上 `async`？
- 你能否判断一个能力应该放进 class、mixin 还是 extension？
- 你能否在进入 Flutter 前，用纯 Dart 写出清晰的数据模型、异步调用和错误/结果处理？
