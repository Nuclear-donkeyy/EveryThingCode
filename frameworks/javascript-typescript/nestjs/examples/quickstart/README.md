# NestJS quickstart

这是一个最小但真实的 NestJS API 项目。它包含根模块、业务模块、控制器、Provider、DTO、管道、守卫、TypeScript 配置和一个不需要联网安装依赖的结构化 smoke test。

## 目标

通过这个案例学会 NestJS 的核心组织方式：`main.ts` 创建应用，`AppModule` 组合业务模块，控制器暴露 HTTP 路由，Provider 承载业务状态和规则，管道处理输入，守卫决定请求是否允许继续执行。

案例使用“图书列表”作为领域对象，保持业务足够小，但框架结构完整。读者可以在不被数据库和认证系统干扰的情况下理解 NestJS 的请求生命周期。

## 学习重点

- `@Module()` 把控制器和 Provider 组成一个可导入的业务单元。
- `@Controller()` 与 `@Get()`、`@Post()` 把类方法映射为 HTTP 路由。
- `BooksService` 是 Provider，通过构造函数注入给控制器。
- `ApiKeyGuard` 展示守卫如何在控制器执行前做权限判断。
- `TrimTitlePipe` 展示管道如何在业务逻辑前转换输入。
- `npm run smoke` 只做本地结构验收；安装依赖后再使用 `npm run start:dev` 或 `npm run build` 运行框架。

## 工程结构

```text
.
├── package.json
├── tsconfig.json
├── scripts/
│   └── smoke.mjs
└── src/
    ├── main.ts
    ├── app.module.ts
    ├── books/
    │   ├── books.module.ts
    │   ├── books.controller.ts
    │   ├── books.service.ts
    │   └── dto/create-book.dto.ts
    └── common/
        ├── guards/api-key.guard.ts
        └── pipes/trim-title.pipe.ts
```

`books` 是业务模块，`common` 放跨模块复用的生命周期组件。真实项目中可以继续增加 `auth`、`database`、`config`、`observability` 等模块。

## 运行前提

- Node.js 24.16.0 LTS，见仓库根目录 `versions.yaml`。
- npm 随 Node.js 安装即可。
- 本目录声明了 NestJS、TypeScript、Reflect Metadata 和 RxJS 等依赖，但仓库不会联网安装依赖；首次真实运行前需要在本目录执行 `npm install` 生成 lockfile。

## 运行

```bash
npm run smoke
```

安装依赖后可以继续运行：

```bash
npm install
npm run start:dev
```

开发服务器默认监听 `3000`，并使用 `/api` 作为全局前缀：

```bash
curl http://localhost:3000/api/books
curl -X POST http://localhost:3000/api/books -H 'Content-Type: application/json' -H 'x-api-key: local-dev-key' -d '{"title":"  Domain-Driven Nest  ","author":"EveryThingCode"}'
```

生产构建验证：

```bash
npm run build
npm run start
```

## 预期输出

`npm run smoke` 会输出类似：

```text
OK: NestJS quickstart structure looks ready
```

`GET /api/books` 会返回内存中的默认图书列表。`POST /api/books` 如果没有 `x-api-key` 请求头会被守卫拒绝；带上默认 `local-dev-key` 后，`TrimTitlePipe` 会把标题首尾空格去掉，再由 `BooksService` 写入内存数组。

## 代码讲解

`src/main.ts` 是启动入口。它调用 `NestFactory.create(AppModule)` 创建应用，设置全局前缀 `/api`，再监听端口。入口文件只做启动和全局配置，不写业务规则。

`src/app.module.ts` 是根模块。它导入 `BooksModule`，表示应用启用图书业务能力。模块导入关系是 NestJS 组织大型服务的核心线索。

`src/books/books.module.ts` 声明 `BooksController` 和 `BooksService`。控制器负责 HTTP，服务负责业务数据。这个分工让测试和替换变得容易。

`src/books/books.controller.ts` 使用装饰器声明路由。`findAll()` 响应 `GET /api/books`，`create()` 响应 `POST /api/books`。`@UseGuards(ApiKeyGuard)` 让创建接口先经过守卫，`@UsePipes(TrimTitlePipe)` 让请求体先经过管道。

`src/books/books.service.ts` 是 Provider。控制器通过构造函数拿到它，而不是自己创建它。换成数据库实现时，可以优先改 service 或进一步引入 repository。

`src/common/guards/api-key.guard.ts` 读取请求头并决定是否允许继续执行。`src/common/pipes/trim-title.pipe.ts` 修改输入 DTO，把标题规范化后再交给控制器。

## 延伸练习

- 给 `GET /api/books/:id` 增加详情接口，并在找不到时抛出 `NotFoundException`。
- 把 `BooksService` 的内存数组替换为 repository 类，再通过 DI 注入 service。
- 增加一个全局异常过滤器或拦截器，统一响应格式和日志。

## 验收

完成后你应该能说明：`Module`、`Controller`、`Provider` 各自负责什么；依赖注入为什么让测试更容易；守卫、管道和业务方法在请求生命周期中的顺序；以及如何把内存数据替换为数据库访问。
