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

`src/app/page.tsx` 对应 `/`。它是 Server Component，因此可以直接 `import { getPosts } from "../lib/posts"` 并在组件执行时读取数据。这里没有使用 `useEffect` 拉取 API，因为服务端渲染阶段已经能拿到数据。

`src/app/api/posts/route.ts` 对应 `/api/posts`。它导出 `GET()` 函数并返回 `Response.json(...)`。这展示了 App Router 下 API Route 的写法：方法名就是 HTTP 动词，返回值是标准 Web Response。

`src/lib/posts.ts` 保存内存数据和查询函数。真实项目可以把这里替换为数据库查询、CMS SDK、远程服务调用或缓存层；页面和 API 不需要知道数据从哪里来。

## 延伸练习

- 新增 `src/app/posts/[slug]/page.tsx`，根据 `slug` 展示文章详情。
- 给 `/api/posts` 增加 `POST` 方法，接收标题和摘要并追加到内存数组。
- 把 `src/lib/posts.ts` 替换为数据库或本地 JSON 文件读取，并思考缓存策略。

## 验收

完成后你应该能说明：`page.tsx` 与 `route.ts` 分别处理什么；为什么首页可以不经过 HTTP API 直接读取数据；什么时候需要 `"use client"`；`next build` 为什么不仅仅是 TypeScript 编译；以及如何把内存数据替换成真实数据访问。
