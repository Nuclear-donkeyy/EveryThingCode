# isolates-message-passing

## 目标

这个例子展示 Dart isolate 的基本思想：CPU 密集计算应该和主执行上下文隔离，通过消息把结果传回来。代码统计一定范围内的质数数量和总和，这类工作如果放在 Flutter 主 isolate 中执行，可能让界面暂停响应；放进 worker isolate 后，主 isolate 可以继续处理 UI 或输入。

学习目标是分清“异步等待”和“并行计算”。`Future` 可以表示稍后完成的结果，但它不会自动把重计算移出当前 isolate。`Isolate.run` 则会在新的 isolate 中执行函数，并把可发送的返回值传回调用方。

## 特性说明

Dart 的 isolate 有独立内存，彼此不共享普通对象。这个模型和共享内存线程不同：worker isolate 不能直接改主 isolate 的变量，只能接收输入并发送结果。`Isolate.run(() => countPrimes(max))` 是标准库提供的简洁入口，适合一次性后台计算；更复杂的长期 worker 可以使用 `ReceivePort` 和 `SendPort` 建立消息通道。

本例的 `countPrimes` 返回一个 record `({int count, int sum})`，它是可发送的简单数据。主 isolate 通过 `await resultFuture` 等待结果，再用 record 解构取出 `count` 和 `sum`。这也说明 isolate 之间通信应该设计成清晰的消息协议，而不是依赖共享可变状态。

## 设计取舍

如果只给 `countPrimes` 加上 `async`，函数内部的循环仍然会在当前 isolate 执行，CPU 时间照样会阻塞 UI 或命令行主流程。`async` 主要改善等待 I/O 的可读性，不负责自动并行。把计算放入 isolate 的好处是隔离明确、数据竞争少；代价是跨 isolate 的数据需要复制或转移，启动 isolate 也有成本。

因此 isolate 不适合每个小函数都使用。它更适合解析大 JSON、图片处理、压缩加密、复杂搜索等明显耗 CPU 的任务。真实 Flutter 项目还要考虑任务取消、错误回传和进度消息；本例先保留一次性计算，让消息传递边界最清楚。

## 运行

```bash
dart run main.dart
```

## 观察点

- 输出会先打印主 isolate 的提示，再等待 worker isolate 返回质数统计结果。
- `Isolate.run` 的返回值仍然表现为 `Future`，说明并行计算结果也可以接入常规异步流程。
- worker 返回的是简单 record，而不是共享对象引用，体现 isolate 的消息传递边界。
- 这个例子没有让多个 isolate 同时修改同一个变量，因此不会出现共享线程常见的数据竞争。

## 延伸练习

- 把 `max` 调大，比较计算耗时变化，并思考 isolate 启动成本是否值得。
- 先直接调用 `countPrimes(max)`，再改回 `Isolate.run`，比较代码结构和主流程输出顺序。
- 把返回值改成包含前 10 个质数的列表，确认简单集合也能作为消息返回。
- 进一步使用 `ReceivePort` 发送进度消息，把一次结果扩展成“计算进度流”。
