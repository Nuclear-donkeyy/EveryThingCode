# C/C++ 框架与工程生态

C/C++ 的“框架”常常不是一个全包式 Web 框架，而是一组分层工具：构建系统负责把源码变成可交付产物，包管理器负责获得第三方库，基础库补齐标准库之外的能力，GUI、网络、游戏和测试框架再按方向组合进项目。学习 C/C++ 生态时，最重要的是先建立工程边界：哪些事情发生在编译期，哪些事情发生在链接期，哪些事情发生在运行期。

## 常用框架清单

| 方向 | 常用选择 | 本仓库状态 | 适合先学什么 |
| --- | --- | --- | --- |
| 构建系统 | [CMake](cmake/)、Make、Ninja、Meson、Bazel | 已覆盖 CMake | target、依赖传播、构建目录、安装规则 |
| GUI/跨平台应用 | [Qt](qt/)、wxWidgets、GTKmm、Dear ImGui | 已覆盖 Qt | 对象模型、信号槽、事件循环、资源与部署 |
| 通用库集合 | [Boost](boost/)、Abseil、Folly、Poco | 已覆盖 Boost | header-only、泛型算法、标准库候选能力 |
| 包管理 | Conan、vcpkg、CPM.cmake、FetchContent | 待扩展 | 锁定版本、profile/toolchain、二进制缓存 |
| 测试 | GoogleTest、Catch2、doctest、CTest | 待扩展 | 单元测试、断言、fixture、CI 集成 |
| 格式化与日志 | fmt、spdlog、Boost.Log | 待扩展 | 类型安全格式化、结构化日志、日志级别 |
| 加密与网络 | OpenSSL、libcurl、gRPC、Boost.Asio、Poco Net | 待扩展 | 证书、TLS、异步 I/O、RPC IDL |
| 游戏与图形 | SDL、SFML、raylib、Unreal Engine、OpenGL/Vulkan 生态 | 待扩展 | 主循环、输入、资源加载、渲染管线 |
| 数据与序列化 | SQLite、PostgreSQL libpqxx、Protocol Buffers、RapidJSON、nlohmann/json | 待扩展 | RAII 封装、错误处理、schema 演进 |

本仓库第一版选择 CMake、Qt、Boost，是因为它们覆盖了 C/C++ 工程最常见的三个入口：如何构建、如何写跨平台应用、如何使用成熟库扩展标准库。

## 选择思路

如果你要做命令行工具、服务端组件、算法库或嵌入式上层模块，先把 CMake 学扎实。现代 CMake 的核心不是“写脚本”，而是声明 target 之间的关系：一个库暴露哪些头文件、需要哪些编译特性、向下游传播哪些宏和链接依赖。target 模型理解之后，接入 GoogleTest、fmt、spdlog、OpenSSL、gRPC 或 Boost 都会更清楚。

如果你要做桌面应用、工业软件、可视化工具或需要同时覆盖 Windows/macOS/Linux 的产品，Qt 通常是最稳妥的起点。Qt 不只是控件库，它提供对象模型、事件循环、信号槽、模型视图、网络、数据库、资源系统和部署工具。学习 Qt 时要先理解事件驱动，而不是急着堆界面控件。

如果你要补齐标准库没有覆盖好的能力，或者希望观察 C++ 生态如何沉淀库设计经验，Boost 是很好的阅读对象。Boost 中许多设计后来影响或进入了标准库，例如 smart pointer、filesystem、regex、asio、variant、optional 等。真实项目中不一定“一定要用 Boost”，但理解它能帮助你判断第三方库的接口质量和成本。

包管理方面，Conan 更像跨平台 C/C++ 依赖管理器，擅长 profile、构建选项和二进制包；vcpkg 更像和 CMake/Visual Studio 深度配合的库仓库。团队项目通常需要明确 toolchain 文件、锁定依赖版本、缓存二进制产物，并把这些规则写进 CI。

## 学习路线

1. 先阅读语言章节：[C/C++ 语言基础](../../languages/c-cpp/) 与语法速览，确认编译、链接、头文件、RAII、模板和未定义行为这些基础概念。
2. 阅读 [CMake](cmake/)：从一个可执行文件开始，理解 out-of-source build、target、compile features、include/link 依赖传播。
3. 阅读 [Boost](boost/)：用 header-only 示例感受泛型库、算法组合和标准库前哨思想。
4. 阅读 [Qt](qt/)：理解事件循环、QObject、信号槽和 CMake 自动 moc，再扩展到 Widgets 或 Qt Quick。
5. 第二阶段再补 Conan/vcpkg、GoogleTest/Catch2、fmt/spdlog、OpenSSL/gRPC、SDL/Unreal 等方向案例。

## 本仓库案例

- [CMake quickstart](cmake/examples/quickstart/)：最小 C++23 命令行项目，演示 `cmake_minimum_required`、`project`、`add_executable`、`target_compile_features` 与 `target_compile_definitions`。
- [Qt quickstart](qt/examples/quickstart/)：最小 Qt Core 事件驱动项目，演示 `QCoreApplication`、`QObject`、信号槽和 CMake `AUTOMOC`。
- [Boost quickstart](boost/examples/quickstart/)：最小 Boost header-only 项目，演示 `boost::algorithm`、`boost::container::small_vector`、`boost::lexical_cast` 与 CMake `find_package`。
