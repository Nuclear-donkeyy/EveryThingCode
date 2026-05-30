# Flutter quickstart

这个案例用一个“学习任务面板”展示 Flutter 的最小真实工程：应用入口、Widget tree、局部状态、布局、事件回调和 Widget 测试都放在可运行文件里。读者不需要先掌握复杂状态管理库，只要会基本编程，就可以观察状态变化如何驱动 UI 重建。

## 目标

完成本案例后，你应该能说明 `main()`、`runApp()`、`MaterialApp`、`StatefulWidget`、`setState()` 和 Widget test 各自负责什么；能把一个页面拆成状态拥有者和展示 Widget；能修改内存任务列表并看到测试反馈。

案例刻意不接网络和数据库。第一步先把 Flutter 的 UI 思想看清：界面不是一堆要手动操作的控件，而是当前状态的一次声明式描述。

## 这个案例解决什么问题

这个 quickstart 模拟的是客户端 UI 最常见的一类问题：页面上有一份任务状态，用户点击按钮后，列表图标、标题样式和完成数量都要保持一致。如果用命令式方式实现，你可能要手动找到计数文本、找到列表项、修改图标、修改样式，还要保证重复点击和边界状态不出错。Flutter 的做法是只修改 `_tasks` 这份状态，让 `build()` 根据新状态重新描述界面。

案例还展示了“状态拥有者”和“展示组件”的边界。`LearningBoard` 拥有任务列表和 `_completeNext()`，因为它知道用户动作如何改变页面状态；`TaskTile` 只接收一个 `LearningTask` 并展示它，不知道列表、不知道按钮，也不负责修改状态。这种拆分解决的是大页面里逻辑和 UI 混在一起的问题。

它也刻意使用 `Column`、`Expanded`、`ListView.separated`、`ListTile` 这些基础布局组件，帮助你看到 Flutter 布局的核心不是写像素坐标，而是在父级约束下组合 Widget。`Expanded` 让列表占据剩余高度，`ListView` 负责滚动，`ListTile` 负责一行内容的常见结构。

最后，`widget_test.dart` 解决的是“UI 只能手动点”的问题。测试通过 `pumpWidget` 构建 Widget tree，通过 `tap` 触发事件，通过 `pump` 推进下一帧，再断言用户看见的文本和图标。它验证的是框架思想是否真的落地：状态变化后，界面描述随之改变。

## 学习重点

- Widget 是不可变配置对象，真正保留生命周期的是 Element 和 State。
- `StatefulWidget` 适合管理局部交互状态；跨页面状态应继续抽到 Provider、Riverpod、Bloc 或显式 service。
- `setState()` 的作用是声明“这个状态对象相关的 UI 需要在下一帧重新构建”，不是立即重绘整个屏幕。
- 布局由 Widget 组合表达，父级 constraints 决定子级可以占多大空间。
- Widget test 可以在没有真机/模拟器的情况下构建 UI、模拟点击并断言文本变化。

## 工程结构

```text
.
├── pubspec.yaml
├── lib/
│   └── main.dart
└── test/
    └── widget_test.dart
```

- `pubspec.yaml`：声明 Dart SDK、Flutter SDK 依赖和 `flutter_test`。
- `lib/main.dart`：应用入口、根 Widget、学习任务页面、状态更新和展示组件。
- `test/widget_test.dart`：构建 `StudyApp`，模拟按钮点击，验证完成数量变化。

## 思想拆解

`pubspec.yaml` 体现的是 Flutter 工程的依赖边界。`flutter` 依赖来自 SDK，说明这个包可以使用 Widget、Material、渲染和平台集成能力；`flutter_test` 只放在 `dev_dependencies`，说明测试工具不进入运行时发布产物。真实项目还会在这里声明 assets、fonts、插件和普通 Dart package。

`main()` 和 `runApp(const StudyApp())` 体现的是启动边界。Flutter 应用入口应该尽量薄，把依赖准备、错误上报、环境配置和根 Widget 装配控制在启动阶段。quickstart 里入口只挂载 `StudyApp`，是为了让读者先把根 Widget 和页面结构看清。

`StudyApp` 返回 `MaterialApp`，体现的是“全局应用外壳也是 Widget”。主题、导航、本地化、文本方向、页面入口都从这层向下传递。`Theme.of(context)` 能在 `LearningBoard` 中工作，是因为 `MaterialApp` 和 `Theme` 这类上层 Widget 通过树结构向下提供上下文信息。

`LearningBoard` 使用 `StatefulWidget` 和 `_LearningBoardState`，体现的是 Widget/State 分离。`LearningBoard` 自身是不可变配置；`_LearningBoardState` 保存 `_tasks`，并在按钮回调中调用 `setState()`。这解决了“界面对象和可变数据绑死”的问题：配置可以重建，状态在对应 Element 位置上延续。

`LearningTask.copyWith()` 体现的是不可变数据更新。点击完成任务时，代码没有直接改旧对象，而是构造一个新的列表和新的任务对象。这样 `build()` 看到的是一份新的状态快照，测试和调试更容易推理。中大型 Flutter 项目常用 `freezed` 或手写不可变模型延续这个思想。

`BuildContext context` 体现的是树位置。`Theme.of(context).textTheme.headlineSmall` 并不是从全局变量取主题，而是沿着当前 context 所在的 Widget tree 向上查找。真实项目里的 Provider、Riverpod scope、Navigator、MediaQuery 也都和“当前位置能看到哪些上层能力”有关。

