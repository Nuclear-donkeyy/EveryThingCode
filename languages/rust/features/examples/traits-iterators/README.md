# traits-iterators

## 目标

理解 trait 如何描述一组能力，泛型函数如何基于能力工作，而不是依赖具体类型。例子同时使用迭代器链完成筛选、映射和聚合，展示 Rust 常见的集合处理风格。

## 运行

```bash
rustc main.rs -o /tmp/rust-feature-example && /tmp/rust-feature-example
```

## 观察点

- `Scored` trait 只要求类型提供 `name` 和 `score`，默认方法 `summary` 可以复用这些能力。
- `best_item<T: Scored>` 对任何实现了 trait 的类型可用，编译器会为具体类型生成代码。
- 迭代器链没有提前构造中间集合，只有在 `sum`、`collect`、`max_by_key` 等消费操作处执行。
- 把 `Task` 增加字段不会影响通用函数，只要 trait 合约仍然成立。
