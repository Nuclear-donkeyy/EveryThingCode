# Python syntax-tour

## 目标

这个示例把 Python 基础语法串成一个小型“任务汇总”脚本。读者可以看到变量绑定、字符串格式化、条件分支、`for` / `range`、函数、集合、轻量数据模型、异常和 `with` 如何一起工作。它不是框架项目，也不引入第三方依赖，重点是让你用一个文件观察 Python 的日常表达方式。

## 覆盖语法

- 变量绑定与常量命名：`DEFAULT_OWNER`、列表对象和函数返回值。
- 基础类型与字符串：`int`、`bool`、`str`、`None`、f-string 和格式化输出。
- 控制流：`if` / `elif` / `else` 兼容 Python 3.9，`for`、`range`、`continue`。
- 函数：类型标注、默认参数、用 `None` 避免可变默认参数共享。
- 集合：`list` 保存任务，`dict` 统计状态，`set` 去重标签，`tuple` 返回汇总结果。
- 数据建模：`@dataclass` 表达轻量任务记录，并在 `__post_init__` 中维护不变量。
- 错误处理和资源边界：捕获 `ValueError`，使用 `with` 和 `TemporaryDirectory` 管理临时文件。
- 模块认知：从标准库导入 `dataclasses`、`pathlib`、`tempfile`、`typing` 中的名字。

## 运行

```bash
python3 main.py
```

如果你在仓库根目录，也可以先进入示例目录再运行：

```bash
cd languages/python/syntax/examples/syntax-tour
python3 main.py
```

## 观察点

输出会先打印任务摘要，再打印按状态统计的字典、去重后的标签集合，以及临时写入文件的路径和内容。脚本中 `parse_priority` 会故意收到一个非法优先级字符串，随后捕获 `ValueError` 并回退到默认值；这展示了 Python 常见的“先尝试，再处理具体异常”的风格。

注意 `collect_tags` 的参数默认值是 `None`，函数内部再创建新列表。这样每次调用都得到独立列表，避免 `def collect_tags(tasks, tags=[])` 这类可变默认参数在多次调用间共享状态。还可以观察 `summarize` 返回的是一个二元 `tuple`，调用方可以直接解包成 `done_count, open_count`。

## 修改练习

- 给 `Task` 增加 `estimate_hours` 字段，并在摘要中输出总工时。
- 把 `status_label` 中的 `if` / `elif` 改成字典分发表，比较哪种更清楚。
- 在任务列表里加入一个空标题，观察 `__post_init__` 抛出的异常。
- 修改 `range(1, 4)` 的边界，确认右边界不包含在结果里。
- 把临时文件内容改成 JSON 字符串，再用标准库 `json` 读取回来。
