# CMake

CMake 是 C/C++ 项目事实上的跨平台构建描述工具。它本身不直接编译代码，而是读取 `CMakeLists.txt`，生成 Ninja、Unix Makefiles、Visual Studio、Xcode 等后端能够执行的构建图。现代 CMake 的学习重点不是背命令，而是用 target 表达工程边界。

## 核心定位

CMake 解决的是“如何稳定、可移植地构建 C/C++ 工程”：源码目录在哪里、要生成哪些库和可执行文件、每个目标需要什么 C++ 标准、暴露哪些头文件、链接哪些库、安装到哪里、测试如何运行。它不负责包仓库治理、不替代编译器、不保证 ABI 兼容，也不自动替你设计模块边界。

在本仓库中，CMake 作为 C/C++ 学习路径的第一站。只要你能看懂一个现代 `CMakeLists.txt`，后续理解 Qt、Boost、GoogleTest、fmt、OpenSSL、gRPC、Conan 和 vcpkg 都会轻松很多。

## 设计思想

现代 CMake 的核心思想是 target-first。旧式写法喜欢全局设置 `include_directories()`、`add_definitions()` 和 `CMAKE_CXX_FLAGS`，这会让依赖关系散落在目录级作用域里。现代写法把可执行文件、静态库、动态库都看作 target，再通过 `target_compile_features`、`target_include_directories`、`target_link_libraries` 等命令把需求挂到具体 target 上。

另一个关键思想是 usage requirements，也就是依赖传播。如果一个库的公共头文件需要某个 include path，那么它应该以 `PUBLIC` 暴露；如果只在库实现内部使用，就用 `PRIVATE`；如果当前 target 不用但下游必须用，就用 `INTERFACE`。这三个词是理解 CMake 工程可维护性的入口。

CMake 也强调 out-of-source build：源码目录保持干净，构建产物进入 `build/`。这让你可以同时保留 Debug、Release、不同编译器、不同平台的构建目录，减少“构建缓存污染源码”的问题。

## 架构模型

一个典型 CMake 项目包含三层：顶层 `CMakeLists.txt` 描述项目元信息和全局策略；一个或多个 target 描述真正的产物；源码目录承载 C++ 文件。大型项目会继续拆分为 `src/`、`include/`、`tests/`、`cmake/`、`examples/`，但核心仍然是 target 关系图。

本案例故意只保留一个可执行 target，让读者先看清最短路径：

- `cmake_minimum_required` 固定 CMake 语义下限，避免不同机器解释规则不一致。
- `project` 声明项目名称、版本和语言。
- `add_executable` 创建可执行 target。
- `target_compile_features` 要求 C++23。
- `target_compile_definitions` 把项目版本写入编译期宏，展示 target 级配置。

## 请求/执行生命周期

CMake 的一次执行可以理解为四个阶段。配置阶段执行 `cmake -S . -B build`，CMake 读取脚本、探测编译器、查找依赖并生成缓存。生成阶段把抽象构建图转成具体后端文件，例如 Ninja 或 Makefile。构建阶段执行 `cmake --build build`，后端根据依赖图调用编译器与链接器。运行阶段执行生成的程序，或者继续执行 `ctest`、`cmake --install`、打包命令。

这个生命周期解释了为什么修改 `CMakeLists.txt` 后通常要重新配置，为什么修改 `.cpp` 后只需要重新构建，也解释了为什么错误可能来自不同层：CMake 语法错误发生在配置期，头文件找不到多半发生在编译期，符号未定义通常发生在链接期。

## 工程结构

本仓库案例结构如下：

```text
frameworks/c-cpp/cmake/examples/quickstart/
├── CMakeLists.txt
├── README.md
└── src/
    └── main.cpp
```

真实项目扩展时，建议把公共头文件放入 `include/<project>/`，实现放入 `src/`，测试放入 `tests/`，第三方查找逻辑放入 `cmake/`。不要把所有依赖都写成全局变量，也不要让业务代码依赖构建目录中的临时路径。

## 配置方式

