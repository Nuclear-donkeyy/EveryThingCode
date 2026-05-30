# CMake quickstart

## 目标

这个案例用一个最小 C++23 命令行程序展示现代 CMake 的基本工作流：源码不直接在根目录编译，而是通过 `cmake -S . -B build` 生成独立构建目录，再用 target 描述可执行文件、编译特性和编译期配置。

学完后，你应该能解释 `CMakeLists.txt` 为什么不是普通 shell 脚本，能区分配置、生成、构建、运行四个阶段，并能把同样的结构迁移到自己的 C++ 项目中。

## 学习重点

- `cmake_minimum_required` 固定 CMake 语义下限，避免不同版本采用不同策略。
- `project(... VERSION ... LANGUAGES CXX)` 声明项目元信息和使用的语言。
- `add_executable` 创建一个 target，而不是直接拼接编译命令。
- `target_compile_features` 在 target 上声明 C++23 要求。
- `target_compile_definitions` 把项目版本以宏的方式传入源码，展示构建配置如何进入程序。

## 这个案例解决什么问题

如果不用构建系统，这个程序在本机也许可以靠一条命令编译：

```bash
c++ -std=c++23 src/main.cpp -o cmake_quickstart
```

但这条命令没有回答团队工程里真正麻烦的问题：Windows 上用 MSVC 时参数怎么写，Debug 和 Release 输出放在哪里，未来拆出库 target 后 include path 怎么传播，测试 target 如何复用同一批编译设置，IDE 如何知道真实的 C++ 标准和宏。项目越小，这些问题越容易被忽略；项目一旦增加平台、依赖和测试，它们就会变成主要维护成本。

这个 quickstart 用最小代码展示 CMake 的基本解法：把“怎么调用编译器”交给 generator，把“项目要生成什么、每个产物需要什么”写成 target 属性，把构建产物放进 `build/`，让源码目录保持干净。它没有引入第三方库，是为了让你先看清 CMake 自己解决的问题。

## 工程结构

```text
.
├── CMakeLists.txt
├── README.md
└── src/
    └── main.cpp
```

`CMakeLists.txt` 是构建入口，`src/main.cpp` 是程序入口。当前案例只有一个可执行文件；真实项目可以继续拆出 `include/`、`src/lib.cpp`、`tests/` 和多个库 target。

## 运行前提

- CMake latest stable，或至少支持 `target_compile_features` 和 C++23 feature 声明的现代版本。
- 支持 C++23 的编译器，例如 Clang、GCC 或 MSVC。
- macOS/Linux/Windows 均可运行；Windows 下可执行文件路径通常是 `build\\Debug\\cmake_quickstart.exe` 或 `build\\Release\\cmake_quickstart.exe`。

## 运行

```bash
cmake -S . -B build
cmake --build build
./build/cmake_quickstart
```

如果使用多配置生成器，例如 Visual Studio 或 Xcode，可以显式选择配置：

```bash
cmake --build build --config Release
```

## 预期输出

程序会输出项目名称、C++ 标准、版本宏和一组任务状态，类似：

```text
CMake target model demo
project version: 1.0.0
C++ standard: 202302
tasks:
- configure: done
- generate: done
- build: ready
```

`C++ standard` 的具体数字由编译器决定；只要能看到任务列表，就说明 CMake 已经完成配置、构建和运行。

## 代码讲解

`CMakeLists.txt` 的第一行声明最低 CMake 版本。它解决的是“同一份脚本在不同 CMake 版本上语义漂移”的问题。CMake 有很长的历史，很多命令会随着 policy 演进；固定下限可以让团队明确自己依赖的是哪一代行为。

`project(CMakeQuickstart VERSION 1.0.0 LANGUAGES CXX)` 声明项目元信息和使用语言。`LANGUAGES CXX` 会触发 CMake 探测 C++ 编译器，并为后续 generator 准备对应规则。`VERSION 1.0.0` 不只是文档，它会成为 `${PROJECT_VERSION}`，后面通过 `target_compile_definitions` 进入 C++ 程序。

