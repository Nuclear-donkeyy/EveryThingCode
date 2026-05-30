# Angular quickstart：任务工作台

## 目标

用一个最小 Standalone Angular 应用理解组件、模板、Service、DI 和 Signals 如何协作。读者应能看出 Angular 为什么适合组织大型前端项目。

## 学习重点

- `bootstrapApplication` 启动 Standalone 应用。
- `TaskStore` 通过 DI 注入到组件，封装业务状态。
- Signals 表示可追踪状态，模板依赖 signal 自动更新。
- 模板中的 `@for`、事件绑定和属性绑定表达 UI 逻辑。
- 用一个很小的任务列表观察 Angular 如何把企业前端的视图、状态、依赖和模板规则拆开。

## 工程结构

```text
.
├── angular.json
├── package.json
├── tsconfig.json
├── scripts/smoke.mjs
└── src/
    ├── index.html
    ├── main.ts
    └── app/
        ├── app.component.ts
        └── task.store.ts
```

## 运行前提

- Node.js 24 LTS。
- 本仓库版本基线使用 Angular 21 active，保留 Angular 20 LTS 的维护信息。
- 离线验证可执行 `npm run smoke`；启动页面需要 `npm install`。

## 运行

```bash
npm run smoke
```

安装依赖后启动：

```bash
npm install
npm run start
```

## 预期输出

`npm run smoke` 输出：

```text
Angular quickstart smoke passed
```

浏览器页面应显示任务列表、完成统计和按钮。点击按钮时 service 中的 signal 改变，模板同步刷新。

## 代码讲解

`main.ts` 调用 `bootstrapApplication(AppComponent)`。这说明现代 Angular 可以从 Standalone Component 开始，不必先学习 NgModule。

这一步解决的是入口复杂度问题。企业应用最终会有 Router、HTTP、国际化、认证和环境配置，但应用入口仍应该是一眼能读懂的组合点：启动哪个根组件，注册哪些全局 provider，失败时如何处理。Standalone 让一个新读者先理解组件和依赖边界，再逐步进入路由、表单和 SSR。

`task.store.ts` 使用 `@Injectable({ providedIn: "root" })` 注册服务。服务拥有 `_tasks` signal，并暴露只读 `tasks` 和 `completedCount`。这种写法让组件不直接管理共享业务状态。

这里的关键不是“把数组挪到另一个文件”，而是把业务状态变成可替换、可测试、可扩展的依赖。今天 `TaskStore` 只保存内存数组；真实项目里它可以继续接入 `HttpClient`、缓存、权限过滤、乐观更新和错误恢复。组件仍然只调用 `store.toggle(id)`，不会被 API 细节污染。`_tasks` 私有、`tasks` 只读，也表达了写入边界：外部只能通过领域方法改变状态，而不是随手改数组。

`signal<Task[]>(...)` 解决状态追踪问题。组件模板读取 `store.tasks()`，Angular 就知道模板依赖这份状态。`computed(() => ...)` 解决派生数据问题，完成数量不需要单独维护一份容易不同步的变量，而是从任务列表计算出来。`toggle(id)` 使用不可变更新返回新数组，让状态变化清晰可见，也更利于测试。

`app.component.ts` 通过 `inject(TaskStore)` 获取服务。组件方法 `toggle` 不操作数组，而是委托给 store。模板用 `store.tasks()` 读取 signal，用 `@for` 渲染列表，用 `(click)` 绑定事件。

`inject(TaskStore)` 解决对象创建和共享范围问题。组件声明自己需要任务状态，但不手写 `new TaskStore()`。测试时可以替换 provider；复杂应用中也可以把某些服务注册在路由级别，让不同业务流程拥有独立实例。DI 让“谁负责创建依赖、依赖活多久、哪些地方共享同一份状态”成为框架管理的规则，而不是每个团队私下约定。

`AppComponent` 是 Angular 推荐的 UI 边界：它知道如何展示标题、统计和列表，也知道按钮点击后调用哪个组件方法；但它不知道任务如何存储、如何请求后端、如何处理缓存。大型项目里，这种边界能防止组件膨胀成“页面、状态、API、权限、格式化、校验全都写在一起”的文件。

模板里的 `@for (task of store.tasks(); track task.id)` 解决列表渲染和性能问题。`@for` 用声明式语法表达“根据数据渲染列表”，`track task.id` 告诉 Angular 每个任务的稳定身份，避免状态变化时粗暴重建整组 DOM。`[class.done]="task.done"` 是属性/类绑定，表示 DOM 状态来自数据；`(click)="toggle(task.id)"` 是事件绑定，表示用户动作回到组件方法；`{{ store.completedCount() }}` 是插值，表示展示值来自 signal 派生状态。

这套拆分回答了 Angular 的核心问题：组件关注视图，service 关注业务状态，DI 负责装配，模板编译负责把声明式 UI 变成高效运行时代码。

这个案例解决的实际痛点是“多人项目里状态和业务逻辑不要藏在组件里”。如果组件直接维护任务数组、请求 API、处理权限和格式化数据，很快就无法复用，也难以测试。把任务逻辑放进 `TaskStore` 后，组件只是消费一个稳定接口；未来 `TaskStore` 可以接入 HTTP、缓存或权限判断，模板仍然不用重写。

DI 的价值也在这里体现：组件声明需要 `TaskStore`，而不是手动 `new TaskStore()`。这让测试可以替换依赖，让不同路由可以拥有不同生命周期的服务，也让大型项目在“谁创建对象、谁共享对象”这件事上有统一答案。

把这个示例扩展到企业应用时，Angular 的其他平台能力会自然接上来：Router 负责页面拆分、权限 guard 和懒加载；Reactive Forms 负责新增任务表单和校验；HttpClient interceptor 负责认证头和统一错误；TestBed 负责替换 `TaskStore` 或验证组件交互；CLI 负责生成一致结构、执行测试和升级迁移。也就是说，quickstart 展示的是一条小链路，但它背后对应的是 Angular 平台化的完整工作方式。

## 延伸练习

- 加入 Angular Router，把任务列表和统计页拆成两个路由。
- 用 `HttpClient` 替换内存 store，并加入 loading/error signal。
- 加入 Reactive Forms，完成新增任务和表单校验。

## 验收

完成后你应该能说明：Angular 为什么强调 DI；Standalone Component 与 service 的边界；signal 如何驱动模板；如果团队有几十个页面，为什么统一路由、表单、HTTP 和测试约定会降低维护成本。
