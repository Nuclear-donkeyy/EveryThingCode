# NestJS core ideas example

## 目标

这个示例把 `NestJS` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

裸 Express/Fastify 服务容易让路由、依赖、校验、权限和测试边界散落在入口文件里。

## 核心思想到代码

Module 建立业务边界，Controller 处理 HTTP，Provider 承载业务，Guard/Pipe 处理横切逻辑，DI 负责装配。

```ts
@Module({
  controllers: [BooksController],
  providers: [BooksService, ApiKeyGuard, TrimTitlePipe]
})
export class BooksModule {}
```

```ts
@Post()
@UseGuards(ApiKeyGuard)
create(@Body(TrimTitlePipe) input: CreateBookDto) {
  return this.booksService.create(input);
}
```

## 代码位置

- [`src/app.module.ts`](../quickstart/src/app.module.ts)
- [`src/books/books.controller.ts`](../quickstart/src/books/books.controller.ts)
- [`src/books/books.service.ts`](../quickstart/src/books/books.service.ts)
- [`src/common/guards/api-key.guard.ts`](../quickstart/src/common/guards/api-key.guard.ts)
- [`src/common/pipes/trim-title.pipe.ts`](../quickstart/src/common/pipes/trim-title.pipe.ts)

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

一次创建图书请求先经过 Guard，再经过 Pipe，最后进入 Controller 和 Service。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`NestJS` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
