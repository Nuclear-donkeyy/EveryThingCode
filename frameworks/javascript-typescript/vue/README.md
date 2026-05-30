# Vue

## 解决的问题

Vue 解决的是“前端交互如何既易读、可维护，又能渐进接入现有系统”的问题。很多团队并不是从零开始重写整站，而是在已有 HTML、服务端模板、CMS、多页面系统或后端渲染页面中逐步加入交互。如果一开始就引入完整 SPA 架构，迁移成本很高；如果继续用零散脚本操作 DOM，状态、事件、渲染和样式又会很快缠在一起。Vue 的渐进式定位让你可以先把一个小交互挂到页面局部，再逐步扩展到组件树、路由、状态管理、SSR 或静态站点。

Vue 还解决了“UI 与状态同步的重复劳动”。传统写法里，输入框变化后通常要手动读取 DOM、筛选数组、更新列表节点、修改完成数量、切换 class。状态分散在 DOM 和 JavaScript 之间后，代码很容易出现“数据已经变了，但界面忘了更新”或“DOM 更新了，但真实业务状态没有同步”的问题。Vue 把源状态放进响应式容器，把派生状态写成 `computed`，模板只声明状态应该如何呈现；状态变化后，Vue 根据依赖追踪自动安排视图更新。

quickstart 用一个任务面板展示 Vue 的核心价值：`keyword` 和 `tasks` 是源状态，`visibleTasks` 和 `doneCount` 是派生状态，`v-model` 负责输入同步，`v-for` 负责列表渲染，`toggleTask` 表达业务动作。读者看到的是接近 HTML 的模板，但背后是响应式依赖追踪：`visibleTasks` 读取了 `keyword.value` 和 `tasks.value`，所以输入或任务变化时它会重新求值；`doneCount` 读取了 `tasks.value` 和 `task.done`，所以点击完成按钮后统计会随之更新。

这套模型把几个常见复杂度拆开了：

- 渐进式接入解决迁移复杂度：可以从一个 Vue 组件开始，而不是要求整站重写。
- 模板可读性解决协作复杂度：设计、前端和全栈开发者都能从模板里直接看出页面结构。
- 响应式依赖追踪解决同步复杂度：开发者描述数据关系，框架负责最小化更新。
- SFC 解决局部上下文复杂度：一个组件的状态、视图和样式放在同一处，修改时不用跨多个目录追踪。
- Composition API 解决逻辑增长复杂度：当组件逻辑变多时，可以按业务能力抽成 `useTasks()`、`useFilters()` 这类 composable，而不是被生命周期选项切碎。

## 核心定位

Vue 是渐进式 UI 框架。它包含组件、模板、响应式、生命周期和单文件组件格式；路由、全局状态、服务端渲染和构建工具由 Vue Router、Pinia、Nuxt、Vite 等生态补齐。

## 设计思想

Vue 的设计思想可以理解为五个互相配合的选择。

第一，渐进式采用。Vue 不把“框架”定义成一个一次性的大迁移，而是允许从局部增强开始：一个表单、一个筛选列表、一个后台页面的小组件，都可以先独立挂载。等交互变复杂，再引入组件拆分、Vue Router、Pinia、Nuxt 或测试工具。这个设计降低了团队试用和迁移的门槛，也适合服务端渲染页面逐步现代化。

第二，模板优先的声明式 UI。Vue 模板保留 HTML 的视觉结构，同时加入 `v-model`、`v-for`、`:class`、`@click` 等声明式指令。quickstart 中 `<input v-model="keyword" />` 不是“给 input 注册事件再手动赋值”，而是声明“这个输入框与 `keyword` 双向同步”；`v-for="task in visibleTasks"` 不是“循环创建 DOM 节点”，而是声明“列表来自 `visibleTasks` 这个派生结果”。模板让页面结构、数据来源和事件意图放在同一个可读层面。

第三，细粒度响应式。`ref` 把普通值包成可追踪的响应式状态，`computed` 描述由状态推导出的值。quickstart 里 `visibleTasks` 依赖 `keyword.value` 和 `tasks.value`；当输入变化时，Vue 知道筛选列表需要重新计算。当 `toggleTask` 修改某个 `task.done` 时，依赖任务完成状态的 `doneCount` 和 `:class="{ done: task.done }"` 会更新。开发者不需要手动告诉 Vue “刷新这三个地方”，因为依赖是在读取状态时被记录下来的。

第四，单文件组件。SFC 把 `<script setup>`、`<template>`、`<style scoped>` 放在同一个 `.vue` 文件中。它不是简单地把三种语言混在一起，而是把“一个组件的状态、视图、局部样式”聚合成一个维护单元。quickstart 的任务面板不需要在多个文件间跳转才能理解：源状态和动作在脚本里，展示结构在模板里，完成状态的视觉效果在 scoped CSS 里。

第五，Composition API。Options API 更适合简单页面的“按选项分组”，Composition API 更适合复杂组件的“按功能分组”。在 quickstart 中，`keyword`、`tasks`、`visibleTasks`、`doneCount` 和 `toggleTask` 都在 `<script setup>` 中保持紧凑；当代码增长时，可以把这组任务逻辑抽成 `useTasks()`，把筛选逻辑抽成 `useTaskFilter()`。这样模板仍然使用同样的变量和函数，但实现细节可以独立测试、复用和演进。

这些设计共同指向一个目标：让开发者把注意力放在“状态之间的关系”和“用户动作的含义”上，而不是反复写 DOM 查询、事件解绑、局部刷新和 class 同步。

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
