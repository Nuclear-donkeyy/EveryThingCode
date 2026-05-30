# Qt

Qt 是跨平台应用框架，覆盖 GUI、事件循环、对象模型、资源系统、网络、数据库、多媒体和部署工具。它最常被认识为桌面 GUI 框架，但更准确地说，Qt 是一套围绕 QObject 元对象系统构建的应用开发平台。

## 核心定位

Qt 解决的是跨平台应用开发中的重复成本：不同操作系统的事件循环、窗口系统、控件、定时器、线程通信、资源打包和部署细节。它不替代 C++ 基础，不保证你可以忽略平台差异，也不是所有场景中最轻的选择。对于只需要一个小型命令行工具的项目，Qt 往往过重；对于复杂桌面应用、工业控制台、可视化工具和长期维护的跨平台产品，它非常有价值。

本仓库先用 Qt Core 写一个控制台事件驱动案例，而不是直接做复杂窗口。这样可以先看清 `QCoreApplication`、`QObject`、信号槽和事件循环，再自然过渡到 Widgets 或 Qt Quick。

## 解决的问题

只用标准 C++ 写一个跨平台 GUI 或事件驱动应用，很快会遇到几类重复问题。第一类是平台事件循环差异：Windows、macOS、Linux/X11/Wayland 对窗口消息、定时器、输入事件和系统通知的模型并不相同，应用还要避免主线程被阻塞。Qt 用 `QCoreApplication`、`QGuiApplication` 和 `QApplication` 把这些平台细节收进统一的 application 对象，开发者只需要在组件构建完成后进入 `app.exec()`，再通过事件、定时器和信号槽响应外部变化。

第二类是控件层级与对象生命周期。GUI 应用天然是树状结构：窗口包含布局，布局包含控件，控件又可能拥有子对象、定时器、动作和模型。如果所有对象都靠裸指针和手工 `delete` 管理，关闭窗口、异常路径、跨线程回调都容易变成内存和悬空引用问题。Qt 让大多数可参与框架协作的类型继承 `QObject`，并通过 parent-child object tree 管理生命周期：父对象析构时会递归销毁子对象，信号槽连接也会在对象销毁后自动断开。

第三类是对象协作。没有框架时，按钮点击、网络完成、模型变更常被写成回调、观察者列表或紧耦合接口，发送者必须知道接收者的形状。Qt 的 signals/slots 把“发生了什么”和“谁来处理”分离：控件、模型、服务都可以发信号，接收者用槽函数、lambda 或普通可调用对象处理。跨线程时，Qt 还可以把调用排进目标对象所属线程的事件队列中，避免直接跨线程操作 UI。

第四类是 C++ 标准能力和 GUI 工程需求之间的缺口。标准 C++ 没有内建反射、属性系统、运行时方法调用、信号声明、QML 暴露和对象元信息。Qt 使用 `Q_OBJECT` 宏和 Meta-Object Compiler，也就是 moc，在构建期生成元对象代码。这个设计让 Qt 能在保持 C++ 编译模型的同时提供属性绑定、动态调用、类型信息和信号槽。

第五类是资源、平台差异和构建集成。真实 GUI 应用会包含图标、翻译、QML、插件、平台主题和部署产物。Qt 提供资源系统、平台抽象层、Widgets/QML 两套主要 UI 技术，以及 CMake imported targets、`AUTOMOC`、`AUTORCC`、`AUTOUIC` 等构建集成。它没有消灭所有平台差异，但把差异收敛到 Qt 模块、平台插件和少量配置点上。

## 设计思想

Qt 的核心思想是“统一应用外壳 + 对象模型 + 事件驱动”。`QCoreApplication`/`QApplication` 不是普通的全局工具类，而是 Qt 程序接入平台事件系统的入口。它解析应用参数，初始化平台抽象，管理事件队列，并通过 `exec()` 持续分发事件。命令行事件服务可以只用 `QCoreApplication`；Widgets 桌面应用使用 `QApplication`；Qt Quick 或纯图形界面可以使用 `QGuiApplication`。

`QObject` 是 Qt 设计的中心。它提供父子对象树、对象名称、运行时类型信息、属性、信号槽、线程亲和性和事件过滤等能力。C++ 标准本身没有反射和跨对象消息机制，Qt 通过 moc 在构建期生成额外代码来补足这部分能力。只要类里有 `Q_OBJECT`，它就能声明信号、暴露元信息，并参与 Qt 的连接、属性和动态调用机制。

