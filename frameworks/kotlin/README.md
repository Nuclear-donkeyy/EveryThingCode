# Kotlin 框架与常用库

Kotlin 的生态横跨服务端、Android、桌面、Web、脚本和多平台共享代码。它不像 Java 那样只围绕大型后端框架展开，也不像 Swift/Dart 那样主要绑定一个 UI 平台；Kotlin 的关键优势是“在 JVM 生态中渐进采用现代语言能力”，同时又能用 Kotlin Multiplatform 把模型、网络、状态和业务规则复用到多个端。

学习 Kotlin 框架时，建议把语言层思想放在前面：空安全、数据类、扩展函数、高阶函数、协程、DSL、sealed 类型和 Gradle Kotlin DSL 都会直接影响框架写法。Ktor 的插件、路由和协程模型，Compose 的声明式 UI 与状态驱动，本质上都是 Kotlin 语言能力在框架层的放大。

## 常用框架清单

| 方向 | 框架/库 | 常见用途 | 本仓库状态 |
| --- | --- | --- | --- |
| Web/API | [`Ktor`](ktor/) | Kotlin-first HTTP 服务端与客户端、插件式应用、协程请求处理 | 已覆盖 |
| 跨平台 UI | [`Compose Multiplatform`](compose-multiplatform/) | Desktop、Android、iOS、Web 等目标的声明式 UI | 已覆盖 |
| Web/API | Spring Boot Kotlin | 使用 Spring Boot、Spring MVC/WebFlux、Spring Data 编写 Kotlin 后端 | 待扩展 |
| Android UI | Android Jetpack Compose | Android 原生声明式 UI、Material Design、生命周期集成 | 待扩展 |
| 多平台共享 | Kotlin Multiplatform | commonMain 共享业务代码，按平台提供 actual 实现 | 待扩展 |
| 数据访问 | Exposed | JetBrains 出品 SQL DSL/DAO，适合 Kotlin 风格数据库访问 | 待扩展 |
| 依赖注入 | Koin / Kodein | Kotlin DSL 风格依赖注入，常用于 Android/KMP/服务端 | 待扩展 |
| 函数式工具 | Arrow | Either、Validated、Option、类型类风格抽象与函数式错误建模 | 待扩展 |
| 测试 | Kotest | Kotlin DSL 测试、属性测试、匹配器、行为规格 | 待扩展 |
| 序列化 | kotlinx.serialization | 编译期生成序列化器，JSON/ProtoBuf/CBOR 等格式 | 待扩展 |
| 异步流 | kotlinx.coroutines / Flow | 协程、结构化并发、冷流、响应式数据管道 | 待扩展 |
| 构建 | Gradle Kotlin DSL | 类型化构建脚本、插件配置、多模块项目组织 | 待扩展 |

## 选择思路

如果目标是后端 API，并且团队希望尽量使用 Kotlin 原生表达方式，优先学习 [`Ktor`](ktor/)。它没有强迫你接受庞大的对象模型，而是把能力拆成插件：路由、内容协商、认证、日志、状态页、CORS、监控都可以按需安装。Ktor 很适合轻量 API、BFF、内部服务、网关原型和 Kotlin-first 团队。

如果团队已有 Spring 生态、依赖 Spring Security、Spring Data、Actuator 或大量 Java 库，可以选择 Spring Boot Kotlin。它的优势是成熟的企业生态和运维设施，代价是框架约定、注解模型和容器生命周期更重。Kotlin 在 Spring 中通常要注意 `open` 类、代理、空安全边界和 Jackson/Kotlin 模块。

如果目标是 UI，先区分平台。Android 原生应用通常从 Android Jetpack Compose 开始；桌面、共享 UI 或多端实验可以看 [`Compose Multiplatform`](compose-multiplatform/)。Compose 的核心不是“控件库”，而是“状态改变后重新计算 UI 描述”。理解 `remember`、状态提升、重组和副作用，比背 API 名称更重要。

如果目标是跨平台复用业务逻辑，可以学习 Kotlin Multiplatform。常见方式是把领域模型、校验、网络 DTO、序列化、仓储接口和 use case 放在 `commonMain`，平台相关能力通过 `expect/actual` 或接口注入实现。UI 是否共享要谨慎决定：共享业务逻辑通常收益稳定，共享 UI 则取决于团队和产品目标。

数据访问方面，Exposed 适合想要 Kotlin DSL 与 SQL 贴近的项目；在 Spring Boot Kotlin 中也可以继续使用 Spring Data JPA/R2DBC。依赖注入方面，Ktor 小项目常用显式传参或轻量模块函数，Android/KMP 项目常见 Koin，复杂 JVM 后端也可以继续使用 Spring 容器。测试方面，Kotest 的 DSL 很贴近 Kotlin 表达习惯，JVM 服务端仍可直接使用 JUnit 5。

## 学习路线

1. 先读 Kotlin 语言章节，重点掌握空安全、数据类、扩展函数、lambda、sealed class、协程和 DSL。
2. 阅读 [`Ktor`](ktor/)：用插件注册、Routing 和 ContentNegotiation 实现最小 JSON API，理解一次请求如何在协程中流动。
3. 阅读 [`Compose Multiplatform`](compose-multiplatform/)：用状态对象和 Composable 函数实现计数器 UI，理解声明式 UI 与重组。
4. 比较服务端与 UI 的共同思想：两者都偏组合式，Ktor 组合插件和路由，Compose 组合函数和状态。
5. 扩展到工程化：Ktor 接入数据库、配置、认证和部署；Compose 拆分状态、领域模型、平台目标和 UI 测试。
6. 继续补充 Kotlin Multiplatform、Exposed、Koin、Kotest 和 Spring Boot Kotlin，形成完整工程链路。

## 本仓库案例

- [`Ktor quickstart`](ktor/examples/quickstart/)：一个真实 Gradle Kotlin DSL 项目，用 Ktor 3.5.0 实现任务 JSON API，展示插件式应用、Routing、ContentNegotiation、协程 handler 和 HTTP 测试。
- [`Compose Multiplatform quickstart`](compose-multiplatform/examples/quickstart/)：一个真实 Gradle Kotlin DSL 项目，用 Compose Multiplatform 1.11.0 实现桌面计数器，展示声明式 UI、状态驱动、重组和可测试状态模型。
