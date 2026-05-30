# NestJS

NestJS 是一个以 TypeScript 为中心的 Node.js 服务端框架。它借鉴了 Angular 的模块和依赖注入思想，又运行在 Express 或 Fastify 等 HTTP 适配器之上，适合构建结构清晰、可测试、可扩展的 API 服务。

## 核心定位

NestJS 解决的是“Node 后端如何从脚本式 HTTP 处理变成工程化服务”的问题。它提供模块系统、控制器、Provider、依赖注入、管道、守卫、拦截器、异常过滤器、配置、测试工具和多种传输层集成。对于中大型 API、后台管理服务、BFF、微服务网关和需要清晰团队边界的 Node 项目，NestJS 能显著提高结构一致性。

它不负责替你设计领域模型、数据库事务或权限策略，也不强迫使用某个 ORM。NestJS 给出组织方式和生命周期钩子，具体业务仍需要你用清楚的模块边界、DTO、服务层和测试去表达。

## 设计思想

NestJS 的第一思想是模块化。`@Module()` 把控制器、Provider、导入模块和导出能力放在一起，形成一个可组合的业务单元。一个真实项目通常会有 `UsersModule`、`OrdersModule`、`AuthModule` 等模块，而不是把所有路由都写在一个入口文件中。

第二思想是依赖注入。Provider 是可被容器管理的类，控制器或其他服务通过构造函数声明依赖。框架负责创建实例、解析依赖和管理生命周期。这样做的好处是业务类不需要手动 new 依赖，测试时也能轻松替换实现。

第三思想是分层处理请求。控制器负责 HTTP 入口和参数绑定，Provider 负责业务规则，DTO 描述输入输出形状，管道负责转换和校验，守卫负责是否允许继续执行，拦截器负责横切逻辑，异常过滤器负责统一错误响应。初学时可以把它想象成一条可插拔的请求流水线。

## 架构模型

一个最小 NestJS 应用由 `main.ts` 启动。`main.ts` 创建 Nest 应用实例，并加载根模块 `AppModule`。`AppModule` 再导入业务模块，例如 quickstart 中的 `BooksModule`。`BooksModule` 声明 `BooksController` 和 `BooksService`，控制器暴露 HTTP 路由，服务保存和查询内存数据。

典型关系如下：

```text
main.ts
  -> AppModule
     -> BooksModule
        -> BooksController
           -> BooksService
        -> TrimTitlePipe
        -> ApiKeyGuard
```

这套模型让入口、路由、业务、校验和权限成为不同对象。项目变大后，可以继续拆分 repository、domain service、application service、adapter、module exports 等边界。

## 请求/执行生命周期

一次 HTTP 请求进入 NestJS 后，先由底层 HTTP 适配器接收，默认是 Express，也可以切换到 Fastify。框架根据控制器装饰器匹配路由，例如 `@Controller("books")` 与 `@Get()` 组合出 `GET /books`。

命中路由后，请求会依次经过守卫、拦截器前置逻辑、管道、控制器方法、Provider 调用、拦截器后置逻辑、异常过滤器等阶段。quickstart 中的 `ApiKeyGuard` 会检查请求头，`TrimTitlePipe` 会整理输入标题，`BooksController` 把请求交给 `BooksService`，最后由框架把返回值序列化为 JSON。

这种生命周期的价值是让职责落在合适的位置：鉴权不要写进每个业务方法，输入清理不要散落在控制器里，业务状态不要放在入口文件中。

## 工程结构

本仓库 quickstart 使用以下结构：

```text
examples/quickstart/
├── package.json
├── tsconfig.json
├── src/
│   ├── main.ts
│   ├── app.module.ts
│   ├── books/
│   │   ├── books.module.ts
│   │   ├── books.controller.ts
│   │   ├── books.service.ts
│   │   └── dto/create-book.dto.ts
│   └── common/
│       ├── guards/api-key.guard.ts
│       └── pipes/trim-title.pipe.ts
└── scripts/smoke.mjs
```

真实项目可以把 `common` 中的通用能力继续拆成 `auth`、`config`、`database`、`observability` 等模块。业务模块内部通常保留 controller、service、dto、entity、repository、spec 等文件，避免跨模块随意访问内部细节。

