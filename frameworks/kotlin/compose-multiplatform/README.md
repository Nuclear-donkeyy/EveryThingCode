# Compose Multiplatform

Compose Multiplatform 是 JetBrains 推动的跨平台声明式 UI 框架。它继承 Jetpack Compose 的核心编程模型：用 Composable 函数描述界面，用状态变化驱动界面更新，再由运行时决定哪些部分需要重组。与传统 UI 框架相比，它更强调“UI 是状态的函数”。

## 核心定位

Compose Multiplatform 解决的是“用一套 Kotlin/Compose 模型构建多平台 UI”的问题。它可以面向 desktop、Android、iOS、Web 等目标，尤其适合共享设计系统、业务表单、内部工具、桌面应用、多端原型，以及 Kotlin Multiplatform 团队希望共享更多 UI 层代码的场景。

它不等于“一次编写，所有平台体验自动完美”。平台导航、权限、窗口、文件系统、生命周期、输入法、无障碍和分发方式仍然有差异。真实项目需要决定哪些 UI 共享，哪些平台能力用 expect/actual、接口或平台模块实现。

## 设计思想

Compose 的核心是声明式 UI。你不直接操作控件树，比如“找到按钮然后改文字”，而是声明在当前状态下界面应该长什么样。当状态改变，Compose 重新执行受影响的 Composable，计算新的 UI 描述，并尽量只更新必要部分。

第二个思想是状态驱动。`mutableStateOf`、`remember`、状态提升和不可变 UI state 共同决定界面如何变化。状态越集中、越可预测，UI 越容易测试。反过来，如果把业务状态散落在多个 Composable 内部，重组和数据流就会变得难以理解。

第三个思想是重组。Composable 函数可能因为状态变化被多次调用，所以它们应该尽量是无副作用的 UI 描述。网络请求、计时器、订阅、资源释放等副作用需要放到专门的 effect API 或更外层的状态管理中。

第四个思想是跨平台分层。可以把纯业务状态、校验、格式化和 use case 放在 `commonMain`，把 desktop/iOS/Android 的入口放在平台 source set。这样既能共享核心逻辑，又能尊重平台差异。

## 架构模型

一个 Compose Multiplatform 项目通常由这些部分构成：

- Gradle 多平台配置：声明 Kotlin Multiplatform、Compose plugin、平台目标和 source sets。
- `commonMain`：共享 UI state、Composable、领域模型和平台无关逻辑。
- 平台入口：例如 `jvmMain` 的 desktop `Window`，Android 的 Activity，iOS 的 ComposeUIViewController。
- 状态层：可以是简单 state holder，也可以是 ViewModel/MVI reducer。
- 测试：纯状态逻辑用普通 Kotlin test，UI 行为按平台选择 Compose UI test。

本仓库 quickstart 先选择 desktop JVM 目标，因为它最容易在本地运行和观察窗口效果，同时仍然保留 `commonMain` 状态模型，展示多平台项目的基本组织方式。

## 请求/执行生命周期

UI 框架没有 HTTP 请求生命周期，但有一次渲染/交互生命周期。应用从平台入口启动，例如 desktop 的 `application { Window { App() } }`。进入 `App()` 后，Composable 函数读取当前状态并声明 UI：标题、文本、按钮、布局。

当用户点击按钮，事件 handler 修改状态。Compose runtime 发现被读取的 state 发生变化，于是安排重组。重组并不是重建整个应用，而是重新执行受影响的 Composable，比较新的 UI 描述与旧树，并把差异提交给底层渲染层。

如果 Composable 中读取的是不可观察普通变量，Compose 不知道它变化了，界面也不会自动更新。如果在 Composable 执行期间直接启动副作用，每次重组都可能重复执行。理解这两点，是避免 Compose 初学坑的关键。

## 工程结构

quickstart 的目录结构如下：

```text
examples/quickstart/
├── build.gradle.kts
├── settings.gradle.kts
└── src/
    ├── commonMain/kotlin/dev/everythingcode/compose/
    │   └── CounterState.kt
    ├── commonTest/kotlin/dev/everythingcode/compose/
    │   └── CounterStateTest.kt
    └── jvmMain/kotlin/dev/everythingcode/compose/
        └── Main.kt
```

