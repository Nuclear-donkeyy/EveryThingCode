# React

## 解决的问题

React 解决的是“复杂界面如何保持可理解”的问题。没有框架时，界面状态、DOM 更新、事件处理和数据同步常常散落在选择器、回调和手写 DOM 操作里；当页面变成搜索、筛选、弹窗、表单、异步加载和权限状态的组合时，读者很难回答“哪个状态驱动了这段 UI”。React 的答案是把界面拆成组件，把可变数据放进 state，把 UI 写成 state 的函数。

本章 quickstart 用任务看板解释这个思想：筛选词、任务列表和完成状态是数据；标题、列表、空状态和按钮是这些数据的投影。你不直接命令 DOM 改哪一行，而是改变状态，让 React 重新计算组件输出。

## 核心定位

React 是 UI 组件库，不是完整应用框架。它负责组件模型、状态更新、事件、渲染和与 DOM 的协调；路由、数据请求、构建、服务端渲染、表单和测试通常由 Next.js、React Router、TanStack Query、Vite、Vitest、Playwright 等生态工具补齐。

## 设计思想

React 的核心思想是组件化、声明式 UI、单向数据流和局部状态。组件把 UI 拆成可组合单元；声明式写法让你描述“当前状态下页面应该长什么样”；单向数据流让父组件把数据传给子组件，子组件通过事件把意图传回父组件；Hooks 把状态和副作用组织在函数组件里。

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

- [quickstart](examples/quickstart/)：任务看板 SPA，展示组件拆分、状态提升、派生数据、事件更新和离线 smoke。

## 版本来源

- 版本基线：React 19.2.x，latest stable，无官方 LTS。
- 官方来源：https://react.dev/versions
- 校验日期：2026-05-30
