# SwiftUI

SwiftUI 是 Apple 平台的声明式 UI 框架。它不要求开发者一步步命令界面“创建按钮、移动 label、刷新 table”，而是让开发者描述“当前状态下界面应该长什么样”。当状态变化时，框架重新计算相关 `View` 的 `body`，对比新旧视图描述，再把最小必要变更提交给底层渲染系统。

## 核心定位

SwiftUI 解决的是 Apple 平台 UI 的表达、组合、状态传播和生命周期管理问题。它适合构建 iOS、macOS、watchOS、tvOS、visionOS 上的现代界面，尤其适合列表、表单、导航、设置页、数据驱动页面和跨设备体验。

它不直接替代所有底层能力。复杂文本排版、精细手势、平台私有控件、老项目中的 UIKit/AppKit 集成，仍可能需要混合使用 UIKit、AppKit 或 `UIViewRepresentable`/`NSViewRepresentable`。学习 SwiftUI 的关键不是背控件 API，而是理解“状态如何流动，副作用放在哪里，视图为什么应该保持轻量”。

## 设计思想

SwiftUI 的核心思想是声明式 UI。`View` 是一个值类型描述，`body` 根据当前状态返回一棵视图树。开发者不直接操作真实控件，而是改变 `@State`、`@Binding`、`@Observable` 对象、环境值或外部模型，框架负责把变化映射到界面更新。

状态绑定是第二个核心。`@State` 表示视图拥有的局部状态，`@Binding` 表示子视图读写父视图状态的通道，`@Environment` 表示从外部注入的上下文，例如颜色方案、locale、dismiss action。真实项目通常还会把业务状态放进可观察模型，再由视图订阅。

第三个思想是组合优先。SwiftUI 鼓励把页面拆成小 `View`，每个 `View` 只接收渲染所需的数据和回调。修饰符也是组合：`.padding()`、`.foregroundStyle()`、`.task()`、`.toolbar()` 都是在描述这棵视图树的附加行为。

## 架构模型

一个 SwiftUI 应用通常由 `App` 入口、若干 `Scene`、页面级 `View`、可复用组件、状态模型和服务层组成。

```text
LearningTasksApp
  -> WindowGroup / Scene
    -> TaskListView
      -> TaskStore
      -> TaskRow
      -> AddTaskView
```

`App` 负责启动和全局依赖注入，`Scene` 描述窗口或文档生命周期，页面级 `View` 负责组合布局和交互入口，状态模型负责保存业务状态，服务层负责网络、本地存储或系统 API。对于有编程经验但没写过 SwiftUI 的读者，最容易踩的坑是把网络请求、数据变换和页面跳转全部写在 `body` 里。`body` 应该是可重复计算的描述，不应该承载不可控副作用。

## 请求/执行生命周期

SwiftUI 没有传统 Web 请求生命周期，但有一次界面事件的执行链：

1. 用户点击按钮、输入文本、切换列表项或系统触发生命周期事件。
2. 事件回调修改状态，例如 `store.toggle(id:)` 或 `draftTitle = ""`。
3. 状态对象发出变化，SwiftUI 标记依赖该状态的视图需要重新计算。
4. 框架重新调用相关 `body`，生成新的视图描述。
5. SwiftUI diff 新旧描述，并把必要更新提交给底层 UIKit/AppKit/渲染系统。
6. 如果视图挂载了 `.task`、`.onAppear`、`.onChange` 等副作用入口，框架按生命周期触发对应代码。

这个模型意味着：不要把“视图对象实例是否同一个”理解成传统面向对象 UI 控件；更应该把 `View` 看成由状态生成的快照。

## 工程结构

本仓库 quickstart 使用 Swift Package 组织一个最小 SwiftUI app：

```text
examples/quickstart/
  Package.swift
  Sources/LearningTasksApp/
    LearningTasksApp.swift
    TaskListView.swift
    TaskStore.swift
```

真实项目通常还会拆出 `Features/`、`Shared/`、`Services/`、`DesignSystem/`、`Persistence/` 和 `Tests/`。学习阶段先保持小结构：入口只负责启动，视图负责渲染，状态模型负责业务变化。等到页面增多后，再按 feature 分组，而不是按 MVC 名词机械分层。

