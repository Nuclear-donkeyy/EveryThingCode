# dsl-metaprogramming

## 目标

用一个小型配置校验器理解 Ruby 的元编程与 DSL。例子使用类方法收集字段定义，用块表达领域规则，再用 `define_method` 生成读取结果的方法。

这个例子对应 Ruby 的 metaprogramming 和 internal DSL 思想：Ruby 代码本身可以被组织成接近领域声明的小语言。真实工程里，路由、任务、测试规格、配置校验、表单字段和权限规则经常有大量重复结构；DSL 把重复样板压缩成少量声明，让读者先看到领域规则，而不是每条规则背后的对象装配过程。

## 特性说明

`ConfigSchema.build do ... end` 创建一个继承自 `ConfigSchema` 的匿名类，并用 `instance_eval(&block)` 在这个类的上下文中执行块。因此块里的 `required :host`、`number :port` 看起来像配置语言，实际调用的是类方法。每个类方法一方面把校验 lambda 存入 `rules`，另一方面通过 `define_method` 为实例生成读取字段的方法。

这解决了“重复声明 + 重复读取”的工程问题。如果不用 DSL，使用者可能要手写数组或哈希描述规则，再手写一堆读取方法，或者在每个配置类里复制相似的校验逻辑。Ruby 允许类在运行期继续接收消息、定义方法和保存状态，所以框架作者可以把重复结构收束到基类中，把变化点留给声明块。

## 设计取舍

DSL 的收益是把领域意图前置。`required :host` 比 `rules[:host] = ...` 更像业务规则，也更容易被非框架作者阅读。动态方法还能减少样板，让 `valid.host` 这种使用方式自然成立。

代价是跳转和调试不如显式代码直接。`host` 方法不是写在源码里的 `def host`，而是在运行期由 `define_method` 生成；`required` 的接收者也被 `instance_eval` 改成了 schema 类。过度使用这类技巧，会让维护者难以搜索方法来源。好的 Ruby DSL 应该边界小、错误清楚、命名贴近领域，并且把元编程留在框架层，不把普通业务判断藏进动态字符串和神秘回调里。

## 运行

```bash
ruby main.rb
```

## 观察点

- `required :host` 和 `number :port` 看起来像声明，实际是类方法在记录规则。
- `instance_eval(&block)` 改变块的执行上下文，让 DSL 使用者不必反复写接收者名称。
- `define_method` 根据规则名生成实例方法，减少重复样板；真实项目中应控制这种技巧的范围，并写清楚错误信息。
- 有效配置输出 `localhost:4567`，说明 `host` 和 `port` 读取方法是在声明规则时生成的。
- 无效配置输出 `host is required` 和 `port must be a number`，说明 DSL 声明被转成了可执行校验逻辑。

## 延伸练习

- 新增 `string :name` 或 `boolean :ssl` 规则，体会 DSL 如何把新声明映射到校验 lambda。
- 在 `required` 中加入 `respond_to?` 或类型检查错误提示，比较“动态灵活”和“错误清楚”的平衡。
- 去掉 `instance_eval`，改成 `yield schema`，让 DSL 写成 `schema.required :host`，比较显式接收者和简洁声明的取舍。
- 把 `rules` 从哈希改成数组，允许同一字段有多条规则，观察 DSL 内部结构如何影响扩展能力。
