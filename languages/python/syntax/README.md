# Python 基础语法速览

## 读者定位

这份速览面向已经写过 C、Java、JavaScript、Go、Rust 或类似语言，但还没有系统写过 Python 的读者。Python 的语法少，真正需要迁移的是心智模型：代码块由缩进决定，变量名只是绑定到对象，类型在运行时跟着对象走，模块文件天然就是命名空间。Python 鼓励把常见流程写得直白，用标准库组合小函数，而不是先设计厚重框架。

如果你来自静态类型语言，要记住类型标注主要服务编辑器、类型检查器和读者，并不自动做运行时校验。如果你来自 JavaScript，要注意 Python 的字典、列表和对象模型更分明，`None`、异常、迭代协议和上下文管理器也有更明确的惯用边界。

## 运行方式

Python 源文件通常以 `.py` 结尾。最小运行方式是：

```bash
python3 main.py
```

当前示例兼容 Python 3.9，因此不会在可运行代码里使用 Python 3.10 才引入的 `match` 语句。日常项目建议使用虚拟环境隔离依赖，但本章示例只依赖标准库。模块被导入时会执行顶层语句，所以可运行脚本常见结构是：

```python
def main() -> None:
    ...


if __name__ == "__main__":
    main()
```

这让同一个文件既能被导入复用，又能直接作为脚本运行。

## 语法速览

Python 用缩进表达代码块，而不是花括号。`if`、`for`、`def`、`class`、`try`、`with` 等语句以冒号结尾，下一层缩进就是它们的块。缩进通常使用 4 个空格；混用 tab 和空格会让代码变得脆弱，解释器也可能直接报错。

变量不需要声明类型。赋值语句是“名字绑定到对象”，不是把对象复制进变量槽：

```python
items = [1, 2]
alias = items
alias.append(3)
print(items)  # [1, 2, 3]
```

这点会影响可变对象、默认参数和函数调用。Python 没有内建常量关键字，常量通常用大写命名表达约定，例如 `MAX_RETRIES = 3`。私有成员也主要靠约定：`_name` 表示模块内部使用，双下划线有名称改写规则，但不是安全边界。

注释使用 `#`。多行字符串可以用三引号，但它本质仍是字符串；函数、类、模块开头的三引号字符串会成为 docstring。

## 类型与值

常见基础类型包括 `int`、`float`、`bool`、`str`、`bytes` 和 `None`。`int` 没有固定溢出宽度，`bool` 是 `int` 的子类但应当按布尔值使用。`None` 表示“没有值”，判断时使用 `is None`，不要用 `== None`。

字符串是不可变 Unicode 文本。最常见的插值方式是 f-string：

```python
name = "Ada"
score = 98.5
message = f"{name} scored {score:.1f}"
```

f-string 在花括号内写表达式，格式说明放在冒号后。它适合生成面向人的文本；如果要拼 SQL、shell 命令或协议内容，应优先使用参数化 API，避免把转义问题藏进字符串模板。

Python 的“真值”规则会把空字符串、空集合、数字零和 `None` 视为假。迁移时常见误解是把 `if value:` 当成“不是 None”。如果空列表和缺失值有不同含义，应写成 `if value is not None:`。

## 控制流

`if` / `elif` / `else` 是基本条件分支。Python 没有 C 风格的 `switch`。Python 3.10 引入了结构化模式匹配 `match` / `case`，可匹配字面量、元组、类和字典形状；但为了兼容 3.9，库代码或教学示例仍常用 `if` / `elif`、字典分发表或多态方法。

`for` 遍历的是可迭代对象，而不是只遍历整数索引：

```python
for name in ["Ada", "Linus", "Guido"]:
    print(name)
```

需要整数序列时使用 `range`。`range(3)` 产生 `0, 1, 2`，不包含右边界；`range(1, 5, 2)` 产生 `1, 3`。需要索引和值时使用 `enumerate`，需要并行遍历时使用 `zip`。这些写法比手动维护下标更少出错，也更符合 Python 的迭代模型。

循环可以有 `break`、`continue`，也可以带 `else`。循环 `else` 只在没有遇到 `break` 时执行，适合表达“找不到时”的逻辑；不过团队不熟悉时，拆成函数和早返回通常更清楚。

## 函数与模块

函数用 `def` 定义，参数和返回值可以写类型标注：

```python
def total(prices: list[float], tax_rate: float = 0.0) -> float:
    return sum(prices) * (1 + tax_rate)
```

默认参数在函数定义时求值，只求一次。不可变默认值如 `0`、`None`、字符串通常安全；可变默认值如 `[]`、`{}` 会在多次调用之间共享，常见替代写法是用 `None` 作为哨兵：

```python
def add_tag(name: str, tags: list[str] | None = None) -> list[str]:
    actual_tags = [] if tags is None else list(tags)
    actual_tags.append(name)
    return actual_tags
```

