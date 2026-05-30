# JavaScript / TypeScript syntax tour

## 目标

这个示例用一个小型任务汇总脚本串起现代 JS/TS 的基础语法。它不依赖第三方包，重点展示 JavaScript 运行时真实行为，同时在注释里提示 TypeScript 会如何给这些对象、函数和错误边界加类型约束。读者应先观察输出，再修改数据和分支，确认自己理解了动态值、对象引用、异步错误和模块作用域。

## 覆盖语法

- `const` / `let`、基础值、模板字符串。
- `if`、`switch`、`for...of` 和数组方法。
- 普通函数、箭头函数、默认参数、对象解构。
- Array、Object、Map、Set 的典型使用。
- 用对象字面量模拟简单数据建模，并说明 TS 类型只是开发期约束。
- `try...catch...finally`、自定义错误、`async` / `await` 和 Promise。
- 通过 `import` 使用 Node 标准库，通过 `export` 暴露模块成员，建立 ES Module 心智。

## 运行

```bash
node main.mjs
```

在仓库根目录运行时也可以：

```bash
node languages/javascript-typescript/syntax/examples/syntax-tour/main.mjs
```

## 观察点

输出会先打印运行环境和模板字符串，再列出任务状态统计。注意 `const tasks = [...]` 后仍然可以修改数组内容，因为 `const` 固定的是变量绑定，不是集合内部。示例用 `for...of` 遍历任务，用 `switch` 把状态映射成展示文本，用 `Map` 统计负责人任务数，用 `Set` 去重标签。

错误部分会故意查找一个不存在的任务，并在调用边界捕获自定义 `TaskError`。异步部分使用 `await Promise.resolve(...)` 模拟远程读取，展示 `async` 函数返回的始终是 Promise。文件末尾的 `export` 在直接运行时不会额外输出，但说明同一个 `.mjs` 文件也可以被其他模块导入复用。

## 修改练习

- 给 `tasks` 增加一个 `blocked` 状态，观察 `switch` 的默认分支，然后补上正式处理。
- 把某个任务的 `estimateHours` 改成 `0`，比较 `??` 和 `||` 作为兜底值时的差异。
- 删除任务的 `owner` 字段，尝试用可选链和空值合并生成默认负责人。
- 在 `loadTaskById` 中抛出普通 `Error`，比较捕获分支和自定义错误分支的输出。
- 把 `Promise.all` 改成逐个 `await`，观察并发收敛和顺序执行在代码形状上的区别。
