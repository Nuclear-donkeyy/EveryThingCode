# React quickstart：任务看板

## 目标

这个案例用一个任务看板解释 React 如何解决前端状态和 UI 同步问题。读完并运行后，你应该能看懂组件如何拆分、state 放在哪里、事件如何改变数据，以及为什么不要手写 DOM 更新。

## 学习重点

- `App` 拥有任务数据和筛选词，是状态所有者。
- `TaskList` 和 `TaskItem` 只接收 props，负责展示和触发事件。
- `visibleTasks` 是派生数据，不需要再保存一份 state。
- 点击完成按钮只改变任务数组，界面由 React 根据新 state 重新渲染。

## 工程结构

```text
.
├── index.html
├── package.json
├── tsconfig.json
├── scripts/smoke.mjs
└── src/
    ├── App.tsx
    ├── main.tsx
    └── styles.css
```

`main.tsx` 是浏览器入口，`App.tsx` 是教学主体，`styles.css` 只提供最小布局，`smoke.mjs` 在不安装依赖时检查项目关键文件和思想标记。

## 运行前提

- Node.js 24 LTS。
- 如果要启动页面，需要联网执行 `npm install` 安装 React/Vite 依赖。
- 离线验收可以直接执行 `npm run smoke`。

## 运行

```bash
npm run smoke
```

安装依赖后启动开发服务器：

```bash
npm install
npm run dev
```

## 预期输出

`npm run smoke` 会输出：

```text
React quickstart smoke passed
```

浏览器页面应显示任务统计、筛选输入框和任务列表。输入筛选词时列表减少；点击任务按钮时完成数量变化。

## 代码讲解

`main.tsx` 调用 `createRoot`，把 `<App />` 挂载到 `#root`。这一步建立了 React 与真实 DOM 的连接。

`App.tsx` 中的 `useState` 保存 `tasks` 和 `filter`。任务列表是源数据，筛选词是用户输入。`visibleTasks` 通过 `tasks.filter(...)` 每次渲染时计算，因此不会出现“筛选结果和原数据不同步”的问题。

`TaskList` 接收 `tasks` 和 `onToggle`。它不知道任务来自服务器、内存还是测试数据，只知道如何把数组变成列表。

`TaskItem` 接收单个任务并渲染按钮。按钮点击时调用 `onToggle(task.id)`，表达“用户想切换这个任务”，真正的数据修改仍然回到 `App`。

这个例子刻意没有引入全局状态库，是因为 React 学习早期最重要的不是“选哪个状态库”，而是先判断状态应该属于谁。`tasks` 被多个子组件使用，但只有 `App` 需要修改它，所以它放在 `App`；`TaskItem` 只知道自己被点击，不知道数组如何更新。这个边界一旦清楚，未来换成 API、缓存库或 reducer 都不会推翻组件结构。

另一个观察点是 `visibleTasks`。很多初学者会把筛选后的列表也放进 state，结果每次新增、删除或修改任务时都要维护两份数据。React 鼓励把能由现有状态算出来的值留在渲染阶段计算，这减少了同步错误。`useMemo` 在这里不是为了“必须优化”，而是提醒读者：派生数据依赖 `tasks` 和 `filter`，它不是新的源状态。

## 延伸练习

- 增加“新增任务”表单，练习受控输入。
- 把任务数据移动到 `useReducer`，比较 reducer 与多个 `useState` 的差异。
- 用 `localStorage` 持久化任务，并思考副作用应该放在哪里。

## 验收

完成后你应该能说明：为什么 React 中 UI 是 state 的函数；为什么派生数据不应该重复存储；父组件如何通过 props 和事件与子组件协作；如果未来接入后端 API，应该替换哪一层。
