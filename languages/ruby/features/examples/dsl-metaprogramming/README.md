# dsl-metaprogramming

## 目标

用一个小型配置校验器理解 Ruby 的元编程与 DSL。例子使用类方法收集字段定义，用块表达领域规则，再用 `define_method` 生成读取结果的方法。

## 运行

```bash
ruby main.rb
```

## 观察点

- `required :host` 和 `number :port` 看起来像声明，实际是类方法在记录规则。
- `instance_eval(&block)` 改变块的执行上下文，让 DSL 使用者不必反复写接收者名称。
- `define_method` 根据规则名生成实例方法，减少重复样板；真实项目中应控制这种技巧的范围，并写清楚错误信息。
