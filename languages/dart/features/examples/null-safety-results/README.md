# null-safety-results

## 目标

这个例子展示 Dart 的 sound null safety 如何改变业务建模方式。输入数据来自外部边界：缓存、JSON、表单或命令行参数都可能缺字段、给出空字符串，甚至把某个键映射到 `null`。代码允许 `Map<String, String?>` 在边界处承认这种不确定性，但一旦创建 `UserProfile`，`id` 和 `displayName` 就恢复为非空字段。

学习目标不是记住几个空值操作符，而是看见“缺失”应该成为显式模型。`loadProfile` 不返回 `UserProfile?`，而是返回 `ProfileResult`，把找到、缺失、无效三种结果分开。调用方用 `switch` 穷尽处理所有结果，不需要猜 `null` 到底代表“用户不存在”还是“数据坏了”。

## 特性说明

Dart 默认类型不可为 `null`，只有写成 `T?` 才表示可空。这个例子的 `rawProfiles` 使用 `String?`，因为它模拟外部数据源；`UserProfile.displayName` 使用 `String`，因为领域对象只允许有效姓名。`rawName == null || rawName.trim().isEmpty` 这段判断完成后，编译器能把后续的 `rawName` 当成非空值使用，这就是 null safety 配合类型提升的价值。

代码还把 sealed class 和模式匹配放在一起。`ProfileResult` 是封闭的结果族，`Found`、`Missing`、`Invalid` 是允许出现的全部情况。`describe` 中的 `switch` 可以按结果类型解构字段，例如 `Found(:final profile)` 直接取出有效对象。真实工程里，类似写法常用于登录结果、表单校验、缓存读取和远端接口响应。

## 设计取舍

如果不用这个特性，常见退化方式是让函数返回 `UserProfile?`，然后在调用处写 `if (profile == null)`。这种写法短，但信息量太少：调用者不知道失败原因，也容易把所有失败都显示成同一句错误提示。另一种退化方式是到处使用 `!` 强制解包，它会把类型系统发现的问题推迟到运行时，等到线上出现偶发崩溃才暴露。

本例的取舍是多写几个小类型，换来更清晰的边界。sealed 结果类型会让代码比单纯返回 `null` 稍长，但它让调用方必须面对所有状态，并且让测试可以逐一覆盖。`Map<String, String?>` 仍然保留在输入边界，因为真实数据确实不干净；区别在于脏数据不会继续污染领域模型。

## 运行

```bash
dart run main.dart
```

## 观察点

- `Map<String, String?>` 只在外部输入边界允许 `null`，进入 `UserProfile` 后字段恢复为非空。
- `containsKey` 和判空把“没有这个 id”与“id 存在但名字无效”分开。
- `switch` 覆盖所有结果类型，调用方不用猜 `null` 代表哪种失败。
- 全例没有使用 `!`，因为类型和结果模型已经把缺失状态表达清楚。
- 运行输出会分别打印成功问候、空白姓名、缓存空值和缺失用户，验证同一个入口能产生不同的显式结果。

## 延伸练习

- 给 `UserProfile` 增加 `email` 字段，并规定邮箱可以缺失还是必须有效；比较 `String?` 与单独 `Invalid` 分支的表达差异。
- 新增 `Blocked` 结果类型，观察 `describe` 的 `switch` 是否需要补充分支。
- 故意把 `rawName.trim()` 移到判空之前，看看分析器会如何提醒可空值风险。
- 把 `Map` 替换成模拟 JSON 的 `Map<String, Object?>`，练习在外部边界做类型检查后再进入领域对象。
