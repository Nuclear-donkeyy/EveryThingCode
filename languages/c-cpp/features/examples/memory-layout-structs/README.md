# 结构体内存布局

## 目标

这个例子对应 C / C++ 的对象布局、对齐和连续存储思想。目标是理解 `struct` 字段顺序并不只是代码风格，它会影响 `sizeof`、字段偏移和数组中相邻对象的距离。示例比较两个字段相同但顺序不同的头部结构体，并用 `std::vector` 与 `std::span` 展示连续存储带来的遍历方式。

这个特性解决的真实工程问题是二进制边界和缓存效率。网络包头、文件格式、共享内存、硬件寄存器映射和高性能数组处理都需要知道数据在内存中怎样排列。C / C++ 允许程序员观察和约束布局，是系统编程能力的一部分；同时也意味着学习者必须理解填充字节、对齐和 ABI 约定。

## 特性说明

`PacketHeader` 包含 `std::uint16_t`、`std::uint32_t` 和 `std::uint8_t`。为了让 `std::uint32_t` 放在满足对齐要求的位置，编译器可能在字段之间插入 padding。`offsetof(PacketHeader, length)` 可以显示 `length` 并不一定紧跟在 `type` 后面。`PackedLikeHeader` 把较大的 `length` 放在前面，通常能减少中间填充，但最终结果仍以当前平台 ABI 为准。

`std::vector<PackedLikeHeader>` 保证元素连续存储，`std::span` 则提供一个不拥有数据的连续视图。这个组合常用于把“拥有内存的容器”和“只需要读写一段连续数据的函数参数”分开。布局知识和 span 视图结合起来，可以写出既清楚又接近底层内存模型的接口。

## 设计取舍

如果完全忽略布局，代码可能在单机测试中正常，却在写入文件、发送网络数据或跨语言共享结构体时出错。直接把结构体内存 `reinterpret_cast` 成字节流也有风险，因为 padding 字节、大小端、ABI 和编译器选项都会影响结果。真实协议通常会显式按字节编码字段，而不是把内存布局当作稳定格式。

另一方面，过度追求紧凑布局也可能伤害性能。某些 CPU 访问未对齐数据会变慢，甚至在特定平台上触发错误；手动 `packed` 属性虽然能减少大小，但会带来可移植性和访问成本问题。这个例子不使用非标准 packed 属性，而是用标准库可观察的 `sizeof`、`alignof` 和 `offsetof` 建立直觉。

## 运行

```bash
c++ -std=c++23 main.cpp -o /tmp/cpp-feature-example && /tmp/cpp-feature-example
```

## 观察点

- 两个结构体字段类型相同，但 `sizeof` 和字段偏移可能不同，说明字段顺序会影响 padding。
- `alignof` 显示对象需要满足的对齐要求，它解释了为什么编译器会插入空洞。
- `std::vector` 中的结构体元素连续排列，`std::span` 只是借用这段连续内存，不负责释放。
- 输出中的 `contiguous lengths` 验证了 span 可以像轻量数组视图一样遍历已有数据。

## 延伸练习

- 调整字段顺序，预测并验证 `sizeof` 和 `offsetof` 的变化。
- 增加一个 `std::uint64_t timestamp` 字段，观察更大对齐需求如何改变结构体大小。
- 写一个函数 `print_lengths(std::span<const PackedLikeHeader>)`，体会 span 如何表达“不拥有，只借用”。
- 尝试把结构体逐字段编码到 `std::vector<std::byte>`，比较显式编码和直接写内存布局的可移植性。
