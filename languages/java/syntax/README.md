# Java 基础语法速览

## 读者定位

这份速览写给已经会写至少一门编程语言、但第一次系统接触 Java 的读者。Java 的心智模型不是“脚本从第一行开始执行”，而是“代码声明在类型里，JVM 从约定的入口方法进入”。即使是最小程序，也通常放在一个 `class` 中，通过 `public static void main(String[] args)` 启动。你会频繁看到显式类型、访问修饰符、包名、导入和异常声明；这些样板不是为了拖慢你，而是为了让大型工程里的边界、依赖和失败路径更稳定。

迁移时要先接受两个事实：Java 是静态、名义类型语言；Java 默认使用引用语义处理对象。变量名保存的不是对象本身，而是指向对象的引用。对象生命周期通常交给 GC，文件、网络连接这类外部资源仍要显式关闭。Java 代码看起来比 Python、Ruby 或 JavaScript 更“声明式”，但换来的是 IDE、编译器和重构工具能在很大代码库里持续提供反馈。

## 运行方式

最小学习路径是安装 JDK，然后用 `javac` 编译、用 `java` 运行：

```bash
cd languages/java/syntax/examples/syntax-tour
javac Main.java && java Main
```

`javac Main.java` 会生成 `.class` 字节码文件，`java Main` 让 JVM 加载名为 `Main` 的类并寻找入口方法。单文件示例通常不写 `package`，因为包名必须和目录结构匹配；真实项目中会使用 `package com.example.app;` 放在文件第一行，并用 Maven 或 Gradle 管理编译、测试和依赖。

## 语法速览

Java 程序由包、导入、类型和成员组成。常见文件结构是：可选 `package`，若干 `import`，然后是 `class`、`record`、`interface` 或 `enum`。一个源文件最多有一个 `public` 顶层类型，且文件名要和它一致，例如 `public class Main` 必须在 `Main.java` 中。

表达式和语句的边界很明确：大多数语句以分号结束，代码块用花括号。局部变量可以写显式类型，也可以用 `var` 让编译器从右侧推断类型；`var` 不是动态类型，只能用于有初始化表达式的局部变量。方法调用、字段访问、构造对象和泛型集合是日常 Java 的主要语法面。

和很多语言相比，Java 更强调 API 形状的稳定性。方法签名里的参数类型、返回类型、异常声明和可见性都是契约的一部分。初学时不要把语法速记成关键字列表，而要问：这个声明是在给编译器、调用者还是运行时提供哪类保证？

## 类型与值

Java 有两大类值：基本类型和引用类型。基本类型包括 `int`、`long`、`double`、`boolean`、`char` 等，它们直接保存值，不能为 `null`。引用类型包括 `String`、数组、集合、自定义对象、record、接口实现等，变量保存引用，可以为 `null`。集合泛型只能使用引用类型，所以 `List<Integer>` 使用的是 `int` 的包装类型 `Integer`。

`String` 是不可变引用类型。拼接会产生新字符串，内容比较要用 `equals`，不要用 `==`；`==` 比较的是两个引用是否指向同一个对象。字符串插值不是 Java 的传统语法，常见写法是 `String.format(...)`、`formatted(...)` 或直接拼接简单片段。

`final` 表示“这个变量不能重新绑定”。对基本类型，它让数值不可再赋新值；对引用类型，它只固定引用本身，不会自动让对象内部不可变。想得到真正更安全的数据模型，优先使用不可变集合、只读字段、`record` 和不暴露可变内部状态的 API。

## 控制流

`if` / `else` 和多数 C 系语言接近，条件必须是 `boolean`，不会把数字、字符串或对象自动当作真假值。循环包括经典 `for`、`while`、`do while` 和增强 `for`。遍历集合时优先使用增强 `for`，需要索引时再使用经典 `for`。

`switch` 既可以是语句，也可以是表达式。现代 Java 常用箭头形式减少漏写 `break` 的错误，例如 `case "high" -> 3`。当 `switch` 作为表达式时，每个分支都要给出值，这让“按类别计算结果”的代码更紧凑。迁移时要注意：Java 的控制流倾向于把条件写清楚，不鼓励依赖隐式真值或隐式类型转换。

## 函数与模块

