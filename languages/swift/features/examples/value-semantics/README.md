# Value Semantics

## 目标

这个例子展示 Swift 为什么默认鼓励用 `struct` 和 `let` 建模。`Cart` 是值类型，复制后修改副本不会影响原始购物车；`ReferenceCounter` 是类，两个变量会指向同一个实例，用来对比引用身份带来的共享修改。

重点不是说类不好，而是看清取舍：当你要表达一份业务数据快照时，值语义更容易局部推理；当你确实需要共享身份或生命周期时，再使用类。

## 运行

```bash
swift main.swift
```

## 观察点

- `var draft = original` 后，`draft.add(...)` 只改变副本，`original` 的商品数量保持不变。
- `Cart` 内部的 `items` 是数组，Swift 标准库用写时复制优化常见场景，所以值语义不等于每次赋值都立刻深拷贝。
- `ReferenceCounter` 的两个变量共享同一个实例，任何一边调用 `increment()` 都会改变同一份状态。
