# Angular core ideas example

## 目标

这个示例把 `Angular` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

大型前端需要统一处理 DI、状态、路由、表单、HTTP、测试和升级，而不是每个页面自己拼装。

## 核心思想到代码

Standalone 组件降低入口复杂度，Service 承载业务状态，DI 管理依赖创建，Signals 驱动模板更新，CLI 统一工程命令。

```ts
@Injectable({ providedIn: "root" })
export class TaskStore {
  private readonly _tasks = signal<Task[]>([
    { id: 1, title: "Bootstrap a standalone component", done: true },
    { id: 2, title: "Inject a service into the component", done: false }
  ]);
  readonly completedCount = computed(() => this._tasks().filter((task) => task.done).length);
}
```

```ts
export class AppComponent {
  protected readonly store = inject(TaskStore);
}
```

## 代码位置

- [`src/main.ts`](../quickstart/src/main.ts)
- [`src/app/app.component.ts`](../quickstart/src/app/app.component.ts)
- [`src/app/task.store.ts`](../quickstart/src/app/task.store.ts)

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

组件没有 new TaskStore，也不维护数组细节；它通过 DI 消费稳定服务接口。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`Angular` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
