# Vapor core ideas example

## 目标

这个示例把 `Vapor` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

Swift 服务端需要路由、Request/Response、JSON、middleware、async/await、配置、数据库和测试约定。

## 核心思想到代码

Application 管生命周期，RoutesBuilder 声明入口，Content 管 JSON，Middleware 处理横切逻辑，Fluent 思路管理持久化。

```swift
let app = Application(.development)
defer { app.shutdown() }
try routes(app)
try app.run()
```

```swift
app.get("tasks") { req async throws in
    try await repository.list()
}
```

## 代码位置

- [`Package.swift`](../quickstart/Package.swift)
- [`Sources`](../quickstart/Sources)

## 运行

先进入 quickstart 目录：

```bash
cd ../quickstart
swift build
```

如果本机缺少对应工具链，可以先运行仓库根目录的 dry-run：

```bash
python3 scripts/run_framework_examples.py --dry-run
```

## 观察点

handler 使用 async throws，让异步 I/O 和错误传播进入 Swift 类型系统。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`Vapor` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
