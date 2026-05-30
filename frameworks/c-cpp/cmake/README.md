# CMake

CMake 是 C/C++ 项目事实上的跨平台构建描述工具。它本身不直接编译代码，而是读取 `CMakeLists.txt`，生成 Ninja、Unix Makefiles、Visual Studio、Xcode 等后端能够执行的构建图。现代 CMake 的学习重点不是背命令，而是用 target 表达工程边界。

## 核心定位

CMake 解决的是“如何稳定、可移植地构建 C/C++ 工程”：源码目录在哪里、要生成哪些库和可执行文件、每个目标需要什么 C++ 标准、暴露哪些头文件、链接哪些库、安装到哪里、测试如何运行。它不负责包仓库治理、不替代编译器、不保证 ABI 兼容，也不自动替你设计模块边界。

在本仓库中，CMake 作为 C/C++ 学习路径的第一站。只要你能看懂一个现代 `CMakeLists.txt`，后续理解 Qt、Boost、GoogleTest、fmt、OpenSSL、gRPC、Conan 和 vcpkg 都会轻松很多。

## 解决的问题

C/C++ 项目的第一个难点不是语法，而是“同一份源码怎样在不同机器上被正确编译、链接、测试和交付”。如果只靠手写编译命令，项目很快会被几类问题拖住。

第一类是编译器和平台差异。Clang、GCC、MSVC 的命令行参数、默认标准、警告开关、运行时库和输出目录都不完全一样。Linux 常用 Make 或 Ninja，Windows 团队可能需要 Visual Studio 工程，macOS 团队可能需要 Xcode 工程。CMake 把这些差异收敛为生成器模型：你描述“要构建什么 target、需要什么特性”，再由 `cmake -G Ninja`、Visual Studio、Xcode 等 generator 生成对应平台的构建文件。

第二类是 include path、link path 和依赖顺序。C/C++ 的头文件搜索路径、库搜索路径、链接顺序和编译宏经常相互影响。旧式工程会把 `-I`、`-L`、`-D`、`-l` 散落在全局变量里，一旦新增库或测试 target，就容易出现“在我机器能编译，在 CI 上找不到头文件”或“编译过了但链接失败”。现代 CMake 用 target 模型把需求挂到具体产物上，再通过 `PRIVATE`、`PUBLIC`、`INTERFACE` 明确哪些需求只属于自己，哪些要传播给下游。

第三类是构建目录和缓存污染。直接在源码目录里生成对象文件、Makefile、IDE 临时文件和测试产物，会让仓库变脏，也会让 Debug/Release、不同编译器、不同平台互相干扰。CMake 的 out-of-source build 用 `cmake -S . -B build` 把源码树和构建树分开，同一个源码目录可以同时拥有 `build-debug/`、`build-release/`、`build-clang/` 等多个构建结果。

第四类是安装、测试和 IDE 集成。真实项目不只是生成一个可执行文件，还要运行测试、安装头文件和库、让下游 `find_package` 找到自己、让 IDE 正确展示 include path 和编译宏。CMake 提供 `CTest`、`install()`、package config、compile commands、Visual Studio/Xcode generator 等机制，把构建系统从“能在命令行跑”推进到“能被团队、CI、IDE 和下游项目稳定消费”。

## 设计思想

现代 CMake 的核心思想是 target-first，也就是先把工程看成一张 target 依赖图。可执行文件是 target，静态库和动态库是 target，第三方包通过 `find_package` 得到的 imported library 也是 target。你不再从“这一整棵目录要加哪些全局参数”出发，而是问“这个 target 要编译哪些源码、需要什么 C++ 标准、暴露哪些头文件、链接哪些库”。本仓库 quickstart 中的 `add_executable(cmake_quickstart src/main.cpp)` 就是在创建这张图里的第一个节点。

target-first 解决的是全局配置失控问题。旧式写法喜欢全局设置 `include_directories()`、`add_definitions()` 和 `CMAKE_CXX_FLAGS`，这会让依赖关系散落在目录级作用域里。现代写法把需求挂到具体 target 上：`target_compile_features(cmake_quickstart PRIVATE cxx_std_23)` 表示只有这个可执行文件需要 C++23；`target_compile_definitions(cmake_quickstart PRIVATE CMAKE_QUICKSTART_VERSION=...)` 表示版本宏只传给这个可执行文件，不污染未来可能新增的库或测试 target。

另一个关键思想是 usage requirements，也就是依赖传播规则。如果一个库的公共头文件需要某个 include path，那么它应该以 `PUBLIC` 暴露；如果只在库实现内部使用，就用 `PRIVATE`；如果当前 target 不用但下游必须用，就用 `INTERFACE`。这三个词是理解 CMake 工程可维护性的入口。它们解决的是“库 A 能编译，但依赖 A 的库 B 拿不到正确编译条件”的问题。

CMake 还强调 properties 和 generator 的分工。`CMakeLists.txt` 描述 target 的属性，例如标准、宏、源码、include path、链接库和安装规则；generator 负责把这些属性翻译成 Ninja、Makefile、Visual Studio 或 Xcode 能执行的文件。这样同一个项目描述可以服务多种平台，也让 IDE 能从构建系统中读取真实的编译参数。

最后是 out-of-source build、CTest 和 package config。out-of-source build 让源码目录保持干净；CTest 让测试成为构建图的一部分；`install()` 与 package config 让项目能被别的 CMake 项目通过 `find_package` 消费。它们共同解决的是“本地能跑”到“团队可维护、CI 可验证、下游可复用”的距离。

## 架构模型

一个典型 CMake 项目包含三层：顶层 `CMakeLists.txt` 描述项目元信息和全局策略；一个或多个 target 描述真正的产物；源码目录承载 C++ 文件。大型项目会继续拆分为 `src/`、`include/`、`tests/`、`cmake/`、`examples/`，但核心仍然是 target 关系图。

本案例故意只保留一个可执行 target，让读者先看清最短路径：

- `cmake_minimum_required` 固定 CMake 语义下限，避免不同机器解释规则不一致。
- `project` 声明项目名称、版本和语言。
- `add_executable` 创建可执行 target。
- `target_compile_features` 要求 C++23。
- `target_compile_definitions` 把项目版本写入编译期宏，展示 target 级配置。

`src/main.cpp` 对应展示了构建信息怎样进入程序：如果 `target_compile_definitions` 正常生效，程序会输出 `project version: 1.0.0`；如果移除这条配置，源码中的 fallback 宏会让版本变成 `dev`。这比单纯讲概念更直观：CMake 不是“额外的脚本层”，它实际决定了编译器看到的语言标准、宏、头文件和链接依赖。

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

- [core-ideas](examples/core-ideas/)：把上一节“解决的问题”和“设计思想”映射到 quickstart 的关键代码片段。
- [quickstart](examples/quickstart/)：C++23 命令行程序，演示现代 CMake target 模型和 out-of-source build。

## 版本来源

- 版本基线：latest stable，CMake 无官方 LTS 概念。
- 策略：使用官方当前稳定版；实际项目中通过 `cmake_minimum_required` 和 CI 镜像固定可接受下限。
- 官方来源：https://cmake.org/documentation/
- 校验日期：2026-05-30
