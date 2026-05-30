# Vue quickstart：响应式任务面板

## 目标

用一个单文件组件理解 Vue 如何把状态、模板和样式组织在一起，并通过响应式系统自动更新界面。

## 学习重点

- `ref` 保存可变状态。
- `computed` 表示由状态推导出的列表和统计。
- 模板中的 `v-model`、`v-for`、`@click` 把输入、列表和事件声明在 HTML-like 结构中。
- `<style scoped>` 让样式默认限定在当前组件。

## 工程结构

```text
.
├── index.html
├── package.json
├── tsconfig.json
├── scripts/smoke.mjs
└── src/
    ├── App.vue
    └── main.ts
```

## 运行前提

- Node.js 24 LTS。
- 离线验证只需 `npm run smoke`。
- 启动页面前需要联网安装 Vue/Vite 依赖。

## 运行

```bash
npm run smoke
```

安装依赖后启动：

```bash
npm install
npm run dev
```

## 预期输出

`npm run smoke` 输出：

```text
Vue quickstart smoke passed
```

浏览器中输入筛选词时，任务列表自动变化；点击按钮时完成状态与统计同步更新。

## 代码讲解

`main.ts` 调用 `createApp(App).mount("#app")`，这和 React 的入口类似，都是把根组件连接到页面挂载点。

`App.vue` 的 `<script setup>` 中声明 `tasks` 和 `keyword`。`tasks` 是任务列表的源状态，`keyword` 是输入框的源状态。它们使用 `ref`，因为这两个值会被用户操作改变，而且模板、`computed` 和事件函数都需要感知这些改变。可以把 `ref` 理解成一个带依赖追踪能力的盒子：脚本里通过 `.value` 读写，模板里可以直接写 `keyword`、`tasks.length`，Vue 会帮你解包。

`visibleTasks` 和 `doneCount` 是 `computed`，它们依赖源状态但不重复存储结果。`visibleTasks` 读取 `keyword.value` 和 `tasks.value`，表示“当前应该展示哪些任务”；`doneCount` 读取每个任务的 `done`，表示“完成统计”。这解决了派生数据容易失真的问题：如果把筛选结果或完成数量也存成普通变量，就必须在新增、筛选、切换完成状态时都记得同步更新，一旦漏掉一个分支，界面就会出现过期数据。`computed` 把规则集中写一次，后续由 Vue 负责缓存、失效和重新计算。

`<template>` 通过 `v-model` 绑定输入，通过 `v-for` 渲染列表，通过 `@click` 触发 `toggleTask`。这让读者能直接从模板读出“界面如何响应用户操作”。`v-model="keyword"` 解决的是输入事件和状态赋值的样板代码；`v-for="task in visibleTasks"` 解决的是列表 DOM 的创建、复用和更新；`:key="task.id"` 告诉 Vue 每个任务的稳定身份，避免列表变化时错误复用节点；`:class="{ done: task.done }"` 把完成状态映射到样式；`@click="toggleTask(task.id)"` 把按钮点击转成一个明确的业务动作。

`toggleTask` 只做一件事：根据 id 找到任务并翻转 `done`。它没有更新 DOM，也没有重新计算完成数量，更没有手动给某个 `<li>` 加 class。这个例子正好展示 Vue 的思想边界：事件函数改变业务状态，响应式系统找出受影响的派生值和模板绑定，渲染器批量更新真实 DOM。代码因此更像业务规则，而不是 DOM 操作脚本。

`<style scoped>` 会把样式限定到当前组件，适合教学小案例。大型项目还会引入设计系统、CSS Modules、Tailwind 或组件库。

这个例子解决的第一个问题是“输入框和列表如何同步”。传统写法里，你可能监听 input 事件、手动读取 DOM 值、再手动隐藏列表项。Vue 的 `v-model` 把输入值绑定到 `keyword`，`computed` 根据 `keyword` 推导列表，模板根据列表重新渲染。你只维护数据关系，不维护 DOM 细节。

第二个问题是“组件逻辑放在哪里”。`<script setup>` 中的变量会暴露给模板，但仍然是普通 TypeScript 代码。你可以把复杂逻辑抽到 composable，模板不需要知道内部实现。这个边界让 Vue 在小页面和大项目之间都有扩展路径。

第三个问题是“HTML 可读性如何保留下来”。如果把页面全部写成字符串拼接或命令式 DOM 操作，结构会被控制流程打散；如果把业务分支完全藏进脚本，读模板时又看不出交互来源。Vue 模板把结构放在主位，再用少量指令表达动态部分：输入来自 `keyword`，列表来自 `visibleTasks`，按钮调用 `toggleTask`。这让有 HTML 基础的读者可以先读懂页面，再追到脚本中的状态和函数。

第四个问题是“组件变大以后如何拆”。当前案例把任务状态、筛选、统计和切换动作都放在一个 SFC 中，是为了教学集中。真实项目中，任务列表项可以拆成 `TaskItem.vue`，任务状态可以抽成 `useTasks()`，筛选关键词可以抽成 `useTaskFilter()`。Composition API 的价值就在这里：它允许按业务能力抽取逻辑，而不是让代码只按照 `data`、`computed`、`methods` 这些框架选项分散。

## 执行链路

输入筛选词时，浏览器触发 input 事件，`v-model` 更新 `keyword`。`visibleTasks` 因为读取过 `keyword.value`，会在下一次访问时得到新的筛选结果。模板中的 `v-for` 使用新的 `visibleTasks` 渲染列表，Vue 只更新发生变化的 DOM。

点击“完成”按钮时，`@click` 调用 `toggleTask(task.id)`。函数修改对应任务的 `done`，依赖 `task.done` 的 `doneCount`、`:class` 和按钮文案都会进入更新流程。读代码时可以顺着这条链路看：用户动作 -> 源状态变化 -> 派生状态失效 -> 模板绑定更新 -> DOM 最小化变更。

这个链路是 Vue 解决前端复杂度的核心：你不再把每一个界面变化写成独立步骤，而是声明状态、派生关系和模板绑定。只要这些关系清楚，UI 就能随着状态稳定地变化。

## 延伸练习

- 把任务项拆成 `TaskItem.vue`，练习 props 和 emits。
- 把任务状态抽成 `useTasks()` composable。
- 接入 Vue Router，增加 `/active` 和 `/done` 两个路由。

## 观察点

运行时可以重点观察三个地方。第一，输入框不需要手动监听 DOM，因为 `v-model` 已经把输入值和 `keyword` 连接起来。第二，`doneCount` 不需要自己维护，它是由任务列表推导出的统计值。第三，模板虽然像 HTML，但里面的 `v-for`、`:class`、`@click` 都是 Vue 编译器理解的声明式指令。

常见坑是把响应式对象过早拆散。例如把 `tasks.value` 赋给普通变量后再修改，可能会绕开你期待的响应式路径。学习时先保持一个清晰规则：源状态放在 `ref` 或 `reactive` 里，派生状态用 `computed`，副作用用 `watch` 或生命周期钩子。

## 验收

完成后你应该能说明：Vue 响应式如何让状态变化驱动 DOM；`computed` 和普通函数的区别；SFC 为什么适合组织组件局部逻辑；如果要引入全局状态，Pinia 应该解决哪类问题。
