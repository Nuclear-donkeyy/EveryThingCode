# SvelteKit

## 解决的问题

Svelte 解决组件表达问题，SvelteKit 解决完整 Web 应用问题：路由、数据加载、表单/API、渲染策略、构建和部署。只用组件库时，页面能被写出来，但应用边界通常要自己拼出来。

第一个痛点是路由。只用组件库时，URL 到页面组件的映射通常依赖前端路由库和手写路由表。项目变大后，页面、嵌套路由、布局、404、错误页、动态参数、代码分割都散落在配置和组件之间。SvelteKit 把 `src/routes` 变成路由表：`src/routes/+page.svelte` 是首页，`src/routes/blog/[slug]/+page.svelte` 是动态页面，目录结构本身就是 URL 结构。

第二个痛点是数据加载。只在组件里 `fetch` 数据，容易把加载态、错误态、鉴权、SSR、客户端导航混在一起。服务端首屏渲染时要加载一遍，客户端跳转时又要加载一遍，重复逻辑很快出现。SvelteKit 用 `+page.ts`、`+page.server.ts` 和 `load` 把“为页面准备数据”放到组件外面，让页面组件专注渲染和交互。

第三个痛点是表单和 API。只用组件库时，表单提交、JSON API、校验错误、重定向、cookie、权限判断通常需要再接一个后端框架，或者在 serverless 函数里另起一套路由。SvelteKit 用 `+server.ts` 写 HTTP 端点，用 form actions 处理渐进增强表单，让页面路由和服务端能力共享一套路由约定。

第四个痛点是 SSR、CSR、SSG 和部署适配。组件库本身通常不告诉你哪些页面应服务端渲染、哪些可以纯静态、哪些要浏览器端运行，也不会统一处理 Node、边缘平台、Serverless、静态站点的构建差异。SvelteKit 通过页面级配置、`prerender`、`ssr`、`csr` 和 adapter，把渲染模式与部署目标变成显式决策。

quickstart 用任务页面和 API 端点展示这条主线：`+page.ts` 加载页面数据，`+page.svelte` 渲染并交互，`+server.ts` 暴露 JSON API。路径和文件名就是框架契约。

## 核心定位

SvelteKit 是基于 Svelte 的全栈前端框架。它提供文件路由、load 函数、form actions、server routes、布局、错误页面、SSR/CSR/prerender 配置和部署 adapters。它不是单纯的组件库，也不是传统后端框架，而是围绕 Web 标准组织页面与服务端能力。

## 设计思想

SvelteKit 的思想可以从五个关键词理解：编译优先、文件约定、数据先行、Web 标准、部署适配。

编译优先来自 Svelte。React、Vue 这类运行时驱动的框架通常在浏览器中保留更多运行时机制；Svelte 在构建阶段把组件编译成更直接的 JavaScript。SvelteKit 继承这个方向：它不是把所有问题都交给浏览器运行时，而是在构建阶段分析路由、页面、布局和 server route，尽量把“框架知道的事情”提前处理掉。

文件约定让结构承担架构信息。`+page.svelte` 表示页面 UI，`+page.ts` 表示通用页面数据加载，`+page.server.ts` 表示只能在服务端运行的数据加载，`+server.ts` 表示 HTTP 端点，`+layout.svelte` 表示共享外壳，`$lib` 表示可复用模块。读目录就能知道应用有哪些页面、哪些接口、哪些共享代码。

数据先行意味着页面先有 `load` 结果，再进入组件渲染。`load` 返回的对象会成为 `+page.svelte` 的 `data`。这条边界解决了“组件既负责发请求又负责展示”的混乱，也让 SSR、客户端跳转、错误处理、重定向和缓存策略有统一入口。

Web 标准让框架 API 不过度私有化。`+server.ts` 接收和返回的是接近标准的 `Request`、`Response`，返回 JSON 用 `json()` helper，本质仍是 HTTP 响应。form actions 也围绕浏览器表单能力设计，JavaScript 失效时仍能保持基本提交语义，再通过增强能力获得更好的交互。

部署适配把平台差异放进 adapter。Node 服务、Vercel、Netlify、Cloudflare Workers、静态托管的运行环境不同，但应用层仍围绕 routes、load、server routes 编写。adapter 负责把同一套应用编译成目标平台需要的产物，避免为了部署平台重写业务结构。

## 架构模型

SvelteKit 项目以 `src/routes` 为中心，以 `src/lib` 为共享模块区。一个典型页面可以拆成四层：