`add_executable(cmake_quickstart src/main.cpp)` 创建 target。target 是现代 CMake 的核心抽象：它代表一个构建产物，也承载这个产物的源码、编译特性、宏、include path、链接库和安装规则。后续所有配置都挂在这个 target 上，而不是写到全局变量里。这样未来新增 `task_library`、`task_tests` 或 `task_cli` 时，每个 target 都能有自己的边界。

`target_compile_features(cmake_quickstart PRIVATE cxx_std_23)` 表示只有这个可执行文件需要 C++23。它解决的是编译器差异和标准声明问题：CMake 会按当前 generator 与编译器组合选择合适的编译参数，而不是让你手写 `-std=c++23` 或 MSVC 对应选项。`PRIVATE` 表示这个要求不向下游传播；当前 target 没有下游，所以这是最清晰的作用域。

`target_compile_definitions(cmake_quickstart PRIVATE CMAKE_QUICKSTART_VERSION="${PROJECT_VERSION}")` 展示构建配置如何进入源码。`src/main.cpp` 中的 `#ifndef CMAKE_QUICKSTART_VERSION` 是一个对照实验：如果 CMake 没有提供宏，程序会输出 `dev`；现在 target 定义了宏，程序会输出 `1.0.0`。这说明 CMake 管的不只是“把文件编译起来”，它还管理编译器看到的宏和条件编译信息。

`src/main.cpp` 使用 `std::vector<Task>` 输出 `configure`、`generate`、`build` 三个状态。它没有依赖任何第三方库，目的是把注意力放在 target 模型上，而不是被包管理和链接细节分散。以后如果把任务逻辑拆到 `src/tasks.cpp` 与 `include/cmake_quickstart/tasks.h`，就可以新增一个库 target，再用 `target_include_directories` 和 `target_link_libraries` 练习依赖传播。

## 设计思想拆解

| 痛点 | CMake 解法 | 本案例位置 |
| --- | --- | --- |
| 不同平台编译命令不同 | 用 generator 生成 Ninja、Makefile、Visual Studio 或 Xcode 工程 | `cmake -S . -B build` |
| 源码目录被构建产物污染 | out-of-source build，把产物放入 `build/` | `-S . -B build` |
| 编译标准在命令行散落 | 在 target 上声明 compile feature | `target_compile_features(... cxx_std_23)` |
| 宏和编译选项污染全局 | 在 target 上声明 private definition | `target_compile_definitions(... PRIVATE ...)` |
| 未来拆库后依赖边界混乱 | 用 target 和 `PRIVATE/PUBLIC/INTERFACE` 表达传播规则 | 当前使用 `PRIVATE`，延伸练习可拆库 |
| 测试无法统一接入构建 | 用 CTest 注册测试并由 CI 运行 | 延伸练习中的 `enable_testing()` |
| 下游项目难以复用库 | 用 `install()` 和 package config 暴露 target | 真实库项目的下一步 |

理解这张表后，再看更大的 CMake 项目就不会只盯着命令名。你应该优先寻找 target、target 之间的链接关系、哪些属性会传播、哪些只属于当前实现。

## 延伸练习

- 新增一个 `src/tasks.cpp` 和 `include/cmake_quickstart/tasks.h`，把任务列表逻辑拆成库 target。
- 加入 `enable_testing()` 和 `add_test()`，用 CTest 运行当前程序。
- 添加 `CMakePresets.json`，为 Debug 和 Release 提供团队共享的配置入口。
- 增加 `install(TARGETS ...)`，观察可执行文件如何安装到统一目录。
- 尝试用 `cmake -G Ninja -S . -B build-ninja` 和 Xcode/Visual Studio generator 生成不同后端，比较源码不变时构建文件如何变化。

## 验收

- 能说明 `cmake -S . -B build`、`cmake --build build`、运行程序分别处于哪个阶段。
- 能指出 `target_compile_features` 为什么比全局修改 `CMAKE_CXX_FLAGS` 更适合教学和团队工程。
- 能修改版本号或任务列表，重新构建并观察输出变化。
