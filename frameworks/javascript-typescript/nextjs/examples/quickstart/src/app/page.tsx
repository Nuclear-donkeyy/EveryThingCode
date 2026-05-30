import { getPosts } from "../lib/posts";

export default async function HomePage() {
  const posts = await getPosts();

  return (
    <main className="page">
      <section className="intro">
        <p className="eyebrow">Next.js App Router</p>
        <h1>服务端组件直接读取数据</h1>
        <p>
          这个页面默认在服务端执行，直接调用共享数据模块，不需要先从浏览器请求自己的 API。
        </p>
      </section>

      <section className="posts" aria-label="文章列表">
        {posts.map((post) => (
          <article key={post.slug} className="post">
            <span>{post.tag}</span>
            <h2>{post.title}</h2>
            <p>{post.summary}</p>
          </article>
        ))}
      </section>
    </main>
  );
}
