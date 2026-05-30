# dataclass-pattern-matching

## 目标

理解 `dataclass` 如何把“带名字的数据”变成清晰的领域对象，并观察结构化模式匹配如何按对象形状分派逻辑。

这个例子使用登录、购买和密码重置事件。较新的 Python 会执行真实的 `match/case` 分支；较旧的 Python 会走兼容实现，让 `python3 main.py` 仍然可以运行。

## 运行

```bash
python3 main.py
```

## 观察点

- `@dataclass(frozen=True)` 让事件像值对象一样传递，不需要手写初始化方法。
- 模式匹配把“哪种事件、哪些字段值”放在同一个分支条件里。
- 兼容路径展示了没有 `match/case` 时同样逻辑会更分散，也更依赖手写判断。
