# Rust 基础语法速览

## 读者定位

这份速览面向已经写过其他语言、但第一次系统接触 Rust 的读者。Rust 的表面语法像 C 系语言：有花括号、`fn`、`if`、`for`、`match`、泛型和模块；真正需要切换的是心智模型。Rust 默认把“值属于谁、谁能改、失败是否被处理”放进类型和编译期检查里，而不是依赖运行时异常、垃圾回收或团队约定。

如果你来自 Java、Go、Python、JavaScript 或 C++，可以先把 Rust 想成一门强类型、表达式导向、无 GC、以所有权组织数据流的语言。初学时不要急着和借用检查器对抗，先让数据从创建者流向使用者；只有确实需要共享时，再选择引用、切片、智能指针或同步原语。

## 运行方式

最小 Rust 程序入口是 `fn main()`。单文件可以直接用 `rustc main.rs` 编译，真实项目通常用 Cargo：

```bash
rustc main.rs -o /tmp/app && /tmp/app
cargo new demo
cargo run
cargo test
```

`rustc` 适合语法实验，Cargo 负责包结构、依赖、测试、格式化和发布。Rust 的编译单元叫 crate；一个可执行 crate 通常从 `src/main.rs` 开始，一个库 crate 通常从 `src/lib.rs` 开始。

## 语法速览

入口函数写作 `fn main() { ... }`，函数体、`if`、`match` 和普通代码块都可以是表达式。很多 Rust 代码不需要显式 `return`，最后一个没有分号的表达式就是返回值：

```rust
fn main() {
    let answer = add(20, 22);
    println!("answer = {answer}");
}

fn add(left: i32, right: i32) -> i32 {
    left + right
}
```

`let` 默认绑定不可变值，`let mut` 才允许重新赋值。这里的“不可变”是绑定层面的设计取舍：Rust 鼓励你先写清楚数据流，减少隐藏的共享可变状态。`const` 是编译期常量，必须写类型，适合全局或固定配置。

常见误解是把 Rust 的分号当成纯粹语句结束符。带分号的表达式会变成 `()`，也就是“没有有用值”。因此函数、`if` 分支和代码块的最后一行是否带分号会影响返回值。

## 类型与值

基础标量包括整数 `i32`、`u64`、浮点 `f64`、布尔 `bool` 和字符 `char`。Rust 不会随意隐式转换数字类型，跨类型运算通常要显式转换，例如 `value as i64`。复合类型包括 tuple、array、slice、struct、enum。局部变量可以靠推断，但函数参数和返回值通常要写清楚。

字符串是初学者最容易卡住的地方。`String` 是拥有堆内存的可变字符串值，适合构造和保存；`&str` 是字符串切片，通常表示对 UTF-8 文本的一段借用，适合只读参数。惯用函数签名通常接收 `&str`，这样既能传字符串字面量，也能传 `String` 的借用：

```rust
fn greet(name: &str) -> String {
    format!("hello, {name}")
}

let owned = String::from("Rust");
let text = greet(&owned);
let literal = greet("reader");
```

引用用 `&value` 创建，只读借用可以有多个；可变借用 `&mut value` 在同一时间只能有一个。这个限制不是语法洁癖，而是 Rust 用来避免数据竞争、悬垂引用和迭代时修改集合等问题的核心规则。

## 控制流

`if` 不需要括号，但条件必须是 `bool`，不会把数字或空集合当真假值。因为 `if` 是表达式，两个分支可以返回同一种类型的值：

```rust
let label = if score >= 60 { "pass" } else { "retry" };
```

`match` 是更强的分支工具，要求穷尽覆盖所有可能。它和 `enum`、`Option`、`Result` 搭配时尤其重要，因为编译器会提醒你是否漏处理状态。`_` 表示兜底分支，但不要为了省事过早使用它，否则会失去穷尽检查带来的帮助。

循环包括 `loop`、`while` 和 `for`。Rust 的 `for` 遍历迭代器，常见写法是 `for item in items.iter()` 只读遍历，`for item in items.iter_mut()` 可变遍历，`for item in items` 消耗集合所有权。选择哪一种，取决于循环后是否还需要原集合。

## 函数与模块

函数使用 `fn name(param: Type) -> ReturnType`。没有返回值的函数实际返回 `()`。Rust 函数不能靠参数名重载；需要不同行为时，常用不同函数名、泛型、trait 或 enum 参数表达。

代码块也可以产生值，这让小范围计算很自然：

```rust
let normalized = {
    let trimmed = input.trim();
    trimmed.to_lowercase()
};
```

