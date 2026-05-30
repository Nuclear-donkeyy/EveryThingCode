# Go 基础语法速览

## 读者定位

这份速览面向已经写过一两门主流语言、但第一次系统接触 Go 的读者。Go 的语法不难，真正需要迁移的是心智模型：它少用隐藏控制流，少用继承层级，强调显式错误、简单组合和统一工具链。你会看到很多代码看起来比其他语言“朴素”，这通常是设计目标，而不是表达能力不足。

如果你来自 Java、C# 或 TypeScript，要特别注意 Go 的接口是隐式实现的，没有 `implements` 声明；如果你来自 Python 或 Ruby，要记住 Go 是静态类型语言，很多约束在编译期完成；如果你来自 C/C++，Go 有垃圾回收和内置 slice/map/string，但资源关闭、并发生命周期和错误传播仍然需要你明确处理。

## 运行方式

最小 Go 程序通常放在一个目录里，入口文件声明 `package main`，并提供 `func main()`。在示例目录执行：

```bash
go run main.go
```

`go run` 会临时编译并运行程序；`go build` 生成可执行文件；`go test ./...` 运行当前模块下的测试。真实项目通常有 `go.mod` 描述模块路径和依赖，但单文件入门示例可以直接用 `go run main.go` 运行。Go 的格式化由 `gofmt` 统一，团队里很少为缩进和换行风格争论。

## 语法速览

Go 文件以 `package` 开头。`package main` 表示可执行程序，其他包通常提供可复用能力。文件内通过 `import` 引入包，标准库包名一般就是导入路径最后一段，例如 `fmt`、`errors`、`strings`。导出的标识符必须以大写字母开头，小写开头只在包内可见，这一点取代了很多语言里的 `public/private` 关键字。

变量声明有三种常见形式：`var name string` 明确类型，`var name = "go"` 让编译器推断类型，`name := "go"` 在函数内部声明并初始化。`:=` 不能在包级别使用，也不能只给已有变量重新赋值；重新赋值使用 `=`。常量用 `const`，只能保存编译期可确定的值，例如数字、字符串和布尔值。

Go 语句末尾通常不写分号。大括号位置有约定，`if condition { ... }` 的左大括号不能随意换到下一行。很多语法限制看似严格，其实是为了让 `gofmt` 和代码审阅更稳定。

## 类型与值

Go 的基础类型包括 `bool`、`string`、整数类型如 `int`、`int64`、无符号整数如 `uint`、浮点数如 `float64`，以及 `byte` 和 `rune`。`byte` 是 `uint8` 的别名，常用于原始字节；`rune` 是 `int32` 的别名，常用于 Unicode 码点。`string` 是不可变字节序列，按字节索引不等于按用户可见字符索引；处理 Unicode 文本时常用 `for _, r := range text` 遍历 rune。

每种类型都有零值：数字是 `0`，布尔是 `false`，字符串是 `""`，指针、slice、map、函数、接口和 channel 的零值是 `nil`。Go 代码喜欢让零值有意义，例如空 `bytes.Buffer` 可直接使用。需要注意的是，nil slice 可以 `append`，但 nil map 不能直接写入，写 map 前要用 `make` 初始化。

类型转换必须显式写出，例如 `float64(count)`。Go 不会自动把 `int` 转成 `int64`，这减少了隐式截断和平台差异。类型别名和自定义类型也很常见：`type UserID int64` 能让编译器区分普通整数和业务 ID。

字符串有两种常见字面量：双引号字符串支持转义，如 `"line\n"`；反引号原始字符串保留换行和反斜杠，适合 SQL、正则或多行文本。格式化输出常用 `fmt.Printf("%s: %d\n", name, count)`，拼接少量字符串可以用 `+`，大量拼接可考虑 `strings.Builder`。

## 控制流

`if` 不需要圆括号，但条件必须是布尔表达式。Go 支持在 `if` 前放一个短语句，常用于限制变量作用域：

```go
if value, err := load(); err != nil {
    return err
} else {
    fmt.Println(value)
}
```

`switch` 默认每个 `case` 后自动 break，不会像 C 那样继续落入下一分支；如果确实要继续，需要显式写 `fallthrough`，但日常代码很少用。`switch` 可以没有表达式，这时每个 `case` 都是布尔条件，适合替代较长的 if/else 链。

Go 只有 `for` 一种循环关键字。传统三段式是 `for i := 0; i < n; i++ {}`；while 风格是 `for condition {}`；无限循环是 `for {}`。遍历集合通常用 `range`：遍历 slice 得到索引和值，遍历 map 得到键和值，但 map 遍历顺序不保证稳定。需要稳定顺序时先取出键并排序。

## 函数与模块

函数用 `func` 声明，参数类型写在参数名后面：`func add(a int, b int) int`。相邻参数类型相同时可以合并成 `func add(a, b int) int`。Go 函数可以返回多个值，最常见的是 `(value, error)`。调用方应立即检查 `err`，这是 Go 显式错误处理的核心习惯。

