# Vue core ideas example

## 目标

这个示例把 `Vue` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

让已有 HTML 思维的团队用渐进方式接入状态驱动 UI，减少手动同步输入、列表和样式状态。

## 核心思想到代码

SFC 把局部逻辑、模板和样式放在一起；ref 保存源状态；computed 描述派生状态；模板指令把数据关系声明出来。

```vue
const keyword = ref("");
const tasks = ref<Task[]>([
  { id: 1, title: "Read Vue SFC structure", done: true },
  { id: 2, title: "Use ref for source state", done: false }
]);
const visibleTasks = computed(() => {
  const value = keyword.value.trim().toLowerCase();
  return value ? tasks.value.filter((task) => task.title.toLowerCase().includes(value)) : tasks.value;
});
```

```vue
<input v-model="keyword" />
<li v-for="task in visibleTasks" :key="task.id" :class="{ done: task.done }">
```

## 代码位置

- [`src/App.vue`](../quickstart/src/App.vue)
- [`src/main.ts`](../quickstart/src/main.ts)

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

输入筛选词时不用操作 DOM，computed 自动失效，模板按新的 visibleTasks 更新。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`Vue` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
