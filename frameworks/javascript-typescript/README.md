# JavaScript / TypeScript 框架生态

JavaScript/TypeScript 的框架生态横跨浏览器 UI、服务端渲染、API 服务、构建工具、静态站点和全栈应用。本目录面向已经有编程经验、但尚未系统使用 JS/TS 框架的读者：先建立选型地图，再进入具体框架的思想、工程结构和可运行案例。

## 常用框架清单

| 方向 | 常用框架/库 | 核心定位 | 本仓库覆盖 |
| --- | --- | --- | --- |
| UI 组件 | React | 用组件和单向数据流构建界面，是 Next.js、Remix 等框架的重要基础 | 通过 [Next.js](nextjs/) 案例间接覆盖 |
| 全栈 React | Next.js | App Router、Server Components、SSR/SSG、API Route、部署一体化 | 已覆盖：[nextjs](nextjs/) |
| UI 组件 | Vue | 渐进式 UI 框架，模板语法、响应式系统和组合式 API 易上手 | 未覆盖 |
| 全栈 Vue | Nuxt | Vue 生态的服务端渲染、文件路由、数据获取和部署框架 | 未覆盖 |
| 企业前端 | Angular | Batteries-included 的前端平台，内置 DI、路由、表单、HTTP、测试约定 | 未覆盖 |
| 编译型 UI | Svelte | 编译期把组件转为高效 JS，减少运行时负担 | 未覆盖 |
| 全栈 Svelte | SvelteKit | 文件路由、load 数据函数、server actions 与部署适配器 | 未覆盖 |
| Node 后端 | NestJS | 用模块、控制器、Provider 和 DI 组织 TypeScript 服务端应用 | 已覆盖：[nestjs](nestjs/) |
| Node 后端 | Express | 极简中间件模型，适合理解 Node HTTP 框架基本形态 | 未覆盖 |
| Node 后端 | Fastify | 高性能、Schema 驱动、插件化的 HTTP 框架 | 未覆盖 |
| React 全栈/路由 | Remix / React Router | 强调 Web 标准、嵌套路由、loader/action 与渐进增强 | 未覆盖 |
| 内容站点 | Astro | 多框架组件岛、静态优先、内容集合，适合文档和营销站点 | 未覆盖 |
| 构建工具 | Vite | 开发服务器、HMR 和现代前端构建入口，被许多框架复用 | 未覆盖 |
| 测试 | Vitest / Playwright | 单元测试和浏览器端到端测试，常与以上框架配套 | 未覆盖 |

本仓库第一阶段选择 Next.js 与 NestJS，是因为它们分别代表 JS/TS 生态中最常见的两个学习入口：一个面向现代 React 全栈 Web，一个面向模块化 TypeScript 后端服务。

## 选择思路

如果目标是产品页面、仪表盘、用户系统、BFF 或需要 SEO 的 Web 应用，优先学习 Next.js。它把 React 组件、路由、服务端渲染、Server Components、缓存和 API Route 放在同一个工程模型里，适合理解“前端框架如何进入全栈边界”。学习时不要只看页面组件，还要观察数据在服务端组件、客户端组件、Route Handler 与浏览器之间怎样移动。

如果目标是业务 API、后台服务、微服务网关或希望在 Node.js 中获得接近 Java/Spring 的结构感，优先学习 NestJS。NestJS 的价值不在于“更少代码”，而在于用模块、控制器、Provider、依赖注入、管道、守卫和拦截器建立可测试、可替换、可扩展的服务端边界。

如果只需要很薄的 HTTP 层，Express 足够直观；如果需要高吞吐和 Schema 驱动，Fastify 更合适；如果团队主要写 Vue，可转向 Vue/Nuxt；如果希望框架内置完整企业前端约定，Angular 更稳定；如果内容站点和静态发布占主导，Astro 往往比全栈框架更轻。

选型时可以用四个问题快速过滤：应用是否需要服务端渲染，业务边界是否复杂，团队是否愿意接受框架约定，部署平台是否支持框架的运行模型。框架不是越重越好，也不是越轻越好，关键是让项目的变化方向有清楚的落点。

## 学习路线

1. 先阅读 `languages/javascript-typescript/README.md` 与语言特性案例，确认 TypeScript 类型、模块系统、Promise/async、包管理和运行时边界。
2. 进入本页建立生态地图，明确 React、Next.js、NestJS、Express、Fastify 等名称解决的是不同层次的问题。
3. 学习 [Next.js](nextjs/)：先读 App Router、Server Components、渲染模式和 API Route，再运行 quickstart，看页面与 API 如何共享同一份内存数据。
4. 学习 [NestJS](nestjs/)：先读模块、控制器、Provider、DI、管道和守卫，再运行 quickstart，看一次 HTTP 请求怎样穿过框架生命周期。
5. 对比两个案例：Next.js 更关注渲染和用户界面边界，NestJS 更关注服务端分层和依赖组织。理解这种差异后，再扩展到 Nuxt、Angular、Fastify、Remix 或 Astro 会更顺。

## 本仓库案例

- [Next.js quickstart](nextjs/examples/quickstart/)：一个 App Router 最小项目，包含 Server Component 页面、Route Handler API、共享数据模块和结构化 smoke test。
- [NestJS quickstart](nestjs/examples/quickstart/)：一个模块化 API 最小项目，包含 `AppModule`、业务模块、控制器、Provider、管道、守卫和结构化 smoke test。