模块心智模型可以先记成三件事：`mod` 声明模块，`use` 把路径引入当前作用域，`pub` 控制对外可见。`mod` 不是导入包的语句，它是在 crate 中声明一棵模块树；`use std::collections::HashMap` 只是让长路径变短。单文件实验可以写内联模块，项目里通常拆成 `mod name;` 对应 `name.rs` 或 `name/mod.rs`。

## 集合与数据建模

`Vec<T>` 是最常用的动态数组，`HashMap<K, V>` 是哈希表，二者都在标准库中。集合保存的是同一种类型的元素；如果需要表达“几种不同形态的数据”，通常用 `enum`，而不是把值塞进宽松的动态对象里。

`struct` 用字段建模一类数据，`impl` 给类型添加方法。方法第一个参数常见为 `&self`、`&mut self` 或 `self`，分别表示只读借用、可变借用和消耗所有权：

```rust
struct User {
    name: String,
    visits: u32,
}

impl User {
    fn visit(&mut self) {
        self.visits += 1;
    }
}
```

`enum` 是 Rust 数据建模的核心。它的每个变体都可以携带不同数据，配合 `match` 能把状态和处理逻辑放在同一张类型地图上。`Option<T>` 和 `Result<T, E>` 都是标准库 enum，因此“空值”和“失败”不是隐藏控制流，而是你必须处理的普通值。

## 错误处理

Rust 没有传统异常作为日常错误处理入口。可能不存在的值用 `Option<T>`：`Some(value)` 或 `None`。可能失败的操作用 `Result<T, E>`：`Ok(value)` 或 `Err(error)`。这两个类型强迫调用方承认不确定性，减少空指针和漏捕获异常。

`match` 可以显式拆开结果，`if let` 适合只关心一个分支，`?` 适合在返回 `Result` 或 `Option` 的函数里提前传播失败：

```rust
fn parse_count(text: &str) -> Result<u32, std::num::ParseIntError> {
    let count = text.parse::<u32>()?;
    Ok(count)
}
```

`panic!` 表示不可恢复的程序错误，适合测试断言、明显违反不变量或启动时无法继续的场景。业务输入错误、文件不存在、网络失败等通常应该返回 `Result`，让上层决定恢复、重试或展示信息。

## 惯用写法

Rust 代码通常从不可变开始，需要修改时再加 `mut`。函数参数优先接收借用，例如 `&str`、`&[T]`、`&HashMap<K, V>`，除非函数确实要取得所有权。集合转换常用迭代器：`iter()`、`map()`、`filter()`、`collect()`，但简单循环也完全可以，清晰比炫技重要。

常见惯用法包括：用 `match` 穷尽状态，用 `Option` 代替可空引用，用 `Result` 代替异常通道，用 `derive(Debug, Clone, PartialEq)` 自动生成常用能力，用 `impl` 把行为靠近数据，用 `use` 引入标准库类型但避免把命名空间铺得过宽。

迁移时最容易过度使用 `clone()`。`clone()` 不是错误，但它表示复制拥有的数据，可能带来额外分配。先问自己：函数只是读取吗？那就传引用。函数要保存或跨线程移动吗？那可能需要所有权或显式 clone。Rust 的好处正在于这些取舍会写在签名里。

## 可运行示例

示例位于 [examples/syntax-tour/](examples/syntax-tour/)，可以直接用标准库和 `rustc` 运行：

```bash
cd languages/rust/syntax/examples/syntax-tour
rustc main.rs -o /tmp/rust-syntax-tour && /tmp/rust-syntax-tour
```

这个示例覆盖 `fn main`、`let`/`mut`、基础类型、`String`/`&str`、`if`/`match`/`for`、函数表达式、`struct`/`enum`/`impl`、`Vec`/`HashMap`、`Result`/`Option`，以及单文件内联 `mod` 和 `use` 的最小心智模型。

## 学习检查

读完后可以用这些问题自测：

- 什么时候应该写 `String`，什么时候应该写 `&str`？
- 一个函数只读取集合时，为什么参数更常写成 `&[T]` 而不是 `Vec<T>`？
- `if`、`match` 和代码块作为表达式时，最后一行分号会带来什么影响？
- `for item in items`、`items.iter()`、`items.iter_mut()` 对所有权有什么不同？
- `Option<T>` 和 `Result<T, E>` 分别表达哪两类不确定性？
- `mod`、`use`、`pub` 各自解决什么问题？

如果这些问题能用自己的话回答，再去看 Cargo 项目结构、trait、泛型、生命周期和异步运行时会顺畅很多。