命名返回值可以用于短函数或需要被 `defer` 修改返回错误的场景，但滥用会让返回路径变得隐晦。普通代码更推荐显式 `return value, nil` 或 `return zero, err`，读者不用回头找返回变量在哪里被改过。

包是 Go 的基本模块边界。一个目录通常对应一个包，同目录文件必须声明同一个包名。`import` 不按文件导入，而按包导入；被导入包里大写开头的标识符才对外可见。Go 鼓励包名短、小写、无下划线，例如 `http`、`json`、`user`。循环依赖不允许，这会迫使你把共享抽象放到更清晰的位置。

## 集合与数据建模

数组 `[3]int` 长度是类型的一部分，日常业务代码更常用 slice：`[]int{1, 2, 3}`。slice 是对底层数组的一段视图，包含指针、长度和容量。`append` 可能复用原数组，也可能分配新数组，所以追加后要使用返回的新 slice：`items = append(items, next)`。

map 用 `map[string]int` 表示键值表，读取不存在的键会得到值类型的零值。需要区分“不存在”和“值正好是零”时使用双返回值：`value, ok := counts[name]`。map 不是并发安全结构，多 goroutine 读写时要用锁、channel 或 `sync.Map`。

struct 是 Go 最常见的数据建模方式。字段名大写表示可被包外访问，小写表示包内私有。方法不是写在 struct 内部，而是通过接收者绑定到类型上：

```go
type User struct {
    Name string
}

func (u User) Label() string {
    return "user:" + u.Name
}
```

interface 描述行为集合，而不是继承树。一个类型只要拥有接口要求的方法，就自动满足接口。惯用做法是让接口保持小，例如 `io.Reader` 只有 `Read` 一个方法。通常由使用方定义接口，这样依赖的是自己真正需要的行为。

## 错误处理

Go 的常规错误是实现了 `error` 接口的值。函数失败时返回错误，调用方显式判断：

```go
value, err := parse(input)
if err != nil {
    return fmt.Errorf("parse config: %w", err)
}
```

`fmt.Errorf` 的 `%w` 可以包装错误，之后用 `errors.Is` 判断错误链里是否包含某个哨兵错误，用 `errors.As` 提取具体错误类型。不要把 `panic` 当异常机制使用；`panic` 更适合程序员错误、不可恢复状态，或启动阶段无法继续的硬失败。

`defer` 会在当前函数返回前执行，常用于关闭文件、释放锁、记录耗时或恢复资源状态。多个 `defer` 按后进先出顺序执行。要注意 `defer` 的参数会在声明时求值，而不是执行时才求值；如果想使用最新变量值，通常传闭包并在闭包里读取。

## 惯用写法

Go 惯用代码偏向小函数、早返回和浅缩进。错误分支通常先处理：

```go
if err != nil {
    return err
}
```

这样主路径保持靠左。命名上不追求长前缀，因为包名已经提供上下文，例如 `user.Service` 比 `user.UserService` 更自然。接口命名常用 `Reader`、`Writer`、`Validator` 这类行为名。

不要过早引入大接口、继承式目录层级或复杂泛型。Go 的泛型适合表达容器、算法和少量类型约束，不适合把所有业务差异都塞进类型系统。组合通常比层级更自然：struct 嵌入、函数参数、接口边界和简单包拆分，足以覆盖大多数服务端代码。

import 按标准库、第三方、本项目分组，`go fmt` 和 `goimports` 会整理顺序。未使用的变量和 import 会编译失败，这迫使代码保持干净。临时忽略值用 `_`，但不要用它掩盖本应处理的错误。

## 可运行示例

本目录提供一个标准库示例：

- [syntax-tour](examples/syntax-tour/)：用一个小型任务统计程序串起 package/main、import、变量、基础类型、字符串、控制流、函数多返回值、slice/map、struct、interface、方法、error 和 defer。

进入示例目录后执行：

```bash
go run main.go
```

建议先直接运行，再修改输入数据观察错误路径和 `defer` 输出。示例刻意保持单文件，是为了让你把注意力放在 Go 的基础语法组合上，而不是项目分层。

## 学习检查

读完后可以用这些问题自检：

- 能否解释 `package main`、`func main()` 和普通包之间的差异？
- 什么时候使用 `var`、`const`、`:=` 和 `=`？
- 为什么 Go 只有 `for`，`range` 遍历 slice 和 map 时分别拿到什么？
- 函数返回 `(T, error)` 时，调用方为什么通常马上检查 `err`？
- nil slice 和 nil map 在追加或写入时有什么差别？
- 一个类型为什么不需要显式声明就能满足 interface？
- `defer` 何时执行，多个 defer 的顺序是什么？
- 什么时候应该包装错误，什么时候不该用 `panic`？