## 配置方式

NestJS 的配置可以来自代码、环境变量和配置模块。最小项目只需要 `main.ts` 中的端口和全局前缀；实际项目通常使用 `@nestjs/config` 读取 `.env`，并把数据库、缓存、第三方服务、JWT 等配置注入到模块中。

quickstart 刻意不引入配置模块，只在 `main.ts` 中读取 `process.env.PORT`，在 `ApiKeyGuard` 中读取 `process.env.API_KEY`。这样能让读者先看清框架结构，再学习更复杂的配置封装。

## 模块与依赖管理

NestJS 的模块和 Provider 是它区别于 Express/Fastify 的核心。`providers` 数组告诉容器哪些类由框架创建，`controllers` 数组告诉框架哪些类暴露 HTTP 路由，`imports` 和 `exports` 决定模块之间如何共享能力。

依赖注入的基本规则是：需要什么，就在构造函数中声明什么。`BooksController` 不直接 new `BooksService`，而是声明 `constructor(private readonly booksService: BooksService)`。测试时可以把 `BooksService` 替换为假实现；扩展时可以把内存服务换成数据库服务，而控制器代码保持稳定。

管道和守卫也可以作为可注入对象参与生命周期。管道适合做输入转换、校验和规范化；守卫适合做鉴权、权限判断和租户隔离；拦截器适合做日志、缓存、响应包装和指标采集。

## 数据访问

quickstart 使用内存数组保存图书列表，目的是让模块、控制器和 Provider 的关系保持清楚。`BooksService` 是唯一修改数据的地方，控制器只负责 HTTP 参数到业务调用的翻译。

接入真实数据时，可以把 `BooksService` 拆成 service + repository，或者使用 Prisma、TypeORM、Drizzle、Mongoose 等数据访问方案。关键原则是：控制器不要直接写 SQL 或数据库 SDK，数据库细节应被 Provider 包装起来，并通过 DI 注入到业务服务中。

## 测试方式

NestJS 常见测试分三层。单元测试直接实例化 service，验证业务规则。模块测试使用 Nest TestingModule，替换 Provider 或加载真实模块。HTTP 集成测试启动应用实例，用 supertest 访问接口，验证管道、守卫和序列化是否协同工作。

本仓库 quickstart 提供 `npm run smoke`，不联网安装依赖，只验证项目文件、脚本和关键装饰器是否存在。安装依赖后，可以运行 `npm run build` 检查 TypeScript 编译，再运行 `npm run start:dev` 启动服务。

## 部署方式

本地开发通常使用 `nest start --watch` 或 `ts-node` 风格脚本。生产环境一般先执行 `tsc` 或 Nest CLI 构建到 `dist`，再用 `node dist/main.js` 启动。容器化部署时，需要把 Node.js 版本、依赖安装、构建步骤、环境变量和健康检查写清楚。

NestJS 是长期运行的服务端进程，因此要关注日志、异常处理、优雅关闭、连接池、限流、超时和探针。它不像静态前端那样只部署文件，运行时资源管理非常重要。

## 适用场景与取舍

优先选择 NestJS 的场景：团队使用 TypeScript，后端业务模块较多，需要统一工程结构，需要可测试的依赖注入，需要守卫、管道、拦截器等生命周期扩展点，或希望 Node 服务有接近传统后端框架的组织方式。

谨慎选择 NestJS 的场景：只有几个极简路由、一次性脚本、极致启动速度要求、团队不愿接受装饰器和 DI 约定。此时 Express 或 Fastify 可能更直接。

NestJS 的主要取舍是结构换复杂度。它会让小项目显得“文件多”，但当业务增长后，这些边界会减少隐式依赖和修改风险。

## 案例索引

- [quickstart](examples/quickstart/)：模块化 API 最小项目，包含根模块、业务模块、控制器、Provider、DTO、管道、守卫和可本地执行的 smoke test。

## 版本来源

- 语言生态：JavaScript / TypeScript / Node.js 24.16.0 LTS。
- 框架版本基线：NestJS latest stable，无官方 LTS 标记。
- 策略：使用官方 latest stable；patch 版本在实际安装时通过包管理器锁定。
- 官方来源：https://docs.nestjs.com/
- 校验日期：2026-05-30
