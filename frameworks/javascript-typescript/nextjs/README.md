# Next.js

Next.js 是 React 生态中最常见的全栈 Web 框架之一。它把路由、渲染、数据获取、缓存、构建和部署放在一个统一模型里，让开发者既能写组件，也能在同一个工程中处理服务端逻辑。

## 核心定位

Next.js 解决的是“React 应用如何工程化地运行在浏览器与服务端之间”的问题。它提供文件系统路由、服务端渲染、静态生成、Server Components、客户端组件、Route Handler API、资源优化和构建部署约定。对于需要 SEO、首屏性能、登录态页面、内容站点、管理后台或轻量 BFF 的应用，Next.js 往往能减少大量胶水代码。

它不直接替代数据库、消息队列、复杂领域服务或独立后端。Next.js 可以写 API Route，但当业务规则、权限模型、事务、后台任务和团队边界变得复杂时，常见做法是让 Next.js 承担 Web 层和 BFF 层，把核心业务服务放在 NestJS、Java、Go、Python 等后端中。

## 设计思想

Next.js 的核心思想是“以路由树组织渲染与数据”。App Router 使用 `src/app` 下的目录表达 URL，每个目录可以拥有 `page.tsx`、`layout.tsx`、`loading.tsx`、`error.tsx` 和 `route.ts` 等文件。目录不只是文件夹，而是应用结构的一部分：它决定页面层级、布局嵌套、数据边界和错误处理范围。

Server Components 是 App Router 的关键。默认情况下，`page.tsx` 与普通组件在服务端执行，可以直接读取服务端资源、调用数据库或访问内部 API，不会把组件代码全部发送到浏览器。需要浏览器状态、事件处理、DOM API 或第三方客户端库时，再用 `"use client"` 明确切换到客户端组件。这种默认服务端、按需客户端的思想，能让页面更快、更少 JavaScript、更接近数据源。

渲染模式不是孤立开关，而是由数据访问和缓存策略共同决定。静态内容可以在构建时生成，动态内容可以在请求时渲染，数据可以按时间或事件重新验证。初学时不要急着记所有配置项，先理解：页面在服务端生成 HTML/React Payload，浏览器接收后进行 hydration，客户端组件接管交互。

API Route 在 App Router 中表现为 `route.ts`。它适合处理轻量接口、表单提交、Webhook、BFF 聚合和与页面同源的小型服务端能力。它不是“页面组件里的函数”，而是一条 HTTP 入口，使用 `GET`、`POST` 等导出函数表达方法。

## 架构模型

一个最小 Next.js 工程通常由以下部分组成：

- `src/app/layout.tsx`：根布局，定义 HTML 外壳、全局样式和跨页面 UI。
- `src/app/page.tsx`：路由 `/` 对应页面，默认是 Server Component。
- `src/app/api/<name>/route.ts`：Route Handler，对应 `/api/<name>` HTTP 入口。
- `src/lib/*`：业务数据、领域函数、外部服务客户端或可复用工具。
- `next.config.ts`：框架配置，例如构建、图片域名、实验特性。
- `package.json`：脚本与依赖声明。

架构上可以把 Next.js 看成三层：路由层负责 URL 到页面/API 的映射，组件层负责渲染 UI，业务层负责数据和规则。初学者最容易犯的错误是把所有逻辑塞进 `page.tsx`。更稳妥的方式是让页面组合数据和组件，把可测试的业务逻辑放进 `src/lib`。

## 请求/执行生命周期

访问 `/` 时，Next.js 根据 App Router 找到 `src/app/page.tsx`，在服务端执行该 Server Component。组件可以调用 `src/lib/posts.ts` 读取数据，然后返回 React 元素。框架把服务端渲染结果发送给浏览器，同时保留客户端组件所需的边界信息。浏览器加载后，只对客户端组件进行 hydration。

访问 `/api/posts` 时，路由命中 `src/app/api/posts/route.ts`。框架根据 HTTP 方法选择导出的 `GET` 或 `POST` 函数，函数读取业务模块并返回 `Response.json(...)`。这条链路没有 React 页面渲染，它是标准 HTTP 请求处理。

执行 `next build` 时，框架会分析路由树、组件边界、导入关系和数据访问方式，生成服务端产物、静态资源和客户端 bundle。构建不是简单转译 TypeScript，它会决定哪些代码留在服务端，哪些代码进入浏览器。

## 工程结构

本仓库 quickstart 使用以下结构：

