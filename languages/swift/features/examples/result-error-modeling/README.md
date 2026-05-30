# Result Error Modeling

## 目标

这个例子展示 Swift 的 `Result<Success, Failure>` 如何把成功和失败都作为普通值返回。`validateSignup` 不抛出错误，而是返回 `.success(Account)` 或 `.failure(SignupError)`，调用方用 `switch` 明确处理两条路径。

学习重点是区分 `throws` 和 `Result`：`throws` 更适合顺序调用中的提前失败，`Result` 更适合把结果保存、传递、排队、组合，或者在回调和状态机中表达一次操作的最终状态。

## 特性说明

`SignupError` 是遵循 `Error` 的枚举，每个 case 表示一种可恢复的表单错误，并能携带上下文。`Result<Account, SignupError>` 的类型签名说明：成功时一定得到 `Account`，失败时一定得到 `SignupError`。这比返回 `(Account?, String?)` 更安全，因为元组可能出现两个值都为空或两个值都有的矛盾组合。

调用方使用 `switch` 处理结果，和枚举关联值一样，成功和失败是互斥的。这个模型适合表单验证、批处理、异步任务完成事件、缓存读取等场景，因为结果可以先收集起来，稍后再统一展示或统计。

如果不用 `Result`，代码可能会退化成布尔返回值加全局错误变量，或返回 Optional 丢掉失败原因。布尔值只能告诉你“过了没有”，不能告诉你为什么失败；Optional 只能表达“有或没有”，也无法区分空邮箱、邮箱格式错误和密码太短。

## 设计取舍

`Result` 的收益是结果可以像普通数据一样流动，尤其适合跨异步边界或需要批量处理的地方。失败类型也可以被限制成领域错误，让调用方不必处理无关错误。代价是顺序流程中每一步都要 `switch` 或 `flatMap`，可能比 `throws` 啰嗦。

这个例子选择 `Result`，因为表单验证结果会被循环打印，且每次尝试都独立存在。若这是一个读取配置后立即启动服务的流程，`throws` 可能更简洁。Swift 同时提供两种模型，是为了让 API 根据边界选择表达方式，而不是用一种错误机制覆盖所有场景。

## 运行

```bash
swift main.swift
```

## 观察点

- 第一条输入会输出标准化后的邮箱，说明成功路径携带的是强类型 `Account`。
- 其余输入会分别输出空邮箱、非法邮箱和弱密码，说明失败路径保留了具体原因。
- `switch` 强制调用方同时考虑 `.success` 和 `.failure`，不会只处理成功后忘记错误。
- `Result` 本身是枚举，因此它和自定义状态枚举使用的是同一套模式匹配思想。

## 延伸练习

- 把 `validateSignup` 改成 `throws -> Account`，比较调用方 `do/catch` 和 `switch` 哪个更适合这个循环。
- 为 `SignupError` 增加 `case disposableDomain(String)`，拒绝某些邮箱域名。
- 使用 `map` 把成功的 `Account` 转成欢迎消息，观察失败值如何保持不变。
- 把多次验证结果存入数组，统计成功和失败数量，体会 `Result` 作为普通值的优势。
