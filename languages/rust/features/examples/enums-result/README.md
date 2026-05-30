# enums-result

## 目标

这个例子对应 Rust 的代数数据类型思想：用 `enum` 描述有限状态，用 `Option<T>` 表达可能缺失，用 `Result<T, E>` 表达可恢复失败。目标是理解 Rust 为什么把状态和错误放进类型，而不是依赖异常、`null`、魔法数字或全局错误码。

示例把一段输入文本解释为负载值，再分类成 `Ready`、`Waiting` 或 `Blocked`。空字符串代表没有输入，因此返回 `None`；无法解析成数字或负载过高时，不是让程序崩溃，而是形成明确的阻塞状态。学习者应该关注：每一种业务状态都在类型定义中出现，每个调用方都必须面对这些分支。

## 特性说明

`enum Readiness` 的每个变体可以携带不同数据：`Ready { load: u32 }` 记录负载，`Waiting(&'static str)` 记录等待原因，`Blocked { code, reason }` 记录错误码和原因。这比单独使用整数状态码更清晰，因为数据和状态绑定在一起，不能把“等待原因”误塞给“就绪状态”。

`parse_load` 返回 `Result<u32, String>`。成功时是 `Ok(load)`，失败时是 `Err(message)`，调用方不能假装解析一定成功。`classify` 返回 `Option<Readiness>`，因为空输入不是失败，只是“没有值”。最后 `match classify(raw)` 明确区分 `Some(state)` 和 `None`，`describe(state)` 再穷尽匹配 `Readiness` 的所有变体。

## 设计取舍

如果不用 `Result`，解析失败常会退化成两种写法：一是抛异常，调用方可能从函数签名看不出失败路径；二是返回特殊值，例如 `0` 或 `-1`，业务值和错误值容易混在一起。Rust 选择让失败成为返回类型的一部分，使调用者必须处理或显式传播。

如果不用 `enum`，复杂状态通常会分散成多个布尔字段、字符串状态码和可选字段组合。例如 `is_ready`、`is_blocked`、`reason`、`code` 可能形成互相矛盾的对象。`enum` 的取舍是：状态集合更封闭，新增状态需要更新匹配代码；代价是初期要多写分支，收益是业务不变量更容易维护。

## 运行

```bash
rustc main.rs -o /tmp/rust-feature-example && /tmp/rust-feature-example
```

## 观察点

- `parse_load` 的返回类型是 `Result<u32, String>`，调用者必须处理成功和失败。
- `classify` 返回 `Option<Readiness>`，空输入会得到 `None`。
- `Readiness` 的每个变体携带不同信息，`match` 让这些分支保持穷尽。
- 新增一个状态变体后，编译器会提醒所有未更新的 `match`。
- 运行输出中 `"42"` 是 ready，`"0"` 是 waiting，`"120"` 和 `"abc"` 都是 blocked，但原因不同，说明同一个 enum 可以表达业务失败和输入失败。
- 空字符串输出 `no value`，验证 `Option` 表达的是缺失，而不是错误。

## 延伸练习

- 给 `Readiness` 增加 `Paused { until: &'static str }`，观察 `describe` 的 `match` 是否需要新增分支。
- 把 `parse_load` 的错误类型从 `String` 改成自定义 `enum ParseLoadError`，区分空白、非数字、超出范围。
- 在 `classify` 中保留 `parse_load` 的错误文本，而不是把所有解析错误都映射为固定原因。
- 把 `describe` 改成返回 `&'static str` 和详细结构体两种版本，比较信息损失和调用便利性。