```text
examples/quickstart/
├── package.json
├── tsconfig.json
├── next.config.ts
├── src/
│   ├── app/
│   │   ├── api/posts/route.ts
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── page.tsx
│   └── lib/posts.ts
└── scripts/smoke.mjs
```

真实项目可以继续扩展 `src/components`、`src/features`、`src/server`、`src/db`、`src/auth` 等目录。一个实用边界是：`app` 里放路由入口，`components` 放展示组件，`lib` 或 `server` 放数据访问与服务端逻辑，跨页面状态和浏览器交互放客户端组件。

## 配置方式

Next.js 的配置分为几类。`next.config.ts` 配置框架行为，`tsconfig.json` 配置 TypeScript 和路径解析，`package.json` 配置脚本与依赖，`.env.local` 等环境文件配置运行时变量。App Router 本身也有文件级配置，例如在页面或 Route Handler 中导出 `dynamic`、`revalidate` 等变量影响渲染和缓存。

本仓库案例保持最小配置：只声明 Next/React/TypeScript 依赖、基础 TypeScript 选项和一个空的 `next.config.ts`。这样能把注意力集中到 App Router、Server Component 和 API Route，而不是脚手架细节。

## 模块与依赖管理

Next.js 没有像 NestJS 那样的依赖注入容器。它依靠 ES Module、React 组件树和文件系统路由组织依赖。组件通过 import 组合，数据函数通过普通函数导入，页面通过目录约定被框架发现。

模块边界的关键是运行位置。默认 Server Component 可以导入服务端模块；带 `"use client"` 的组件会进入客户端 bundle，不能直接导入只适合服务端的数据库连接、密钥读取或 Node-only API。学习 Next.js 时要经常问一句：这段代码运行在服务端、浏览器，还是两边都可能运行？

## 数据访问

quickstart 使用 `src/lib/posts.ts` 中的内存数组模拟文章列表，页面和 API Route 共享同一组读取函数。这能展示一个重要思想：Next.js 页面不是只能从 HTTP API 拉数据，Server Component 可以直接调用服务端函数。

接入真实数据时，常见路径有三种：在 Server Component 中直接调用数据库或 SDK，在 Route Handler 中封装 HTTP API，在独立后端服务中实现业务能力并由 Next.js 聚合。小项目可以从第一种开始；多人协作或复杂业务建议尽早明确 BFF 与核心服务的边界。

## 测试方式

Next.js 项目通常有四类验证。第一类是类型检查和构建验证，例如 `next build`。第二类是业务函数单元测试，例如测试 `src/lib` 中的数据转换。第三类是组件测试，适合纯展示或交互组件。第四类是端到端测试，使用 Playwright 验证页面加载、表单和路由跳转。

本仓库 quickstart 提供 `npm run smoke`，它不安装依赖，只检查项目关键文件和脚本是否齐全；真实运行时再执行 `npm install`、`npm run dev` 或 `npm run build`。

## 部署方式

本地开发使用 `next dev`，生产构建使用 `next build`，启动 Node 部署产物使用 `next start`。如果部署到支持 Next.js 的平台，平台会识别路由、静态资源、服务端函数和缓存策略。如果部署到容器或普通服务器，需要确认 Node.js 版本、环境变量、构建产物和运行命令一致。

部署前应明确页面是静态生成、动态服务端渲染，还是依赖边缘运行时。不同运行时对 Node API、连接池、文件系统和冷启动的约束不同。

## 适用场景与取舍

优先选择 Next.js 的场景：需要 SEO 或首屏性能的 React 应用，需要把页面和轻量 API 放在同一仓库，需要服务端组件减少客户端 JavaScript，需要统一的路由、构建和部署约定。

谨慎选择 Next.js 的场景：纯后端 API、复杂微服务、长连接和后台任务为主的系统，或团队并不使用 React。此时 NestJS、Fastify、Go、Java 或其他后端框架可能更清晰。

Next.js 的学习成本主要来自运行边界：同样是 TypeScript 文件，有的在服务端，有的在浏览器，有的在构建时被分析。掌握这条边界，比记住更多 API 更重要。

## 案例索引

- [quickstart](examples/quickstart/)：App Router 最小项目，包含首页 Server Component、`/api/posts` Route Handler、共享数据模块和可本地执行的 smoke test。

## 版本来源

- 语言生态：JavaScript / TypeScript / Node.js 24.16.0 LTS。
- 框架版本基线：Next.js 16.x Active LTS。
- 策略：使用官方 LTS/Active LTS；patch 版本在实际安装时通过包管理器锁定。
- 官方来源：https://nextjs.org/docs
- 校验日期：2026-05-30
