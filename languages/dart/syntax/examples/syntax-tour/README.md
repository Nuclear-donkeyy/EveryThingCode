# Dart syntax-tour

## 目标

这个示例用一个任务汇总脚本展示 Dart 基础语法如何组合在一起。它不是 Flutter 项目，也不依赖第三方包；重点是让你看到单文件 Dart 程序如何从 `Future<void> main() async` 进入，声明变量和常量，遍历集合，解析数据，建模结果，并处理同步与异步错误。

## 覆盖语法

- `import 'dart:async';` 和 `Future<void> main() async` 的最小异步入口。
- `const`、`final`、`var`、显式类型、`String` 插值和 sound null safety。
- `if`、`switch`、三段式 `for`、`for in` 以及集合 `for`。
- 普通函数、箭头函数、命名参数和默认值。
- `List<String>`、`Map<String, int>`、记录 `({String title, int priority})`。
- `class`、构造函数、getter、`mixin`、`extension` 和 sealed result 类型。
- `try` / `on` / `catch` / `finally`、`Future` 错误和 `Stream` 错误事件。

## 运行

```bash
dart run main.dart
```

第一条命令会运行当前目录下的 `main.dart`。如果你在仓库根目录，可以先进入示例目录再执行同一条命令：

```bash
cd languages/dart/syntax/examples/syntax-tour
dart run main.dart
```

## 观察点

程序先把原始字符串解析为 `Task`，其中空标题会返回 sealed failure，非法优先级会抛出 `FormatException` 并在调用方恢复。有效任务进入 `List`，随后通过循环写入 `Map` 统计状态。`record` 用来返回最重要任务的标题和优先级，适合这种轻量固定形状数据。

异步部分包含一个成功的 `Future`、一个会失败的 `Future`，以及一个会发出错误事件的 `Stream`。注意 `try/catch` 包住 `await` 才能捕获 future 错误；`await for` 遍历 stream 时同样可以捕获错误事件。`extension` 给 `String` 增加了标题规范化方法，`mixin` 给任务对象复用日志标签。

## 修改练习

- 给 `rawTasks` 增加一条缺少分隔符的数据，观察 sealed failure 和异常路径的区别。
- 把 `TaskStatus` 增加一个新状态，并更新 `switch` 中的显示文本。
- 把 `mostUrgent` 改成返回一个小 `class`，比较它和 record 的可读性。
- 给 `fetchRemoteCount` 增加参数，让调用方决定是否模拟失败。
