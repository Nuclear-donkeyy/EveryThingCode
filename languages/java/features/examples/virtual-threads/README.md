# virtual-threads

## 目标

这个例子展示 Java 虚拟线程如何让阻塞式任务保持顺序可读，同时并发等待多个慢操作。三个库存查询都用 `Thread.sleep` 模拟 I/O 等待；使用虚拟线程后，调用方仍然写普通方法和 `Future.get()`，但总耗时接近最慢的单个查询。

## 运行

```bash
javac Main.java && java Main
```

## 观察点

- `Executors.newVirtualThreadPerTaskExecutor()` 为每个任务创建虚拟线程，适合大量等待型任务。
- `try-with-resources` 会在离开作用域时关闭 executor，表达任务生命周期边界。
- 虚拟线程降低等待成本，但共享状态、超时、取消和下游容量仍需要设计。
