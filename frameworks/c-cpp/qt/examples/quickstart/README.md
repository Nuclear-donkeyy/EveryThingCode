# Qt quickstart

## 目标

这个案例用 Qt Core 写一个最小事件驱动程序。它不弹出窗口，而是用 `QCoreApplication`、`QObject`、信号槽和 `QTimer` 展示 Qt 应用的骨架。这样可以先理解 Qt 的思想，再扩展到 Widgets 或 Qt Quick。

学完后，你应该能说明 moc 为什么存在、信号槽如何降低对象耦合、`app.exec()` 为什么是 Qt 程序的核心，以及 CMake 如何通过 `AUTOMOC` 接入 Qt 元对象系统。

## 这个案例解决什么问题

这个 quickstart 故意不从窗口开始，而是先用 Qt Core 拆开 Qt 最底层的工程问题。一个跨平台 GUI 应用最终都会遇到事件循环、对象协作、对象生命周期和构建接线；如果一开始就看按钮和布局，反而容易把这些机制误认为“界面语法”。本例用控制台输出模拟“任务被添加后界面要更新”的场景，让你先看清 Qt 如何处理事件驱动程序的骨架。

`QCoreApplication app(argc, argv)` 解决的是应用如何接入 Qt 事件系统的问题。没有它，`QTimer`、排队连接、socket notifier 等能力都没有统一的事件循环来调度。GUI 程序会把它换成 `QApplication`，但思想相同：先创建应用对象，再创建组件和连接，最后进入 `app.exec()`。

`TaskBoard` 解决的是业务状态和外部反应如何解耦的问题。它只维护任务列表并发出 `taskAdded`，并不知道日志输出、界面刷新或测试断言在哪里发生。真实 Qt Widgets 程序里，类似信号可能来自按钮、模型或网络层；槽函数可能更新 `QLabel`、刷新表格或触发保存。

`QObject::connect` 解决的是对象之间不必直接互相调用的问题。这里连接到 lambda 是最小写法；真实项目也可以连接到窗口槽函数、服务对象方法或跨线程 worker。Qt 会跟踪连接两端的 QObject 生命周期，对象销毁后连接会失效，减少手工观察者列表带来的悬空引用风险。

`CMAKE_AUTOMOC` 解决的是 Qt 元对象代码如何进入普通 C++ 构建的问题。`TaskBoard` 使用 `Q_OBJECT` 和 `signals` 后，moc 必须生成额外代码；如果忘记配置，编译或链接阶段通常会出现和 vtable、meta-object 或 signal 相关的错误。本案例把 `AUTOMOC` 明确放进 `CMakeLists.txt`，让 CMake 自动扫描并生成需要的 moc 文件。

## 学习重点

- `QCoreApplication` 创建应用对象并启动事件循环。
- `QObject` 通过 `Q_OBJECT` 宏接入元对象系统。
- `signals` 声明事件，`slots` 或普通可调用对象处理事件。
- `QTimer::singleShot` 把工作安排到事件循环中执行。
- CMake `find_package(Qt6 REQUIRED COMPONENTS Core)` 和 `CMAKE_AUTOMOC` 负责查找 Qt 与生成 moc 代码。

## 工程结构

```text
.
├── CMakeLists.txt
├── README.md
└── src/
    └── main.cpp
```

`main.cpp` 中的 `TaskBoard` 是一个教学用 QObject：它维护内存任务列表，添加任务时发出 `taskAdded` 信号。真实项目应把 QObject 类拆到头文件和源文件中，并把 UI、业务模型、外部服务访问分层。

把它迁移到 Widgets 时，常见结构会变成：`main.cpp` 创建 `QApplication` 和主窗口，窗口类拥有按钮、列表、模型等子对象，业务类继续发出类似 `taskAdded` 的信号。把它迁移到 QML/Qt Quick 时，C++ 后端对象可以通过属性和信号暴露给 QML，界面用声明式绑定响应状态变化。

## 运行前提

- Qt 6 latest LTS，并安装 Qt Core 开发文件。
- CMake latest stable。
- 支持 C++23 的编译器。
- 如果你使用 vcpkg、Conan 或 Qt Creator，需要让 CMake 能找到 Qt6，例如设置 `CMAKE_PREFIX_PATH` 或使用对应 toolchain。

## 运行

```bash
cmake -S . -B build -DCMAKE_PREFIX_PATH=/path/to/Qt
cmake --build build
./build/qt_quickstart
```

如果 Qt 安装在系统默认路径或 Qt Creator 已经配置 kit，可以省略 `-DCMAKE_PREFIX_PATH`。Windows 或多配置生成器下，可执行文件可能在 `build/Debug/` 或 `build/Release/`。

## 预期输出

运行后会看到信号槽触发的日志：

```text
Qt event loop demo
added task #1: connect signal to slot
added task #2: let event loop deliver work
total tasks: 2
```

程序输出后会主动调用 `app.quit()`，因此不会一直挂起。

## 代码讲解

