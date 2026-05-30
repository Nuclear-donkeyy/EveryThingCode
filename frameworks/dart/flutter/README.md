# Flutter

Flutter 是 Dart 生态最重要的应用框架。它不是把原生控件简单包一层，也不是 WebView 容器，而是一套自带渲染、布局、手势、动画、主题、测试和打包工具的跨平台 UI 框架。学习 Flutter 的关键，是把“界面是一棵由状态驱动的 Widget tree”这件事理解透。

## 核心定位

Flutter 解决的是跨平台应用的 UI、交互、渲染和发布问题。它让你用 Dart 描述一棵 Widget tree，再由框架把这棵树转换成 Element tree、RenderObject tree，最终在不同平台上绘制出界面。它适合移动端、桌面端、Web、嵌入式屏幕、内部工具和高度定制的交互界面。

Flutter 不负责替你定义后端架构、数据库模型或业务分层。网络请求、认证、缓存、状态管理、路由和本地存储都可以接入 Flutter 生态里的库，但项目是否清晰，取决于你如何划分 Widget、状态、服务、模型和平台能力边界。

本仓库版本基线是 Flutter 3.44 stable，语言基线是 Dart 3.12.x，策略是 latest stable / officially supported，无官方 LTS 标记。

## 解决的问题

Flutter 首先解决的是“同一套产品体验如何在多个客户端平台上稳定交付”。如果分别用 Android、iOS、Web 和桌面原生技术实现同一个界面，团队往往要维护多套布局、多套状态更新逻辑、多套测试和多套视觉细节。业务越快变化，平台之间越容易出现按钮间距、字体、动画、边界状态和错误提示不一致的问题。Flutter 通过自带渲染引擎、统一 Widget 体系和一套工具链，把大部分 UI 差异收敛到 Dart 代码里。

第二个问题是状态和界面同步。命令式 UI 很容易变成“改数据时还要记得改这里、改那里、再改另一个角落的控件”。列表项完成、计数器更新、按钮禁用、空状态显示这些变化如果靠手动操作控件，会让状态来源越来越模糊。Flutter 用声明式 UI 把界面变成状态的函数：状态变化后重新描述 Widget tree，框架负责复用 Element、更新 RenderObject 和提交绘制。

第三个问题是跨平台 UI 的像素一致性和可定制性。很多跨平台方案依赖平台原生控件，因此不同平台的控件行为、主题、动画和可组合能力都不完全一致。Flutter 选择自绘：Material/Cupertino/自定义组件都可以在同一渲染模型里工作。代价是团队必须理解 Flutter 自己的布局、绘制和语义模型，而不能完全照搬 Web CSS 或原生 View 的经验。

第四个问题是复杂界面的结构化表达。真实应用不会只有一个按钮，而是有导航、主题、滚动、列表、弹窗、表单、动画、权限和平台能力。Flutter 把“可见控件”和“不可见能力”都表达为 Widget，例如 `MaterialApp`、`Scaffold`、`Theme`、`MediaQuery`、`Navigator`、`ListView` 都能进入同一棵树。这样做让组合规则统一，但也要求开发者清楚 Widget tree、Element tree 和 RenderObject tree 的职责差异。

第五个问题是开发反馈和测试成本。客户端 UI 如果每次修改都要完整编译、安装、手动点一遍流程，迭代速度会很慢。Flutter 的 hot reload 让多数 UI 与状态逻辑修改可以快速注入运行中的应用；Widget test 则能在没有真机或模拟器的情况下构建 Widget tree、模拟输入并断言用户可见结果。它们解决的是“客户端 UI 难以快速验证”的问题，而不是替代所有设备级集成测试。

第六个问题是平台差异的边界管理。摄像头、定位、推送、支付、原生 SDK、文件系统和系统分享仍然是平台相关能力。Flutter 通过插件、MethodChannel、EventChannel、FFI 和平台视图把这些能力接入 Dart 层。理想结构不是让 Widget 直接写平台调用，而是把平台能力封装成 service/repository，让 UI 层只依赖清晰的业务接口。

## 设计思想

