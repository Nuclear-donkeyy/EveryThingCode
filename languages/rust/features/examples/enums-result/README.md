# enums-result

## 目标

用 `enum` 表达业务状态，用 `Result` 表达解析可能失败，用 `Option` 表达可能没有可用值。这个例子强调：状态、缺失和失败都应该被调用方看见，而不是藏在异常或特殊数字里。

## 运行

```bash
rustc main.rs -o /tmp/rust-feature-example && /tmp/rust-feature-example
```

## 观察点

- `parse_load` 的返回类型是 `Result<u32, String>`，调用者必须处理成功和失败。
- `classify` 返回 `Option<Readiness>`，空输入会得到 `None`。
- `Readiness` 的每个变体携带不同信息，`match` 让这些分支保持穷尽。
- 新增一个状态变体后，编译器会提醒所有未更新的 `match`。
