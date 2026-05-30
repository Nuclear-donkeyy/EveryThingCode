# modules-mixins

## 目标

通过一个可审核对象的小例子理解 Ruby 的 module / mixin。例子展示模块既可以作为命名空间，也可以通过 `include` 把一组行为混入多个类，让不同领域对象共享能力而不强迫它们进入同一条继承链。

这个例子对应 Ruby 的模块组合思想。真实工程中，订单、工单、配置变更、用户资料都可能需要“记录事件”“判断状态”“格式化输出”等横切能力，但它们并不天然是同一种父类。module 让这些能力按角色复用，避免为了共享两个方法而制造抽象父类。

## 特性说明

`Auditable` 定义了 `record_event` 和 `audit_trail`。`Order` 与 `Deployment` 通过 `include Auditable` 获得这两个实例方法，同时保留各自的构造参数和业务方法。调用方不需要知道行为来自模块还是类本身，只要对象能响应 `record_event` 和 `audit_trail`，就能参与审核流程。

如果不用 mixin，代码常会退化成重复复制方法，或建立一个模糊的 `AuditableBase` 父类。复制会让修复和改动散落多处；父类会把不相关对象绑到同一继承层级里。Ruby 选择 module，是因为它已经有动态消息派发和开放对象模型，组合一组方法比提前设计庞大层级更贴近日常业务变化。

## 设计取舍

模块混入的优点是轻量、局部、容易复用。它适合表达“这个对象也具备某种能力”，例如可序列化、可验证、可审核。模块还可以作为命名空间，避免常量和类名污染全局。

代价是方法来源可能变多。一个对象的方法可能来自自身、父类、多个 included modules 和 prepended modules；如果模块太大或命名太泛，就会增加查找成本甚至产生命名冲突。因此 mixin 应保持小而具体，方法名要贴近协议，并用 `ancestors` 或测试确认查找顺序。模块不是继承的万能替代品，它更适合共享能力，而不是表达严格的“是什么”关系。

## 运行

```bash
ruby main.rb
```

## 观察点

- `Order.ancestors` 和 `Deployment.ancestors` 中都能看到 `Auditable`，说明模块进入了方法查找链。
- 两个类没有共同业务父类，却都能调用 `record_event` 和 `audit_trail`。
- 输出中的审核记录保留了各自对象的业务动作，说明 mixin 提供的是横切能力，不接管领域模型。
- `Auditable` 内部使用实例变量 `@audit_events`，展示模块也会依赖宿主对象状态，因此命名和初始化策略要谨慎。

## 延伸练习

- 给 `Auditable` 增加 `last_event` 方法，观察两个类是否都自动获得新能力。
- 新增 `Ticket` 类并 `include Auditable`，只写自己的业务方法，验证模块复用成本。
- 故意在 `Order` 中定义同名 `audit_trail`，观察类自身方法和模块方法的优先级。
- 把 `include Auditable` 改成 `prepend Auditable` 并在模块方法里调用 `super`，比较两种方法查找顺序。