object tree 是 Qt 对生命周期问题的回答。窗口、控件、动作、定时器和业务对象可以形成父子关系，父对象析构时负责清理子对象。这个模型尤其适合 GUI，因为界面天然有包含关系。它不等于所有权设计都不用思考：共享服务、跨线程 worker、模型对象仍然需要清晰的归属；但在控件树和短生命周期组件中，它显著减少了手工释放。

信号槽是 Qt 最重要的解耦机制。发送者只声明“发生了什么”，接收者决定“如何处理”。连接可以是同步的，也可以跨线程排队执行。对学习者来说，信号槽比回调更直观的一点是：发送者不需要持有接收者的业务接口，生命周期也能由 QObject 父子关系辅助管理。

事件循环是 Qt 应用的心跳。用户点击、定时器、socket 可读、跨线程消息都会进入事件队列，由 `app.exec()` 驱动分发。理解事件循环后，才知道为什么不要在 UI 线程里做长时间阻塞任务，为什么耗时工作要放进 worker 或异步 API。

Widgets 和 QML 是 Qt 的两条常见界面路线。Widgets 更接近传统桌面控件体系，适合复杂表单、内部工具、工业软件和原生风格控件；QML/Qt Quick 偏声明式和动画友好，适合现代交互、触控界面和快速迭代的 UI。两者背后都依赖 Qt 的事件循环、对象模型和资源系统，只是 UI 表达方式不同。

CMake integration 是 Qt 工程化的一部分，而不只是构建细节。`find_package(Qt6 REQUIRED COMPONENTS Core Widgets Quick)` 让项目按模块声明能力，`target_link_libraries(app PRIVATE Qt6::Core)` 让依赖进入 target 图，`CMAKE_AUTOMOC` 自动处理 `Q_OBJECT` 对应的 moc 生成。对于资源文件和 `.ui` 文件，项目还会使用 `AUTORCC`、`AUTOUIC` 或 Qt 提供的 CMake 函数。这样 Qt 的元对象系统、资源系统和 C++ 构建系统可以在同一套 target 模型里协作。

## 架构模型

Qt 应用通常由应用对象、QObject 组件、界面层、业务层和资源组成。GUI 程序会使用 `QApplication` 或 `QGuiApplication`，纯控制台/服务类程序可以使用 `QCoreApplication`。Widgets 项目通常有窗口类、控件树和槽函数；Qt Quick 项目则有 QML 组件、C++ 后端对象和属性绑定。

本案例结构保持最小：`main.cpp` 中定义 `TaskBoard` QObject，它维护内存任务列表，暴露 `taskAdded` 信号，并在槽函数里打印状态。`QTimer::singleShot` 把工作安排进事件循环，最后调用 `app.quit()` 退出。这样不用打开窗口也能观察 Qt 的执行模型。

## 请求/执行生命周期

Qt 中一次“执行”通常不是从请求到响应，而是从事件产生到槽函数处理。程序启动后创建 application 对象，构建 QObject 组件并建立 signal-slot 连接，然后进入 `app.exec()`。事件进入队列后，Qt 根据对象线程亲和性和连接类型分发事件；槽函数执行完后控制权回到事件循环。

如果是 Widgets 应用，用户点击按钮会产生平台事件，Qt 把它转换成控件事件，再触发信号，例如 `clicked()`；业务槽函数更新模型或界面。若是本案例，`QTimer` 事件触发 lambda，lambda 调用 `addTask`，`addTask` 发出 `taskAdded` 信号，连接的槽函数输出消息。

## 工程结构

本仓库案例结构如下：

```text
frameworks/c-cpp/qt/examples/quickstart/
├── CMakeLists.txt
├── README.md
└── src/
    └── main.cpp
```

真实 Qt 项目可以扩展为 `src/` 放 C++ 类，`ui/` 放 `.ui` 文件，`qml/` 放 Qt Quick 界面，`resources/` 放 `.qrc` 资源，`tests/` 放 Qt Test 或普通 C++ 测试。UI 代码、业务模型和外部服务访问应保持边界清楚，避免所有逻辑塞进窗口类。

## 配置方式

