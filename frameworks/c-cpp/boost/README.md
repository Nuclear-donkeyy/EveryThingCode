# Boost

Boost 是 C++ 生态中最重要的高质量库集合之一。它既是生产可用的工具箱，也是观察 C++ 标准库演进的窗口：许多后来进入标准库的设施都曾在 Boost 中长期验证设计，例如 smart pointers、filesystem、regex、thread、optional、variant、any、asio 等。

## 核心定位

Boost 解决的是标准库之外的大量通用需求：字符串算法、容器、日期时间、异步 I/O、序列化、图算法、数学、元编程、日志、测试等。它不提供统一应用框架，也不强制项目结构；更像一个经过社区审查的库集合。你可以只用一个 header-only 组件，也可以引入需要编译链接的复杂库。

本仓库把 Boost 放在 CMake 之后学习，是因为真实项目中通常需要先理解构建和依赖，再判断一个 Boost 组件是 header-only、需要链接库，还是需要额外编译选项。

## 设计思想

Boost 的重要思想是“泛型、组合、零成本倾向和标准化前哨”。许多 Boost 库偏向模板和 header-only，让类型在编译期组合，运行时只留下必要成本。它也非常重视和标准库风格兼容，例如使用迭代器、range、allocator、异常、RAII 和值语义。

另一个思想是实验与沉淀。Boost 库通常需要经过评审，文档、接口、可移植性和测试都会被讨论。即使某个库最终没有进入标准库，它也能代表一类成熟问题的 C++ 解法。学习 Boost 不是为了记住每个库，而是学习如何读高质量 C++ API：接口如何表达所有权、错误如何传播、模板参数如何约束、默认值如何兼顾易用和性能。

## 架构模型

Boost 不是一个单体框架，而是许多库的集合。使用方式大致分两类：header-only 库只需要 include 头文件；需要编译的库还要在构建系统中链接二进制库。CMake 中通常用 `find_package(Boost REQUIRED)` 或具体组件查找，再把 `Boost::headers` 或组件 target 链接到项目 target。

本案例选择 header-only 能力，降低运行门槛：`boost::algorithm` 做字符串清洗和切分，`boost::container::small_vector` 展示小对象优化容器，`boost::lexical_cast` 展示字符串到数字的转换与异常处理。

## 请求/执行生命周期

Boost 库本身没有统一的请求生命周期。它的执行模型取决于你使用的组件：Algorithm 是普通函数调用，Asio 是事件循环和异步回调，Spirit 是 parser 组合，Graph 是算法遍历，Test 是测试 runner。

本 quickstart 的执行生命周期很简单：程序读取一段逗号分隔文本，调用 Boost 字符串算法拆分并清洗，使用 lexical_cast 转成整数，放入 small_vector，再计算统计结果并输出。重点是观察库函数如何组合进普通 C++ 程序，而不是把 Boost 当成一个侵入式框架。

## 工程结构

本仓库案例结构如下：

```text
frameworks/c-cpp/boost/examples/quickstart/
├── CMakeLists.txt
├── README.md
└── src/
    └── main.cpp
```

真实项目中，建议按业务边界拆分自己的库 target，然后在需要的 target 上链接 Boost。不要在全局 CMake 配置里盲目加入所有 Boost 头文件和库，也不要因为用了一个小组件就把项目设计成“Boost 风格”。第三方库应服务于领域模型，而不是吞掉领域模型。

## 配置方式

Boost 的配置取决于安装方式。系统包管理器、源码安装、Conan、vcpkg 都可以提供 Boost。CMake 中可以先从最简单的 `find_package(Boost REQUIRED)` 开始；需要具体编译库时，再写成 `find_package(Boost REQUIRED COMPONENTS filesystem program_options)` 并链接对应 target。

本案例只需要 Boost headers。如果使用 vcpkg，常见命令会带 `-DCMAKE_TOOLCHAIN_FILE=<vcpkg>/scripts/buildsystems/vcpkg.cmake`；如果使用 Conan，则通常通过 profile 和生成器把依赖写入构建目录。团队项目必须锁定版本，否则不同开发者机器上的 Boost 版本差异可能导致行为或编译错误不同。

## 模块与依赖管理

Boost 的模块粒度很细，同一个项目可以只依赖其中几个库。header-only 库对链接阶段影响小，但会增加编译期模板实例化成本；二进制库则要关注 ABI、编译器版本、运行时库、静态/动态链接和平台包命名差异。

依赖管理上，推荐让 CMake target 表达 Boost 依赖。例如某个内部库的公共头文件暴露了 Boost 类型，就把 Boost 作为 `PUBLIC` 依赖；如果只是 `.cpp` 内部使用，则用 `PRIVATE`。这样下游 target 不需要猜测 include path 和链接参数。

## 数据访问

Boost 本身包含不少可用于数据处理的库，例如 JSON、Serialization、Beast、Asio、Interprocess、Iostreams。选择时要区分“格式处理”“网络传输”“持久化存储”和“进程间通信”。不要把数据访问全部塞进 main 函数，而应封装成清晰的解析、传输、存储模块。

本案例的数据来自一段字符串，目的是突出算法和容器组合。后续可以把输入替换为文件、HTTP 响应或命令行参数，再分别引入 Boost.Program_options、Boost.Beast 或标准库文件 I/O。

## 测试方式

Boost 自带 Boost.Test，也可以和 GoogleTest、Catch2、doctest 混用。测试 Boost 相关代码时，重点不是测试 Boost 自己，而是测试你对库的组合方式：异常是否处理，边界输入是否覆盖，容器容量假设是否合理，异步操作是否能可靠收尾。

本 quickstart 可以先通过运行程序观察输出；进阶练习可以加入 CTest 和一个测试 target，把字符串解析逻辑从 `main` 拆出来做单元测试。

## 部署方式

header-only Boost 组件部署成本较低，最终二进制不需要额外 Boost 动态库。需要编译链接的 Boost 组件则要处理动态库随程序分发、静态链接许可、目标平台 ABI 和包管理器路径。容器和 CI 中，最好在镜像或缓存中固定 Boost 版本。

对于企业项目，建议把 Boost 获取方式写进构建文档：系统包版本、vcpkg baseline、Conan lockfile 或源码 vendor 策略至少选择一种，避免“我机器能编译”成为主要依赖管理方法。

## 适用场景与取舍

Boost 适合需要成熟、跨平台、泛型 C++ 能力的项目，尤其是标准库还没有覆盖或实现质量参差的领域。它的优势是范围广、质量高、社区沉淀久；代价是部分库模板复杂、编译时间长、错误信息难读，版本和 ABI 管理也需要纪律。

如果标准库已经足够，优先用标准库可以降低依赖成本；如果只需要格式化或日志，fmt/spdlog 可能比引入 Boost 更直接；如果是大型异步网络服务，Boost.Asio/Beast 很强，但也要和 gRPC、libuv、Poco、语言级协程方案一起比较。

## 案例索引

- [quickstart](examples/quickstart/)：Boost header-only 小程序，演示字符串算法、small_vector、lexical_cast 和 CMake 依赖查找。

## 版本来源

- 版本基线：latest stable，Boost 无官方 LTS 概念。
- 策略：使用官方当前稳定版；真实项目通过包管理器 lockfile、vcpkg baseline 或 CI 镜像锁定具体版本。
- 官方来源：https://www.boost.org/
- 校验日期：2026-05-30
