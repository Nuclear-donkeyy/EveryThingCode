# Ktor core ideas example

## 目标

这个示例把 `Ktor` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

Kotlin 服务端需要把协程、路由、JSON 协商、插件和测试宿主组织清楚。

## 核心思想到代码

Application 是装配根，Plugin 管横切能力，Routing 管入口，ContentNegotiation 管序列化，testApplication 复用真实模块。

```kotlin
fun Application.taskModule() {
    install(ContentNegotiation) { json() }
    routing {
        get("/tasks") { call.respond(store.list()) }
    }
}
```

```kotlin
testApplication {
    application { taskModule() }
    client.get("/tasks")
}
```

## 代码位置

- [`build.gradle.kts`](../quickstart/build.gradle.kts)
- [`src/main/kotlin`](../quickstart/src/main/kotlin)
- [`src/test/kotlin`](../quickstart/src/test/kotlin)

## 运行

先进入 quickstart 目录：

```bash
cd ../quickstart
gradle test
```

如果本机缺少对应工具链，可以先运行仓库根目录的 dry-run：

```bash
python3 scripts/run_framework_examples.py --dry-run
```

## 观察点

测试和生产启动调用同一个 `taskModule`，减少配置漂移。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`Ktor` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