## 配置方式

SwiftUI 的配置通常分三层。第一层是构建配置，由 Xcode project、Swift Package 或 app target 决定平台、部署版本、bundle 标识和依赖。第二层是运行期环境，例如 `@Environment(\.colorScheme)`、`@Environment(\.dismiss)`、`@Environment(\.locale)`。第三层是业务配置，例如 API base URL、feature flags、mock service，可以通过构造函数、环境对象或 dependency container 注入。

quickstart 只依赖 Swift Package 的 `Package.swift` 和 macOS 平台约束。真实 App Store 应用还需要 Xcode target、Info.plist、asset catalog、entitlements、签名和发布配置。

## 模块与依赖管理

SwiftUI 的模块机制主要依赖 Swift Module、Swift Package Manager 和 target 边界。小应用可以把所有视图放在一个 target 中；中大型应用可把 design system、domain model、network client、persistence 和 feature module 分拆成多个 Swift package。

依赖传递有三种常见方式：简单数据用构造函数传入，父子视图共享可写状态用 `@Binding`，跨层上下文用 environment。业务服务不建议直接在视图内部全局获取，最好从入口创建后注入，让预览、测试和替换实现更容易。

## 数据访问

quickstart 使用内存数组保存任务，目的是突出状态驱动 UI。真实项目常见路线有三种：小型本地应用可以用 SwiftData；需要成熟对象图、迁移和复杂关系时使用 Core Data；需要远端同步时，把网络 client 和本地 persistence 分开，让视图只观察一个简洁的状态模型。

数据访问不应该污染 `View` 的 `body`。可以在 `.task` 中触发加载，在 model/service 中执行异步请求，再把结果映射成页面状态。这样 UI 测试、预览和错误态都更容易覆盖。

## 测试方式

SwiftUI 测试通常分层处理。纯业务逻辑和状态模型优先用 XCTest 或 Swift Testing 做单元测试；页面布局和导航可以用 Xcode UI Tests；复杂组件可以通过 preview、snapshot 或可访问性标识辅助验证。

quickstart 的最小验收是能 `swift build`，并能说明状态变化如何驱动列表刷新。后续可补充 `TaskStore` 单元测试，验证新增、完成、过滤逻辑，而不是一上来测试整个 UI 树。

## 部署方式

SwiftUI 应用的部署路径取决于平台。iOS、watchOS、visionOS 应用通常通过 Xcode archive、签名、TestFlight 和 App Store Connect 发布；macOS 应用可以走 App Store、Developer ID notarization 或企业分发。Swift Package quickstart 主要用于学习框架结构，不等同于完整可发布 App 工程。

团队项目中要把最低系统版本、Swift 版本、Xcode 版本、签名证书、entitlements 和 CI 构建环境固定下来，否则 UI 框架升级时很容易出现编译和运行差异。

## 适用场景与取舍

优先选择 SwiftUI 的场景：新 Apple 平台应用、数据驱动界面、多设备共享 UI、表单列表密集页面、与 SwiftData/Observation 深度结合的应用。它的优势是代码少、组合强、状态表达清晰，并且能跟随 Apple 平台新能力快速演进。

需要谨慎的场景：大量 UIKit/AppKit 遗留代码、极端自定义控件、底层渲染强控制、复杂输入法或平台私有行为。此时可以混合使用，而不是在 SwiftUI 和传统 UI 之间二选一。

## 案例索引

- [quickstart](examples/quickstart/)：列表 UI 的最小 Swift Package，展示 `App` 入口、状态模型、`@State`、`@Binding`、环境值和列表交互。

## 版本来源

- 语言基线：Swift 6.3.x，策略为 latest stable，无官方 LTS。
- 框架基线：SwiftUI latest stable，随 Xcode 与 Apple SDK 发布。
- 官方来源：https://developer.apple.com/xcode/swiftui/
- Swift 安装来源：https://www.swift.org/install/
- 校验日期：2026-05-30
