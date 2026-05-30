# context-manager-resource

## 目标

理解上下文管理器如何定义资源边界，并观察 EAFP 如何让数据处理的正常路径保持清楚。

这个例子把订单处理结果写入临时审计日志。`AuditLog` 负责打开和关闭文件，`process_orders()` 只依赖日志对象有 `record()` 行为，体现 Python 常见的 duck typing。

## 运行

```bash
python3 main.py
```

## 观察点

- `with AuditLog(...) as log` 把文件生命周期限制在一个块里。
- `__exit__` 无论处理成功还是中途失败都会关闭文件。
- `process_orders()` 捕获具体的 `KeyError`、`TypeError`、`ValueError`，而不是裸 `except`。