上面 `list[str] | None` 需要 Python 3.10；若要兼容 3.9，应从 `typing` 导入 `Optional` 或启用 `from __future__ import annotations` 后再配合类型检查器。示例代码为了 3.9 会使用兼容写法。

模块就是 `.py` 文件。`import pathlib` 导入模块，`from pathlib import Path` 导入名字。导入会执行目标模块顶层代码，所以模块顶层适合放常量、函数、类定义，不适合做网络请求、写文件或启动长任务。包是带有多个模块的目录；现代 Python 可以使用命名空间包，但入门阶段把目录、模块名和导入路径保持简单最重要。

## 集合与数据建模

Python 内建集合覆盖大多数日常数据处理：

- `list`：有序、可变，适合保存一串同类或同流程的数据。
- `dict`：键值映射，保持插入顺序，适合按 ID、名称或字段组织数据。
- `set`：无序去重集合，适合成员判断、交集、差集。
- `tuple`：有序、不可变，适合固定形状的小记录或多返回值。

推导式是 Python 的高频表达方式：

```python
squares = [number * number for number in range(5)]
active_by_name = {user.name: user for user in users if user.active}
unique_tags = {tag.lower() for tag in tags}
```

推导式适合短、单层、意图明显的转换；如果条件和转换都很复杂，拆成普通循环更可读。

简单数据建模优先考虑 `dataclass`。它能自动生成初始化、展示和比较等样板代码：

```python
from dataclasses import dataclass


@dataclass
class Task:
    title: str
    done: bool = False
```

`dataclass` 不会自动验证类型，标注仍主要是文档和工具信号。需要强校验时，可以在 `__post_init__` 中检查，或在应用边界使用专门的解析/校验库。

## 错误处理

Python 用异常表达失败。基本结构是 `try` / `except` / `else` / `finally`。`except` 应捕获具体异常，例如 `ValueError`、`FileNotFoundError`，避免裸 `except` 吞掉键盘中断、系统退出和真正的程序错误。

```python
try:
    count = int(raw_text)
except ValueError as error:
    raise ValueError(f"invalid count: {raw_text!r}") from error
```

`from error` 保留异常链，调试时能看到原始原因。`else` 适合放没有异常时才执行的逻辑，`finally` 适合释放资源，但文件、锁、连接更推荐用 `with`：

```python
from pathlib import Path

with Path("notes.txt").open("w", encoding="utf-8") as file:
    file.write("hello\n")
```

`with` 调用对象的上下文管理协议，确保离开代码块时执行清理逻辑。相比手写 `try/finally`，它更短，也更容易让资源边界一眼可见。

## 惯用写法

Python 代码通常追求“读起来像直接描述数据流”。常见惯用写法包括：

- 用 `for item in items` 直接遍历元素，用 `enumerate(items, start=1)` 获取序号。
- 用 `dict.get(key, default)` 处理可缺失键，但当缺失是错误时让 `KeyError` 暴露。
- 用 `pathlib.Path` 处理路径，而不是手动拼接字符串。
- 用 `with` 管理文件和连接。
- 用 `dataclass` 表达轻量记录，用普通类封装有行为和不变量的对象。
- 用小函数和清楚命名替代过长推导式或嵌套条件。

Python 社区常说 EAFP，即“先做，失败再处理异常”，与 LBYL“先检查再做”相对。它适合文件打开、字典读取、类型转换等存在竞争或边界失败的场景；但不要把异常当普通循环控制，也不要捕获过宽导致问题静默消失。

另一个迁移提示是导入风格。标准库、第三方库、本地模块通常分组导入；避免 `from module import *`，因为它会模糊名字来源。模块名、函数名、变量名使用 `snake_case`，类名使用 `PascalCase`，常量使用 `UPPER_SNAKE_CASE`。

## 可运行示例

本章示例位于：

- [syntax-tour](examples/syntax-tour/)：一个任务汇总脚本，演示变量绑定、f-string、条件与循环、函数默认值、集合、`dataclass`、异常和 `with`。

运行：

```bash
cd languages/python/syntax/examples/syntax-tour
python3 main.py
```

示例只使用标准库，并兼容 Python 3.9。它故意使用 `if` / `elif` 而不是 `match`，便于在仍停留于 3.9 的环境中复制运行。

## 学习检查

读完并运行示例后，可以用这些问题确认自己是否掌握了迁移重点：

- 你能解释“变量绑定到对象”和“变量保存对象副本”的差异吗？
- 为什么 `def f(items=[])` 可能在第二次调用时出现意外结果？
- 什么时候 `if value:` 不等价于 `if value is not None:`？
- `for item in items`、`range`、`enumerate` 分别适合什么场景？
- 为什么导入模块时要避免顶层副作用？
- `dataclass` 自动生成了什么，又没有自动保证什么？
- 哪些资源应该交给 `with` 管理？
- 如果要兼容 Python 3.9，为什么不能在示例源码里使用 `match`？