`CounterState` 放在 `commonMain`，说明它可以被多个平台共享。`Main.kt` 是 desktop 平台入口，负责创建窗口并调用共享状态。真实项目通常会继续拆分 `ui/`、`designsystem/`、`feature/`、`domain/`、`platform/` 等目录。

## 配置方式

Compose Multiplatform 的配置主要在 Gradle 中完成。`kotlin("multiplatform")` 声明多平台项目，`org.jetbrains.compose` 提供 Compose 依赖和 desktop 打包能力，`org.jetbrains.kotlin.plugin.compose` 让 Kotlin 编译器启用 Compose 编译插件。

source set 是理解配置的关键。`commonMain` 面向共享代码，`jvmMain` 面向 desktop/JVM，后续可以增加 `androidMain`、`iosMain`、`wasmJsMain` 等。依赖应该尽量放在最低可用层级：共享依赖放 `commonMain`，平台依赖放对应平台 source set。

## 模块与依赖管理

Compose 使用函数组合组织 UI，而不是 XML、模板或继承控件。小组件通过参数接收状态和事件回调，例如 `CounterPanel(count, onIncrement)`。这种写法让 UI 组件更容易预览、测试和复用。

依赖管理上，Compose 与 Kotlin Multiplatform 深度绑定。跨平台应用常用模块拆分：`:shared` 放业务和共享 UI，`:desktopApp`、`:androidApp`、`:iosApp` 放平台入口。本案例是单模块最小项目，适合先学习 source set 与状态模型。

## 数据访问

本案例没有接入数据库或网络，只用 `CounterState` 表示可测试的内存状态。UI 教学中这样做有一个好处：读者可以先看清“状态改变 -> UI 重组”的主线。

真实应用的数据访问通常放在共享层：使用 Ktor Client 调 HTTP API，用 kotlinx.serialization 解析 JSON，用 SQLDelight 或平台数据库保存本地数据，再把 repository 注入到状态 holder 或 ViewModel 中。UI 层只观察 state，并把用户事件上报给状态层。

## 测试方式

本案例把计数逻辑放到 `CounterState`，因此可以使用普通 `kotlin.test` 在 `commonTest` 中验证，不依赖窗口或渲染环境。这是 Compose 项目非常实用的策略：能用纯状态测试验证的逻辑，不要急着上 UI 自动化。

UI 层测试可以按平台补充。Desktop 可以使用 Compose UI test 或截图测试；Android 可以使用 Jetpack Compose testing；跨平台共享逻辑继续用 common test。测试金字塔的底部应是状态、reducer、格式化和校验。

## 部署方式

Desktop 应用可以通过 Gradle 的 Compose desktop application 插件运行，也可以打包成 DMG、MSI、DEB 等原生分发格式。Android、iOS、Web 的部署方式则分别遵循对应平台工具链。

生产分发需要考虑 JDK/runtime 打包、签名、公证、自动更新、平台权限、图标、版本号和崩溃日志。Compose Multiplatform 提供 UI 与构建入口，但平台发布仍然需要平台知识。

## 适用场景与取舍

优先选择 Compose Multiplatform 的场景：Kotlin 团队、需要桌面应用、希望共享 UI 或设计系统、业务逻辑已经使用 Kotlin Multiplatform、内部工具需要快速迭代。它的声明式模型能让复杂状态 UI 更可控。

需要谨慎的场景：团队完全没有 Kotlin 经验、产品高度依赖平台原生细节、UI/无障碍/输入法体验要求极高且各平台差异大，或组织已有成熟原生团队和组件体系。此时可以只共享业务逻辑，UI 仍按平台原生实现。

## 案例索引

- [quickstart](examples/quickstart/)：桌面计数器应用，包含 Gradle Kotlin DSL、commonMain 状态对象、commonTest 单元测试和 jvmMain Compose Desktop 入口。

## 版本来源

- Kotlin 版本基线：2.3.21，策略为 latest stable，无官方 LTS。
- Compose Multiplatform 版本基线：1.11.0，策略为 latest stable，无官方 LTS。
- 官方来源：https://kotlinlang.org/docs/releases.html
- 官方来源：https://www.jetbrains.com/help/kotlin-multiplatform-dev/compose-multiplatform-and-jetpack-compose.html
- 校验日期：2026-05-30
