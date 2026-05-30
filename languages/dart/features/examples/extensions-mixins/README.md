# extensions-mixins

## 目标

这个例子展示 Dart 中 class、mixin 和 extension 的分工。`LessonTask` 是有字段和核心行为的领域对象，`ScoredTask` mixin 复用评分逻辑，`LessonTaskList` extension 给任务列表补充汇总方法。

## 运行

```bash
dart run main.dart
```

## 观察点

- class 负责对象身份、构造函数、字段和核心方法。
- mixin 适合复用一组依赖很少的行为，本例通过抽象 getter 要求宿主提供数据。
- extension 不修改 `Iterable<LessonTask>` 的定义，却能让调用处读成领域语言。
- 组合优先于继承层级：新增另一种可评分任务时，可以复用 mixin 而不必塞进同一棵基类树。
