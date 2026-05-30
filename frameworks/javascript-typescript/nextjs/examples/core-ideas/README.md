# Next.js core ideas example

## 目标

这个示例把 `Next.js` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

React SPA 的首屏、SEO、路由、数据请求瀑布、缓存、API/BFF 和部署经常被分散处理。

## 核心思想到代码

App Router 用文件路由组织页面，Server Components 把部分渲染移回服务端，Route Handler 提供同仓库 API 边界。

```tsx
export default function HomePage() {
  const posts = listPosts();
  return <PostList posts={posts} />;
}
```

```ts
export async function GET() {
  return Response.json({ items: listPosts() });
}
```

## 代码位置

- [`src/app/page.tsx`](../quickstart/src/app/page.tsx)
- [`src/app/api/posts/route.ts`](../quickstart/src/app/api/posts/route.ts)
- [`src/lib/posts.ts`](../quickstart/src/lib/posts.ts)

## 运行

先进入 quickstart 目录：

```bash
cd ../quickstart
npm run smoke
```

如果本机缺少对应工具链，可以先运行仓库根目录的 dry-run：

```bash
python3 scripts/run_framework_examples.py --dry-run
```

## 观察点

页面和 API 共享 `lib/posts.ts`，说明 UI 渲染和 BFF 端点可以围绕同一领域模块组织。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`Next.js` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
