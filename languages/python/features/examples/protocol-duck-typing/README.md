# protocol-duck-typing

## 目标

理解 Python 为什么常说“看行为而不是只看继承”，并观察 `typing.Protocol` 如何把 duck typing 的隐式约定写成可阅读、可检查的接口。

## 特性说明

这个例子对应 protocol 与 duck typing。订单发布函数 `publish_paid_orders()` 并不关心日志写到终端、内存、文件还是消息队列；它只关心接收者是否有 `write_event(event)` 这个行为。`ConsoleSink` 和 `MemorySink` 没有共同基类，却都能作为接收者使用，因为它们满足同一个小协议。

这种特性解决的真实工程问题是解耦。业务函数如果直接依赖某个具体类，测试时就必须构造真实输出目标，换成别的基础设施时也要改业务代码。用行为协议表达边界后，生产环境可以传终端或网络实现，测试可以传内存实现，函数主体保持稳定。`Protocol` 的价值在于把原本只存在于人脑里的“只需要这个方法”写进类型标注，让编辑器和类型检查工具更容易发现不匹配。

## 设计取舍

duck typing 的好处是轻量，不需要为每个小边界都设计继承层级；代价是协议过大或命名含糊时，错误会延后到调用处。`Protocol` 缓解了这个问题，但它主要是开发期工具，不会自动校验外部输入。真实项目里，公共 API 边界常用 `Protocol`、抽象基类或清晰的测试替身共同约束；内部小函数则可以保持更自然的动态风格。

如果不用这个特性，代码通常会退化成两种形态：要么 `publish_paid_orders()` 写死 `ConsoleSink`，导致复用困难；要么用 `if isinstance(...)` 分支识别每种接收者，导致业务函数知道太多实现细节。本例把边界压缩成一个方法，展示了 Python 倾向于用小协议连接对象。

## 运行

```bash
python3 main.py
```

## 观察点

- 输出中同一批已支付订单会先写到 `ConsoleSink`，再写到 `MemorySink`，业务函数没有变化。
- `MemorySink.summary()` 证明内存实现可以额外保存状态，但协议只暴露 `write_event()` 这一个必要行为。
- `EventSink` 没有要求继承，类只要结构上拥有同名方法，就能满足这段代码的需求。
- 如果把 `MemorySink.write_event` 改名，类型标注和运行调用都会暴露协议不匹配。

## 延伸练习

- 新增一个 `FileSink`，把事件写到临时文件，再传给 `publish_paid_orders()`。
- 给 `EventSink.write_event()` 增加返回值，观察两个实现和调用方需要怎样同步修改。
- 删除 `Protocol` 标注，只保留运行时 duck typing，比较代码仍能运行但边界说明变少的差异。
- 写一个测试替身 `CountingSink`，只统计调用次数，体会小协议如何降低测试成本。
