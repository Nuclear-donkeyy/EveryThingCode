# Event Loop Promises

## 目标

通过一个短程序观察 JavaScript 的同步调用栈、Promise 微任务、`queueMicrotask`、`setTimeout` 和 `await` 的顺序。重点不是背术语，而是建立判断：Promise 表示未来结果，它把后续逻辑排进任务队列，并不创建一条新的 JavaScript 执行线程。

这个例子对应的语言特性是事件循环、微任务队列和 `async`/`await`。真实工程里，前端要在请求接口时保持页面可交互，Node 服务要在等待数据库或文件系统时继续处理别的连接；如果不用这套异步模型，代码很容易退化成阻塞式等待，或者到处手写回调嵌套，既难推断顺序，也难统一处理错误。

## 特性说明

JavaScript 在同一条主执行线上先跑完当前同步调用栈，然后清空微任务，再进入计时器、I/O 等后续阶段。`Promise.then` 和 `queueMicrotask` 都会把回调放进微任务队列；`setTimeout(..., 0)` 的 `0` 不是“立刻插队”，而是“达到计时条件后进入后续任务阶段”。`await` 会把 `async` 函数拆开：`await` 左边的同步部分立即执行，右边的继续步骤作为 Promise 后续逻辑排队。

代码里的 `loadProfile()` 故意等待一个已经 resolved 的 Promise。即使结果已经准备好，`async:after await` 也不会同步打印；这能证明 `await` 的语义是暂停当前 async 函数，而不是把整个运行时卡住。运行输出中如果看到 `script:end` 早于 `async:after await`，就说明主脚本没有等待 `loadProfile` 后半段。

## 设计取舍

事件循环让普通业务代码不必直接管理线程、锁和共享内存，这非常适合 I/O 密集场景。代价是执行顺序不只由代码的视觉位置决定，还要理解同步栈、微任务和任务阶段的边界。Promise 比回调更容易组合，但它仍然可能制造“忘记 await”“未处理 rejection”“并发任务提前退出”等问题。

如果不用 Promise 和 `async`/`await`，同样逻辑通常会退化成回调层层嵌套，错误处理分散在多个回调里。反过来，如果误把 Promise 当线程，可能会以为 `Promise.resolve().then(...)` 可以并行执行 CPU 重活；实际它仍会占用同一条 JavaScript 执行线。

## 运行

```bash
node main.mjs
```

## 观察点

- `script:start` 和 `script:end` 是同步代码，先于异步回调完成。
- `Promise.then` 与 `queueMicrotask` 属于微任务，会在本轮同步代码结束后运行。
- `setTimeout(..., 0)` 需要等到后续任务阶段，所以通常晚于微任务。
- `await` 会把函数后半段拆成 Promise 后续步骤，因此 `async:after await` 不会夹在同步日志中间。
- 输出顺序能验证：同步代码先完成，微任务紧随其后，计时器最后才有机会运行。
- 把 `loadProfile()` 前后移动，只会改变 `async:before await` 的同步位置，不会让 `async:after await` 变成同步输出。

## 延伸练习

把 `Promise.resolve()` 换成 `new Promise((resolve) => setTimeout(resolve, 0))`，观察 `async:after await` 会不会仍然早于第一个计时器。再尝试删除 `await`，直接把 Promise 打印出来，体会“异步结果的容器”和“容器里的值”不是同一个东西。

还可以连续添加多个 `queueMicrotask`，或在 `Promise.then` 里面再创建新的微任务，观察微任务队列会在进入下一个任务阶段前被继续清空。这个练习能帮助你判断真实项目中哪些日志属于“当前请求的同步路径”，哪些已经被安排到后续阶段。
