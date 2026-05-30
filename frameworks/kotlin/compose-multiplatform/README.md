# Compose Multiplatform

Compose Multiplatform 是 JetBrains 推动的跨平台声明式 UI 框架。它继承 Jetpack Compose 的核心编程模型：用 Composable 函数描述界面，用状态变化驱动界面更新，再由运行时决定哪些部分需要重组。与传统 UI 框架相比，它更强调“UI 是状态的函数”。

## 核心定位

Compose Multiplatform 解决的是“用一套 Kotlin/Compose 模型构建多平台 UI”的问题。它可以面向 desktop、Android、iOS、Web 等目标，尤其适合共享设计系统、业务表单、内部工具、桌面应用、多端原型，以及 Kotlin Multiplatform 团队希望共享更多 UI 层代码的场景。

它不等于“一次编写，所有平台体验自动完美”。平台导航、权限、窗口、文件系统、生命周期、输入法、无障碍和分发方式仍然有差异。真实项目需要决定哪些 UI 共享，哪些平台能力用 expect/actual、接口或平台模块实现。

## 解决的问题

传统跨平台 UI 往往在两个极端之间摇摆：一端是完全原生实现，每个平台都有独立 UI、状态管理和测试用例，长期维护成本高；另一端是 WebView 或高度抽象的跨平台层，虽然共享代码多，但容易牺牲平台体验、性能调优空间和原生能力。Compose Multiplatform 要解决的是“哪些 UI 可以共享、哪些平台差异必须保留”的工程边界问题。

第一个痛点是状态同步。命令式 UI 中常见写法是先更新模型，再手动找到控件修改文本、颜色、可见性和按钮状态；当同一个状态影响多个控件时，很容易出现某个控件漏更新。Compose 把 UI 看成状态的函数：`count` 变化后，读取它的 Composable 会重组，文本、按钮启用态、布局内容都从同一份状态重新计算。

第二个痛点是组件复用。传统桌面、Android、iOS、Web UI 通常有不同组件 API，同一个业务面板要写多份实现。Compose Multiplatform 用 `@Composable` 函数组合 UI，尽量让按钮、表单、列表、设计系统 token 和业务组件复用在 `commonMain`；平台入口只负责窗口、Activity、UIViewController 或 Web 挂载点。

第三个痛点是平台差异。跨平台不是抹平所有差异，而是把差异集中管理。共享层可以定义领域模型、UI state、格式化和平台无关组件；文件选择、系统通知、窗口菜单、权限、导航宿主等能力可以放到平台 source set，或通过 `expect`/`actual` 暴露统一接口。这样业务 UI 不必散落大量 `if platform` 判断。

第四个痛点是布局与重组的复杂度。复杂界面中，局部状态变化不应该导致整棵 UI 以不可控方式刷新，也不应该要求开发者手工维护控件树。Compose runtime 追踪 state 读取并安排重组，开发者的主要任务变成设计清晰的数据流：状态在哪里拥有，事件如何上报，哪些 Composable 只是展示。

第五个痛点是测试。跨平台 UI 如果把业务规则写在平台控件回调里，就只能靠手工点击或昂贵的 UI 自动化验证。Compose Multiplatform 鼓励把计数、校验、格式化、reducer、use case 放在 `commonMain`，用 `commonTest` 做快速单元测试；平台 UI 测试只覆盖窗口、交互和渲染边界。

## 设计思想

Compose 的核心是声明式 UI。你不直接操作控件树，比如“找到按钮然后改文字”，而是声明在当前状态下界面应该长什么样。当状态改变，Compose 重新执行受影响的 Composable，计算新的 UI 描述，并尽量只更新必要部分。这个思想把“同步 UI 细节”的责任从开发者手里移到 runtime 和编译器协作的模型里。

第二个思想是 Composable 函数组合。Composable 不是传统意义上的控件对象，而是可组合的 UI 描述函数。它通过参数接收数据，通过回调上报事件，内部尽量少保存业务状态。这样的组件可以从简单按钮组合成表单、从表单组合成页面、从页面组合成应用，同时保持测试和替换边界。

第三个思想是状态驱动。`mutableStateOf`、`remember`、状态提升和不可变 UI state 共同决定界面如何变化。`remember` 保存与当前 composition 生命周期绑定的局部状态，`mutableStateOf` 让 Compose 能观察值变化，状态提升则把可复用组件变成“只展示、只发事件”的无状态组件。状态越集中、越可预测，UI 越容易测试。

第四个思想是重组。Composable 函数可能因为状态变化被多次调用，所以它们应该尽量是无副作用的 UI 描述。网络请求、计时器、订阅、资源释放等副作用需要放到专门的 effect API 或更外层的状态管理中。理解重组不是“重新启动页面”，而是“重新执行受影响的 UI 描述”，是写好 Compose 的关键。

第五个思想是跨平台分层。可以把纯业务状态、校验、格式化、UI state、部分设计系统和平台无关 Composable 放在 `commonMain`，把 desktop/iOS/Android/Web 的入口放在平台 source set。遇到平台能力时，不应该让共享 UI 直接依赖具体平台 API，而应该通过接口、依赖注入或 `expect`/`actual` 提供统一抽象。

第六个思想是平台目标显式声明。Gradle 中的 `jvm()`、后续可能加入的 `androidTarget()`、`iosArm64()`、`wasmJs()` 等目标，决定哪些代码会编译到哪个平台。source set 让“共享”和“平台特有”成为构建系统可检查的边界，而不是靠目录命名或团队约定维持。

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

`CounterState` 放在 `commonMain`，说明它可以被多个平台共享。`Main.kt` 是 desktop 平台入口，负责创建窗口并调用共享状态。真实项目通常会继续拆分 `ui/`、`designsystem/`、`feature/`、`domain/`、`platform/` 等目录。如果需要读取系统名称、文件路径或通知权限，可以在 `commonMain` 声明接口或 `expect fun`，再在 `jvmMain`、`androidMain`、`iosMain` 中分别提供实现。

## 配置方式

Compose Multiplatform 的配置主要在 Gradle 中完成。`kotlin("multiplatform")` 声明多平台项目，`org.jetbrains.compose` 提供 Compose 依赖和 desktop 打包能力，`org.jetbrains.kotlin.plugin.compose` 让 Kotlin 编译器启用 Compose 编译插件。本案例的 `jvmToolchain(25)` 固定 JDK 工具链，`jvm()` 声明 desktop/JVM 目标，`compose.desktop.application` 声明入口类与原生打包格式。

source set 是理解配置的关键。`commonMain` 面向共享代码，`commonTest` 面向共享测试，`jvmMain` 面向 desktop/JVM，后续可以增加 `androidMain`、`iosMain`、`wasmJsMain` 等。依赖应该尽量放在最低可用层级：共享依赖放 `commonMain`，平台依赖放对应平台 source set。这样构建系统会阻止共享代码误用平台 API。

## 模块与依赖管理

Compose 使用函数组合组织 UI，而不是 XML、模板或继承控件。小组件通过参数接收状态和事件回调，例如 `CounterPanel(count, onIncrement)`。这种写法让 UI 组件更容易预览、测试和复用。一个常见原则是“状态拥有者少一点，展示组件纯一点”：`App()` 可以拥有当前屏幕状态，`CounterPanel()` 只负责把状态画出来并把点击事件交回上层。

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
