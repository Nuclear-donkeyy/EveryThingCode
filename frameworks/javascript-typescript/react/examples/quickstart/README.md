# React quickstart：任务看板

## 目标

这个案例用一个任务看板解释 React 如何解决前端状态和 UI 同步问题。读完并运行后，你应该能看懂组件如何拆分、state 放在哪里、事件如何改变数据，以及为什么不要手写 DOM 更新。

## 学习重点

- `App` 拥有任务数据和筛选词，是状态所有者。
- `TaskList` 和 `TaskItem` 只接收 props，负责展示和触发事件。
- `visibleTasks` 是派生数据，不需要再保存一份 state。
- 点击完成按钮只改变任务数组，界面由 React 根据新 state 重新渲染。

这个案例刻意选择“任务看板”，因为它足够小，却能暴露前端界面最常见的同步问题：同一份任务数据会影响列表、按钮文案、完成数量、筛选结果和空状态。没有 React 时，你通常要在每个事件回调里手动更新这些 DOM 节点；有 React 后，你只需要更新源 state，然后让组件重新计算页面。

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

`App.tsx` 是状态所有者。它用 `useState` 保存两份源状态：`tasks` 是任务事实，`filter` 是用户输入。完成数量 `completed`、可见列表 `visibleTasks` 和空状态都不再单独保存，因为它们可以从这两份源状态推导出来。这个原则很重要：React 应用越大，越应该减少“同一事实的多份拷贝”。

`visibleTasks` 用 `useMemo` 包起来：

```tsx
const visibleTasks = useMemo(() => {
  const keyword = filter.trim().toLowerCase();
  return keyword ? tasks.filter((task) => task.title.toLowerCase().includes(keyword)) : tasks;
}, [filter, tasks]);
```

这里的重点不是性能，而是依赖关系。`visibleTasks` 只依赖 `filter` 和 `tasks`，所以它是派生数据。筛选词改变时，列表重新计算；任务完成状态改变时，列表也重新计算；除此之外不需要维护第三份“当前可见任务”状态。这样可以避免手写 DOM 时代常见的错误：任务已经完成了，但筛选列表或统计数字还停留在旧值。

`toggleTask` 是本例最核心的事件更新：

```tsx
function toggleTask(id: number) {
  setTasks((current) =>
    current.map((task) => (task.id === id ? { ...task, done: !task.done } : task))
  );
}
```

按钮点击不会直接改 DOM，也不会让 `TaskItem` 偷偷修改父组件数组。`TaskItem` 只发出“切换这个 id”的意图，`App` 用函数式 `setTasks` 基于当前任务数组生成新数组。`{ ...task, done: !task.done }` 保留原任务的其他字段，只改变 `done`；未命中的任务保持原样。React 随后重新执行组件函数，`completed`、`visibleTasks`、按钮文案和 CSS 类名都会从新 state 得到新结果。

`TaskList` 接收 `tasks` 和 `onToggle`。它不知道任务来自服务器、内存还是测试数据，只知道如何把数组变成列表。

`TaskItem` 接收单个任务并渲染按钮。按钮点击时调用 `onToggle(task.id)`，表达“用户想切换这个任务”，真正的数据修改仍然回到 `App`。

把这三层合起来看，数据流是单向的：`App -> TaskList -> TaskItem`。事件流反向表达意图：`TaskItem -> onToggle -> App`。这就是 React 用来替代“到处查询 DOM、到处绑定事件、到处同步变量”的基本模型。你可以沿着 props 找到数据从哪里来，也可以沿着回调找到状态在哪里改。

这个例子刻意没有引入全局状态库，是因为 React 学习早期最重要的不是“选哪个状态库”，而是先判断状态应该属于谁。`tasks` 被多个子组件使用，但只有 `App` 需要修改它，所以它放在 `App`；`TaskItem` 只知道自己被点击，不知道数组如何更新。这个边界一旦清楚，未来换成 API、缓存库或 reducer 都不会推翻组件结构。

另一个观察点是 `visibleTasks`。很多初学者会把筛选后的列表也放进 state，结果每次新增、删除或修改任务时都要维护两份数据。React 鼓励把能由现有状态算出来的值留在渲染阶段计算，这减少了同步错误。`useMemo` 在这里不是为了“必须优化”，而是提醒读者：派生数据依赖 `tasks` 和 `filter`，它不是新的源状态。

如果用手写 DOM 实现同样功能，点击“完成”后至少要处理这些事情：更新任务数组，切换列表项 class，改按钮文案，重新计算完成数量，重新应用筛选，决定是否显示空状态。React 让这些步骤收敛成一个状态更新：`setTasks(...)`。其他界面变化都来自重新渲染，这正是“声明式 UI”解决的问题。

## 延伸练习

- 增加“新增任务”表单，练习受控输入。
- 把任务数据移动到 `useReducer`，比较 reducer 与多个 `useState` 的差异。
- 用 `localStorage` 持久化任务，并思考副作用应该放在哪里。

## 验收

完成后你应该能说明：为什么 React 中 UI 是 state 的函数；为什么派生数据不应该重复存储；父组件如何通过 props 和事件与子组件协作；如果未来接入后端 API，应该替换哪一层。
