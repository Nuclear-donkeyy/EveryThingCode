# React

## 解决的问题

React 解决的是“复杂界面如何保持可理解、可复用、可同步”的问题。没有框架时，前端代码很容易变成三类交织在一起的脚本：用选择器找到 DOM，手写 `textContent`、`className` 和 `appendChild`；给按钮、输入框和列表项注册事件；在回调里维护一堆变量，并手动把变量变化同步回页面。页面越复杂，越难回答“这段 DOM 现在为什么长这样”“哪个事件改了这个状态”“这个列表和统计数字是不是来自同一份数据”。

第一个痛点是手写 DOM 与事件同步。假设任务完成状态变化，你需要同时更新按钮文案、任务样式、完成数量、筛选后的列表，甚至空状态。只要漏掉其中一处，界面就会和数据不一致。React 把这个问题反过来处理：你不直接命令 DOM 改哪一行，而是改变 state；组件函数根据最新 state 重新描述 UI，React 再负责把变化提交到真实 DOM。

第二个痛点是状态散落。传统写法里，筛选词可能在输入框事件回调里，任务数组可能在模块变量里，完成数量可能存在另一个变量里，列表项又在 DOM dataset 上藏一份 id。React 鼓励把“源状态”放在清晰的所有者组件中，再通过 props 向下传递。本章 quickstart 中，`App` 拥有 `tasks` 和 `filter`；`TaskList`、`TaskItem` 只是读取 props 并发出用户意图。

第三个痛点是派生数据重复存储。完成数量、筛选后的任务列表、是否显示空状态都能从 `tasks` 和 `filter` 算出来。如果把它们也保存为 state，就会出现“双写”问题：修改任务时要记得同步完成数，修改筛选词时要记得同步可见列表。React 的常见做法是只保存最小源状态，把 `completed`、`visibleTasks` 这类值留在渲染阶段计算。quickstart 用 `useMemo` 标出 `visibleTasks` 依赖 `tasks` 和 `filter`，强调它是派生数据，不是新的事实来源。

第四个痛点是组件复用困难。手写 DOM 常把创建节点、绑定事件、读写全局变量写在同一段函数里，想把“任务项”搬到另一个页面时会连带搬走很多上下文。React 用组件边界解决复用问题：`TaskItem` 只关心一个 `task` 和一个 `onToggle` 回调，不知道任务数据来自本地数组、HTTP API 还是测试夹具；这种低耦合让组件能被组合、替换和测试。

本章 quickstart 用任务看板解释这个思想：筛选词、任务列表和完成状态是数据；标题、列表、空状态和按钮是这些数据的投影。你不直接命令 DOM 改哪一行，而是改变状态，让 React 重新计算组件输出。

## 核心定位

React 是 UI 组件库，不是完整应用框架。它负责组件模型、状态更新、事件、渲染和与 DOM 的协调；路由、数据请求、构建、服务端渲染、表单和测试通常由 Next.js、React Router、TanStack Query、Vite、Vitest、Playwright 等生态工具补齐。

## 设计思想

React 的核心思想可以从一句话理解：UI 是 state 的函数。你维护的是数据模型和用户意图，组件负责把当前数据投影成界面。只要源状态一致，界面就应该一致；只要 state 改变，界面就应该重新计算。

组件化是 React 的第一层答案。组件不是单纯的 HTML 片段，而是一个小的 UI 单元：它接收 props，返回当前应该显示的内容，可以拥有局部 state，也可以把事件意图交给上层。quickstart 中 `App` 是有状态的容器组件，`TaskList` 是列表展示组件，`TaskItem` 是单项展示与交互组件。这样的拆分让“谁拥有数据”和“谁负责展示”变得明确。

声明式渲染是第二层答案。你在 JSX 里描述“当 `task.done` 为真时类名是 `task done`，按钮显示 `重开`；否则类名是 `task`，按钮显示 `完成`”。这和手写 DOM 的区别很大：手写 DOM 关注“先找到按钮，再改文字，再改 class”；React 关注“当前状态下按钮应该是什么样”。真实 DOM 的最小更新由 React 协调。

单向数据流是第三层答案。数据从父组件通过 props 流向子组件，事件从子组件以回调形式流回父组件。`App` 把 `visibleTasks` 和 `toggleTask` 传给 `TaskList`，`TaskList` 再把单个 `task` 和同一个 `onToggle` 传给 `TaskItem`。当按钮点击时，`TaskItem` 不直接修改数组，而是调用 `onToggle(task.id)`；最终由 `App` 里的 `setTasks` 更新源状态。这个方向性让调试路径变短：数据往下看，修改往上找。

