# ownership-borrowing

## 目标

这个例子对应 Rust 最核心的语言思想：所有权（ownership）和借用（borrowing）。目标不是记住几条孤立规则，而是看懂资源在函数之间如何流动：什么时候值被移动，什么时候只是临时查看，什么时候可以独占修改。示例里的库存列表 `Inventory` 拥有一个 `Vec<String>`；报告字符串会被 `consume_report` 接收并归档；库存可以先被 `list_items` 只读借用，再被 `add_item` 可变借用更新。

学完后应该能回答三个问题：变量是否仍然拥有数据，函数调用是否拿走了所有权，当前是否存在会阻止修改的只读借用。这个能力会直接影响真实工程中的 API 设计，例如日志归档、缓存更新、请求处理和文件句柄管理。

## 特性说明

Rust 没有垃圾回收器，也不要求程序员手写 `free`。它选择让每个值在任意时刻只有一个所有者，所有者离开作用域时资源自动释放。`String`、`Vec<T>` 这类拥有堆内存的值被传给 `consume_report(report)` 时会发生移动，函数成为新的所有者；调用点之后原来的 `report` 变量不能再使用，这避免了重复释放和悬垂指针。

借用则允许函数临时访问数据而不接管资源。`list_items(&inventory)` 接收 `&Inventory`，只能读取库存；调用结束后库存仍归 `main` 所有。`add_item(&mut inventory, "radio")` 接收 `&mut Inventory`，可以修改库存，但可变借用必须独占，不能和其他活跃借用同时存在。`first_word(&note)` 返回 `&str`，它只是 `note` 内部数据的一段视图，没有分配新字符串；这个引用的有效时间不能超过 `note`。

## 设计取舍

如果没有所有权，系统语言通常要在两种风险之间选择：靠人工释放资源，容易出现 use-after-free、double free；或者靠运行时垃圾回收，释放时机不完全由程序结构表达。Rust 的取舍是把这些约束提前交给编译器检查，初学时会多遇到编译错误，但换来的是运行时更少隐藏状态。

如果不用借用，代码常会退化成两类形态：到处 `clone`，让所有函数都拿到自己的副本，简单但浪费内存和时间；或者到处传可变共享对象，短期灵活，长期难以判断谁改了数据。Rust 用 `&T` 和 `&mut T` 把“只读共享”和“独占修改”分开，迫使 API 在签名里说明意图。这个设计不是为了禁止共享，而是让共享发生在可推理的边界内。

## 运行

```bash
rustc main.rs -o /tmp/rust-feature-example && /tmp/rust-feature-example
```

## 观察点

- `consume_report(report)` 会移动 `String` 的所有权，调用后原变量不能再使用。
- `list_items(&inventory)` 只读取库存，不取得所有权。
- `add_item(&mut inventory, ...)` 需要独占的可变借用，因此不能和其他活跃借用同时存在。
- `first_word` 返回的是输入字符串的一段视图，不会分配新的 `String`。
- 输出中先看到报告被归档，再看到两个初始库存项，最后库存数量变为 3，说明只读查看没有消耗库存，可变借用确实更新了原集合。
- 可以尝试在 `consume_report(report)` 后面添加 `println!("{report}")`，编译器会指出值已经被移动。这条错误正是所有权规则在工作。

## 延伸练习

- 把 `consume_report` 的参数从 `String` 改成 `&str`，再比较调用方是否还能继续使用 `report`。
- 在 `let word = first_word(&note);` 后面尝试修改 `note`，观察只读切片仍在使用时为什么不能同时可变借用。
- 把 `add_item` 改成返回新的 `Inventory`，比较“移动并返回”和“可变借用原地修改”的 API 风格。
- 给 `Inventory` 增加 `capacity: usize` 字段，在 `add_item` 中拒绝超过容量的写入，为后续学习 `Result` 做准备。
