# Angular quickstart：任务工作台

## 目标

用一个最小 Standalone Angular 应用理解组件、模板、Service、DI 和 Signals 如何协作。读者应能看出 Angular 为什么适合组织大型前端项目。

## 学习重点

- `bootstrapApplication` 启动 Standalone 应用。
- `TaskStore` 通过 DI 注入到组件，封装业务状态。
- Signals 表示可追踪状态，模板依赖 signal 自动更新。
- 模板中的 `@for`、事件绑定和属性绑定表达 UI 逻辑。

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

`task.store.ts` 使用 `@Injectable({ providedIn: "root" })` 注册服务。服务拥有 `_tasks` signal，并暴露只读 `tasks` 和 `completedCount`。这种写法让组件不直接管理共享业务状态。

`app.component.ts` 通过 `inject(TaskStore)` 获取服务。组件方法 `toggle` 不操作数组，而是委托给 store。模板用 `store.tasks()` 读取 signal，用 `@for` 渲染列表，用 `(click)` 绑定事件。

这套拆分回答了 Angular 的核心问题：组件关注视图，service 关注业务状态，DI 负责装配，模板编译负责把声明式 UI 变成高效运行时代码。

这个案例解决的实际痛点是“多人项目里状态和业务逻辑不要藏在组件里”。如果组件直接维护任务数组、请求 API、处理权限和格式化数据，很快就无法复用，也难以测试。把任务逻辑放进 `TaskStore` 后，组件只是消费一个稳定接口；未来 `TaskStore` 可以接入 HTTP、缓存或权限判断，模板仍然不用重写。

DI 的价值也在这里体现：组件声明需要 `TaskStore`，而不是手动 `new TaskStore()`。这让测试可以替换依赖，让不同路由可以拥有不同生命周期的服务，也让大型项目在“谁创建对象、谁共享对象”这件事上有统一答案。

## 延伸练习

- 加入 Angular Router，把任务列表和统计页拆成两个路由。
- 用 `HttpClient` 替换内存 store，并加入 loading/error signal。
- 加入 Reactive Forms，完成新增任务和表单校验。

## 验收

完成后你应该能说明：Angular 为什么强调 DI；Standalone Component 与 service 的边界；signal 如何驱动模板；如果团队有几十个页面，为什么统一路由、表单、HTTP 和测试约定会降低维护成本。
