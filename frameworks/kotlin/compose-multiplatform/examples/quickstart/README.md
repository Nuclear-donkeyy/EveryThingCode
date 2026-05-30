# Compose Multiplatform quickstart

这是一个最小但真实的 Compose Multiplatform desktop 项目。它用 Gradle Kotlin DSL 配置 Kotlin Multiplatform 和 Compose plugin，把可测试的计数状态放在 `commonMain`，把桌面窗口入口放在 `jvmMain`。

## 目标

完成本案例后，你应该能：

- 理解 Compose 的声明式 UI：界面由当前状态计算出来。
- 使用 `remember` 和 `mutableStateOf` 让点击事件触发重组。
- 把纯状态逻辑放在 `commonMain`，让它具备跨平台复用能力。
- 使用 `commonTest` 测试状态模型，而不是只依赖手工点击窗口。
- 看懂 Gradle 中 Compose Multiplatform 的 plugin、source set 和 desktop application 配置。

## 学习重点

重点观察状态流向。`CounterState` 是平台无关的普通 Kotlin 类，负责计数规则；`Main.kt` 中的 Composable 读取 count 并声明 UI；按钮点击时调用状态方法，然后把新 count 写回 Compose state。状态变化后，Compose 重新执行相关 Composable，窗口内容自动更新。

另一个重点是 source set。`commonMain` 不知道 desktop 窗口是什么，因此可以复用到 Android、iOS 或 Web；`jvmMain` 才创建 desktop `Window`。这就是 Kotlin Multiplatform 项目的基本边界。

## 这个案例解决什么问题

这个计数器很小，但它刻意覆盖了跨平台 UI 最容易混乱的几类问题。

第一，状态同步问题。点击 `Add` 后，如果用命令式 UI 写法，通常要同时更新内存变量和屏幕文本；功能一多，还要同步按钮、提示、列表、表单错误等多个控件。本案例把屏幕上的数字交给 `count`，按钮点击只改变状态，Compose 负责让读取 `count` 的文本在重组后显示新值。

第二，组件复用问题。`CounterPanel` 不知道自己运行在 desktop、Android 还是 Web，它只接收 `count`、`onIncrement`、`onReset`。这种写法让面板可以移动到 `commonMain` 或共享 UI 模块中；平台入口只负责提供窗口和宿主环境。

第三，平台差异问题。`CounterState` 在 `commonMain`，因此可以跨平台复用；`application { Window { ... } }` 在 `jvmMain`，因为窗口 API 是 desktop 特有的。真实项目可以继续用接口或 `expect`/`actual` 隔离平台通知、文件系统、系统主题、设备信息等能力。

第四，重组边界问题。`App()` 中的 `remember { mutableStateOf(...) }` 让 Compose 知道 `count` 是可观察状态。点击按钮时设置 `count`，Compose 只需要重新执行受影响的 Composable，而不是让开发者手工销毁和重建整棵控件树。

第五，测试问题。计数规则没有写在按钮回调深处，而是写在 `CounterState`，所以 `CounterStateTest` 可以在 `commonTest` 中快速验证。UI 自动化可以留给更少、更关键的交互路径。

## 工程结构

```text
.
├── build.gradle.kts
├── settings.gradle.kts
└── src/
    ├── commonMain/kotlin/dev/everythingcode/compose/
    │   └── CounterState.kt      # 平台无关状态模型
    ├── commonTest/kotlin/dev/everythingcode/compose/
    │   └── CounterStateTest.kt  # 纯 Kotlin 单元测试
    └── jvmMain/kotlin/dev/everythingcode/compose/
        └── Main.kt              # Compose Desktop 窗口与 UI
```

真实项目可以继续拆出 `feature/counter/`、`designsystem/`、`platform/` 和 `data/`。本案例故意保持很小，便于聚焦声明式 UI 和状态驱动。

## 运行前提

- JDK 25 LTS 或兼容的现代 JDK。
- Gradle 8.14+，或使用 IDE 自带 Gradle 运行。
- 首次运行需要联网下载 Kotlin、Compose Multiplatform 和 Kotlin test 依赖。
- 本仓库版本基线：Kotlin 2.3.21、Compose Multiplatform 1.11.0，均为 latest stable，无官方 LTS。

## 运行

先运行共享状态测试：

```bash
gradle test
```

启动桌面应用：

```bash
gradle run
```

可选：打包当前系统的 desktop 应用：

```bash
gradle packageDistributionForCurrentOS
```

## 预期输出