Qt 项目常见配置入口有三个。CMake 中使用 `find_package(Qt6 REQUIRED COMPONENTS Core Widgets)` 查找模块，用 `target_link_libraries(app PRIVATE Qt6::Core)` 链接 imported target，用 `CMAKE_AUTOMOC` 自动运行 moc。运行时配置则通常放在 `QSettings`、命令行参数、环境变量或平台配置目录中。

本案例只依赖 Qt Core，因此 `find_package` 只查 `Core`。如果你改成 Widgets 程序，需要把 `QCoreApplication` 换成 `QApplication`，并在 CMake 中加入 `Widgets` 组件和 `Qt6::Widgets` 链接。

## 模块与依赖管理

Qt 以模块组织能力，例如 Core、Gui、Widgets、Network、Sql、Quick、Test。每个模块在 CMake 中都有对应 target。项目自己的模块则建议拆成普通 C++ 类或库 target，再由应用 target 组合。QObject 的父子关系负责对象生命周期，不等于业务依赖注入；复杂项目仍然需要清晰的服务构造、接口隔离和测试替身。

信号槽是运行时通信机制，CMake target 是构建时依赖机制，两者不要混淆。一个类可以通过信号槽降低运行时耦合，但它所属的库仍然需要在 CMake 中显式链接 Qt 模块和项目内部库。

## 数据访问

Qt 提供 Qt SQL、Qt Network、JSON、文件系统和设置存储等能力。桌面应用常见做法是界面层只操作模型或服务接口，服务层再访问 SQLite、HTTP API、本地文件或设备 SDK。这样 UI 线程只负责交互和展示，耗时 I/O 可以放进工作线程、异步网络请求或后台任务。

本案例使用内存 `QStringList` 保存任务，只为突出信号槽和事件循环。后续可以把任务来源替换为 `QNetworkAccessManager`、SQLite 或本地 JSON 文件，但要注意不要在事件循环中做阻塞 I/O。

## 测试方式

Qt 项目可以使用 Qt Test，也可以用 GoogleTest/Catch2 测试纯 C++ 业务层。GUI 测试通常成本较高，因此推荐把业务逻辑放在可测试的普通类中，把窗口类保持为薄适配层。对于信号槽，可以用 `QSignalSpy` 观察信号是否发出、参数是否正确。

本 quickstart 的最小验收是构建并运行，看到任务添加信号按顺序输出。进一步测试可以把 `TaskBoard` 拆到独立头/源文件，使用 Qt Test 验证 `taskAdded` 信号次数和任务数量。

## 部署方式

本地运行阶段，只要 Qt SDK、CMake 和编译器可用即可构建。真正交付时，Qt 应用需要带上对应平台插件和动态库。Windows 常用 `windeployqt`，macOS 常用 `macdeployqt`，Linux 可以使用系统包、AppImage、Flatpak 或容器。Qt Quick 项目还要考虑 QML 模块和资源打包。

服务端或控制台 Qt Core 程序部署相对简单，但仍要确认动态库路径、OpenSSL 版本、插件目录和目标平台 ABI。商业项目还必须遵守 Qt 的许可策略。

## 适用场景与取舍

Qt 适合长期维护的跨平台桌面应用、工业软件、设备控制台、带复杂状态的 GUI 工具，以及需要 C++ 性能和成熟 UI 生态的项目。它的优势是工程完整、文档丰富、平台覆盖好；代价是工具链和部署复杂度较高，元对象系统也要求理解 moc 生成代码。

如果界面非常简单，Dear ImGui 或原生平台控件可能更轻；如果目标是游戏，SDL、SFML、Unreal 或 Unity 生态更合适；如果主要是 Web 管理后台，用浏览器技术栈可能更快。选择 Qt 时，要确认团队愿意接受它的构建、部署和许可模型。

## 案例索引

- [core-ideas](examples/core-ideas/)：把上一节“解决的问题”和“设计思想”映射到 quickstart 的关键代码片段。
- [quickstart](examples/quickstart/)：Qt Core 控制台事件驱动程序，演示 QObject、信号槽、事件循环和 CMake `AUTOMOC`。

## 版本来源

- 版本基线：latest LTS。
- 策略：使用 Qt 官方当前 LTS 线；项目通过 Qt SDK/包管理器和 CI 镜像锁定具体 patch。
- 官方来源：https://www.qt.io/product/qt6
- 校验日期：2026-05-30
