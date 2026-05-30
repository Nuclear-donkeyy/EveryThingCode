# try-with-resources

## 目标

这个例子展示 Java 的 `try-with-resources` 如何管理外部资源边界。导入订单行时，程序打开一个 `LineCursor` 读取输入，同时打开 `AuditTrail` 记录审计信息；第二行输入故意是坏格式，解析失败后仍然会关闭两个资源。

真实工程中，GC 会回收普通对象内存，但不会替你及时释放文件句柄、Socket、数据库连接、锁或审计缓冲区。资源关闭如果依赖人工在每个分支里写 `close()`，很容易在异常路径漏掉。本例希望你观察：把资源放进 `try (...)` 后，Java 会在离开作用域时按规则关闭它们，并保留关闭阶段发生的附加异常。

## 特性说明

`LineCursor` 和 `AuditTrail` 都实现 `AutoCloseable`。`importOrders` 在 `try (LineCursor cursor = ...; AuditTrail audit = ...)` 中创建资源，然后读取并解析每一行。遇到 `BROKEN-LINE` 时，`parse` 抛出 `IOException`，主流程失败；即便如此，Java 仍会先关闭 `AuditTrail`，再关闭 `LineCursor`。

`AuditTrail.close()` 故意抛出 `IOException`，用于展示 suppressed exception。主异常是“invalid csv line”，关闭审计资源时的“audit flush failed”不会覆盖主异常，而是被挂到 suppressed 列表里。例子把底层 `IOException` 包装成领域更清楚的 `ImportFailedException`，同时保留 cause 和 suppressed 信息。

如果不用 `try-with-resources`，你需要手写 `finally`，并小心处理“业务异常”和“关闭异常”同时发生的情况。很多代码会不小心让关闭异常覆盖原始失败，或者为了省事吞掉关闭异常，排查线上问题时就缺少关键线索。

## 设计取舍

Java 没有把所有资源都交给析构函数自动释放，因为对象被 GC 的时间不可预测。`try-with-resources` 选择用词法作用域表达资源生命周期：资源从哪里打开，就在离开哪段代码时关闭。这让生命周期比“等某个对象未来被回收”更确定。

代价是资源类型需要实现 `AutoCloseable`，调用方也需要把边界写出来。好处是边界非常清楚，异常传播规则可预测，并且能和受检异常配合，让 I/O、解析、关闭失败都出现在方法签名或处理逻辑里。

## 运行

```bash
javac Main.java && java Main
```

## 观察点

- 输出先出现 `open line cursor`，然后第一行订单被审计，说明资源在进入 try 块时创建。
- 遇到 `BROKEN-LINE` 后，仍会输出 `close audit trail` 和 `close line cursor`，说明异常路径也执行关闭。
- `cause: invalid csv line: BROKEN-LINE` 是真正导致导入失败的主异常。
- `suppressed during close: audit flush failed` 说明关闭资源时也失败了，但它没有覆盖主异常。

如果把资源创建移到普通代码里，并删除 `try-with-resources`，解析失败时很容易跳过关闭逻辑。真实项目中这会表现为文件无法删除、连接池耗尽或审计数据卡在缓冲区。

## 延伸练习

- 让输入全部合法，观察 `ImportReport` 正常返回时资源是否仍然关闭。
- 删除 `AuditTrail.close()` 中的异常，比较 suppressed 输出如何变化。
- 增加第三个资源，观察关闭顺序是否与创建顺序相反。
- 把 `ImportFailedException` 改成运行时异常，再讨论调用方是否还能从方法签名看见导入失败。
