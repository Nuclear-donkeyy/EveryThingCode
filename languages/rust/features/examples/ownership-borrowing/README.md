# ownership-borrowing

## 目标

理解 Rust 如何用所有权决定资源释放，用不可变借用读取数据，用可变借用在独占访问时修改数据。例子还展示字符串切片返回值的生命周期直觉：返回的 `&str` 指向输入字符串，因此不能比输入活得更久。

## 运行

```bash
rustc main.rs -o /tmp/rust-feature-example && /tmp/rust-feature-example
```

## 观察点

- `consume_report(report)` 会移动 `String` 的所有权，调用后原变量不能再使用。
- `list_items(&inventory)` 只读取库存，不取得所有权。
- `add_item(&mut inventory, ...)` 需要独占的可变借用，因此不能和其他活跃借用同时存在。
- `first_word` 返回的是输入字符串的一段视图，不会分配新的 `String`。
