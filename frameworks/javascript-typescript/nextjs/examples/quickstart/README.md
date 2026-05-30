# Next.js quickstart

这是一个最小但真实的 Next.js App Router 项目。它包含首页 Server Component、`/api/posts` Route Handler、共享数据模块、TypeScript 配置和一个不需要联网安装依赖的结构化 smoke test。

## 目标

通过这个案例学会三件事：第一，App Router 如何用 `src/app` 目录表达页面和 API；第二，Server Component 如何直接读取服务端数据函数；第三，Route Handler 如何在同一个工程里提供 HTTP API。

案例故意只做文章列表，不引入数据库和登录态。这样读者可以把注意力放在框架边界：哪些代码是页面入口，哪些代码是业务函数，哪些代码会成为 HTTP API。

## 学习重点

- `src/app/page.tsx` 默认是 Server Component，可以直接调用 `getPosts()`。
- `src/app/api/posts/route.ts` 导出 `GET` 函数，表示 `GET /api/posts`。
- `src/lib/posts.ts` 是页面和 API 共享的服务端数据模块。
- `layout.tsx` 定义根 HTML 外壳，`globals.css` 负责全局样式。
- `npm run smoke` 只做本地结构验收；安装依赖后再使用 `npm run dev` 或 `npm run build` 真正运行框架。

## 这个案例解决什么问题

在传统 React SPA 中，首页常见写法是：浏览器先下载 React bundle，组件挂载后在 `useEffect` 里请求 `/api/posts`，拿到数据后再渲染文章列表。这个流程能工作，但会把首屏内容推迟到 JavaScript 执行和 API 请求之后；页面 HTML 初始内容少，SEO、社交分享、弱网首屏和重复 loading 处理都会变差。

本案例用三个文件展示 Next.js 的替代思路：

- `src/app/page.tsx` 负责 `/` 页面，在服务端直接读取文章数据并生成页面内容。
- `src/lib/posts.ts` 负责文章数据和查询函数，让页面与 API 共享同一份业务能力。
- `src/app/api/posts/route.ts` 负责 `/api/posts`，当浏览器、移动端或第三方需要 JSON 时，再提供标准 HTTP 入口。

这种结构把“页面首屏渲染”和“对外 JSON API”分开。页面不必为了读取自己的数据绕一圈 HTTP；API 也不必混进组件里。读者可以把它理解为一个极小的 BFF：页面层直接使用服务端函数，对外集成点使用 Route Handler。

## 工程结构

```text
.
├── package.json
├── tsconfig.json
├── next.config.ts
├── scripts/
│   └── smoke.mjs
└── src/
    ├── app/
    │   ├── api/posts/route.ts
    │   ├── globals.css
    │   ├── layout.tsx
    │   └── page.tsx
    └── lib/posts.ts
```

`app` 目录由 Next.js 识别，决定路由结构。`lib` 目录不是框架强制要求，而是教学中推荐的业务边界：页面只组合 UI 和数据，真实业务放在可复用模块里。

## 运行前提

- Node.js 24.16.0 LTS，见仓库根目录 `versions.yaml`。
- npm 随 Node.js 安装即可。
- 本目录声明了 Next.js、React 和 TypeScript 依赖，但仓库不会联网安装依赖；首次真实运行前需要在本目录执行 `npm install` 生成 lockfile。

## 运行

```bash
npm run smoke
```

安装依赖后可以继续运行：

```bash
npm install
npm run dev
```

开发服务器启动后访问：

```bash
curl http://localhost:3000
curl http://localhost:3000/api/posts
```

生产构建验证：

```bash
npm run build
npm run start
```

## 预期输出

`npm run smoke` 会输出类似：

```text
OK: Next.js quickstart structure looks ready
```

`npm run dev` 启动后，首页会显示三篇文章的标题、摘要和标签；访问 `/api/posts` 会返回 JSON 数组。页面和 API 都读取 `src/lib/posts.ts`，所以修改那里的数据会同时影响两个入口。

## 代码讲解

`package.json` 声明了真实 Next 项目需要的脚本。`dev` 调用 `next dev`，`build` 调用 `next build`，`start` 调用 `next start`，`smoke` 调用本地 Node 脚本做结构验证。

