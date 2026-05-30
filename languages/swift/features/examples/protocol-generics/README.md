# Protocols and Generics

## 目标

这个例子展示 Swift 如何用协议描述能力，用泛型复用算法。`Scorable` 只要求一个值能提供标题和分数；`topItem` 不关心具体类型是任务还是课程，只关心元素满足这个能力。

协议让调用方表达需要什么，泛型让函数保留具体类型。这样既能复用逻辑，又不用把所有模型塞进同一个父类。

## 运行

```bash
swift main.swift
```

## 观察点

- `TaskCard` 和 `Lesson` 没有共同父类，但都满足 `Scorable`，因此都能传给 `topItem`。
- `topItem<T: Scorable>` 返回的仍是 `T?`，调用方拿回的是原来的具体类型，而不是丢失信息的通用容器。
- `Array where Element: Scorable` 的扩展只对满足协议约束的数组开放，算法边界写在类型系统里。
