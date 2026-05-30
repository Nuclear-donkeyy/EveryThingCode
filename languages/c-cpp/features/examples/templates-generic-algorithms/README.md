# 模板与泛型算法

## 目标

这个例子展示一个模板算法如何通过迭代器和投影函数处理不同容器。它不关心数据来自 `std::vector` 还是 `std::array`，只要求元素能被投影成可累加的数值。

## 运行

```bash
c++ -std=c++23 main.cpp -o /tmp/cpp-feature-example && /tmp/cpp-feature-example
```

## 观察点

- `summarize` 的算法主体只写一次，调用点决定元素类型和投影方式。
- 模板在编译期为具体类型生成代码，通常不需要运行时虚函数分派。
- 约束写在 `requires` 中，错误会尽量停在“不满足接口”的位置。
