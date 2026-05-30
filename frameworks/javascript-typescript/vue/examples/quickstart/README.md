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

`App.vue` 的 `<script setup>` 中声明 `tasks` 和 `keyword`。`tasks` 是源状态，`keyword` 来自输入框。`visibleTasks` 和 `doneCount` 是 computed，它们依赖源状态但不重复存储结果。

`<template>` 通过 `v-model` 绑定输入，通过 `v-for` 渲染列表，通过 `@click` 触发 `toggleTask`。这让读者能直接从模板读出“界面如何响应用户操作”。

`<style scoped>` 会把样式限定到当前组件，适合教学小案例。大型项目还会引入设计系统、CSS Modules、Tailwind 或组件库。

这个例子解决的第一个问题是“输入框和列表如何同步”。传统写法里，你可能监听 input 事件、手动读取 DOM 值、再手动隐藏列表项。Vue 的 `v-model` 把输入值绑定到 `keyword`，`computed` 根据 `keyword` 推导列表，模板根据列表重新渲染。你只维护数据关系，不维护 DOM 细节。

第二个问题是“组件逻辑放在哪里”。`<script setup>` 中的变量会暴露给模板，但仍然是普通 TypeScript 代码。你可以把复杂逻辑抽到 composable，模板不需要知道内部实现。这个边界让 Vue 在小页面和大项目之间都有扩展路径。

## 延伸练习

- 把任务项拆成 `TaskItem.vue`，练习 props 和 emits。
- 把任务状态抽成 `useTasks()` composable。
- 接入 Vue Router，增加 `/active` 和 `/done` 两个路由。

## 观察点

运行时可以重点观察三个地方。第一，输入框不需要手动监听 DOM，因为 `v-model` 已经把输入值和 `keyword` 连接起来。第二，`doneCount` 不需要自己维护，它是由任务列表推导出的统计值。第三，模板虽然像 HTML，但里面的 `v-for`、`:class`、`@click` 都是 Vue 编译器理解的声明式指令。

常见坑是把响应式对象过早拆散。例如把 `tasks.value` 赋给普通变量后再修改，可能会绕开你期待的响应式路径。学习时先保持一个清晰规则：源状态放在 `ref` 或 `reactive` 里，派生状态用 `computed`，副作用用 `watch` 或生命周期钩子。

## 验收

完成后你应该能说明：Vue 响应式如何让状态变化驱动 DOM；`computed` 和普通函数的区别；SFC 为什么适合组织组件局部逻辑；如果要引入全局状态，Pinia 应该解决哪类问题。
