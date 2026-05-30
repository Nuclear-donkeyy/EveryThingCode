# Angular

## 解决的问题

Angular 解决的是“大型前端应用如何形成统一平台”的问题。企业前端的复杂度往往不是按钮、表格或一个页面本身，而是几十到几百个页面长期协作时出现的组织成本：路由权限写在哪里、表单校验谁来负责、HTTP 错误如何统一处理、共享状态由谁创建、组件如何测试、升级如何不拖垮业务迭代、新人如何快速读懂项目约定。如果每个团队自己拼装路由库、表单库、请求层、状态方案、测试工具和脚手架，项目会在目录结构、生命周期、错误处理和命令入口上逐渐分裂。

Angular 的答案是把这些能力收束成一个 batteries-included 的应用平台。它内置 Router、Reactive Forms、HttpClient、DI、模板编译、CLI、测试集成、SSR/SSG 与官方升级路径，让团队优先讨论业务边界，而不是反复争论基础设施怎么搭。对大型团队来说，这种统一性本身就是生产力：不同业务线可以共享组件写法、依赖注册方式、测试习惯和发布流程。

具体痛点可以这样看：

- 路由：企业应用通常有登录态、权限、懒加载、面包屑、数据预取和错误页。Angular Router 用 route config、guard、resolver、lazy route 把导航规则集中表达，避免每个页面手写进入逻辑。
- 表单：复杂后台表单需要同步校验、异步校验、禁用态、脏值判断、提交错误和类型约束。Reactive Forms 把表单状态建模为对象树，使校验和 UI 展示可以分层处理。
- HTTP：真实系统需要认证头、重试、统一错误、loading 状态和 mock 测试。HttpClient 与 interceptor 提供统一管道，业务 service 只暴露领域方法。
- DI：组件树里到处 `new` 对象会让生命周期和测试替换失控。Angular Injector 负责创建、共享和覆盖依赖，让组件声明“需要什么”，而不是管理“怎么创建”。
- 测试：大型项目不能只靠浏览器手点。Angular 的 TestBed、HttpTestingController 和 CLI 测试入口让组件、服务、HTTP 边界都有标准验证方式。
- 升级：企业项目通常要维护多年。Angular 的发布节奏、LTS 窗口、CLI migration 和 `ng update` 把升级从人工搜文档变成可执行流程。
- 团队约定：框架预设了组件、服务、路由、表单、构建和测试的基本形状，减少“每个模块一种风格”的维护成本。

quickstart 用任务工作台展示 Angular 的核心回应：Standalone Component 负责视图边界，Service 负责状态和业务操作，DI 负责把依赖交给组件，Signals 负责细粒度状态变更，模板语法负责把数据、事件和列表渲染连起来。`TaskStore`、`AppComponent`、`inject(TaskStore)`、`signal`、`computed` 和 `@for` 不是孤立 API，而是一组面向长期维护的分工方式。

## 核心定位

Angular 是完整前端应用平台，而不仅是 UI 库。它覆盖组件、模板、Signals、依赖注入、路由、表单、HTTP、SSR/SSG、CLI、测试和升级工具。对于团队协作，它的价值是让多数基础决策落在官方约定内。

## 设计思想

Angular 的设计思想是平台化、显式边界、依赖注入、响应式状态和模板编译。

平台化意味着 Angular 不把自己定位成“只渲染 UI 的库”，而是把应用常见基础设施放在同一个官方体系中。Router、Forms、HttpClient、SSR、测试、构建和升级工具使用一致的 TypeScript、装饰器、DI 与 CLI 约定。这样做的代价是概念更多，但收益是项目越大，团队越少需要为基础设施拼装和风格分歧付费。

显式边界体现在组件、服务、路由和外部 I/O 的职责拆分。组件负责局部 UI 和用户事件，不应该长期塞满业务规则；服务负责领域状态、请求、缓存和副作用；路由负责页面进入规则；拦截器负责跨请求横切逻辑。quickstart 里的 `AppComponent` 只渲染任务和转发点击，`TaskStore` 才拥有任务数组、完成统计和切换逻辑。这种拆分让未来接入 HTTP、权限、缓存或测试替身时，不必重写模板。

依赖注入是 Angular 的组织核心。`@Injectable({ providedIn: "root" })` 把 `TaskStore` 注册到应用级 injector，`inject(TaskStore)` 让组件声明依赖。组件并不知道 `TaskStore` 如何构造，也不负责单例共享。大型应用可以在 root、route 或 component 层级提供不同实例：全局用户会话放 root，某个业务流程的临时状态放 route，局部控件状态放 component。这解决的是“对象生命周期和共享范围没人说得清”的问题。

Signals 是 Angular 对细粒度响应式的现代答案。`signal<Task[]>(...)` 表示可追踪状态，`computed(...)` 表示从状态派生出的只读值，模板调用 `store.completedCount()` 时会建立依赖关系。状态改变后，Angular 能知道哪些表达式需要重新计算。相比把所有变化都塞进手写订阅或大型全局 store，Signals 更适合在组件和服务边界内表达局部业务状态。

Standalone 是为了降低历史包袱和提升局部可读性。过去 Angular 入口常从 NgModule 开始，读者需要先理解 declarations、imports、providers。现代 Angular 可以用 `bootstrapApplication(AppComponent)` 直接启动 Standalone Component，组件自己声明依赖的 imports。大型项目仍可以按 feature 和 route 组织，但单个页面的依赖更容易从文件本身读出来。

模板编译是 Angular 区别于“运行时模板字符串”的关键。`@for (task of store.tasks(); track task.id)`、`[class.done]`、`(click)` 和插值表达式会经过框架编译与类型检查。它解决的不是“少写几行 DOM 操作”，而是让模板成为可分析、可优化、可测试的应用代码。`track task.id` 也体现了大型列表的性能意识：框架可以稳定识别列表项，避免不必要的 DOM 重建。

CLI 与 LTS 策略把工程治理纳入框架生命周期。`ng generate` 让团队生成一致结构，`ng test`/`ng build` 统一命令入口，`ng update` 配合官方迁移脚本处理破坏性变更。对生命周期长、人员流动大的企业项目来说，Angular 的价值不只是运行时能力，也包括可预期的升级和维护路径。

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

- [core-ideas](examples/core-ideas/)：把上一节“解决的问题”和“设计思想”映射到 quickstart 的关键代码片段。
- [quickstart](examples/quickstart/)：Standalone + Service + Signals 任务工作台。

## 版本来源

- 版本基线：Angular 21.x Active；Angular 20.x 仍处于 LTS 窗口。
- 官方来源：https://angular.dev/reference/releases
- 校验日期：2026-05-30
