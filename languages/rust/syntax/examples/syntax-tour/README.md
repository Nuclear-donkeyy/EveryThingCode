# Rust Syntax Tour

## 目标

这个示例用一个单文件小程序串起 Rust 基础语法。它假设你已经理解变量、函数、集合和分支等通用概念，重点观察 Rust 如何把可变性、所有权、缺失值和错误处理写进普通代码路径里。

程序模拟一份课程报名清单：创建学生记录，统计课程人数，按状态输出说明，并解析一段可能失败的输入。它只使用标准库，不需要 Cargo，也不需要第三方 crate。

## 覆盖语法

- `fn main()` 入口，以及返回 `Result` 的辅助函数。
- `let`、`let mut`、常量、基础数字和布尔类型。
- `String` 与 `&str` 的拥有和借用差异。
- `if` 表达式、`match` 穷尽分支、`for` 迭代。
- 带返回值的函数、代码块表达式和 `?` 错误传播。
- `Vec`、`HashMap`、`struct`、`enum`、`impl`。
- `Option` 表示可能缺失，`Result` 表示可能失败。
- 单文件内联 `mod` 和 `use`，建立模块与命名空间的最小认知。

## 运行

```bash
rustc main.rs -o /tmp/rust-syntax-tour && /tmp/rust-syntax-tour
```

在仓库根目录运行时，可以先进入示例目录：

```bash
cd languages/rust/syntax/examples/syntax-tour
rustc main.rs -o /tmp/rust-syntax-tour && /tmp/rust-syntax-tour
```

预期输出会包含学生数量、课程统计、每个学生的状态说明，以及成功和失败的分数解析结果。

## 观察点

注意 `Student::new` 接收 `&str`，但结构体字段保存 `String`：函数调用方只是借出文本，结构体获得自己的拥有数据。`students.iter()` 让循环只读遍历，因此循环后还可以继续使用 `students`。`HashMap::entry(...).or_insert(0)` 是更新计数的惯用写法，避免手写“存在就加一，不存在就插入”的重复分支。

`status_label` 使用 `match` 覆盖 `Enrollment` 的所有变体。`find_student` 返回 `Option<&Student>`，因为查找可能失败，但失败不是错误。`parse_score` 返回 `Result<u32, String>`，因为输入格式不对或分数越界都需要调用方处理。两者都没有隐藏控制流，调用处必须面对结果。

## 修改练习

- 给 `Student` 增加 `email: Option<String>` 字段，并在输出中只展示存在的邮箱。
- 新增一个 `Enrollment::Waitlisted(u32)` 变体，表示候补序号，然后修正 `match` 分支直到编译通过。
- 把 `parse_score` 的上限从 100 改成常量，并尝试解析 `"101"`。
- 把课程统计改成按学生状态统计，练习 `HashMap` 的键从 `String` 变成枚举或文本标签。
