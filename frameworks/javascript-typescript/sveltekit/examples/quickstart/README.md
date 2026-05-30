# SvelteKit quickstart：页面与 API

## 目标

用一个任务页面和一个 JSON API 理解 SvelteKit 如何把组件、路由、数据加载和服务端端点放进同一套文件约定。

读完后，你应该能回答一个更实际的问题：如果只用 Svelte 这样的组件库，哪些应用能力需要自己补；SvelteKit 又如何把这些能力变成默认工程结构。

## 学习重点

- `src/routes/+page.ts` 负责页面数据加载。
- `src/routes/+page.svelte` 负责页面渲染和交互。
- `src/routes/api/tasks/+server.ts` 负责 HTTP API。
- `$lib/tasks.ts` 放共享领域数据，避免页面和 API 各写一份。
- 文件位置就是路由声明，不再手写一份独立路由表。
- `load` 先准备页面数据，组件再负责展示和浏览器局部状态。

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

这个 quickstart 故意不用复杂业务，而是把 SvelteKit 最关键的四个文件放在同一个小例子里：`+page.ts` 解决页面数据从哪里来，`+page.svelte` 解决页面如何展示和交互，`+server.ts` 解决 HTTP API 如何暴露，`$lib/tasks.ts` 解决共享领域代码放在哪里。

`+page.ts` 导出 `load` 函数。它从 `$lib/tasks` 读取任务数据并返回给页面。这样页面组件不需要知道数据来自内存、数据库还是远程 API。只用组件库时，你可能会在组件挂载后发请求；这会让首屏 HTML 没有数据，也会把加载、错误、权限和渲染混在同一个组件里。SvelteKit 的 `load` 把“准备页面数据”前置，SSR 和客户端导航都能复用这条路径。

```ts
import { listTasks } from "$lib/tasks";

export function load() {
  return {
    tasks: listTasks()
  };
}
```

`+page.svelte` 接收 `data`，用 Svelte 模板渲染列表。这里保留了一个局部筛选输入，帮助你区分“服务端加载的数据”和“浏览器里的临时交互状态”。`data.tasks` 是页面进入时已经准备好的数据，`keyword` 是用户在浏览器里输入的临时状态，两者不应该混为一谈。

```svelte
let { data }: { data: PageData } = $props();
let keyword = $state("");

const visibleTasks = $derived(
  keyword.trim()
    ? data.tasks.filter((task) => task.title.toLowerCase().includes(keyword.trim().toLowerCase()))
    : data.tasks
);
```

这段代码体现了 SvelteKit 和 Svelte 的分工：SvelteKit 决定页面、数据和服务端边界；Svelte 负责编译组件、响应式状态和 DOM 更新。组件库只关心最后这部分，应用框架则要把前面的工程问题一起解决。

`api/tasks/+server.ts` 导出 `GET`。SvelteKit 会把它变成 `/api/tasks` 的 HTTP 处理函数，返回标准 `Response`。这说明 SvelteKit 的服务端端点和页面路由共享同一套文件系统路由。只用组件库时，你通常要另外维护一个 API 服务或 serverless 函数目录；SvelteKit 让 API 和页面在同一套路由约定下组织。

```ts
import { json } from "@sveltejs/kit";
import { listTasks } from "$lib/tasks";

export function GET() {
  return json({ items: listTasks() });
}
```

`+server.ts` 适合处理 JSON API、webhook、文件下载、第三方回调等 HTTP 端点。它使用 Web 标准的请求/响应模型，所以理解成本接近原生 HTTP，而不是学习一套完全私有的控制器抽象。

`$lib/tasks.ts` 是共享领域模块。真实项目中，服务端访问数据库的逻辑应放进 `.server.ts`，防止被客户端导入。

```ts
export type Task = {
  id: number;
  title: string;
  done: boolean;
};

export function listTasks() {
  return tasks;
}
```

这个文件解决的是“业务概念应该放在哪里”的问题。如果页面和 API 各自维护任务结构，字段一变就会出现重复修改。把类型和纯领域函数放进 `$lib`，页面加载和 API 端点都能复用。若未来接入数据库，可以把读取逻辑迁移到 server-only 模块，页面和 API 的外层结构仍保持稳定。

这个例子解决的第一个问题是“页面和 URL 的关系在哪里声明”。在 SvelteKit 中，`src/routes/+page.svelte` 就是首页，`src/routes/api/tasks/+server.ts` 就是 `/api/tasks`，你不需要再维护一份手写路由表。文件位置本身就是架构信息。

第二个问题是“数据加载和组件渲染如何分离”。如果把请求写进组件，服务端渲染、错误处理和客户端导航都会混在一起。`load` 让页面先拿到数据，再把数据交给组件；组件只负责展示和局部交互。这个边界是 SvelteKit 从组件库升级为应用框架的关键。

第三个问题是“哪些代码运行在服务端”。`+server.ts` 只在服务端处理请求，适合访问数据库、密钥和内部 API。quickstart 只是返回内存数组，但路径和边界已经与真实项目一致。

第四个问题是“渲染和部署如何决策”。这个 quickstart 没有额外声明，因此默认展示 SvelteKit 的常规 SSR/客户端导航模型。真实项目可以按页面导出 `prerender`、`ssr`、`csr`，再在 `svelte.config.js` 里选择 adapter。也就是说，部署到 Node、边缘平台、Serverless 或静态站点时，业务文件仍围绕 `routes`、`load`、`+server.ts` 组织。

## 延伸练习

- 增加 form action，让页面可以提交新任务。
- 把 `tasks.ts` 拆成 `tasks.server.ts` 并模拟数据库访问。
- 增加 `+layout.svelte`，为多个页面共享导航和样式。
- 增加 `src/routes/tasks/[id]/+page.ts` 和 `+page.svelte`，观察动态路由如何来自目录名。
- 增加 `POST` 到 `api/tasks/+server.ts`，对比 API 写操作和 form action 的边界。
- 尝试导出 `export const prerender = true`，思考哪些页面适合静态生成。

## 观察点

运行或阅读时可以关注三个边界。第一，`+page.ts` 返回的数据会成为页面的 `data`，所以它适合准备页面渲染所需的数据。第二，`+page.svelte` 中的 `keyword` 是浏览器局部状态，不需要传回服务端。第三，`+server.ts` 返回标准 JSON 响应，适合给页面、移动端或第三方调用。

常见坑是把所有逻辑都塞进 `.svelte` 文件。SvelteKit 允许这样起步，但项目变大后，应把领域数据、服务端逻辑和 UI 交互分开：共享类型放 `$lib`，只在服务端运行的代码放 `.server.ts`，页面组件保留展示和局部交互。

另一个常见坑是把 SvelteKit 当成“带路由的组件库”。它真正提供的是应用框架边界：文件路由管理 URL，`load` 管理页面数据，server routes 管理 HTTP，adapter 管理部署目标。理解这四个边界，再去学 form actions、layout、hooks、错误页和 streaming，会顺很多。

## 验收

完成后你应该能说明：SvelteKit 文件路由如何映射 URL；页面 `load` 与组件渲染的边界；server route 如何返回 JSON；什么时候选择 SSR、CSR 或 prerender。
