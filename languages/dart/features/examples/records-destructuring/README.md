# records-destructuring

## 目标

这个例子展示 Dart 的 records 和 destructuring 如何表达轻量结构化数据。成绩行 `ScoreRow` 不需要完整 class：它只是一次计算中的临时数据，包含姓名、答对题数和总题数。`grade` 返回比例和标签两个值，也不必为了一个很小的返回值专门创建类。

学习目标是判断“什么时候 class 太重，什么时候 record 正好”。真实工程里，经常有函数需要返回两个紧密相关的值，例如分页结果的 `(items, total)`、坐标的 `(x, y)`、统计结果的 `(min, max)`。record 可以让这些结构带着类型流动，同时比 `Map<String, Object?>` 更安全。

## 特性说明

`typedef ScoreRow = ({String name, int correct, int total});` 定义了一个命名字段 record 类型。每一行都必须有这些字段，字段名也是类型的一部分。`for (final (:name, :correct, :total) in rows)` 使用 record pattern 解构字段，循环体里直接得到本地变量。

`grade` 返回 `({double ratio, String label})`，调用处用 `final (:ratio, :label) = grade(...)` 解构命名字段。`summarize` 返回 `(int earned, int possible)` 这种位置字段 record，调用处用 `final (earned, possible)` 解构。两种写法分别适合“字段名提高可读性”和“位置关系已经非常明显”的场景。

## 设计取舍

如果不用 record，轻量数据常会退化成 `List` 或 `Map`。`List` 依赖位置约定，`row[1]` 很难表达业务含义；`Map` 依赖字符串键，拼错键名要到运行时才发现，还会丢失精确类型。class 更稳，但为一次局部计算写构造函数和字段有时显得过重。

record 的取舍是它适合小而局部的数据形状，不适合承载长期演进的领域对象。只要数据需要方法、不变量、文档化构造或跨模块稳定 API，就应该考虑 class。本例把 `ScoreRow` 留在教学计算里，而没有把它包装成“学生实体”，就是为了保留 record 的轻量定位。

## 运行

```bash
dart run main.dart
```

## 观察点

- 运行输出会逐行打印姓名、分数、百分比和标签，说明命名字段 record 能清楚携带多列数据。
- `grade` 一次返回 `ratio` 和 `label`，调用方不需要额外类或可变输出参数。
- `summarize` 展示位置字段 record，适合两个含义紧密且顺序容易理解的汇总值。
- 解构语法让循环和赋值处少写临时对象访问，仍然保留静态类型检查。

## 延伸练习

- 给 `ScoreRow` 增加 `lateMinutes` 字段，观察所有构造和解构位置需要怎样更新。
- 把 `summarize` 改成返回命名字段 record，比较 `final (earned, possible)` 和 `final (:earned, :possible)` 的可读性。
- 尝试用 `Map<String, Object?>` 重写 rows，体验需要多少强制转换和键名约定。
- 当你想给成绩行增加 `isPassing` 方法时，把 record 改成 class，并比较两种建模边界。
