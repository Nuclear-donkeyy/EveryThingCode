export type Post = {
  slug: string;
  title: string;
  summary: string;
  tag: "routing" | "rendering" | "api";
};

const posts: Post[] = [
  {
    slug: "app-router",
    title: "App Router 用目录表达 URL",
    summary: "src/app 下的 page.tsx、layout.tsx 和 route.ts 共同组成路由树。",
    tag: "routing"
  },
  {
    slug: "server-components",
    title: "Server Components 默认在服务端执行",
    summary: "页面可以直接调用服务端数据函数，减少浏览器端 JavaScript 和额外请求。",
    tag: "rendering"
  },
  {
    slug: "route-handlers",
    title: "Route Handler 是标准 HTTP 入口",
    summary: "导出 GET、POST 等函数即可在 App Router 中创建轻量 API。",
    tag: "api"
  }
];

export async function getPosts(): Promise<Post[]> {
  return posts;
}
