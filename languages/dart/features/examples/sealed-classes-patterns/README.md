# sealed-classes-patterns

## 目标

这个例子展示 Dart 的 sealed class 和 pattern matching 如何表达有限状态。结账流程不会处在任意字符串状态中，它只能是编辑购物车、等待支付、已支付或失败。把这些状态写成 `CheckoutState` 的 sealed 子类，可以让编译器和调用方都知道状态集合是封闭的。

学习目标是用类型系统替代脆弱的状态码。真实业务里，订单、登录、加载页面、权限申请、表单提交都有类似“有限个状态，每个状态携带不同数据”的结构。sealed class 让每个状态拥有自己的字段，pattern matching 让读取这些字段的代码保持紧凑。

## 特性说明

`sealed class CheckoutState` 声明一个封闭的父类型，当前库里定义的 `EditingCart`、`AwaitingPayment`、`Paid`、`Failed` 构成这个状态族。`renderCheckout` 使用 `switch` 表达式按具体子类型处理状态，并通过对象模式取出字段，例如 `AwaitingPayment(:final orderId, :final total)`。

例子里还有一个带 guard 的分支：`EditingCart(items: final items) when items.isEmpty`。它先匹配购物车状态，再额外检查列表是否为空。这样可以把“空购物车”和“有商品的购物车”写在同一个状态类型下，而不是为了每个细节都扩展一个子类。

## 设计取舍

如果不用 sealed class，常见退化是给订单放一个 `String status`，再把 `total`、`receiptCode`、`reason` 都做成可空字段。这样对象看起来灵活，却允许很多非法组合，例如 `status == 'paid'` 但没有收据号，或 `status == 'failed'` 却还带着支付金额。调用方也会散落大量字符串比较。

sealed class 的取舍是类型数量增加，但状态边界更清楚。每个子类只携带自己真正需要的数据，`switch` 也能提示你补齐分支。pattern matching 的取舍是语法需要熟悉；一旦掌握，它比手写 `is` 判断和强制转换更少样板，也更不容易漏掉字段。

## 运行

```bash
dart run main.dart
```

## 观察点

- 运行输出会覆盖空购物车、有商品、等待支付、支付成功和支付失败五种路径。
- `switch` 分支直接解构字段，没有写 `as AwaitingPayment` 之类的手动转换。
- `when items.isEmpty` 说明 pattern 可以和额外条件组合，适合表达状态中的细分规则。
- 每个状态类只声明自己需要的字段，避免一个大对象堆满互相矛盾的可空属性。

## 延伸练习

- 新增 `Refunded` 状态，观察 `renderCheckout` 是否需要补充分支。
- 把 `Failed.reason` 改成错误码和用户提示两个字段，再用 pattern 同时取出它们。
- 尝试改回 `String status` 加多个可空字段，比较调用处需要多少判空和字符串判断。
- 为 `AwaitingPayment` 增加超时状态时，思考应该新增子类还是用 guard 细分。