Hooks 是第四层答案。`useState` 把函数组件里的可变状态显式声明出来；`useMemo` 用依赖数组表达“这个派生值只依赖哪些输入”；真实项目还会用 `useEffect` 连接浏览器 API、订阅、计时器和网络副作用。Hooks 的价值不是把代码写得更短，而是把状态、派生值和副作用按生命周期组织在组件附近。

React 不追求模板语法的“少写”，而追求 UI 与 JavaScript 模型一致。JSX 看起来像 HTML，但本质是 JavaScript 表达式；这让条件渲染、列表渲染、函数传递和类型检查都留在同一种语言里。

## 架构模型

一个典型 React 应用包含入口 `main.tsx`、根组件 `App.tsx`、若干展示组件、状态提升位置、领域数据类型和样式。入口只负责把根组件挂载到 DOM；根组件负责把数据与交互组织起来；子组件尽量通过 props 接收数据并触发事件。

quickstart 中 `App.tsx` 保存任务列表和筛选词，`TaskList` 只负责渲染列表，`TaskItem` 只负责单个任务的展示与切换。这个拆分把“数据拥有者”和“展示者”分开，避免每个组件都偷偷改全局状态。

## 请求/执行生命周期

React 浏览器应用从 `createRoot(...).render(<App />)` 开始。首次渲染时，React 调用组件函数，得到一棵元素树，再提交到 DOM。用户点击按钮或输入文本时，事件处理函数调用 `setState`，React 调度更新，重新执行受影响组件，比较新旧输出并提交最小 DOM 改动。

这条生命周期的教学重点是：组件函数不是“只运行一次的初始化脚本”，而是可以在每次状态变化时重新执行的 UI 计算。副作用应该放在事件、框架数据层或 `useEffect` 中，而不是直接写在渲染逻辑里。

## 工程结构

```text
examples/quickstart/
├── index.html
├── package.json
├── tsconfig.json
├── src/
│   ├── App.tsx
│   ├── main.tsx
│   └── styles.css
└── scripts/
    └── smoke.mjs
```

真实项目会继续拆出 `components/`、`features/`、`hooks/`、`lib/`、`routes/` 和 `tests/`。拆分标准不是文件数量，而是谁拥有状态、谁负责展示、谁连接外部系统。

## 配置方式

React 自身配置很少，主要由构建工具承担。quickstart 使用 Vite 风格的 `index.html`、`main.tsx` 和 `tsconfig.json`，生产项目还会配置 ESLint、格式化、测试、路径别名、环境变量和构建目标。

## 模块与依赖管理

React 组件通过 ES Module 导入导出，通过 props 组合，通过 Context 或状态管理库跨层传递共享状态。学习早期不要急着引入全局 store；先练习状态提升、受控组件和派生数据，只有当多个远距离组件确实共享同一份可变数据时，再考虑 Context、Redux Toolkit、Zustand 或 TanStack Query。

## 数据访问

React 不规定数据访问方式。页面可以直接 `fetch`，也可以使用 React Router loader、Next.js Server Components、TanStack Query 或 GraphQL 客户端。quickstart 故意使用内存数组，帮助你先理解状态更新与渲染，再把数据源替换为 HTTP API。

## 测试方式

React 常见测试分三层：纯函数和 hooks 的单元测试，组件交互测试，浏览器端到端测试。本仓库 quickstart 的 `npm run smoke` 是离线结构验证；真实项目可使用 Vitest + Testing Library 验证用户交互，用 Playwright 覆盖关键路径。

## 部署方式

React SPA 通常构建为静态文件，部署到 CDN、对象存储、Nginx 或静态托管平台。若需要 SSR、边缘渲染、路由数据加载和服务端能力，通常转向 Next.js、Remix/React Router 或自建 Node 服务。

## 适用场景与取舍

React 适合组件复杂、交互密集、生态要求高、团队熟悉 TypeScript 的前端项目。它的取舍是自由度高但需要自己选择路由、数据和工程约定；小项目容易上手，大项目需要团队主动建立目录、状态和测试规范。

## 案例索引

- [core-ideas](examples/core-ideas/)：把上一节“解决的问题”和“设计思想”映射到 quickstart 的关键代码片段。
- [quickstart](examples/quickstart/)：任务看板 SPA，展示组件拆分、状态提升、派生数据、事件更新和离线 smoke。

## 版本来源

- 版本基线：React 19.2.x，latest stable，无官方 LTS。
- 官方来源：https://react.dev/versions
- 校验日期：2026-05-30
