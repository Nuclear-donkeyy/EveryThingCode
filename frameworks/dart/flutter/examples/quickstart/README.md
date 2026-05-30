# Flutter quickstart

这个案例用一个“学习任务面板”展示 Flutter 的最小真实工程：应用入口、Widget tree、局部状态、布局、事件回调和 Widget 测试都放在可运行文件里。读者不需要先掌握复杂状态管理库，只要会基本编程，就可以观察状态变化如何驱动 UI 重建。

## 目标

完成本案例后，你应该能说明 `main()`、`runApp()`、`MaterialApp`、`StatefulWidget`、`setState()` 和 Widget test 各自负责什么；能把一个页面拆成状态拥有者和展示 Widget；能修改内存任务列表并看到测试反馈。

案例刻意不接网络和数据库。第一步先把 Flutter 的 UI 思想看清：界面不是一堆要手动操作的控件，而是当前状态的一次声明式描述。

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

`StudyApp` 返回 `MaterialApp`。它提供 Material Design 主题、默认文本方向、导航外壳和页面根节点。真实项目里，全局主题、路由、本地化和状态容器通常也从这里挂载。

`LearningBoard` 是 `StatefulWidget`，因为“任务是否完成”是会随用户点击变化的局部状态。`_LearningBoardState` 持有 `_tasks` 列表和 `_completeNext()` 方法。按钮回调调用 `setState()`，修改第一条未完成任务，然后让 Flutter 在下一帧重新执行相关 `build()`。

`TaskTile` 是无状态展示组件。它接收一个 `LearningTask`，根据 `done` 决定图标、文字样式和副标题。这样页面状态和单行展示分开，读者可以清楚看到状态拥有者与纯展示 Widget 的边界。

`widget_test.dart` 使用 `testWidgets` 创建测试环境，`pumpWidget` 构建整棵 Widget tree，`tap` 模拟用户点击，`pump` 等待状态更新后的下一帧。这个测试关注用户可见结果，而不是直接访问私有字段。

## 延伸练习

1. 把任务列表拆到 `TaskRepository`，用构造参数注入到 `LearningBoard`，再在测试中传入假数据。
2. 增加“重置全部任务”按钮，练习多个状态更新路径和 Widget test。
3. 把局部 `setState()` 改成 `ValueNotifier` 或 Riverpod provider，观察状态边界如何变化。

## 验收

- 能指出 `pubspec.yaml`、`main.dart`、`widget_test.dart` 的职责。
- 能说明点击按钮后，事件、`setState()`、`build()`、布局和绘制之间的关系。
- 能新增一个任务字段或一个按钮，并补一条 Widget test 验证行为。
