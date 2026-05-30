# Compose Multiplatform core ideas example

## 目标

这个示例把 `Compose Multiplatform` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

跨平台 UI 容易在不同平台重复写控件、状态同步和布局逻辑。

## 核心思想到代码

Composable 描述 UI，state 驱动重组，source set 共享业务和 UI，平台目标只承载必要差异。

```kotlin
@Composable
fun CounterPanel(state: CounterState) {
    Column {
        Text("Count: ${state.count}")
        Button(onClick = state::increment) { Text("Add") }
    }
}
```

```kotlin
var count by mutableStateOf(0)
fun increment() { count += 1 }
```

## 代码位置

- [`build.gradle.kts`](../quickstart/build.gradle.kts)
- [`src/commonMain`](../quickstart/src/commonMain)
- [`src/jvmMain`](../quickstart/src/jvmMain)
- [`src/commonTest`](../quickstart/src/commonTest)

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

按钮只改变 state，界面通过 recomposition 更新；这和命令式刷新控件不同。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`Compose Multiplatform` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
