# Optional and Errors

## 目标

这个例子把 Swift 的 `Optional` 和错误处理放在同一条配置读取路径里。字典查询会得到 `String?`，因为键可能不存在；字符串转数字也会得到 `Int?`，因为内容可能不是合法数字。`loadPort` 用 `guard` 把这些缺失或无效情况转换成具体错误。

这样做的好处是调用方能区分“没有配置”“格式错误”和“超出范围”，而不是只得到一个空值或崩溃。

## 运行

```bash
swift main.swift
```

## 观察点

- `settings["port"]` 的类型是 `String?`，代码必须先解包才能继续使用。
- `Int(rawPort)` 也是 Optional，因为转换可能失败；这里把失败升级成 `ConfigError.invalidNumber`。
- `do/catch` 让调用点清楚看见 `try` 可能失败，并集中决定如何向用户展示错误。
