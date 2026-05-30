# Interfaces and Composition

## 目标

这个例子展示 Go 如何用小接口和 struct 组合替代继承式扩展。`Service` 只依赖 `Notifier` 和 `AuditLogger` 两个行为，不关心具体类型来自哪里。`EmailNotifier` 没有写 `implements`，但只要方法集合匹配，就能作为接口使用。

例子也展示显式 `error`：发送失败时，调用点立刻看到 `err`，并用 `%w` 包装底层原因，保留可判断的错误链。

## 运行

```bash
go run main.go
```

## 观察点

- `Notifier` 是由使用方 `Service` 需要什么来定义的，而不是由实现方强迫所有通知类型继承同一个父类。
- `Service` 通过字段组合两个能力，测试或真实项目中可以替换成别的 notifier/logger。
- `errors.Is` 仍能识别被包装的 `ErrMissingRecipient`，说明补充上下文不等于丢掉根因。