`src/app/layout.tsx` 是根布局。Next.js 会用它包裹路由树，适合放全局 CSS、站点元信息、HTML 语言和跨页面外壳。这个文件返回 `<html>` 与 `<body>`，而普通页面组件不需要重复这些标签。

`src/app/page.tsx` 对应 `/`。它是 Server Component，因此可以直接 `import { getPosts } from "../lib/posts"` 并在组件执行时读取数据。这里没有使用 `useEffect` 拉取 API，因为服务端渲染阶段已经能拿到数据。这个文件里最重要的不是 JSX，而是数据流方向：请求进入 Next.js 服务端，服务端执行 `HomePage()`，`HomePage()` 调用 `getPosts()`，然后把包含文章内容的渲染结果交给浏览器。浏览器不需要再发一次“给我首页文章”的请求。

`src/app/api/posts/route.ts` 对应 `/api/posts`。它导出 `GET()` 函数并返回 `Response.json(...)`。这展示了 App Router 下 Route Handler 的写法：方法名就是 HTTP 动词，返回值是标准 Web Response。它解决的是“同一份数据也要给非页面消费者使用”的问题，例如移动端、管理脚本、第三方集成或客户端组件的增量刷新。注意它和 `page.tsx` 平级但职责不同：`page.tsx` 生产 HTML/UI，`route.ts` 生产 HTTP 响应。

`src/lib/posts.ts` 保存内存数据和查询函数。它是这个案例的业务边界：文章是什么结构、如何读取文章，都放在这里。真实项目可以把这里替换为数据库查询、CMS SDK、远程服务调用或缓存层；页面和 API 不需要知道数据从哪里来。这个分层能避免把数据细节写进路由入口，也能让单元测试更容易落在业务函数上。

## 思想拆解

第一，App Router 让路由成为目录结构。`src/app/page.tsx` 映射 `/`，`src/app/api/posts/route.ts` 映射 `/api/posts`。读者不需要再维护一份独立路由表，也不需要猜某个 URL 的入口在哪里。

第二，Server Component 让页面靠近数据。`HomePage()` 是 `async` 函数，它在服务端调用 `getPosts()`。如果未来 `getPosts()` 改成数据库查询，查询仍然留在服务端，不会把数据库密钥或 Node-only 代码打进浏览器。

第三，Route Handler 让 Web 层拥有轻量 BFF 能力。`GET()` 可以聚合多个服务、做鉴权、裁剪字段或处理缓存头，再向浏览器返回稳定 JSON。这个能力适合页面附近的小型 HTTP 能力；如果业务规则变复杂，应把核心逻辑继续下沉到独立服务或清晰的 `src/lib`/`src/server` 模块。

第四，缓存和渲染策略要跟业务新鲜度绑定。本案例的文章数组是静态内存数据，天然适合静态或缓存渲染。真实内容站可以设置按时间重新验证；个人工作台、购物车或审批流通常需要动态渲染或更精细的失效策略。学习 Next.js 时，不要只记 API 名称，要把问题翻译成“这份数据多久可以过期”。

第五，客户端组件是例外而不是默认。这个 quickstart 没有 `"use client"`，因为它没有浏览器状态、点击交互或 DOM API。等你加入搜索框、点赞按钮、实时编辑器时，再把那一小块拆成客户端组件。这样可以减少首屏 JS，也让服务端数据读取保持简单。

## 延伸练习

- 新增 `src/app/posts/[slug]/page.tsx`，根据 `slug` 展示文章详情。
- 给 `/api/posts` 增加 `POST` 方法，接收标题和摘要并追加到内存数组。
- 把 `src/lib/posts.ts` 替换为数据库或本地 JSON 文件读取，并思考缓存策略。

## 验收

完成后你应该能说明：`page.tsx` 与 `route.ts` 分别处理什么；为什么首页可以不经过 HTTP API 直接读取数据；什么时候需要 `"use client"`；`next build` 为什么不仅仅是 TypeScript 编译；以及如何把内存数据替换成真实数据访问。
