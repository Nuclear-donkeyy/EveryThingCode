# SwiftUI quickstart

这个案例用 Swift Package 写一个最小 SwiftUI macOS 应用。它不是完整 App Store 工程，而是为了让读者用最少文件看清 SwiftUI 的入口、状态、绑定、环境值和列表交互。

## 目标

完成后你应该能说明：`App` 如何启动窗口，`View.body` 为什么是状态的声明式描述，`@State` 如何保存页面局部状态，`@Binding` 如何让子视图修改父视图状态，以及为什么业务状态应放在独立模型中，而不是散落在 `body` 里。

## 这个案例解决什么问题

这个案例把一个常见任务列表写成 SwiftUI，是为了对照 UIKit/AppKit 命令式 UI 的典型复杂度：如果手写传统控件，你需要创建窗口或 view controller，放置输入框、按钮、列表和 footer；新增任务时要更新数组、刷新列表、清空输入框、更新剩余数量；切换完成状态时要处理 cell 复用、文字样式、按钮禁用态；切换深色模式时还要确保颜色不会写死。

SwiftUI 把这些问题收敛成一条状态驱动链路：

1. `TaskStore.tasks` 是任务数据的事实来源。
2. `TaskListView.body` 根据 `store.tasks`、`draftTitle` 和 `colorScheme` 描述界面。
3. `Button("Add")`、`Toggle`、`Clear Completed` 只修改状态，不直接刷新某个控件。
4. 状态变化后，`List`、`Text`、`Button.disabled` 和行样式自动从新状态重新推导。

因此这个 quickstart 不是在展示“如何写一个漂亮待办应用”，而是在展示 SwiftUI 如何解决 Apple UI 开发里最核心的同步问题：界面不再拥有另一份状态，界面只是状态的投影。

## 学习重点

- 声明式 UI：界面由当前状态推导出来，状态改变后框架重新计算视图描述。
- 状态所有权：`TaskListView` 拥有 `TaskStore` 和输入框状态，`TaskRow` 通过 `@Binding` 修改单条任务。
- 环境值：从 `@Environment(\.colorScheme)` 读取系统上下文，理解环境不是全局变量，而是视图树上的依赖注入。
- 组件拆分：入口、页面、行组件、状态模型分文件，避免所有逻辑堆在一个 `ContentView`。
- 列表绑定：`List($store.tasks)` 让每个行组件拿到可写绑定，避免子视图复制数据或反向查找父状态。
- Preview：`#Preview` 让页面不用跑完整应用也能被构造出来，适合教学、组件开发和视觉检查。

## 工程结构

```text
.
├── Package.swift
└── Sources/LearningTasksApp
    ├── LearningTasksApp.swift
    ├── TaskListView.swift
    └── TaskStore.swift
```

- `Package.swift`：声明 macOS SwiftUI executable package 和 Swift 版本。
- `LearningTasksApp.swift`：`@main` 入口，创建 `WindowGroup`。
- `TaskListView.swift`：页面和行组件，展示 `@State`、`@Binding`、`@Environment`。
- `TaskStore.swift`：内存任务模型和业务方法，集中处理新增、切换完成、清理已完成。

## 运行前提

- macOS，安装 Xcode 或 Swift toolchain。
- Swift 6.3.x 或兼容当前仓库 `versions.yaml` 的 latest stable Swift。
- SwiftUI 随 Apple SDK 提供；Linux Swift toolchain 无法直接运行该 UI 案例。

## 运行

```bash
swift build
```

如果要打开应用窗口，可以继续执行：

```bash
swift run LearningTasksApp
```

## 预期输出

`swift build` 成功时会生成 `.build/` 产物并显示 build complete。`swift run LearningTasksApp` 会打开一个标题为 `SwiftUI Tasks` 的 macOS 窗口，页面中包含任务输入框、添加按钮、任务列表、完成状态切换和清理按钮。

## 代码讲解

`Package.swift` 先把案例限定为一个 macOS executable package。`platforms: [.macOS(.v14)]` 表示案例依赖较新的 SwiftUI/Observation 能力；`.executable(name: "LearningTasksApp", targets: ["LearningTasksApp"])` 表示 `swift run LearningTasksApp` 会启动这个目标。这里没有 Xcode app target、asset catalog、签名和 entitlements，是因为 quickstart 的目标是学习 SwiftUI 思想，而不是交付 App Store 工程。

`LearningTasksApp.swift` 中的 `@main` 标记告诉 Swift 这是程序入口。`LearningTasksApp` 遵守 `App` 协议，`body` 返回 `some Scene`。`WindowGroup("SwiftUI Tasks")` 描述一组窗口，它不会手工创建 `NSWindow`，而是声明每个窗口的内容是 `TaskListView()`。`.frame(minWidth:minHeight:)` 也是声明式修饰符：它描述内容希望拥有的最小尺寸，而不是命令某个窗口对象立刻改 frame。

