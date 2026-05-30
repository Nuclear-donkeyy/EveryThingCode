# pattern-matching

## 目标

这个例子对应 Rust 的模式匹配（pattern matching）思想。目标是理解 `match` 不只是替代 `switch`，它可以同时完成结构拆解、条件判断、变量绑定和穷尽性检查。示例把文本命令解析成 `Command` enum，再用模式匹配执行不同逻辑。

真实工程中，协议消息、命令行参数、状态机事件、编译器 AST、UI 事件都很适合用 enum 加模式匹配建模。学习重点是：把输入先变成结构化数据，再按结构处理，而不是在各处散落字符串判断和下标访问。

## 特性说明

`parse_command` 使用 `parts.as_slice()` 匹配字符串切片。`["move", x, y]` 能同时确认命令形状并绑定参数；`["write", rest @ ..]` 使用剩余模式收集后续词；`_` 捕获未知命令。这里的模式描述的是数据形状，而不是布尔条件。

`handle` 再匹配 `Command`。`Command::Move { x: 0, y: 0 }` 匹配特定字段值，`Command::Move { x, y } if x.abs() + y.abs() > 10` 使用 guard 添加额外条件，`Command::ChangeColor(255, 0, 0)` 匹配特定 RGB 值。因为 `match` 必须覆盖所有可能的 `Command` 变体，新增变体时编译器会提醒处理逻辑需要更新。

## 设计取舍

如果不用模式匹配，命令处理通常会变成多层 `if`、字符串比较和数组下标读取。这样的代码容易漏掉长度检查，也容易把解析和执行混在一起。Rust 的取舍是用 enum 表达合法命令集合，再用 `match` 把每种形状拆开处理；代码更啰嗦一点，但状态空间更清楚。

模式匹配也有边界：复杂解析不应该全部堆进 `match`，真实项目可能使用解析器组合库或 CLI 库。但即使使用库，最终得到的领域事件仍然适合用 enum 和 `match` 表达。这个例子只用标准库，是为了突出语言内建的结构化分支能力。

## 运行

```bash
rustc main.rs -o /tmp/rust-feature-example && /tmp/rust-feature-example
```

## 观察点

- `"move 0 0"` 命中特定字段模式，输出停留在原点；`"move 8 7"` 命中 guard，输出远距离移动。
- `"write hello rust"` 中的 `rest @ ..` 捕获多个词，说明模式可以描述可变长度输入。
- `"color 255 0 0"` 命中特定元组值，被识别为 red；其他颜色走通用 RGB 分支。
- `Command::Quit` 必须在 `handle` 中出现，否则 `match` 不穷尽。
- 解析阶段和执行阶段分开，减少了在业务逻辑里反复处理原始字符串的机会。

## 延伸练习

- 新增 `Command::Resize { width: u32, height: u32 }`，观察编译器提示哪些 `match` 需要更新。
- 把解析失败改成 `Result<Command, String>`，让未知命令保留错误原因。
- 增加 `move x y fast` 的形式，用切片模式区分普通移动和快速移动。
- 把 `handle` 拆成多个小函数，比较模式匹配集中处理和分层处理的可读性。
