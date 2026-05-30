# asyncio-task-group

## 目标

理解 `asyncio` 如何把等待 I/O 的时间让出来，并观察 `TaskGroup` 如何把一组并发任务限制在同一个生命周期边界内。

这个例子并发读取三个模拟探针。Python 3.11 及以上会使用 `asyncio.TaskGroup`；旧版本会使用 `asyncio.gather()` 兼容运行。

## 运行

```bash
python3 main.py
```

## 观察点

- `await asyncio.sleep(...)` 代表一次 I/O 等待，等待期间事件循环可以调度其他任务。
- `TaskGroup` 把创建任务和等待任务放在同一个 `async with` 块中。
- 单个探针失败被转换成结果对象，调用方仍能展示整批任务的状态。
