# future-streams

## 目标

这个例子区分 Dart 中两种常见异步形状：`Future` 表示稍后得到的一次结果，`Stream` 表示按时间到达的多次事件。代码模拟加载用户摘要和任务进度，不依赖网络或外部包。

## 运行

```bash
dart run main.dart
```

## 观察点

- `Future.wait` 收集多个一次性异步结果，适合“等全部完成再继续”的场景。
- `await for` 按顺序消费 `Stream` 事件，适合进度、消息、传感器读数等持续输入。
- `async/await` 让等待期间事件循环可以继续处理别的任务，但它不等于并行 CPU 计算。
- 真正耗 CPU 的工作应该考虑 isolate；本例的延迟只是模拟 I/O 等待。
