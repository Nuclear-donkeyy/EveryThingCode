# Vue

## 解决的问题

Vue 解决的是“前端组件如何既易读又可渐进采用”的问题。很多团队并不是从零开始重写整站，而是在已有 HTML、服务端模板或多页面系统中逐步加入交互。Vue 可以从一个局部组件开始，也可以扩展到 SPA、SSR 或静态站点；它用模板保留 HTML 的直觉，用响应式系统自动把状态变化同步到 DOM。

quickstart 用一个任务面板展示 Vue 的核心价值：`ref` 保存状态，`computed` 生成派生列表，模板声明界面，事件绑定表达用户意图。你看到的是 HTML-like 模板，但背后是响应式依赖追踪。

## 核心定位

Vue 是渐进式 UI 框架。它包含组件、模板、响应式、生命周期和单文件组件格式；路由、全局状态、服务端渲染和构建工具由 Vue Router、Pinia、Nuxt、Vite 等生态补齐。

## 设计思想

Vue 的设计思想是渐进式采用、声明式模板、细粒度响应式和单文件组件。模板让 HTML/CSS 背景的开发者能快速阅读界面结构；Composition API 让复杂逻辑可以按功能聚合；响应式系统自动追踪读取过的状态，在状态改变时更新依赖它的视图。

## 架构模型

Vue 应用从 `createApp(App).mount("#app")` 启动。`App.vue` 把 `<script setup>`、`<template>` 和 `<style scoped>` 放在同一个文件里。小组件可以按页面或业务特性拆分，跨组件共享状态可以先用 props/emits，再使用 provide/inject 或 Pinia。

## 请求/执行生命周期

首次加载时，Vue 创建应用实例、编译或加载组件、建立响应式依赖并挂载 DOM。用户输入或点击事件修改 `ref` 后，依赖该值的 `computed` 与模板会重新求值，Vue 批量更新真实 DOM。组件挂载、更新和卸载时可以使用生命周期钩子接入外部系统。

## 工程结构

```text
examples/quickstart/
├── index.html
├── package.json
├── tsconfig.json
├── src/
│   ├── App.vue
│   └── main.ts
└── scripts/
    └── smoke.mjs
```

这个结构刻意很小：入口负责挂载，单文件组件负责教学主体。真实项目可继续拆成 `components/`、`composables/`、`stores/`、`routes/`。

## 配置方式

Vue 常见配置在 Vite、TypeScript、Vue Router、Pinia 和测试工具中。框架本身更强调组件内的局部声明：props、emits、computed、watch、provide/inject、生命周期钩子。

## 模块与依赖管理

Vue 组件通过 SFC 导入导出，通过 props 向下传数据，通过 emits 向上传事件。Composition API 可以把可复用逻辑抽成 `useSomething()` composable。状态跨越多个页面时，用 Pinia 比手写事件总线更清晰。

## 数据访问

Vue 不限制数据访问方式。SPA 可以在组件或 composable 中 `fetch`；Nuxt 项目可用服务端数据加载；企业项目常把 API client 放在 `services/` 中。quickstart 用内存数据，让你先看清响应式和模板。

一个常见学习误区是把 API 请求直接散落在每个组件里。更稳妥的方式是先抽出 `useTasks()` 这样的 composable，让组件只关心任务列表、加载状态、错误状态和操作函数；如果后续迁移到 Pinia 或 Nuxt server routes，组件模板仍然保持稳定。

## 测试方式

Vue 项目常用 Vitest、Vue Test Utils 和 Playwright。测试重点是：状态变化后模板是否更新，事件是否发出，组件边界是否稳定。本案例用 `npm run smoke` 做离线结构验证。

## 部署方式

Vue SPA 可构建为静态文件部署到 CDN 或静态托管；需要 SSR/SSG、路由数据和服务端能力时，可转向 Nuxt。

## 适用场景与取舍

Vue 适合希望保留模板可读性、渐进式接入、团队成员前端背景不完全一致的项目。取舍是生态约定比 Angular 少，架构纪律需要团队建立；同时大型全栈需求通常需要 Nuxt 或额外工具组合。

从思想上看，Vue 在“显式 JavaScript”和“模板可读性”之间取了一个中间位置：不像 React 那样把所有 UI 分支都写进 JSX，也不像 Angular 那样把平台约定全部纳入框架。它适合从局部交互逐渐长成完整应用，但当项目进入多人长期维护阶段，仍然要尽早约定组件拆分、composable 命名、状态层和路由层。

对已经会其他语言的读者，可以把 Vue 的 SFC 想成“一个组件的局部模块”：`script` 是状态和行为，`template` 是声明式视图，`style scoped` 是局部表现。三者放在一起不是为了混乱，而是为了让一个组件的变更上下文足够近。

## 案例索引

- [quickstart](examples/quickstart/)：任务面板，展示 `ref`、`computed`、模板事件和 SFC。

## 版本来源

- 版本基线：Vue 3.5.x，latest stable，无官方 LTS。
- 官方来源：https://vuejs.org/about/releases
- 校验日期：2026-05-30
