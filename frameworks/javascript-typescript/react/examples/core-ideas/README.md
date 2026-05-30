# React core ideas example

## 目标

这个示例把 `React` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

避免手写 DOM 更新和多份状态互相不同步，把界面变成 state 的可预测投影。

## 核心思想到代码

组件拆分负责复用，state 保存源数据，props 单向传递数据，事件把用户意图传回状态所有者，派生数据在渲染阶段计算。

```tsx
const [tasks, setTasks] = useState(initialTasks);
const [filter, setFilter] = useState("");
const visibleTasks = useMemo(() => {
  const keyword = filter.trim().toLowerCase();
  return keyword ? tasks.filter((task) => task.title.toLowerCase().includes(keyword)) : tasks;
}, [filter, tasks]);
```

```tsx
<TaskList tasks={visibleTasks} onToggle={toggleTask} />
```

## 代码位置

- [`src/App.tsx`](../quickstart/src/App.tsx)
- [`src/main.tsx`](../quickstart/src/main.tsx)

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

修改任务完成状态时，只有 state 改变；列表、统计和按钮文本都由 React 重新计算。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`React` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