`gradle test` 应通过 `CounterStateTest`。运行 `gradle run` 后会打开一个名为 `Compose Quickstart` 的桌面窗口，窗口中显示当前计数、一个增加按钮和一个重置按钮。

点击 `Add` 后数字增加。点击 `Reset` 后数字回到 0。这个变化不是手动修改某个标签文本，而是状态变化触发 Compose 重组后重新绘制出来的。

## 代码讲解

`CounterState.kt` 是普通 Kotlin 代码，不导入任何 Compose API。它提供 `increment()` 和 `reset()`，并保证计数不会分散在 UI 组件内部。真实项目可以把校验、格式化、业务规则和 use case 放在类似位置。

`build.gradle.kts` 用三类 plugin 建立 Compose Multiplatform 项目：`kotlin("multiplatform")` 负责 source set 和平台目标，`org.jetbrains.kotlin.plugin.compose` 负责启用 Compose 编译插件，`org.jetbrains.compose` 负责 Compose 依赖和 desktop 应用打包。`jvm()` 明确这个 quickstart 当前只跑 desktop/JVM 目标；以后加入 Android、iOS 或 Web 时，应新增目标和对应 source set，而不是把平台代码塞进共享层。

`sourceSets` 展示了依赖应该放在哪里。`commonMain` 只依赖 `compose.runtime`，因为共享状态只需要可被 Compose 观察的运行时能力；`jvmMain` 才依赖 `compose.desktop.currentOs`、`compose.foundation`、`compose.material`，因为窗口和桌面 UI 组件属于 desktop/JVM 目标。这个边界能防止共享代码意外调用平台 API。

`Main.kt` 的 `main` 使用 `application { Window(...) { App() } }` 创建桌面窗口。这个入口属于 JVM/desktop 平台，因此放在 `jvmMain`。

`App()` 使用 `var count by remember { mutableStateOf(counter.count) }` 创建 Compose 可观察状态。`remember` 让状态在重组之间保留，`mutableStateOf` 让 Compose 能观察变化。点击 `Add` 时，事件回调先调用 `counter.increment()` 执行业务规则，再把返回值写回 `count`；写入后 Compose runtime 安排重组，`Text("Count: $count")` 重新计算显示内容。

`CounterPanel(...)` 是无状态 Composable。它只接收 `count` 和事件回调，不自己保存业务状态。这样的组件更容易复用，也更符合 Compose 的状态提升思想。它内部的 `Column`、`Row`、`Spacer` 负责布局，`Button` 只负责把用户动作上报给 `onIncrement` 或 `onReset`，不直接知道计数规则。

这条链路可以按顺序理解为：

```text
用户点击 Button
-> CounterPanel 调用 onIncrement
-> App 调用 CounterState.increment()
-> App 写入 mutableStateOf 管理的 count
-> Compose 发现被读取的 state 变化
-> 相关 Composable 重组
-> 文本和布局基于新 count 重新声明
```

`CounterStateTest.kt` 证明计数规则不依赖 UI。把逻辑拆到 common 层后，即使未来加入 Android 或 iOS 入口，这些测试仍然能覆盖共享行为。

如果要演示平台差异，可以在 `commonMain` 定义一个接口：

```kotlin
interface PlatformInfo {
    val name: String
}
```

然后在 `jvmMain` 提供 JVM/desktop 实现，在未来的 `androidMain` 或 `iosMain` 提供各自实现。也可以用 Kotlin Multiplatform 的 `expect`/`actual` 声明共享 API 和平台实现。关键不是把所有平台代码写成一份，而是让共享 UI 依赖稳定抽象。

## 延伸练习

- 增加一个 `Step` 输入，让每次点击可以加 1、5 或 10，并思考输入状态放在哪里。
- 把按钮和文字拆成更小的 Composable，再给它们传入不可变 UI state。
- 增加 `androidMain` 或 `wasmJsMain` 入口，复用 `CounterState` 和大部分 UI。
- 把 `CounterPanel` 移到共享 UI source set，并只在平台 source set 保留窗口入口。
- 用接口或 `expect`/`actual` 增加 `PlatformInfo`，在界面上显示当前平台名称。

## 验收

完成后你应该能说明：

- 声明式 UI 与命令式 UI 操作的差异。
- `remember`、`mutableStateOf` 和重组之间的关系。
- 为什么业务状态适合放在 `commonMain`，平台入口适合放在 `jvmMain`。
- source set 如何把共享逻辑和平台差异变成可编译检查的边界。
- 什么时候应该共享 Composable，什么时候应该保留平台特有入口或平台实现。
- 如何先测试纯状态逻辑，再逐步补充 UI 测试。
