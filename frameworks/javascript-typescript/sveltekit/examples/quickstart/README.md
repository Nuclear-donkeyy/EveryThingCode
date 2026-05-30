# SvelteKit quickstart：页面与 API

## 目标

用一个任务页面和一个 JSON API 理解 SvelteKit 如何把组件、路由、数据加载和服务端端点放进同一套文件约定。

## 学习重点

- `src/routes/+page.ts` 负责页面数据加载。
- `src/routes/+page.svelte` 负责页面渲染和交互。
- `src/routes/api/tasks/+server.ts` 负责 HTTP API。
- `$lib/tasks.ts` 放共享领域数据，避免页面和 API 各写一份。

## 工程结构

```text
.
├── package.json
├── svelte.config.js
├── tsconfig.json
├── scripts/smoke.mjs
└── src/
    ├── lib/tasks.ts
    └── routes/
        ├── +page.svelte
        ├── +page.ts
        └── api/tasks/+server.ts
```

## 运行前提

- Node.js 24 LTS。
- 离线验证只需 `npm run smoke`。
- 启动开发服务器需要联网安装 SvelteKit/Vite 依赖。

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
SvelteKit quickstart smoke passed
```

浏览器打开首页会看到任务列表和完成统计；访问 `/api/tasks` 会返回 JSON。

## 代码讲解

`+page.ts` 导出 `load` 函数。它从 `$lib/tasks` 读取任务数据并返回给页面。这样页面组件不需要知道数据来自内存、数据库还是远程 API。

`+page.svelte` 接收 `data`，用 Svelte 模板渲染列表。这里保留了一个局部筛选输入，帮助你区分“服务端加载的数据”和“浏览器里的临时交互状态”。

`api/tasks/+server.ts` 导出 `GET`。SvelteKit 会把它变成 `/api/tasks` 的 HTTP 处理函数，返回标准 `Response`。这说明 SvelteKit 的服务端端点和页面路由共享同一套文件系统路由。

`$lib/tasks.ts` 是共享领域模块。真实项目中，服务端访问数据库的逻辑应放进 `.server.ts`，防止被客户端导入。

这个例子解决的第一个问题是“页面和 URL 的关系在哪里声明”。在 SvelteKit 中，`src/routes/+page.svelte` 就是首页，`src/routes/api/tasks/+server.ts` 就是 `/api/tasks`，你不需要再维护一份手写路由表。文件位置本身就是架构信息。

第二个问题是“数据加载和组件渲染如何分离”。如果把请求写进组件，服务端渲染、错误处理和客户端导航都会混在一起。`load` 让页面先拿到数据，再把数据交给组件；组件只负责展示和局部交互。这个边界是 SvelteKit 从组件库升级为应用框架的关键。

第三个问题是“哪些代码运行在服务端”。`+server.ts` 只在服务端处理请求，适合访问数据库、密钥和内部 API。quickstart 只是返回内存数组，但路径和边界已经与真实项目一致。

## 延伸练习

- 增加 form action，让页面可以提交新任务。
- 把 `tasks.ts` 拆成 `tasks.server.ts` 并模拟数据库访问。
- 增加 `+layout.svelte`，为多个页面共享导航和样式。

## 观察点

运行或阅读时可以关注三个边界。第一，`+page.ts` 返回的数据会成为页面的 `data`，所以它适合准备页面渲染所需的数据。第二，`+page.svelte` 中的 `keyword` 是浏览器局部状态，不需要传回服务端。第三，`+server.ts` 返回标准 JSON 响应，适合给页面、移动端或第三方调用。

常见坑是把所有逻辑都塞进 `.svelte` 文件。SvelteKit 允许这样起步，但项目变大后，应把领域数据、服务端逻辑和 UI 交互分开：共享类型放 `$lib`，只在服务端运行的代码放 `.server.ts`，页面组件保留展示和局部交互。

## 验收

完成后你应该能说明：SvelteKit 文件路由如何映射 URL；页面 `load` 与组件渲染的边界；server route 如何返回 JSON；什么时候选择 SSR、CSR 或 prerender。
