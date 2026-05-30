# blocks-iterators

## 目标

通过一个订单汇总小例子观察 Ruby 的对象模型、block 和 iterator。重点不是记住 `map` 或 `reduce` 的名字，而是理解集合对象负责“怎么遍历”，块负责“每个元素上做什么”。

## 运行

```bash
ruby main.rb
```

## 观察点

- `3.times` 展示数字也是对象，重复执行由数字对象接收 `times` 消息完成。
- `select`、`map`、`reduce` 都把业务动作放进 block，避免把遍历细节散落在业务代码里。
- `Order` 是普通对象，但只要提供读取方法，就能自然进入集合管道。
