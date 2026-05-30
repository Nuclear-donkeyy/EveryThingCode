# Async Iterators Streams

## 目标

用 Node 标准库里的 `Readable.from` 和 `for await...of` 观察异步迭代器与流式处理。这个例子对应的语言特性是 async iterator：消费者可以一段一段地等待数据，而不是一次性把所有内容读进内存。

真实工程中，日志文件、HTTP 响应体、数据库游标和消息队列都可能持续产生数据。如果不用异步迭代或流，代码常会退化成“先攒完整数组再处理”，数据量一大就浪费内存，也难以在中途取消或处理背压。

## 特性说明

`delayedEvents` 是一个 async generator。它每次 `yield` 一个事件前都会 `await` 一个小延迟，用来模拟网络或文件分块到达。`Readable.from(delayedEvents())` 把这个异步可迭代对象包装成 Node readable stream；随后 `for await (const event of stream)` 按到达顺序逐个消费。

`for await...of` 的关键是“循环本身会等待下一项”。它不像普通 `for...of` 那样要求数据已经全部准备好，也不像回调式流那样把处理逻辑拆到事件监听器里。示例在循环里维护 `counts`，说明业务逻辑可以用顺序代码表达，同时仍然保持流式读取。

## 设计取舍

异步迭代器把异步数据源抽象成统一协议，代码比手写 `data`、`end`、`error` 事件更线性。它也能自然配合 `break`、`try...catch` 和 `finally`，便于表达提前停止和清理。代价是你仍要理解底层流的背压、错误传播和资源关闭；`for await` 只是消费语法，不会自动替你设计协议。

如果不用这个特性，处理流式输入通常会有两种退化：一种是把所有数据先收集到数组，牺牲内存和首条结果延迟；另一种是事件回调分散，状态变量散落在多个监听器里。异步迭代器在二者之间提供了更可读的标准接口。

## 运行

```bash
node main.mjs
```

## 观察点

- `source ready` 会按延迟逐条出现，说明数据不是一次性准备好的。
- `consumer got` 紧跟每条源数据，说明消费者可以边到达边处理。
- `counts snapshot` 每次输出当前累计结果，验证业务状态能用普通顺序代码维护。
- 最后的 `final counts` 只在流结束后打印，对应异步迭代完成。
- 把延迟调大后，程序总耗时会变长，但内存模型仍是逐条处理。

## 延伸练习

在循环里加入 `if (event.kind === "error") break;`，观察提前退出后哪些数据不会被消费。再给 `delayedEvents` 加一个 `try...finally`，打印清理日志，理解异步生成器被提前关闭时如何释放资源。

还可以把 `Readable.from(delayedEvents())` 去掉，直接 `for await` 遍历生成器。比较两种写法后思考：异步迭代协议是语言层能力，Node stream 是标准库里的数据源实现，它们可以互相衔接。