Java 没有脱离类型独立存在的顶层函数，行为通常写成方法。`static` 方法属于类本身，适合工具函数和入口示例；实例方法属于对象，适合读取或修改对象状态。方法签名由可见性、可选修饰符、返回类型、方法名、参数列表和可选异常声明组成。

包是 Java 最常见的命名空间。`package` 声明决定类的完整名字，`import` 只是让代码里可以少写限定名。导入不会复制代码，也不会改变运行时依赖；它更像编译期的名称解析规则。大型工程通常通过包结构表达层次，例如 `controller`、`service`、`repository`，再由 Maven 或 Gradle 负责把源码组织成可编译的模块或制品。

## 集合与数据建模

常用集合接口是 `List`、`Set` 和 `Map`。写 API 时尽量依赖接口类型，例如返回 `List<String>` 而不是 `ArrayList<String>`；创建时再选择实现。`List.of(...)`、`Map.of(...)` 会创建不可变集合，适合示例、配置和小型常量数据。需要增删时使用 `new ArrayList<>()` 或 `new HashMap<>()`。

简单数据载体优先考虑 `record`。`record Task(String title, int hours)` 会自动得到构造器、访问器、`equals`、`hashCode` 和 `toString`，适合表达“这是值对象，不是复杂可变实体”。需要封装可变状态、继承层次或复杂不变量时再使用 `class`。`interface` 用来定义能力边界，调用方依赖接口，具体实现可以替换；这也是 Java 工程里测试和分层设计的基础。

## 错误处理

Java 用异常表达失败。`try` / `catch` 捕获可恢复或需要转换的错误，`finally` 或 `try-with-resources` 用来关闭资源。异常分为受检异常和非受检异常：受检异常必须捕获或在方法签名上 `throws`，常见于 I/O、网络、解析；非受检异常继承自 `RuntimeException`，常用于参数非法、状态错误等编程或业务前置条件问题。

不要把异常当作普通分支控制，也不要捕获后只打印一句就继续运行。好的迁移习惯是：在靠近失败源的地方补足上下文，在系统边界把底层异常转成调用方能理解的错误，并让无法恢复的问题尽快暴露。空值也是 Java 的常见风险；如果方法可能找不到结果，可以考虑返回空集合、明确抛异常，或在合适场景使用 `Optional`。

## 惯用写法

- 入口示例使用 `public class Main` 和 `public static void main(String[] args)`，真实项目让构建工具负责入口、测试和依赖。
- 局部常量用 `final`，字段不可变时也用 `final`；但要记住它固定的是绑定，不一定固定对象内容。
- 字符串内容比较用 `equals`，对可能为 `null` 的值可以写 `"ok".equals(status)`。
- 公开 API 用接口类型表达集合，内部再选择 `ArrayList`、`HashMap` 等实现。
- 小型不可变数据用 `record`，行为边界用 `interface`，复杂状态和生命周期用 `class`。
- 遍历集合优先增强 `for`；链式 Stream 适合清晰的数据转换，不适合塞入复杂副作用。
- 资源释放优先 `try-with-resources`，异常处理要么恢复，要么转换，要么继续抛出。
- 包名全小写并反向域名组织，导入标准库或其他包中的类型，不要依赖通配导入来掩盖边界。

## 可运行示例

示例位于 [examples/syntax-tour](examples/syntax-tour/)，覆盖变量与 `final`、基本类型与 `String`、条件与循环、方法、`List` / `Map`、`record`、异常和最小包/import 认知。它刻意保持单文件、无第三方依赖，方便你先观察 Java 的语法轮廓，再把同样的代码迁移到 Maven 或 Gradle 项目中。

运行：

```bash
cd languages/java/syntax/examples/syntax-tour
javac Main.java && java Main
```

## 学习检查

读完后建议确认自己能回答这些问题：为什么 Java 示例通常要有 `class Main` 和 `main` 方法？`final List<String>` 是否意味着列表内容不可变？`String` 为什么要用 `equals` 比较内容？`record` 和普通 `class` 的取舍是什么？什么时候使用 `List.of`，什么时候使用 `new ArrayList<>()`？捕获异常后应该恢复、转换还是继续抛出？如果你能把示例改成带 `package` 的目录结构，并解释为什么直接在原目录运行会失败，就已经掌握了 Java 基础语法的核心迁移点。
