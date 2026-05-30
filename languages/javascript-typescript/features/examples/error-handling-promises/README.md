# Error Handling Promises

## 目标

通过并发加载多个“配置片段”观察 Promise 错误处理、`try...catch`、`Promise.allSettled` 和自定义 `Error` 的作用。这个例子对应的语言特性是异步错误传播：Promise rejection 会沿 `await` 边界变成可捕获错误，但多个并发任务需要显式收敛。

真实工程中，页面启动、服务初始化、批量 API 请求经常同时发起多个异步任务。如果不用清晰的 Promise 错误边界，代码容易退化成每个任务各写一个零散 `catch`，或者使用 `Promise.all` 时一个失败就丢掉其他任务的诊断信息。

## 特性说明

`loadConfigPart` 模拟三个异步配置来源，其中 `secrets` 会失败并抛出带 `code` 和 `cause` 的 `ConfigLoadError`。`loadAllConfig` 使用 `Promise.allSettled` 等待所有任务结束：成功项进入 `config`，失败项进入 `errors`。这样调用方能同时看到可用配置和失败原因。

示例还在最外层使用 `try...catch` 捕获不可恢复的聚合错误。这里故意没有让单个失败立刻终止流程，是为了展示 Promise 并发的一个常见设计点：有些场景需要 fail fast，有些场景需要收集所有结果后再决定能否继续。

## 设计取舍

`async`/`await` 让异步错误看起来接近同步 `try...catch`，可读性很强。代价是并发边界不再由缩进自动暴露：`await Promise.all(...)`、`await Promise.allSettled(...)` 和循环里逐个 `await` 的行为差异很大。选择哪一种，取决于是否需要并发、是否允许部分成功、是否要保留全部错误。

如果不用自定义错误，调用方只能从字符串里猜失败类型；如果不用 `cause`，底层错误上下文会丢失。真实项目中，错误通常需要包含 `code`、可读消息、原始原因和必要上下文，但也要避免把密钥、令牌等敏感数据放进错误文本。

## 运行

```bash
node main.mjs
```

## 观察点

- `loaded featureFlags` 和 `loaded limits` 证明成功任务不会因为另一个任务失败而消失。
- `failed secrets E_CONFIG_LOAD` 展示自定义错误 code，调用方可以据此分类处理。
- `cause: vault timeout` 保留了底层错误原因，便于定位真实故障。
- 最后的 `startup blocked` 是聚合后的业务决策，而不是任意单个 Promise 偷偷吞错。
- 把 `Promise.allSettled` 改成 `Promise.all` 后，观察输出中还能不能看到所有成功和失败细节。

## 延伸练习

新增一个也会失败的配置项，比较 `Promise.allSettled` 是否能同时报告多个错误。再把 `loadAllConfig` 改成 fail fast 策略：只要任何配置失败就立即抛出，思考这种策略适合支付初始化还是适合加载可选 UI 文案。

还可以在最外层删除 `await main().catch(...)` 的 `catch`，观察 Node 对未处理 rejection 的提示。这个练习能帮助你理解：Promise 错误必须在明确边界被等待、返回或捕获，不能假设运行时会自动把它们变成同步异常。