- `+page.ts`：为页面准备数据，可以在服务端和客户端导航时运行，适合调用公开 API 或读取可安全暴露的数据。
- `+page.server.ts`：只在服务端运行，适合访问数据库、密钥、私有服务和会话。
- `+page.svelte`：接收 `data` 并渲染 UI，保留局部交互状态，例如输入框、筛选条件、折叠面板。
- `$lib`：共享领域类型、纯函数、组件和服务。服务端专用模块应命名为 `.server.ts`，防止进入客户端 bundle。

`+server.ts` 是同一套路由系统里的 HTTP 端点。它适合给页面、移动端、第三方系统或后台任务提供 JSON API。`svelte.config.js` 配置 adapter 和预处理，`vite.config.ts` 连接 Vite 插件。

## 请求/执行生命周期

用户访问页面时，SvelteKit 根据 URL 匹配路由目录，执行对应的 `load` 函数，生成页面数据，再渲染 `+page.svelte`。后续客户端导航会复用同一套路由和数据加载模型。请求 `/api/tasks` 时，框架调用同目录或子目录中的 `+server.ts` 方法并返回标准 Response。

这个生命周期让你不必把“页面数据加载”和“组件渲染”混在一起，也不必手写前端路由表。服务端首屏访问时，`load` 可以先拿到数据并生成 HTML；浏览器内导航时，SvelteKit 会再次按路由执行加载逻辑并局部更新页面。对读者来说，重要的是看到同一份文件约定同时服务 SSR 和客户端导航。

写操作有两条常见路径。偏页面的写操作可以用 form actions，让表单、校验、重定向和渐进增强保持在页面附近；偏 API 的写操作可以用 `+server.ts` 的 `POST`、`PUT`、`DELETE`。二者都依赖 Web 请求/响应模型，只是使用场景不同。

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

SvelteKit 配置主要在 `svelte.config.js` 和 Vite 配置中。路由、加载和 API 大多通过文件约定完成，因此不会出现一份巨大路由配置文件控制全站行为的情况。

部署时选择 adapter：Node、Vercel、Netlify、Cloudflare、static 等。页面也可以声明渲染策略，例如导出 `prerender` 生成静态页面，导出 `ssr` 控制服务端渲染，导出 `csr` 控制客户端接管。框架鼓励你按页面选择策略，而不是让整个应用被一种渲染模式绑死。

## 模块与依赖管理

页面通过 `$lib` 导入共享模块。组件状态可以使用 Svelte 5 runes、stores 或普通模块；服务端专用逻辑应放在 `.server.ts` 或 server route 中，避免泄漏到客户端 bundle。

quickstart 的 `$lib/tasks.ts` 同时被 `+page.ts` 和 `+server.ts` 导入，是为了演示“领域数据不要散落在页面和接口里”。真实项目中，如果 `tasks` 来自数据库，应把它改为 `$lib/server/tasks.ts` 或 `tasks.server.ts`，让 SvelteKit 在构建时阻止客户端误导入服务端代码。

## 数据访问

SvelteKit 鼓励把页面数据加载放在 `load`，把服务端写操作放在 form actions 或 server routes。quickstart 使用本地数组；真实项目可以在 server-only 模块中访问数据库、认证服务或外部 API。

判断数据放在哪里，可以用一个简单规则：页面渲染必须先知道的数据放 `load`；只服务于局部交互且不影响首屏的数据可以在组件中获取；需要隐藏密钥、连接数据库或读取 session 的逻辑放服务端文件；需要被多个客户端调用的能力放 `+server.ts`。

## 测试方式

常用 Vitest 测纯模块和 load 函数，Playwright 测页面行为。quickstart 的 `npm run smoke` 离线检查文件约定、load 函数和 server route。

## 部署方式

根据 adapter 部署到 Node 服务、边缘平台、Serverless 或纯静态站点。SvelteKit 的优势是让部署目标成为配置，而不是重写应用结构。

## 适用场景与取舍

SvelteKit 适合希望组件语法轻、产物小、页面路由和服务端能力统一的项目，例如内容站、产品官网、控制台、文档站、小到中型全栈应用，以及需要在 SSR、静态生成和边缘部署之间切换的项目。

它解决的是“组件库到完整应用之间缺少约定”的问题。取舍是生态规模小于 React/Vue，团队需要接受 Svelte 的编译模型和文件约定；对于高度依赖大型企业组件生态、复杂后台低代码生态的场景，React/Vue/Angular 可能更容易找到现成方案。

## 案例索引

- [quickstart](examples/quickstart/)：任务页面 + JSON API，展示 `+page.ts`、`+page.svelte`、`+server.ts`。

## 版本来源

- 版本基线：SvelteKit 2.x / Svelte 5.x，latest stable，无官方 LTS。
- 官方来源：https://svelte.dev/docs/kit/introduction
- 校验日期：2026-05-30