Flutter 的第一层思想是声明式 UI：你不直接命令按钮“把标题改成 X”，而是修改状态，然后在 `build` 方法里重新描述“当前状态下 UI 应该长什么样”。框架负责比较新旧描述、复用 Element、更新 RenderObject，并把必要部分重新布局和绘制。这一思想专门回应状态同步问题：代码里应该只有一个可信状态来源，UI 是这个状态的当前投影。

第二层思想是 Widget 是配置，Element 是实例位置，RenderObject 是布局和绘制对象。`Text`、`ListView`、`Scaffold` 这样的 Widget 本身通常很轻量、不可变，描述“要什么”；Element 把 Widget 挂到树上的具体位置，负责生命周期、脏标记和复用；RenderObject 负责 constraints、size、paint 等底层工作。理解这三者，才能明白为什么 `build()` 可以频繁执行、为什么 `Key` 会影响复用、为什么布局错误通常来自约束传播。

第三层思想是组合优先。Flutter 几乎所有可见与不可见的能力都是 Widget：文本、按钮、布局、主题、路由、手势、滚动、动画、媒体查询、方向感知都通过 Widget 组合。真实项目的代码质量通常取决于你是否能把大页面拆成有明确职责的小 Widget：状态拥有者负责变更，展示 Widget 负责呈现，服务层负责数据或平台能力。

第四层思想是状态拥有者要清楚。局部交互可以放在 `StatefulWidget` 的 `State` 中；跨页面或跨模块状态应该提升到更高层，通过 Provider、Riverpod、Bloc 或显式构造参数传递。`StatefulWidget` 只是配置，真正保存可变数据的是 `State` 对象；`setState()` 的职责是告诉对应 Element “下一帧需要重新构建”，而不是直接操作屏幕像素。状态放错位置会导致重建范围过大、测试困难或业务逻辑散落在 UI 里。

第五层思想是 `BuildContext` 表达“当前 Widget 在树中的位置”。通过 context，Widget 可以找到主题、媒体信息、路由、InheritedWidget 或状态容器。`BuildContext` 不是全局服务定位器，而是树位置的句柄；在错误的生命周期或错误的树层级使用 context，常常会导致找不到依赖、导航异常或测试困难。

第六层思想是约束驱动布局。Flutter 布局不是 CSS 流式模型，而是父节点把 constraints 传给子节点，子节点选择自己的 size，父节点再决定 position。理解 constraints、`Row`/`Column`、`Expanded`、`Flexible`、`ListView`、`SingleChildScrollView` 的关系，是避免布局溢出的基础。这个模型让布局在多平台、多屏幕尺寸下更可预测，但需要开发者主动处理可滚动区域和剩余空间。

第七层思想是平台能力通过插件和平台通道接入。摄像头、定位、传感器、通知、原生 SDK 等能力通常由插件封装；需要自定义时，可以用 MethodChannel、EventChannel 或 FFI 连接原生代码。Flutter 负责 UI 与跨平台运行时，平台细节仍然需要清晰边界。大型项目应该让平台通道停留在 service 层，Widget 只关心“请求权限”“获取位置”“发起支付”这样的业务动作。

## 架构模型

一个 Flutter 应用通常从 `main()` 进入，调用 `runApp()` 挂载根 Widget。根部常见结构是 `MaterialApp` 或 `CupertinoApp`，它们提供主题、路由、本地化和导航外壳。页面由 Widget tree 表达，局部状态由 `StatefulWidget` 管理，跨页面状态放到状态管理层，业务逻辑放到 service/repository/use case 层。

可以把 Flutter 工程理解成几个互相连接的层次：入口层负责启动和全局配置；UI 层负责 Widget 组合；状态层负责把用户动作转成数据变化；服务层负责网络、数据库、本地存储或平台能力；模型层负责描述数据结构；测试层从不同边界验证行为。

本仓库 quickstart 只保留最小结构：`pubspec.yaml` 声明依赖，`lib/main.dart` 放入口、Widget 和内存状态，`test/widget_test.dart` 用 Widget test 验证交互。真实项目可以继续拆出 `lib/features/<feature>/`、`lib/shared/`、`lib/data/`、`lib/domain/` 和 `lib/platform/`。

