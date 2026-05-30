# duck-typing-protocols

## 目标

通过多个报告输出对象理解 duck typing：调用方不关心对象属于哪个类，只要求它能响应 `write`。例子同时展示 `ensure` 如何保证文件资源在成功或失败后都被关闭。

## 运行

```bash
ruby main.rb
```

## 观察点

- `ReportPrinter` 只调用 `writer.write(line)`，这就是它需要的最小协议。
- `ConsoleWriter`、`MemoryWriter`、`FileWriter` 没有共同父类声明，但都能被同一个打印流程使用。
- `FileWriter#close` 使用 `ensure`，即使关闭时发生错误，也会清掉内部文件引用，避免对象继续持有失效资源。
