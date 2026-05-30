# Event Loop Promises

## 目标

通过一个短程序观察 JavaScript 的同步调用栈、Promise 微任务、`queueMicrotask`、`setTimeout` 和 `await` 的顺序。重点不是背术语，而是建立判断：Promise 表示未来结果，它把后续逻辑排进任务队列，并不创建一条新的 JavaScript 执行线程。

## 运行

```bash
node main.mjs
```

## 观察点

- `script:start` 和 `script:end` 是同步代码，先于异步回调完成。
- `Promise.then` 与 `queueMicrotask` 属于微任务，会在本轮同步代码结束后运行。
- `setTimeout(..., 0)` 需要等到后续任务阶段，所以通常晚于微任务。
- `await` 会把函数后半段拆成 Promise 后续步骤，因此 `async:after await` 不会夹在同步日志中间。