## 请求/执行生命周期

Flutter 没有传统 Web 框架里的“请求生命周期”，更准确地说它有一次启动、一次事件和一次渲染帧的执行链。

启动时，Dart VM 或 AOT 产物加载应用，执行 `main()`，`runApp()` 把根 Widget 交给 Flutter engine。框架创建 Element tree，并根据 Widget 创建或更新 RenderObject tree。随后进入事件循环，等待输入、定时器、Future、Stream、平台消息或动画 tick。

用户点击按钮时，手势系统把平台输入事件转换为 Flutter 手势回调。回调修改状态，例如调用 `setState()`。`setState()` 不直接重绘屏幕，而是把对应 Element 标记为 dirty。下一帧调度时，框架重新执行相关 `build()`，得到新的 Widget 描述，再更新 Element/RenderObject。

布局阶段，父节点向子节点传 constraints，子节点返回 size。绘制阶段，RenderObject 生成绘制指令，最终由 engine 绘制到屏幕。这个过程解释了为什么 Flutter 推荐不可变 Widget、轻量 build 方法和清晰状态边界：你写的是 UI 描述，框架负责高效执行。

平台通道参与的是另一条生命周期：Dart 代码调用 channel，消息经过 engine 传到 Android/iOS/macOS/Windows/Linux/Web 对应平台实现，原生代码返回结果或事件。大型项目通常把平台通道封装在 service 层，避免 Widget 直接依赖平台细节。

## 工程结构

quickstart 使用最小 Flutter 工程：

```text
examples/quickstart/
├── pubspec.yaml
├── lib/
│   └── main.dart
└── test/
    └── widget_test.dart
```

`pubspec.yaml` 描述 SDK 约束、Flutter 依赖和测试依赖。`lib/main.dart` 包含 `StudyApp`、学习任务页面、状态更新逻辑和可复用 Widget。`test/widget_test.dart` 启动 Widget tree，模拟点击，断言页面文本变化。

真实项目扩展时，建议按功能域组织，而不是按技术层堆满 `screens/`、`widgets/`、`models/`。例如 `lib/features/tasks/` 可以包含页面、状态、模型、repository 和测试；跨功能的主题、路由、HTTP 客户端放在 `lib/shared/` 或 `lib/core/`。这样能让业务边界比框架目录更清楚。

## 配置方式

Flutter 的基础配置集中在 `pubspec.yaml`：SDK 版本、依赖、dev dependencies、assets、fonts、flutter 插件声明都在这里。包版本解析结果通常写入 `pubspec.lock`，应用项目建议提交 lockfile，以保证 CI 和开发机使用一致依赖。

平台配置分散在 `android/`、`ios/`、`macos/`、`windows/`、`linux/`、`web/` 等目录。权限、bundle id、应用图标、原生 SDK 配置和构建参数通常需要在对应平台目录维护。quickstart 为了聚焦 Flutter 思想，没有提交这些平台目录；真实项目可用 `flutter create` 生成。

运行环境配置常见做法包括 `--dart-define`、不同 flavor、环境变量生成文件、远程配置服务和构建脚本。教学阶段先用常量或内存数据，避免过早把配置系统引入 UI 学习。

## 模块与依赖管理

Flutter 使用 Dart 的 package 机制，通过 `pubspec.yaml` 和 `dart pub`/`flutter pub` 管理依赖。一个应用可以依赖普通 Dart package、Flutter plugin、本地 path package 或 Git package。多包仓库常用 Melos 管理版本、脚本和发布。

在应用内部，模块化的核心不是“文件夹多”，而是依赖方向清晰。Widget 可以依赖状态对象和展示模型；状态对象可以依赖 repository/service；repository 可以依赖 HTTP、本地数据库或平台能力；底层服务不应该反向依赖 Widget。这样才能让 UI 测试、单元测试和替换数据源变得简单。

