# Dart

## 语言定位

Dart 的第一版学习基线是 **3.12.x**，工具链入口是 **Dart 3.12**。Dart 最知名的使用场景是 Flutter，但它本身是一门面向客户端体验、快速迭代和稳定工程交付设计的通用语言。它既能 JIT 热重载提升开发速度，也能 AOT 编译发布产物，还可编译到 Web 相关目标。

Dart 的设计哲学是“对应用开发友好”：语法接近主流 C 系语言，类型系统提供可靠约束，空安全把大量空值错误提前暴露，异步模型直接服务 UI、网络和事件驱动程序。学习 Dart 时要把语言和 Flutter 适度分开：先掌握 Dart 的类型、集合、异步、错误和包管理，再进入 widget、状态管理和平台集成，会更稳。

## 适合场景

Dart 适合 Flutter 移动端、桌面端、Web UI、原型产品、跨平台客户端工具，以及需要共享业务模型的前端团队。它的语法学习成本相对平滑，标准工具链统一，格式化、分析、测试和依赖管理都有官方默认方案。对于 UI 业务，Dart 的异步、空安全和声明式对象构造非常贴合日常需求。

不适合场景包括：极度依赖浏览器原生 JavaScript 生态的项目、需要大量科学计算或底层系统库的任务、团队完全不使用 Flutter 且无法从 Dart 生态获益的后端服务、以及对运行时体积和启动开销极端敏感的嵌入式场景。Dart 可以写 CLI 和服务端，但它的最大生态红利仍然在 Flutter 和客户端应用。

## 核心语法

Dart 使用 `var`、显式类型、`final` 和 `const` 声明变量。`final` 表示引用只赋值一次，`const` 表示编译期常量；在 Flutter 中理解二者差异会直接影响 widget 构造和性能。函数是一等值，支持可选位置参数、命名参数、默认值和箭头函数。类、枚举、扩展方法、mixin、泛型和库导入是组织代码的基础。

集合字面量是 Dart 的高频语法：`List`、`Map`、`Set` 配合集合 `if`、集合 `for`、展开运算符，可以很自然地构造 UI 列表或数据转换结果。Dart 还支持模式匹配、记录、sealed class 等现代特性，用于表达结构化数据和有限状态。惯用写法强调清晰命名、不可变数据、命名参数、早返回，以及通过小类或 sealed 层次表达业务结果。

## 类型/内存/并发模型

类型模型：Dart 是带类型推断的静态类型语言，支持 sound null safety。默认情况下变量不能为 `null`，只有写成 `T?` 才表示可空；通过类型提升，编译器能在判空后自动把可空值收窄为非空值。`dynamic` 会绕过大部分静态检查，应只在 JSON、反射式边界或渐进迁移时谨慎使用。泛型在集合、仓储、状态容器和结果类型中非常常见。

内存与资源：Dart 使用垃圾回收管理对象内存，开发者主要关注对象生命周期、监听器取消、流订阅关闭、文件和 socket 释放。Flutter 中还要注意 `State.dispose`、控制器和动画对象的释放。不可变对象可以降低 UI 重建和状态共享的复杂度，`const` 构造也能帮助框架复用对象。

并发模型：Dart 的日常异步以事件循环、`Future`、`async/await` 和 `Stream` 为核心，适合网络请求、计时器、文件 I/O 和 UI 事件。CPU 密集任务不应阻塞主 isolate；需要并行计算时使用 isolate，让消息在隔离内存之间传递。学习时要明确：`Future` 不是线程，`await` 让异步流程可读，但不会自动把计算挪到后台线程。

## 标准库与包管理

包管理入口：pub。`pubspec.yaml` 描述包名、SDK 约束、依赖、开发依赖和资源，`dart pub get` 安装依赖，`pubspec.lock` 锁定应用依赖版本。常用命令包括 `dart run`、`dart test`、`dart format`、`dart analyze`。标准库中 `dart:core` 自动导入，`dart:async`、`dart:convert`、`dart:io`、`dart:collection` 在数据处理和工具脚本中很常用。

生态方面，Flutter 项目会大量使用 pub.dev 包，例如路由、状态管理、网络、序列化、本地存储和代码生成工具。第一阶段案例优先使用标准库，避免一上来就陷入框架选择；进入 Flutter 后，再比较 Provider、Riverpod、Bloc、go_router、dio、freezed、json_serializable 等生态工具的取舍。

## 错误处理

Dart 使用 `throw`、`try`、`catch`、`on`、`finally` 处理异常。通常用 `Exception` 表示可预期的运行失败，用 `Error` 表示程序错误或不应恢复的问题。异步错误会随 `Future` 和 `Stream` 传播，因此 `await` 调用要放在合适的 `try/catch` 中，流也要处理错误事件。

业务层不一定要把所有失败都做成异常。对于登录失败、校验失败、远端返回错误等可预期情况，可以用 sealed class 或结果类型表达成功与失败，让 UI 或调用方穷尽处理。错误处理的关键是边界清楚：底层保留技术细节，中间层转换成领域错误，界面层展示用户能理解的状态。

## 工程化

Dart 工程默认工具链很完整。`dart create` 或 `flutter create` 生成项目，`analysis_options.yaml` 配置 lint，`dart format` 保持风格一致，`dart analyze` 做静态检查，`dart test` 运行测试。库代码通常放在 `lib/`，测试放在 `test/`，命令行入口放在 `bin/`，Flutter 应用还会有 `assets/`、平台目录和集成测试目录。

大型 Dart/Flutter 工程要关注模块拆分、状态管理边界、依赖版本约束、代码生成可重复性、国际化、性能分析、包体积和平台差异。CI 应至少执行格式检查、静态分析和测试。发布前还要关注权限、签名、崩溃上报、日志脱敏和网络错误降级。

## 常见坑

- 只学习 Flutter widget，不理解 Dart 的空安全、异步、集合和包管理，后期很难定位问题。
- 滥用 `dynamic`、`!` 和可空类型，把 sound null safety 的保护主动拆掉。
- 误以为 `async/await` 等于多线程，在主 isolate 中执行重计算导致 UI 卡顿。
- 忘记取消 `StreamSubscription`、关闭控制器或在 Flutter `dispose` 中释放资源。
- 在 `pubspec.yaml` 中放宽依赖过度，导致团队环境解析出不同版本。
- 把所有错误都弹 toast 或打印日志，没有在领域层建立可测试的失败模型。

## 案例索引

- [特性与思想辅助教学](features/)：通过解释和可运行例子理解语言设计。
- [hello](examples/hello/)：最小程序与运行方式
- [data-flow](examples/data-flow/)：数据建模、集合处理和函数组合
- [errors](examples/errors/)：错误建模、恢复和资源边界

建议按 `hello`、`data-flow`、`errors` 推进：先确认 SDK 和入口函数，再练习集合、空安全和不可变数据，最后观察同步异常、异步错误和结果类型。

## 版本来源

- 策略：`latest-stable-no-lts`
- 官方来源：https://dart.dev/get-dart/archive
- 校验日期：2026-05-30
