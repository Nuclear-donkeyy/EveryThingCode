# Java Syntax Tour

## 目标

这个示例用一个小型任务工时汇总程序串起 Java 的基础语法。它面向已经会编程的读者，所以重点不是解释“什么是循环”，而是观察 Java 如何把入口方法、静态方法、显式类型、不可变数据、集合和异常放在同一个单文件程序里。示例不写 `package`，这样可以在当前目录直接 `javac Main.java && java Main`；真实项目中再把类放进与包名一致的目录。

## 覆盖语法

- `class Main` 与 `public static void main(String[] args)` 入口。
- 局部变量、`final` 常量、`int` / `double` / `boolean` 和 `String`。
- `if`、增强 `for`、现代 `switch` 表达式。
- 静态方法、返回值、参数和 `throw`。
- `List`、`Map`、`ArrayList`、`Map.of` 等标准库集合。
- `record Task(...)` 表达轻量不可变数据。
- `try` / `catch` 捕获参数校验失败。
- `import java.util...` 展示包与导入的最小认知。

## 运行

```bash
javac Main.java && java Main
```

如果你从仓库根目录运行，可以先执行：

```bash
cd languages/java/syntax/examples/syntax-tour
javac Main.java && java Main
```

## 观察点

输出里会先打印团队名、任务数量、总工时和风险等级，再展示从异常中恢复后的默认任务。注意 `final List<Task> tasks` 固定的是变量绑定，示例仍然复制到 `ArrayList` 后新增了任务；如果使用 `List.of(...)` 得到的原列表直接新增，会抛出不支持修改的异常。`Task` 是 `record`，所以访问字段时写 `task.title()` 和 `task.hours()`，不是直接读字段。

还可以观察 `switch` 表达式：每个分支返回一个字符串，结果赋给 `label`。`parseHours` 对非法输入抛出 `IllegalArgumentException`，调用方用 `try` / `catch` 决定恢复策略，这比静默返回魔法数字更符合 Java 的常见错误处理习惯。

## 修改练习

1. 给 `Task` 增加 `owner` 字段，并在输出中按负责人汇总工时。
2. 把 `riskLabel` 的 `switch` 改成传统 `switch` 语句，比较两种写法的漏写 `break` 风险。
3. 把文件放进 `demo/syntax/Main.java` 并添加 `package demo.syntax;`，再尝试从正确目录用 `javac` 和 `java` 运行。
