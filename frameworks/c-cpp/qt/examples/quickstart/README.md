# Qt quickstart

## 目标

这个案例用 Qt Core 写一个最小事件驱动程序。它不弹出窗口，而是用 `QCoreApplication`、`QObject`、信号槽和 `QTimer` 展示 Qt 应用的骨架。这样可以先理解 Qt 的思想，再扩展到 Widgets 或 Qt Quick。

学完后，你应该能说明 moc 为什么存在、信号槽如何降低对象耦合、`app.exec()` 为什么是 Qt 程序的核心，以及 CMake 如何通过 `AUTOMOC` 接入 Qt 元对象系统。

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

## 延伸练习

- 把案例改成 Widgets：使用 `QApplication`、`QPushButton` 和 `QLabel` 展示任务数量。
- 把 `TaskBoard` 拆成 `.h/.cpp`，并用 Qt Test 的 `QSignalSpy` 测试信号次数。
- 把内存任务列表替换为读取本地 JSON 文件或通过 `QNetworkAccessManager` 获取远程数据。

## 验收

- 能说明 `Q_OBJECT`、moc 和 `CMAKE_AUTOMOC` 的关系。
- 能指出信号、槽、事件循环分别在代码哪里体现。
- 能新增一个信号或任务字段，并重新构建运行观察输出。
