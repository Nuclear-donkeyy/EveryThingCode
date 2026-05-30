# context-manager-resource

## 目标

理解上下文管理器如何定义资源边界，并观察 EAFP 如何让数据处理的正常路径保持清楚。

这个例子把订单处理结果写入临时审计日志。`AuditLog` 负责打开和关闭文件，`process_orders()` 只依赖日志对象有 `record()` 行为，体现 Python 常见的 duck typing。

## 特性说明

这个例子对应 Python 的 context manager 思想：资源的获得和释放应该写成一个清楚的词法边界。文件、锁、临时目录、网络连接和数据库事务都不是普通内存对象，它们背后占着操作系统或外部系统资源。如果调用方在每个成功路径和失败路径都手动 `close()`，代码很快会被清理逻辑淹没，而且异常一旦发生就容易漏掉收尾。

`AuditLog` 实现 `__enter__` 和 `__exit__` 后，就能被 `with AuditLog(...) as log` 使用。进入 `with` 时打开文件并记录开始，离开 `with` 时无论订单处理是否抛出异常都会写入关闭日志并关闭句柄。`process_orders()` 的主体采用 EAFP 风格：先按期望读取 `id` 和 `quantity`，遇到缺字段或非法数值时捕获具体异常并记录。这样正常路径保持短，失败路径也没有被吞掉。

这个例子还展示 duck typing：`process_orders()` 实际只需要一个有 `record(message)` 方法的对象。参数类型写成 `AuditLog` 是为了初学时更直观；如果把它换成内存日志、测试替身或网络日志，只要提供同名行为，业务循环就可以复用。

## 运行

```bash
python3 main.py
```

程序会创建一个临时目录，处理四条订单，再打印被接受的数量和审计日志内容。临时目录由标准库自动清理，审计文件由自定义上下文管理器关闭。

## 设计取舍

上下文管理器把资源生命周期集中到对象内部，调用方更难忘记清理，这是它最大的收益。代价是资源对象要实现一个小协议：`__enter__` 返回可用对象，`__exit__` 决定是否吞掉异常。本例的 `__exit__` 返回 `False`，表示如果块内出现未处理异常，异常仍然向外传播；这通常比悄悄吞掉错误更安全。

如果不用 `with`，代码会退化成 `log = AuditLog(...); log.open(); try: ... finally: log.close()` 这样的手写结构。它并非错误，但每个调用处都要重复同一套防漏逻辑。真实项目里，标准库和生态已经把很多资源做成上下文管理器，例如 `Path.open()`、`tempfile.TemporaryDirectory()`、线程锁、数据库事务对象。学习重点不是记住魔术方法名字，而是看到 Python 用语法把“失败时也要清理”的承诺固定下来。

## 观察点

- `with AuditLog(...) as log` 把文件生命周期限制在一个块里。
- `__exit__` 无论处理成功还是中途失败都会关闭文件。
- `process_orders()` 捕获具体的 `KeyError`、`TypeError`、`ValueError`，而不是裸 `except`。
- 输出中先出现 `audit log opened`，最后出现 `audit log closed`，说明资源边界被对象自己维护。
- 非法数量和缺失字段被记录为跳过，而不是让整批订单处理立刻停止。

## 延伸练习

- 在 `process_orders()` 中故意抛出一个未捕获异常，观察 `__exit__` 是否仍会记录关闭信息。
- 新建一个 `MemoryLog`，只把消息追加到列表里，再让 `process_orders()` 使用它，体会 duck typing 的测试价值。
- 把 `__exit__` 改成返回 `True`，观察异常传播行为如何变化，并思考为什么生产代码要谨慎吞异常。
- 使用 `contextlib.contextmanager` 重写 `AuditLog`，比较类实现和生成器实现的可读性。
