# traits-iterators

## 目标

这个例子对应 Rust 的 trait、泛型和迭代器思想。目标是理解 trait 如何描述“类型具备什么能力”，泛型函数如何依赖能力而不是依赖具体结构体，以及迭代器如何把集合处理拆成可组合的步骤。示例中的 `Task` 实现 `Scored`，于是可以被通用函数 `best_item<T: Scored>` 处理，也能在迭代器链中筛选、转换和汇总。

学完后应该能看懂 Rust 常见的 API 形状：函数参数写成 `T: Trait` 是在约束能力，`.iter().filter(...).map(...).collect()` 是延迟组合集合操作。它们解决的是真实工程里的复用问题：评分规则、排序、过滤、报表生成经常跨类型共享，但又不希望把所有数据都塞进同一个基类。

## 特性说明

`trait Scored` 要求实现者提供 `name` 和 `score`，并提供一个默认方法 `summary`。默认方法可以复用必需方法，因此每个实现类型只要说明自己如何给出名字和分数，就自动拥有摘要输出。`impl Scored for Task` 把 `Task` 的字段映射成这组能力。

`best_item<T: Scored>(items: &[T]) -> Option<&T>` 是泛型函数。它不关心 `T` 是 `Task`、`Bug` 还是 `Experiment`，只关心 `T` 能被评分。返回 `Option<&T>` 是因为空切片没有最佳项；返回引用则避免复制整个元素。迭代器链里，`filter` 选择高分任务，`map` 转成摘要文本，`collect` 才真正收集成 `Vec<String>`。这展示了 Rust 让数据转换保持显式、组合式、类型安全的风格。

## 设计取舍

如果不用 trait，复用逻辑常会退化成复制粘贴：为每个类型写一套 `best_task`、`best_bug`、`best_experiment`。另一种退化是把所有数据强行统一成宽泛结构，导致字段可选、含义模糊。trait 的取舍是把“共享行为”抽出来，而让每个类型保留自己的数据布局。

Rust 的泛型默认使用静态分发，编译器会为实际类型生成代码，通常没有虚函数表查找的运行时成本。这也是“零成本抽象”的一部分：源代码可读性提高，但机器码不必为每次调用支付动态分发成本。代价是泛型边界要写清楚，过度泛型会让错误信息变长；需要异构集合或插件边界时，可以改用 `dyn Trait` 做动态分发。

## 运行

```bash
rustc main.rs -o /tmp/rust-feature-example && /tmp/rust-feature-example
```

## 观察点

- `Scored` trait 只要求类型提供 `name` 和 `score`，默认方法 `summary` 可以复用这些能力。
- `best_item<T: Scored>` 对任何实现了 trait 的类型可用，编译器会为具体类型生成代码。
- 迭代器链没有提前构造中间集合，只有在 `sum`、`collect`、`max_by_key` 等消费操作处执行。
- 把 `Task` 增加字段不会影响通用函数，只要 trait 合约仍然成立。
- 输出中只打印分数达到阈值的任务摘要，然后打印最佳任务，说明筛选和求最大值都通过同一套 `score` 能力完成。
- `best_item` 返回 `Option`，可以把 `tasks` 改成空数组观察 `if let Some(best)` 不会执行，空集合不会造成崩溃。

## 延伸练习

- 新增 `struct Incident` 并实现 `Scored`，把它传给 `best_item`，验证泛型函数不依赖 `Task`。
- 把 `visible` 的类型注解去掉，观察编译器能否从 `collect` 的使用位置推断类型。
- 增加一个 `priority_label` 默认方法，根据 `score` 返回 `high`、`medium` 或 `low`。
- 尝试创建 `Vec<Box<dyn Scored>>`，比较动态分发适合异构集合，但需要处理所有权和装箱。
