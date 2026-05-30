# null-safety-results

## 目标

这个例子展示 sound null safety 如何改变建模方式。输入数据来自外部边界，所以用户名可能缺失、为空或根本不存在；领域对象 `UserProfile` 的字段则保持非空。代码用 sealed class 表达查找结果，而不是用 `null` 或 `!` 把失败路径藏起来。

## 运行

```bash
dart run main.dart
```

## 观察点

- `Map<String, String?>` 只在外部输入边界允许 `null`，进入 `UserProfile` 后字段恢复为非空。
- `containsKey` 和判空把“没有这个 id”与“id 存在但名字无效”分开。
- `switch` 覆盖所有结果类型，调用方不用猜 `null` 代表哪种失败。
- 全例没有使用 `!`，因为类型和结果模型已经把缺失状态表达清楚。
