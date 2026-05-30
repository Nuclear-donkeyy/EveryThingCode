# extensions-mixins

## 目标

这个例子展示 Dart 中 class、mixin 和 extension 的分工。`LessonTask` 是有字段、构造函数和核心行为的领域对象；`ScoredTask` mixin 复用“得分/满分/等级”这一组能力；`LessonTaskList` extension 给 `Iterable<LessonTask>` 补充领域化的汇总方法。

学习目标是避免把所有复用都塞进继承。真实项目里，课程任务、测验、项目作业都可能需要评分，但它们不一定共享同一个父类；同时，标准库的 `Iterable` 已经存在，我们无法也不应该修改它的源码。mixin 和 extension 让“对象身份”“可复用能力”“调用便利语法”分开放置。

## 特性说明

`class LessonTask with ScoredTask` 表示 `LessonTask` 组合了一个可复用能力。`ScoredTask` 不保存字段，而是声明 `earnedPoints` 和 `totalPoints` 两个 getter，由宿主类提供数据；mixin 自己只负责计算 `completionRatio` 和 `gradeLabel`。这种方式适合“多个类型都能做同一类计算，但数据来源由各自类型决定”的场景。

`extension LessonTaskList on Iterable<LessonTask>` 则给任务集合增加 `earnedTotal`、`possibleTotal` 和 `firstNeedsPractice`。调用处可以写 `tasks.earnedTotal`，读起来像领域语言，但没有修改 `Iterable` 本身，也没有要求每个列表都继承某个自定义集合类。Flutter 和 Dart 业务代码常用 extension 为字符串、日期、集合或领域模型增加小而明确的表达。

## 设计取舍

如果所有逻辑都放进 class，`LessonTask` 会越来越胖，集合级别的操作也可能散落成工具函数。工具函数虽然简单，但调用处 `earnedTotal(tasks)` 不如 `tasks.earnedTotal` 贴近“这批任务的总得分”。extension 的取舍是可发现性：方法不是原类型定义的一部分，团队需要通过命名和导入边界控制它的范围。

如果所有复用都靠继承，任务类型很快会被迫进入同一棵基类树。继承适合表达“是一个”的身份关系，mixin 更适合表达“具备某种能力”。mixin 的代价是行为来源可能变得分散，所以本例让 mixin 很小，只依赖两个抽象 getter，并把真正的数据仍放在 class 里。

## 运行

```bash
dart run main.dart
```

## 观察点

- class 负责对象身份、构造函数、字段和核心方法。
- mixin 适合复用一组依赖很少的行为，本例通过抽象 getter 要求宿主提供数据。
- extension 不修改 `Iterable<LessonTask>` 的定义，却能让调用处读成领域语言。
- 组合优先于继承层级：新增另一种可评分任务时，可以复用 mixin 而不必塞进同一棵基类树。
- 运行输出先打印每个任务的评分标签，再打印集合总分和需要复习的任务，分别验证对象级、能力级和集合级逻辑。

## 延伸练习

- 新增一个 `QuizAttempt` class，同样 `with ScoredTask`，但字段名或构造方式不同，观察 mixin 是否仍然可复用。
- 给 extension 增加 `averageRatio`，注意处理空集合，避免除以零。
- 把 `gradeLabel` 从 mixin 移回 `LessonTask`，比较新增第二种可评分类型时会出现多少重复。
- 尝试把 extension 改成顶层函数，比较调用处的可读性和导入后的 API 暴露范围。