`TaskStore.swift` 定义两层模型。`LearningTask` 遵守 `Identifiable`，所以 `List` 能用稳定 `id` 识别每一行；它也遵守 `Equatable`，方便后续测试或 diff。`TaskStore` 标记为 `@Observable`，表示 SwiftUI 可以追踪它的可观察属性。`tasks` 是列表事实来源，`remainingCount` 是派生状态，`add(title:)` 和 `clearCompleted()` 是业务动作。注意：剩余数量没有额外存一份，而是由 `tasks` 计算得到，这能避免“列表已经变了但统计没更新”的常见 bug。

`TaskListView` 保存两个局部状态：`@State private var store = TaskStore()` 和 `@State private var draftTitle = ""`。前者是页面拥有的业务状态模型，后者是输入框临时文本。这里使用 `@State` 的含义是“这个视图拥有状态生命周期”；当 `draftTitle` 改变时，输入框文字随之变化；当 `store.tasks` 改变时，列表和剩余数量随之变化。

`@Environment(\.colorScheme)` 读取系统颜色模式。它解决的是“系统上下文从哪里来”的问题：视图不需要全局查询当前主题，也不需要父视图手动把主题一层层传下去。SwiftUI 在视图树上提供环境值，读者后续会在真实项目里看到 `dismiss`、`locale`、`dynamicTypeSize`、`managedObjectContext` 等类似用法。

`body` 中的 `VStack`、`HStack`、`List`、`TextField`、`Button` 和 `Toggle` 都是视图描述。`header` 使用 `store.remainingCount` 和 `colorScheme` 生成标题区；`composer` 把 `TextField` 绑定到 `$draftTitle`，点击 Add 后调用 `store.add(title:)` 并清空输入；`footer` 的 `.disabled(!store.tasks.contains { $0.isDone })` 让按钮状态由数据推导，不需要额外维护一个 `isClearButtonEnabled`。

`List($store.tasks) { $task in ... }` 是这个案例最值得停下来的代码。`$store.tasks` 把数组变成可写绑定集合，闭包里的 `$task` 是某一行任务的绑定。`TaskRow(task: $task)` 不需要知道完整数组，也不需要知道 `TaskStore`，只拿到自己要渲染和修改的那一条任务。

`TaskRow` 接收 `@Binding var task`，因此 `Toggle(isOn: $task.isDone)` 能直接修改父级数组中对应任务的完成状态。这里的绑定是 SwiftUI 解决父子状态同步的关键：如果只传 `LearningTask` 值，子视图只能展示，不能修改；如果把整个 store 传给子视图，子组件会知道过多父级细节。`@Binding` 则把权限控制在“只读写这一条任务”。

`#Preview { TaskListView() }` 体现 SwiftUI 的反馈方式。传统 UIKit/AppKit 页面常需要启动完整应用才能检查布局，SwiftUI preview 可以直接构造视图。真实项目里通常会为 preview 注入 mock store、深色模式、不同 locale 和大字号环境，用来提前发现布局和状态问题。

完整事件链可以这样读：用户输入文本时，`TextField` 写入 `draftTitle`；用户点击 Add 时，`store.add(title:)` 清洗文本并插入 `LearningTask`；`tasks` 变化触发 `TaskListView.body` 重新求值；`List` 多出一行，`remainingCount` 更新，Clear Completed 的禁用状态也重新计算。用户勾选某行时，`TaskRow` 的 `Toggle` 通过 `@Binding` 写回父级任务，行文字样式和 footer 状态随之更新。

## 延伸练习

- 给 `TaskStore` 增加过滤条件：全部、未完成、已完成，并在 UI 中用 segmented control 切换。
- 把内存数组替换为 SwiftData model，观察持久化代码应该放在模型层还是视图层。
- 为 `TaskStore` 增加单元测试，验证空标题不会新增任务、清理按钮只删除已完成任务。
- 给 `#Preview` 增加深色模式和大字号环境，观察 `@Environment` 如何影响视图。
- 把 `TaskRow` 的完成切换改成回调版本，对比 `@Binding` 和 closure 回传在组件边界上的差异。

## 验收

- 能解释 `@State` 和 `@Binding` 的区别，并指出哪个类型拥有状态。
- 能把 `TaskRow` 拆成更小组件，同时不破坏父子状态同步。
- 能添加一个新字段，例如 priority 或 due date，并让列表正确刷新。
- 能说明为什么不能在 `body` 中直接执行网络请求或写数据库。
