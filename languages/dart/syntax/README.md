# Dart 基础语法速览

## 读者定位

这份速览面向已经写过 Java、C#、JavaScript、TypeScript、Go、Kotlin 或 Swift，但还没有系统写过 Dart 的读者。Dart 看起来像一门 C 系语言：花括号、分号、类、泛型、`async/await` 都很熟悉；真正需要迁移的是它为应用开发做出的组合取舍：默认非空、官方格式化、清晰的库导入、轻量数据结构和事件循环式异步。

学习 Dart 时不要一开始就把所有概念都投射到 Flutter widget。Flutter 是 Dart 的最大舞台，但 Dart 先是一门语言。先理解 `void main()`、变量声明、空安全、集合、类、记录、sealed class、mixin、extension、`Future` 和 `Stream`，再看 Flutter 的构造函数、不可变 widget、状态流和回调，会少很多“框架魔法”的错觉。

## 运行方式

Dart 源文件通常以 `.dart` 结尾。最小程序入口是：

```dart
void main() {
  print('Hello, Dart');
}
```

`void main()` 表示程序入口不返回业务值；也可以写成 `Future<void> main() async` 来等待异步初始化。单文件示例可以直接运行：

```bash
dart run main.dart
```

`dart:core` 会自动导入，提供 `String`、`int`、`List`、`Map`、`Object`、`print` 等基础能力。其他标准库用 `import 'dart:async';`、`import 'dart:convert';`、`import 'dart:io';` 这样的 URI 导入。项目中的包导入通常使用 `package:name/path.dart`，相对导入适合当前库内部的小范围文件。

## 语法速览

Dart 使用花括号和分号，代码块、条件和循环对 C 系读者很直接。变量声明最常见的是 `var`、显式类型、`final` 和 `const`。`var name = 'Ada';` 由初始化值推断静态类型，之后仍然是 `String`，不是 JavaScript 那种随意换类型的变量。`final` 表示只能赋值一次，运行时才能知道的值也可以是 `final`；`const` 表示编译期常量，常用于固定配置和可复用的不可变对象。

注释用 `//` 和 `/* ... */`，文档注释用 `///`。字符串既可以用单引号也可以用双引号，社区中单引号很常见。字符串插值用 `$name` 或 `${expression}`，多行字符串用三引号。Dart 没有 Python 式缩进语义，也没有 JavaScript 的隐式分号陷阱；格式化交给 `dart format`。

## 类型与值

Dart 是静态类型语言，支持类型推断。默认启用 sound null safety：`String name = 'Ada';` 不能保存 `null`，只有 `String? nickname` 才表示可空。判空之后，编译器会做类型提升：

```dart
String? nickname = findNickname();
if (nickname != null) {
  print(nickname.toUpperCase());
}
```

常见误解是把 `!` 当成“修好空值”。`value!` 只是告诉编译器“我保证不是 null”，如果保证错了，运行时仍会抛错。迁移时优先用判空、默认值 `??`、可空访问 `?.` 和清楚的数据边界，而不是到处加 `!`。

基础值包括 `int`、`double`、`num`、`bool`、`String`、`Object`、`Null`。`String` 是不可变 Unicode 文本，拼接短文本可用插值，批量构造文本用 `StringBuffer` 更合适。`dynamic` 会绕过静态检查，适合 JSON、插件边界或渐进迁移；`Object?` 则更诚实地表示“我现在只知道它可能是任何值，使用前要检查”。

## 控制流

`if` / `else` 和多数语言相似，但条件必须是 `bool`，不会把 `0`、空字符串或空列表自动当成假。`switch` 在 Dart 3 中更强，可以配合模式匹配和记录解构表达分支；普通枚举、字符串和整数分支也能直接使用。sealed class 搭配 `switch` 时，分析器可以帮助检查分支是否穷尽。

循环以 `for` 为主：三段式 `for (var i = 0; i < n; i++)` 适合索引，`for (final item in items)` 适合遍历集合。`while` 和 `do while` 也可用。Dart 的集合字面量支持 collection if 和 collection for，例如在一个 `List` 里按条件加入元素，这也是 Flutter UI 列表中非常常见的语言基础。

## 函数与模块

函数是一等值，可以赋给变量、传入回调，也可以作为返回值。完整函数写法适合多步逻辑：

```dart
int add(int a, int b) {
  return a + b;
}
```

只有一个表达式时可以用箭头函数：

```dart
int add(int a, int b) => a + b;
```

箭头函数不是“短函数体”，它只能返回一个表达式。参数可以是必需位置参数、可选位置参数或命名参数。Dart/Flutter 中命名参数非常重要，`required` 用来标记必填命名参数，默认值让 API 调用更可读。库和模块由文件组成，`import` 引入库，`as` 给库起别名，`show`/`hide` 限制导入名字；文件名前下划线不是私有，Dart 的库级私有以标识符前缀 `_` 表示，只在同一个 library 内可见。

