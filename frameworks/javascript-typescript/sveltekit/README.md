# SvelteKit

## 解决的问题

Svelte 解决组件表达问题，SvelteKit 解决完整 Web 应用问题：路由、数据加载、表单、服务端端点、渲染策略、构建和部署。只用组件库时，页面如何和 URL 对应、数据在哪里加载、哪些代码只能在服务端运行、静态页面和 SSR 如何切换，都需要自己拼装。SvelteKit 把这些常见问题变成文件约定。

quickstart 用任务页面和 API 端点展示这条主线：`+page.ts` 加载页面数据，`+page.svelte` 渲染并交互，`+server.ts` 暴露 JSON API。路径和文件名就是框架契约。

## 核心定位

SvelteKit 是基于 Svelte 的全栈前端框架。它提供文件路由、load 函数、form actions、server routes、布局、错误页面、SSR/CSR/prerender 配置和部署 adapters。它不是单纯的组件库，也不是传统后端框架，而是围绕 Web 标准组织页面与服务端能力。

## 设计思想

SvelteKit 的思想是编译优先、文件约定、Web 标准和可切换渲染。Svelte 编译组件，减少浏览器运行时负担；SvelteKit 用 `src/routes` 决定 URL；`load`、`Request`、`Response`、form action 等 API 尽量贴近 Web 平台；同一页面可以按需要选择 SSR、CSR 或 prerender。

## 架构模型

SvelteKit 项目以 `src/routes` 为中心。`+page.svelte` 是页面组件，`+page.ts` 或 `+page.server.ts` 加载数据，`+server.ts` 定义 API 端点，`+layout.svelte` 提供共享布局。`svelte.config.js` 配置 adapter 和预处理，`vite.config.ts` 连接 Vite 插件。

## 请求/执行生命周期

用户访问页面时，SvelteKit 根据 URL 匹配路由目录，执行对应的 `load` 函数，生成页面数据，再渲染 `+page.svelte`。后续客户端导航会复用同一套路由和数据加载模型。请求 `/api/tasks` 时，框架调用同目录或子目录中的 `+server.ts` 方法并返回标准 Response。

这个生命周期让你不必把“页面数据加载”和“组件渲染”混在一起，也不必手写前端路由表。

## 工程结构

```text
examples/quickstart/
├── package.json
├── svelte.config.js
├── tsconfig.json
├── src/
│   ├── lib/tasks.ts
│   └── routes/
│       ├── +page.svelte
│       ├── +page.ts
│       └── api/tasks/+server.ts
└── scripts/
    └── smoke.mjs
```

## 配置方式

SvelteKit 配置主要在 `svelte.config.js` 和 Vite 配置中。路由、加载和 API 大多通过文件约定完成。部署时选择 adapter：Node、Vercel、Netlify、Cloudflare、static 等。

## 模块与依赖管理

页面通过 `$lib` 导入共享模块。组件状态可以使用 Svelte 5 runes、stores 或普通模块；服务端专用逻辑应放在 `.server.ts` 或 server route 中，避免泄漏到客户端 bundle。

## 数据访问

SvelteKit 鼓励把页面数据加载放在 `load`，把服务端写操作放在 form actions 或 server routes。quickstart 使用本地数组；真实项目可以在 server-only 模块中访问数据库、认证服务或外部 API。

## 测试方式

常用 Vitest 测纯模块和 load 函数，Playwright 测页面行为。quickstart 的 `npm run smoke` 离线检查文件约定、load 函数和 server route。

## 部署方式

根据 adapter 部署到 Node 服务、边缘平台、Serverless 或纯静态站点。SvelteKit 的优势是让部署目标成为配置，而不是重写应用结构。

## 适用场景与取舍

SvelteKit 适合希望组件语法轻、产物小、页面路由和服务端能力统一的项目。取舍是生态规模小于 React/Vue，团队需要接受 Svelte 的编译模型和文件约定。

## 案例索引

- [quickstart](examples/quickstart/)：任务页面 + JSON API，展示 `+page.ts`、`+page.svelte`、`+server.ts`。

## 版本来源

- 版本基线：SvelteKit 2.x / Svelte 5.x，latest stable，无官方 LTS。
- 官方来源：https://svelte.dev/docs/kit/introduction
- 校验日期：2026-05-30
