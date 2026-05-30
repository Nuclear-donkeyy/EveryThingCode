# SwiftUI quickstart

这个案例用 Swift Package 写一个最小 SwiftUI macOS 应用。它不是完整 App Store 工程，而是为了让读者用最少文件看清 SwiftUI 的入口、状态、绑定、环境值和列表交互。

## 目标

完成后你应该能说明：`App` 如何启动窗口，`View.body` 为什么是状态的声明式描述，`@State` 如何保存页面局部状态，`@Binding` 如何让子视图修改父视图状态，以及为什么业务状态应放在独立模型中，而不是散落在 `body` 里。

## 学习重点

- 声明式 UI：界面由当前状态推导出来，状态改变后框架重新计算视图描述。
- 状态所有权：`TaskListView` 拥有 `TaskStore` 和输入框状态，`TaskRow` 通过 `@Binding` 修改单条任务。
- 环境值：从 `@Environment(\.colorScheme)` 读取系统上下文，理解环境不是全局变量，而是视图树上的依赖注入。
- 组件拆分：入口、页面、行组件、状态模型分文件，避免所有逻辑堆在一个 `ContentView`。

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

`LearningTasksApp.swift` 中的 `@main` 标记告诉 Swift 这是程序入口。`WindowGroup` 描述一组窗口，它不会手工创建 `NSWindow`，而是声明窗口内容是 `TaskListView()`。

`TaskListView` 保存两个局部状态：`store` 是任务数据与操作集合，`draftTitle` 是输入框内容。点击添加按钮时，视图调用 `store.add(title:)` 修改状态；状态变化后，`body` 被重新计算，`List` 展示新的任务数组。

`TaskRow` 接收 `@Binding var task`，因此子视图能切换父级数组中某个任务的完成状态。这里的绑定是教学重点：它避免子组件复制数据，也避免子组件知道整个 `TaskStore`。

`TaskStore` 是独立模型，负责新增任务、切换状态和删除已完成任务。真实项目中可以把这里替换为 SwiftData、Core Data 或网络同步服务，而 `TaskListView` 的结构不需要大改。

## 延伸练习

- 给 `TaskStore` 增加过滤条件：全部、未完成、已完成，并在 UI 中用 segmented control 切换。
- 把内存数组替换为 SwiftData model，观察持久化代码应该放在模型层还是视图层。
- 为 `TaskStore` 增加单元测试，验证空标题不会新增任务、清理按钮只删除已完成任务。

## 验收

- 能解释 `@State` 和 `@Binding` 的区别，并指出哪个类型拥有状态。
- 能把 `TaskRow` 拆成更小组件，同时不破坏父子状态同步。
- 能添加一个新字段，例如 priority 或 due date，并让列表正确刷新。
- 能说明为什么不能在 `body` 中直接执行网络请求或写数据库。
