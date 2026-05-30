# linq-data-flow

## 目标

把一组报名事件转换成课程报表，观察 LINQ 如何把过滤、分组、排序、投影和聚合连接成声明式数据流。例子也刻意打印一次枚举次数，用来提醒 LINQ 查询通常是延迟执行的。

这个例子对应的核心思想是：把集合处理写成可组合的数据管道。真实项目里，报名记录可能来自数据库、CSV、API 或消息队列；最终要得到的往往不是原始行，而是面向页面、报表或接口的摘要。LINQ 让代码先说明“要哪些数据、怎样分组、怎样排序”，而不是先陷入索引变量和临时集合。

## 特性说明

LINQ 建立在 `IEnumerable<T>`、扩展方法和 lambda 之上。`Where` 过滤已完成报名，`GroupBy` 按课程聚合，`Select` 把每组转换为 `CourseSummary`，`OrderByDescending` 和 `ThenBy` 控制报表顺序。这些操作的类型都是泛型的，所以每一步都知道当前元素是什么，不需要把对象拆成无类型字典。

例子里的 `inspectedRows` 是为了展示延迟执行。定义 `activeCourseSummaries` 时，查询还没有真正遍历数组，所以输出是 `before ToList: inspected rows = 0`。调用 `ToList()` 时才开始枚举，计数随之增加。这个行为让查询可以继续组合，也能避免不必要的工作；但如果你多次枚举同一个查询，也可能重复执行昂贵操作。

如果不用 LINQ，代码通常会退化成多层 `foreach`、手写字典分组、临时列表排序和计数变量。那样并非错误，尤其在需要逐步调试或性能微调时很有用；但业务意图容易被迭代细节淹没。LINQ 的优势是让常见转换保持统一形状。

## 设计取舍

LINQ 不是越长越好。链式调用过长时，读者需要在脑中记住每一步的元素类型和执行时机。真实项目里可以把中间查询拆成有名字的变量，例如 `completedEnrollments`、`groupedByCourse`、`summaries`，让业务阶段更清楚。

延迟执行是一把双刃剑。它能让查询保持惰性，也会让错误、耗时和副作用推迟到枚举时才发生。本例在 `Where` 中修改 `inspectedRows` 是刻意演示副作用；生产代码里应避免在 LINQ 查询里修改外部状态，否则多次枚举会让结果难以推理。

对于数据库查询，LINQ 还可能被翻译成 SQL；不是所有 .NET 方法都能被查询提供器翻译。这个例子只用内存数组和标准库，是为了先理解语言层面的 `IEnumerable<T>` 数据流，再进入 Entity Framework Core 等生态工具。

## 运行

```bash
cd languages/csharp-dotnet/features/examples/linq-data-flow && dotnet run
```

## 观察点

- 查询变量 `activeCourseSummaries` 描述的是转换流程，不是立即生成好的列表。
- `Where`、`GroupBy`、`Select` 和 `OrderByDescending` 让代码强调“要什么结果”。
- `ToList()` 是真正执行查询的位置；如果不缓存，多次枚举可能重复计算。
- 第一行输出中 `before ToList` 的计数为 0，证明查询定义阶段没有遍历数据。
- `after ToList` 的计数等于原始报名行数，说明过滤发生在枚举期间。
- 输出按完成人数降序、课程名升序排列，可以反向验证 `OrderByDescending` 和 `ThenBy` 的顺序。

## 延伸练习

- 删除 `ToList()`，直接在 `foreach` 中枚举 `activeCourseSummaries` 两次，观察 `inspectedRows` 是否重复增加。
- 增加一个未完成报名很多的课程，确认 `Where` 会先过滤再进入分组。
- 把查询拆成三个命名变量，比较“长链式调用”和“分阶段命名”哪种更适合团队阅读。
