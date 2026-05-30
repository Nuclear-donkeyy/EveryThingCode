# Angular

## 解决的问题

Angular 解决的是“大型前端应用如何形成统一平台”的问题。一个企业前端通常不只有组件，还需要路由、表单、HTTP、依赖注入、测试、构建、升级策略、团队约定和长期维护窗口。如果每个团队自己拼装这些能力，项目很快会在目录结构、状态边界和工程命令上分裂。Angular 的答案是提供一套 batteries-included 的前端平台。

quickstart 用任务工作台展示 Angular 的核心：Standalone Component 负责视图，Service 负责状态和业务操作，DI 负责把依赖交给组件，模板语法负责把数据、事件和条件渲染连起来。

## 核心定位

Angular 是完整前端应用平台，而不仅是 UI 库。它覆盖组件、模板、Signals、依赖注入、路由、表单、HTTP、SSR/SSG、CLI、测试和升级工具。对于团队协作，它的价值是让多数基础决策落在官方约定内。

## 设计思想

Angular 的设计思想是平台化、显式边界、依赖注入和模板编译。组件只描述页面局部；服务封装共享状态和副作用；DI 容器管理服务生命周期；模板经过编译获得类型检查与性能优化；CLI 和 update 工具把项目维护纳入框架生命周期。

## 架构模型

现代 Angular 项目可以使用 Standalone Components，不必从 NgModule 入门。入口 `main.ts` 调用 `bootstrapApplication`，根组件声明 template、styles 和 imports，服务通过 `providedIn: "root"` 注册到应用级 injector。

quickstart 中 `TaskStore` 是业务状态服务，`AppComponent` 注入它并把信号暴露给模板。模板通过 `@for` 渲染任务，通过事件调用组件方法，组件再委托给服务。

## 请求/执行生命周期

浏览器加载 bundle 后，Angular bootstrap 根组件，创建依赖注入树，渲染模板。用户输入或点击触发模板事件，事件调用组件方法，组件修改 service 中的 signal。signal 变化后，依赖它的模板表达式被重新计算，Angular 更新 DOM。

真实项目中，请求生命周期还可能经过 Router guard、resolver、HTTP interceptor、component lifecycle、表单校验和错误边界。Angular 把这些扩展点放进统一平台，而不是让每个页面各写一套。

## 工程结构

```text
examples/quickstart/
├── angular.json
├── package.json
├── tsconfig.json
├── src/
│   ├── index.html
│   ├── main.ts
│   └── app/
│       ├── app.component.ts
│       └── task.store.ts
└── scripts/
    └── smoke.mjs
```

大型项目会继续拆成 `features/`、`shared/`、`core/`、`routes/`、`data-access/`。Angular 的关键不是目录名字，而是组件、服务、路由和外部 I/O 的职责分离。

## 配置方式

Angular 配置集中在 `angular.json`、`tsconfig.json`、`package.json` 和应用启动配置中。CLI 负责构建目标、开发服务器、测试、生成代码和升级。业务配置通常通过环境文件、DI token 或运行时配置服务进入应用。

## 模块与依赖管理

Angular 的依赖管理核心是 DI。组件声明自己需要什么服务，框架负责创建并注入。服务可以注册在 root、route 或 component 层级，从而控制共享范围。Standalone API 让组件直接声明 imports，降低学习 NgModule 的门槛。

## 数据访问

Angular 常通过 `HttpClient` 与后端通信，通过 service 或 facade 隔离 API 细节。复杂项目会把 data-access 层、缓存、错误处理和 loading 状态封装起来。quickstart 使用内存 service，先让读者看懂 DI 与模板更新。

## 测试方式

Angular 可用 TestBed 做组件测试，用 HttpTestingController 测 HTTP，用 Playwright/Cypress 做端到端测试。本案例的 `npm run smoke` 离线检查 Standalone、DI 和 signal 标记；真实项目应补交互测试和路由测试。

## 部署方式

Angular SPA 可以构建为静态文件部署；SSR/SSG 可通过 Angular server-side rendering 能力扩展。企业项目通常把构建、环境配置和版本升级纳入 CI。

## 适用场景与取舍

Angular 适合长期维护、团队规模较大、希望官方约定覆盖路由/表单/HTTP/测试/升级的项目。取舍是入门概念较多，轻量页面可能显得重；但当项目复杂度上来，统一平台会减少许多组织成本。

## 案例索引

- [quickstart](examples/quickstart/)：Standalone + Service + Signals 任务工作台。

## 版本来源

- 版本基线：Angular 21.x Active；Angular 20.x 仍处于 LTS 窗口。
- 官方来源：https://angular.dev/reference/releases
- 校验日期：2026-05-30
