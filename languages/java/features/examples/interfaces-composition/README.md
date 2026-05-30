# interfaces-composition

## 目标

这个例子展示 Java 如何用 interface 定义行为边界，并用组合把多个可替换策略装配成一个业务流程。结账服务需要折扣、税费和收据输出，但它不应该继承某个“会员结账类”或“普通结账类”才能变化；它只依赖 `DiscountPolicy`、`TaxPolicy` 和 `ReceiptSink` 这些能力接口。

真实工程里的变化点通常不是整棵对象层级一起变化，而是某几个规则单独变化：促销规则会换，税率会换，输出渠道会从控制台变成邮件或消息队列。如果用继承表达这些组合，很快会出现 `MemberCheckoutWithEmailReceipt` 之类的类爆炸。本例希望你观察：组合让对象按能力拼装，变化被限制在小接口和实现类里。

## 特性说明

`CheckoutService` 通过构造器接收三个接口，而不是自己创建具体实现。`NoDiscount` 和 `PercentageDiscount` 都实现 `DiscountPolicy`，调用方可以在不修改结账流程的情况下切换折扣规则。`FixedRateTax` 实现税费规则，`ConsoleReceipt` 负责输出。

Java 的接口是名义类型边界：一个类明确声明 `implements DiscountPolicy`，就承诺提供 `discountFor` 行为。这和“对象刚好有同名方法”的结构类型不同，更适合多人协作和长期维护的 API。调用方看到接口就知道它依赖哪种能力，而不是依赖某个具体类的全部细节。

如果不用接口组合，结账逻辑通常会退化成一个巨大方法，里面根据用户等级、地区、渠道写满 `if/else`；或者退化成继承层级，每新增一种折扣和输出组合都要加一个子类。两种写法都会让变化点互相缠绕。

## 设计取舍

接口组合的好处是解耦和可测试。你可以给 `CheckoutService` 传入一个测试用的 `ReceiptSink`，只验证收据内容，不必真的写控制台、文件或网络。你也可以在运行时按配置选择不同折扣策略。

代价是小类型会变多，构造关系也需要管理。Java 生态常用依赖注入框架处理这种装配，但本例只用标准库和手写构造器，是为了让边界本身更清楚。学习时要避免“为了接口而接口”：只有存在真实变化点或测试边界时，接口才值得引入。

## 运行

```bash
javac Main.java && java Main
```

## 观察点

- `standard checkout` 和 `member sale checkout` 使用同一个 `CheckoutService` 类，但折扣输出不同，说明行为来自组合进来的策略对象。
- 税费规则没有因为折扣策略变化而改动，说明变化点被拆开。
- `Cart` 和 `CartLine` 使用 `record` 表达值数据，接口只负责行为边界，二者职责不同。
- 如果把 `PercentageDiscount` 的比例改成 `0.50`，只有会员结账的折扣和总价变化，标准结账不受影响。

如果不用这个特性，你需要在 `CheckoutService.checkout` 里写 `if (member)` 或创建多个子类。随着促销、地区税率、输出渠道增加，组合数量会膨胀，核心流程也会越来越难读。

## 延伸练习

- 新增一个 `ThresholdDiscount`：满 200 减 30，然后把它传给 `CheckoutService`。
- 新增一个 `MemoryReceipt`，把收据保存到列表中，模拟单元测试里断言输出。
- 把 `TaxPolicy` 改成按地区计算，比较把地区判断放在策略里和放在 `CheckoutService` 里的差异。
- 故意让 `CheckoutService` 直接 new `PercentageDiscount`，观察它的可替换性和测试便利性如何下降。