Flutter 本身没有内建依赖注入容器。小项目可以显式构造并向下传参；中大型项目通常使用 Provider、Riverpod、get_it 或 Bloc 生态管理依赖和状态生命周期。无论选哪个库，都要能回答：对象在哪里创建、什么时候释放、测试时如何替换。

## 数据访问

quickstart 使用内存列表保存学习任务，目的是让读者先观察状态改变如何驱动 UI 重建。内存数据不需要异步、不需要序列化，也没有失败路径，适合展示 `StatefulWidget` 和 `setState()` 的最小模型。

真实 Flutter 应用常见数据来源包括 REST/GraphQL API、本地 SQLite/drift、文件、SharedPreferences/SecureStorage、平台 SDK 和推送事件。建议用 repository 隔离数据访问，把 JSON 解析、缓存策略、错误转换和重试逻辑放到 UI 外面。

当 API 数据变复杂时，可以用 `json_serializable` 生成 JSON 映射，用 `freezed` 建不可变模型和联合状态。这样 UI 层接收到的是明确的 `Loading`、`Data`、`Error` 状态，而不是散落的布尔变量和 nullable 字段。

## 测试方式

Flutter 测试通常分三层。纯 Dart 业务逻辑用 `dart test` 或 `flutter test` 运行普通单元测试。Widget test 用 `flutter_test` 在测试环境中构建 Widget tree、模拟点击、输入和滚动，并断言文本、图标或布局存在。集成测试用 `integration_test` 在真实设备或模拟器上验证端到端流程。

quickstart 使用 Widget test，因为它刚好覆盖 Flutter 的核心：给定初始状态，页面展示什么；用户点击后，状态如何变化；下一帧 UI 是否更新。后续如果引入 repository，可以把 repository 抽象成接口，在 Widget test 中替换为内存实现。

测试时要避免把所有逻辑都藏在 Widget 回调里。能抽到纯 Dart 函数或状态对象的逻辑，优先单测；需要验证用户体验的交互，再用 Widget test；需要验证平台权限、真实网络或设备能力时，再上集成测试。

## 部署方式

本地开发通常使用 `flutter run`，可选择设备或平台。测试使用 `flutter test`。构建发布产物时，移动端使用 `flutter build apk`、`flutter build appbundle` 或 `flutter build ios`，桌面端和 Web 使用对应的 `flutter build macos/windows/linux/web`。

真实发布还要处理签名、证书、渠道、环境配置、崩溃收集、性能监控和应用商店审核。Flutter 统一了大量 UI 与构建体验，但平台发布规范仍然要按 Android、iOS、Web 或桌面平台分别处理。

CI 中常见流水线是安装 Flutter SDK、缓存 Pub 依赖、运行 `flutter analyze`、`flutter test`、按平台构建。对于多平台项目，建议先保证测试和静态检查稳定，再逐步加入各平台构建矩阵。

## 适用场景与取舍

优先选择 Flutter 的场景包括：需要一套代码覆盖多个客户端平台；UI 定制程度高；团队愿意以 Dart/Flutter 为主栈；产品需要较好动画和一致视觉；业务更像应用而不是内容网页。

谨慎选择 Flutter 的场景包括：项目只需要传统网站 SEO；团队主要能力集中在 Web 技术栈；应用大量依赖复杂原生 SDK 且没有成熟插件；包体、首屏、平台控件一致性有极端要求。Flutter 可以做 Web，但它的强项仍然是应用式 UI，而不是替代所有网页技术。

和原生开发相比，Flutter 带来跨平台一致性和较快迭代，但需要团队理解自己的渲染与布局模型。和 React Native 相比，Flutter 更强调自绘和完整 UI 工具链；代价是生态选择、平台适配和 Dart 学习成本需要纳入评估。

## 案例索引

- [quickstart](examples/quickstart/)：学习任务面板，展示 `runApp`、`MaterialApp`、`StatefulWidget`、`setState`、布局组合和 Widget test。

## 版本来源

- 语言基线：Dart 3.12.x
- 框架基线：Flutter 3.44 stable
- 版本策略：latest stable / officially supported，无官方 LTS
- 官方来源：https://docs.flutter.dev/release/archive
- 校验日期：2026-05-30