CMake 配置有三种常见来源。第一种是命令行缓存变量，例如 `-DCMAKE_BUILD_TYPE=Release`、`-DCMAKE_TOOLCHAIN_FILE=...`、`-DENABLE_TESTS=ON`。第二种是 `CMakePresets.json`，团队可以用它统一 Debug/Release、编译器、生成器和工具链。第三种是 target 命令，它们描述项目自身的编译特性、宏、头文件和链接依赖。

学习阶段优先使用命令行即可；团队项目再引入 presets 和包管理器 toolchain。要避免把机器相关路径硬编码进 `CMakeLists.txt`，这会让项目离开作者电脑后立即失效。

## 模块与依赖管理

CMake 的模块机制主要通过 target、子目录和包查找来组织。`add_subdirectory` 引入仓库内模块，`find_package` 查找系统或包管理器安装的依赖，`FetchContent` 可以在配置期拉取外部源码，Conan/vcpkg 则常通过 toolchain 文件把依赖注入 CMake。

依赖管理的关键仍然是边界：库 A 如果在公共头文件中暴露了库 B 的类型，就应该 `target_link_libraries(A PUBLIC B)`；如果只在 `.cpp` 中使用 B，就应该是 `PRIVATE`。这比“能编译过就行”更重要，因为它决定下游项目是否能正确获得 include path、编译宏和链接参数。

## 数据访问

CMake 本身不处理业务数据访问，但它负责把数据访问库正确接入工程。接 SQLite、PostgreSQL、OpenSSL、libcurl、gRPC、Protocol Buffers 或 Boost.Asio 时，通常是 `find_package` 得到 imported target，然后通过 `target_link_libraries(app PRIVATE Some::Target)` 链接。

本案例用内存 `std::vector` 生成输出，避免把数据库依赖混进构建系统第一课。等 target 模型清楚后，再接数据库或网络库会更容易定位问题是“业务代码错误”还是“构建配置错误”。

## 测试方式

CMake 可以通过 CTest 管理测试。常见做法是 `enable_testing()`，再用 `add_test(NAME ... COMMAND ...)` 注册可执行测试。真实项目会把 GoogleTest、Catch2 或 doctest 编译成测试 target，并在 CI 中运行 `ctest --test-dir build --output-on-failure`。

本 quickstart 以构建和运行可执行文件作为冒烟验证。学习者可以在延伸练习中加入 `enable_testing()`，把当前程序输出检查改造成自动测试。

## 部署方式

本地部署通常是构建后直接运行 `build/cmake_quickstart`。库项目会进一步写 `install(TARGETS ...)`、`install(FILES ...)` 和包配置文件，便于下游 `find_package`。跨平台交付时，要明确运行时依赖、动态库位置、RPATH、Debug/Release 产物和包格式。

容器化场景中，CMake 经常放在多阶段构建里：第一阶段安装编译器和依赖并构建，第二阶段只复制可执行文件和运行时库。嵌入式或交叉编译场景则重点依赖 toolchain 文件。

## 适用场景与取舍

CMake 适合跨平台 C/C++ 工程、需要 IDE 生成器支持的项目、依赖多种第三方库的项目，以及希望接入 Conan/vcpkg/CTest/CDash 的团队。它的生态非常广，但语义历史包袱也重，网上很多旧教程会混用全局变量和 target 写法。

如果项目极小，直接用一条编译命令或 Makefile 也可以；如果你追求极致可重复构建和大规模 monorepo，Bazel 可能更合适；如果你更喜欢声明式和简洁语法，Meson 也值得看。但对于主流 C/C++ 工程，CMake 仍然是必须掌握的共同语言。

## 案例索引

- [quickstart](examples/quickstart/)：C++23 命令行程序，演示现代 CMake target 模型和 out-of-source build。

## 版本来源

- 版本基线：latest stable，CMake 无官方 LTS 概念。
- 策略：使用官方当前稳定版；实际项目中通过 `cmake_minimum_required` 和 CI 镜像固定可接受下限。
- 官方来源：https://cmake.org/documentation/
- 校验日期：2026-05-30
