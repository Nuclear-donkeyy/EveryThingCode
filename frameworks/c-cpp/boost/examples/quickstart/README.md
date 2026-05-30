# Boost quickstart

## 目标

这个案例用一个 header-only 示例展示 Boost 如何作为“高质量库集合”嵌入普通 C++ 项目。程序读取一段文本，使用 Boost 字符串算法拆分并清洗，再用 `boost::lexical_cast` 转成数字，最后放入 `boost::container::small_vector` 做统计。

学完后，你应该能判断一个 Boost 组件是否需要链接二进制库，能在 CMake 中查找 Boost headers，并能解释为什么 Boost 经常被称为标准库的前哨。

## 学习重点

- `find_package(Boost REQUIRED)` 让 CMake 查找已安装的 Boost。
- `Boost::headers` 表示只使用 header-only 能力，不需要链接具体 Boost 二进制库。
- `boost::algorithm::split`、`trim`、`token_compress_on` 展示泛型字符串算法。
- `boost::lexical_cast<int>` 展示类型转换与异常处理。
- `boost::container::small_vector` 展示小规模数据的栈内优化思路。

## 工程结构

```text
.
├── CMakeLists.txt
├── README.md
└── src/
    └── main.cpp
```

当前案例只有一个可执行 target。真实项目中，可以把解析逻辑拆成库 target，并让测试 target 链接该库；如果公共头文件暴露 Boost 类型，要把 Boost 依赖设置为 `PUBLIC`。

## 这个案例解决什么问题

这个小程序模拟的是 C++ 项目中非常常见的一段“边界层代码”：外部输入是一段松散文本，里面混着空白、合法数字和非法片段；业务真正需要的是一组整数以及统计结果。只用标准库也能完成，但你通常要手写切分循环、空白清理、转换错误处理和小规模数据存储策略。代码量不大，却容易在多个项目里重复出现，边界条件也容易不一致。

Boost 在这里解决了三个问题。第一，Boost.Algorithm 把字符串切分和清洗变成可读的泛型算法，避免把“怎么扫描逗号”和“业务上要处理数字”混在一起。第二，Boost.LexicalCast 把字符串到目标类型的转换写成 `boost::lexical_cast<int>`，让目标类型、失败语义和异常处理集中在一个地方。第三，Boost.Container 的 `small_vector<int, 4>` 表达了“小集合优先不分配堆内存，超出后再扩容”的性能假设，展示 Boost 如何补足标准容器之外的取舍空间。

这个案例没有展示 Boost.Asio、Beast、Program_options、Filesystem 等大型组件，但它们解决的是同一类工程问题：把网络 I/O、HTTP/WebSocket、命令行参数、路径和文件差异这些非业务复杂度沉淀为可复用库。理解本例的关键，是看到 Boost 如何以低侵入方式进入现有 C++ 工程，而不是把整个项目改造成某个框架。

## 运行前提

- Boost latest stable，至少安装 headers。
- CMake latest stable。
- 支持 C++23 的编译器。
- 如果通过 vcpkg 或 Conan 安装 Boost，需要为 CMake 传入对应 toolchain 或生成文件。

## 运行

```bash
cmake -S . -B build
cmake --build build
./build/boost_quickstart
```

如果 CMake 找不到 Boost，可以显式传入安装路径，例如：

```bash
cmake -S . -B build -DBOOST_ROOT=/path/to/boost
```

## 预期输出

程序会打印清洗后的数字和汇总值：

```text
skip non-integer token: invalid
Boost utility demo
values: 42 7 13
sum: 62
average: 20.6667
```

如果输入中加入无法转换为整数的片段，程序会捕获异常并输出跳过信息。

## 代码讲解

`CMakeLists.txt` 使用 `find_package(Boost REQUIRED)` 查找 Boost，并把 `Boost::headers` 链接到 `boost_quickstart`。这里的“链接”更多是在 CMake target 层面传播 include path；因为案例只使用 header-only 组件，不需要额外 Boost 动态库。

如果改用需要编译链接的库，例如 Boost.Program_options 或 Boost.Filesystem，CMake 通常会变成 `find_package(Boost REQUIRED COMPONENTS program_options filesystem)`，并在 `target_link_libraries` 中链接对应组件 target。这个差异很重要：Boost 不是一个单一依赖，有些能力只传播头文件，有些能力还牵涉 ABI、动态库分发、编译器版本和包管理器路径。

`main.cpp` 先用 `boost::algorithm::split` 按逗号切分字符串，再对每个 token 调用 `boost::algorithm::trim` 去掉空白。这里解决的是输入边界的可读性问题：切分和清洗被命名为算法调用，业务读者不需要从手写循环里推断逗号、空白和空 token 的处理策略。

转换阶段使用 `boost::lexical_cast<int>`，它失败时会抛出 `boost::bad_lexical_cast`。这能让输入清洗和错误处理集中在一处。示例中的 `invalid` token 不会让程序崩溃，而是被捕获并输出 `skip non-integer token`；这体现了 Boost API 常见的风格：正常路径保持简洁，失败路径用明确的异常类型交给调用方处理。

`small_vector<int, 4>` 表示前几个元素可以直接放在对象内部存储，超过容量后再退化为动态分配。这个容器适合“小数据居多、偶尔变大”的场景；它展示了 Boost 经常提供标准库之外性能取舍工具的特点。

最后，`std::accumulate` 直接作用于 `small_vector` 的迭代器，说明 Boost 容器尽量保持标准库兼容。好的第三方库不应该切断你和标准算法、范围、迭代器生态的连接；Boost 的许多组件之所以值得学习，正是因为它们把扩展能力放进了 C++ 已有的抽象体系里。

## 延伸练习

- 把输入改为命令行参数，并尝试引入 Boost.Program_options。
- 把解析函数拆出来，用 CTest 或 GoogleTest 测试空输入、非法数字和负数。
- 改用标准库实现同样功能，比较代码复杂度和错误处理方式。

## 验收

- 能说明 header-only Boost 库和需要编译链接的 Boost 库有什么区别。
- 能指出 CMake 中 `Boost::headers` 的作用。
- 能新增一个非法输入片段，观察异常处理输出并解释程序为什么没有崩溃。
