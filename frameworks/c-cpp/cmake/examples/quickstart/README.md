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

`CMakeLists.txt` 的第一行声明最低 CMake 版本。项目行设置 `VERSION 1.0.0`，后面通过 `${PROJECT_VERSION}` 传给编译宏 `CMAKE_QUICKSTART_VERSION`。这展示了构建元数据如何进入 C++ 程序。

`add_executable(cmake_quickstart src/main.cpp)` 创建 target。后续所有配置都挂在这个 target 上，而不是写到全局变量里。`target_compile_features(cmake_quickstart PRIVATE cxx_std_23)` 表示只有这个可执行文件需要 C++23；如果以后新增库 target，可以分别声明各自需求。

`src/main.cpp` 使用标准库容器和格式化输出组织任务列表。它没有依赖任何第三方库，目的是把注意力放在 CMake target 模型上，而不是被包管理和链接细节分散。

## 延伸练习

- 新增一个 `src/tasks.cpp` 和 `include/cmake_quickstart/tasks.h`，把任务列表逻辑拆成库 target。
- 加入 `enable_testing()` 和 `add_test()`，用 CTest 运行当前程序。
- 添加 `CMakePresets.json`，为 Debug 和 Release 提供团队共享的配置入口。

## 验收

- 能说明 `cmake -S . -B build`、`cmake --build build`、运行程序分别处于哪个阶段。
- 能指出 `target_compile_features` 为什么比全局修改 `CMAKE_CXX_FLAGS` 更适合教学和团队工程。
- 能修改版本号或任务列表，重新构建并观察输出变化。