`Column`、`Expanded` 和 `ListView.separated` 体现的是约束驱动布局。`Padding` 给内部内容留出边距；`Column` 纵向排列子节点；`Expanded` 告诉列表使用剩余空间；`ListView` 在有限高度内滚动。这里没有手写屏幕高度，因为 Flutter 的布局系统会在父子约束传递中算出尺寸。

`TaskTile` 体现的是组合与复用。它把一行任务的图标、标题、样式和副标题收在一个无状态 Widget 里，输入只有 `LearningTask`。当任务完成状态改变时，父组件重新传入新的 `task`，`TaskTile.build()` 再描述对应 UI。它解决的是“列表项展示逻辑到处复制”的问题。

`widget_test.dart` 体现的是可测试的 UI 合约。测试不读取 `_tasks` 私有字段，而是断言 `已完成 0 / 3`、`已完成 1 / 3` 和图标数量。这种写法把测试绑定到用户可见行为，而不是绑定到内部实现细节。以后把 `setState()` 换成 Riverpod，只要用户行为不变，测试仍然有价值。

## 运行前提

- Flutter 3.44 stable 或与仓库基线兼容的最新 stable。
- Dart 3.12.x。
- 已执行 Flutter 官方安装步骤，并能在当前 shell 中运行 `flutter --version`。

本仓库没有提交平台目录。真实开发时可以用 `flutter create .` 生成 `android/`、`ios/`、`web/` 等平台目录；学习本案例和运行 Widget test 只需要 `lib/`、`test/` 和 `pubspec.yaml`。

## 运行

```bash
flutter test
```

如果要在设备或桌面平台上启动应用，可在安装 Flutter SDK 并生成平台目录后运行：

```bash
flutter pub get
flutter run
```

## 预期输出

运行 `flutter test` 时，应看到 Widget test 通过。测试会先断言页面显示 `已完成 0 / 3`，然后点击完成按钮，等待下一帧，再断言页面显示 `已完成 1 / 3`。

启动应用后，页面顶部显示学习任务面板，列表中包含 Dart、Flutter 和 Shelf 三个任务。点击右上角的完成按钮会把下一个未完成任务标记为完成，完成数量随状态变化更新。

## 代码讲解

`main()` 只做一件事：调用 `runApp(const StudyApp())`。这让启动入口保持干净，后续加入配置、依赖注入或错误上报时，也能围绕根 Widget 扩展。

`StudyApp` 返回 `MaterialApp`。它提供 Material Design 主题、默认文本方向、导航外壳和页面根节点。真实项目里，全局主题、路由、本地化和状态容器通常也从这里挂载。这个例子用 `ColorScheme.fromSeed(seedColor: Colors.teal)` 说明 Flutter 可以在一套自绘 UI 体系里统一视觉，而不依赖每个平台的原生按钮默认样式。

`LearningBoard` 是 `StatefulWidget`，因为“任务是否完成”是会随用户点击变化的局部状态。`_LearningBoardState` 持有 `_tasks` 列表和 `_completeNext()` 方法。按钮回调调用 `setState()`，修改第一条未完成任务，然后让 Flutter 在下一帧重新执行相关 `build()`。此时你不需要手动更新计数文本、列表图标和标题删除线，它们都会从 `_tasks` 重新计算出来。

`_completedCount` 是派生数据，而不是额外保存的一份状态。它每次根据 `_tasks.where((task) => task.done).length` 计算完成数量，避免出现“任务已经完成，但计数忘了更新”的状态不一致。Flutter 项目里应优先保存最小必要状态，把能从状态推导出的值写成 getter、computed provider 或 selector。

`Scaffold`、`AppBar`、`Padding`、`Column`、`Expanded`、`ListView.separated` 共同组成页面结构。`Scaffold` 给页面提供标准 Material 骨架；`AppBar` 放标题和按钮；`Padding` 控制安全的阅读边距；`Expanded` 让任务列表在剩余空间内滚动。这个结构展示了 Flutter 如何用 Widget 组合代替手写布局过程。

`TaskTile` 是无状态展示组件。它接收一个 `LearningTask`，根据 `done` 决定图标、文字样式和副标题。这样页面状态和单行展示分开，读者可以清楚看到状态拥有者与纯展示 Widget 的边界。

`widget_test.dart` 使用 `testWidgets` 创建测试环境，`pumpWidget` 构建整棵 Widget tree，`tap` 模拟用户点击，`pump` 等待状态更新后的下一帧。这个测试关注用户可见结果，而不是直接访问私有字段。

如果这个例子接入真实平台能力，例如读取本地通知权限或调用相机，推荐新增 `TaskPlatformService` 一类接口，在 service 中封装 plugin 或 MethodChannel。Widget 仍然只调用“完成任务”“读取提醒状态”等业务方法。这样做能把平台差异留在边界层，避免 `build()` 里混入原生调用。

## 延伸练习

1. 把任务列表拆到 `TaskRepository`，用构造参数注入到 `LearningBoard`，再在测试中传入假数据。
2. 增加“重置全部任务”按钮，练习多个状态更新路径和 Widget test。
3. 把局部 `setState()` 改成 `ValueNotifier` 或 Riverpod provider，观察状态边界如何变化。

## 验收

- 能指出 `pubspec.yaml`、`main.dart`、`widget_test.dart` 的职责。
- 能说明点击按钮后，事件、`setState()`、`build()`、布局和绘制之间的关系。
- 能新增一个任务字段或一个按钮，并补一条 Widget test 验证行为。