`CMakeLists.txt` 开启 `CMAKE_AUTOMOC`，这是 Qt CMake 项目的关键配置。`TaskBoard` 使用 `Q_OBJECT` 宏后，moc 需要为它生成元对象代码；`AUTOMOC` 会在构建时自动扫描并处理这个步骤。`find_package(Qt6 REQUIRED COMPONENTS Core)` 获取 Qt Core target，`target_link_libraries(qt_quickstart PRIVATE Qt6::Core)` 把依赖挂到应用 target 上。

`TaskBoard::addTask` 先把任务写入 `QStringList`，再发出 `taskAdded` 信号。`QObject::connect` 把这个信号连接到 lambda，lambda 负责打印消息。发送者不知道接收者是谁，只知道“任务已添加”这个事件发生了。

`QTimer::singleShot(0, ...)` 的含义是：应用进入事件循环后尽快执行这段 lambda。lambda 添加两条任务，打印总数，然后调用 `app.quit()` 退出事件循环。这个流程很适合观察 Qt 的事件驱动模型。

## 思想拆解

`CMakeLists.txt` 展示的是 Qt 如何融入现代 C++ target 模型。`find_package(Qt6 REQUIRED COMPONENTS Core)` 表示本例只依赖 Qt Core，不需要 Widgets、Gui 或 Quick；这让案例可以专注事件循环和对象模型。`target_compile_features(qt_quickstart PRIVATE cxx_std_23)` 把 C++ 标准要求挂到应用 target 上；`target_link_libraries(qt_quickstart PRIVATE Qt6::Core)` 则把 include path、编译定义、链接库和平台依赖都通过 Qt 的 imported target 传给编译器。

`TaskBoard final : public QObject` 展示的是 Qt 的对象边界。它不是普通数据结构，因为它要发信号；也不是窗口类，因为它不负责展示。这个拆分对应真实项目中的“模型/服务层”：业务对象维护状态，界面或日志只是状态变化的订阅者。如果以后把控制台输出换成 `QLabel::setText`，`TaskBoard` 不需要改。

`Q_OBJECT` 是这个类进入 Qt 元对象世界的开关。`signals:` 不是普通 C++ 标准关键字，而是 Qt 借助 moc 支持的声明方式。moc 会读取类声明，生成信号调用、元信息和动态调用所需的代码；文件末尾的 `#include "main.moc"` 是因为这个 QObject 类写在 `.cpp` 文件中，方便单文件教学。真实项目通常把 QObject 类放到头文件，`AUTOMOC` 会处理对应头文件。

`QObject::connect(&board, &TaskBoard::taskAdded, lambda)` 展示的是解耦后的执行链路：`addTask` 更新源状态，`emit taskAdded(...)` 传播事实，lambda 决定如何响应。这里是直接连接，信号发出时立即执行 lambda；如果接收者在其他线程，Qt 可以用排队连接把调用投递到目标线程事件循环中。这也是 Qt 能让后台任务和 UI 主线程协作的基础。

`QTimer::singleShot(0, &app, ...)` 展示的是“把工作交给事件循环”。参数 `0` 不代表立刻在当前调用栈执行，而是进入事件队列后尽快执行。真实 GUI 中，用户点击、窗口重绘、网络完成、定时任务都以类似方式回到事件循环。`app.quit()` 则投递退出请求，让 `app.exec()` 返回，程序自然结束。

## 与完整 GUI 程序的对应关系

| quickstart 元素 | Widgets 程序中的对应物 | 解决的问题 |
| --- | --- | --- |
| `QCoreApplication` | `QApplication` | 接入平台事件循环、参数、插件和应用生命周期 |
| `TaskBoard` | model/service QObject | 把业务状态从窗口控件中拆出来 |
| `taskAdded` signal | `clicked()`、`dataChanged()`、自定义业务信号 | 把状态变化广播给感兴趣的对象 |
| lambda slot | 窗口槽函数、服务方法、测试 spy | 用独立处理器响应事件 |
| `QTimer::singleShot` | 用户事件、网络完成、动画帧、后台消息 | 把工作排进事件循环，避免手写平台消息分发 |
| `CMAKE_AUTOMOC` | Qt Widgets/QML 项目的 moc 集成 | 让 `Q_OBJECT`、signals/slots、属性和元信息参与构建 |

## 延伸练习

- 把案例改成 Widgets：使用 `QApplication`、`QPushButton` 和 `QLabel` 展示任务数量。
- 把 `TaskBoard` 拆成 `.h/.cpp`，并用 Qt Test 的 `QSignalSpy` 测试信号次数。
- 把内存任务列表替换为读取本地 JSON 文件或通过 `QNetworkAccessManager` 获取远程数据。

## 验收

- 能说明 `Q_OBJECT`、moc 和 `CMAKE_AUTOMOC` 的关系。
- 能指出信号、槽、事件循环分别在代码哪里体现。
- 能新增一个信号或任务字段，并重新构建运行观察输出。