## 集合与数据建模

`List<T>` 表示有序列表，`Map<K, V>` 表示键值映射，`Set<T>` 表示去重集合。字面量写法简洁：

```dart
final scores = <String, int>{'Ada': 98, 'Linus': 91};
final names = <String>['Ada', 'Linus'];
```

在 Dart 中，`final` 只固定变量绑定，不自动让集合内容不可变。`final names = <String>[]; names.add('Ada');` 是合法的；如果要不可变视图或常量集合，需要使用 `const` 字面量或标准库中的不可修改包装。迁移时要区分“引用不变”和“对象内容不变”。

数据建模可以从 `class` 开始：字段、构造函数、方法和 getter 是基本工具。`record` 适合轻量固定形状的返回值，例如 `({String name, int count})`，比临时小类更短，但不适合承载复杂行为。`sealed class` 适合表达有限状态或结果类型，让调用方用 `switch` 穷尽处理。`mixin` 用来复用一组方法或状态，避免只为共享行为建立继承层次。`extension` 可以给已有类型添加语法上像成员的方法，适合让领域代码更贴近业务语言，但不要滥用到让方法来源变得难找。

## 错误处理

Dart 用 `throw`、`try`、`on`、`catch`、`finally` 处理异常。`on FormatException catch (error)` 适合捕获具体异常，`catch (error, stackTrace)` 可以拿到错误和堆栈。通常用 `Exception` 表示可预期失败，用 `Error` 表示程序错误或不应恢复的问题。

异步错误会沿着 `Future` 和 `Stream` 传播。`await someFuture()` 外层的 `try/catch` 可以捕获 future 完成时的错误；`Stream` 则可能在多个数据事件之间发出错误事件，可以用 `await for` 配合 `try/catch`，或在 `listen` 中提供 `onError`。常见坑是创建了 future 却没有 `await`，导致错误在当前 `try/catch` 外部发生。

业务失败不一定都要抛异常。登录失败、表单校验失败、远端状态失败可以用 sealed class 结果类型表达，例如 `LoadSuccess` / `LoadFailure`，让 UI 或调用方清楚处理每一种状态。

## 惯用写法

Dart 代码通常偏向小而清楚的类型、不可变默认值和命名参数。能用 `final` 就先用 `final`，只有确实要重新赋值时才用可变变量。能用 `const` 的固定对象优先用 `const`，这在 Flutter 中尤其常见，因为 widget 构造、主题值和静态配置可以被复用。

常见惯用写法包括：用 `for (final item in items)` 直接遍历；用 `map`、`where`、`fold` 做短数据转换，但复杂逻辑改回普通循环；用 `??` 提供默认值；用 `?.` 访问可空对象；用级联操作符 `..` 对同一个对象做连续设置；用 extension 封装领域小转换；用 sealed class 或 record 表达结构化结果。

进入 Flutter 前，建议先把语言层基础练稳：理解 `BuildContext` 之前先理解作用域和对象生命周期，理解 `setState` 之前先理解可变状态，理解 `FutureBuilder` 和 `StreamBuilder` 之前先理解 `Future`、`Stream` 和错误传播，理解 widget 构造前先理解命名参数、`const` 构造和不可变字段。

## 可运行示例

本章示例位于：

- [syntax-tour](examples/syntax-tour/)：一个标准库任务汇总脚本，演示 `void main`、变量声明、字符串、条件、`switch`、循环、函数和箭头函数、`List`/`Map`、class、record、sealed class、mixin、extension、null safety、`Future`/`Stream` 错误处理和 `import`。

运行：

```bash
cd languages/dart/syntax/examples/syntax-tour
dart run main.dart
```

示例只使用标准库，不需要 `pubspec.yaml` 或第三方依赖。

## 学习检查

读完并运行示例后，可以用这些问题确认自己是否掌握了迁移重点：

- `void main()` 和 `Future<void> main() async` 分别适合什么入口？
- `var` 的类型推断为什么不等于 JavaScript 的动态变量？
- `final` 和 `const` 的差异是什么？`final List` 的内容是否一定不可变？
- 为什么 Dart 的 `if` 条件必须是 `bool`？
- 可空类型 `T?`、`?.`、`??` 和 `!` 分别表达什么风险边界？
- 箭头函数能不能包含多条语句？
- 什么时候用 record，什么时候应该建立 class 或 sealed class？
- `Future` 错误和 `Stream` 错误分别在哪里捕获？
- `import`、`as`、`show`、`hide` 解决的是什么命名和边界问题？
