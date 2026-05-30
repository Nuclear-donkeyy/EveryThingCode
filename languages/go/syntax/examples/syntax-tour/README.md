# Go syntax-tour

## 目标

这个示例用一个小型任务统计程序展示 Go 基础语法如何组合在一起。它不是框架项目，也不依赖第三方库；重点是让你看到一个 `package main` 文件里如何声明类型、写函数、处理错误、遍历集合，并用 `defer` 表达函数退出前必须发生的动作。

## 覆盖语法

- `package main`、`import` 和 `func main()` 的最小可执行程序结构。
- `const`、`var`、`:=`、基础类型、字符串格式化和原始字符串。
- `if` 短语句、`switch`、三段式 `for`、`range` 遍历 slice 和 map。
- 函数多返回值，特别是 `(value, error)` 的错误处理风格。
- slice 保存任务列表，map 统计状态数量。
- `struct` 表达任务数据，方法实现 `fmt.Stringer` 接口。
- `errors.Is`、`fmt.Errorf("%w")` 和 `defer` 展示错误包装与收尾动作。

## 运行

```bash
go run main.go
```

第一条命令会编译并运行当前目录的 `main.go`。如果你在仓库根目录，可以先进入示例目录再执行同一条命令：

```bash
cd languages/go/syntax/examples/syntax-tour
go run main.go
```

## 观察点

程序开始和结束时各有一行输出，结束行来自 `defer`，即使中途遇到可恢复错误也会执行。任务数据先经过 `parseTask`，这个函数返回 `Task, error`；调用方在 `err != nil` 时立刻处理，并用 `errors.Is` 判断是否是空标题。有效任务进入 slice，随后通过 `range` 写入 map 统计状态。

`Task` 拥有 `String() string` 方法，所以它自动满足 `fmt.Stringer` 接口。代码里没有 `implements` 关键字，这是 Go 和 Java/C# 等语言很不一样的地方。`switch` 用来给状态打标签，每个 `case` 默认不会继续落入下一个分支。

## 修改练习

- 给 `rawTasks` 增加一个非法优先级，观察错误信息如何被包装并继续处理后续任务。
- 把 `summarize` 改成返回排序后的状态名称，让 map 的输出顺序稳定。
- 给 `Task` 增加 `Owner string` 字段，并在 `String()` 中输出负责人。
- 新增一个小接口，例如 `type Validator interface { Validate() error }`，让 `Task` 用方法满足它。
