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

`Main.kt` 的 `main` 使用 `application { Window(...) { App() } }` 创建桌面窗口。这个入口属于 JVM/desktop 平台，因此放在 `jvmMain`。

`App()` 使用 `var count by remember { mutableStateOf(counter.count) }` 创建 Compose 可观察状态。`remember` 让状态在重组之间保留，`mutableStateOf` 让 Compose 能观察变化。

`CounterPanel(...)` 是无状态 Composable。它只接收 `count` 和事件回调，不自己保存业务状态。这样的组件更容易复用，也更符合 Compose 的状态提升思想。

`CounterStateTest.kt` 证明计数规则不依赖 UI。把逻辑拆到 common 层后，即使未来加入 Android 或 iOS 入口，这些测试仍然能覆盖共享行为。

## 延伸练习

- 增加一个 `Step` 输入，让每次点击可以加 1、5 或 10，并思考输入状态放在哪里。
- 把按钮和文字拆成更小的 Composable，再给它们传入不可变 UI state。
- 增加 `androidMain` 或 `wasmJsMain` 入口，复用 `CounterState` 和大部分 UI。

## 验收

完成后你应该能说明：

- 声明式 UI 与命令式 UI 操作的差异。
- `remember`、`mutableStateOf` 和重组之间的关系。
- 为什么业务状态适合放在 `commonMain`，平台入口适合放在 `jvmMain`。
- 如何先测试纯状态逻辑，再逐步补充 UI 测试。
