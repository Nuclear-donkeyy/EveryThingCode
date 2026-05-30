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

## 解决的问题

这个 quickstart 刻意选择一个很小的“图书列表”API，因为小案例最容易看清 NestJS 解决的问题。如果用 Express/Fastify 裸写它，也许只需要一个 `server.ts`：注册 `GET /books`、注册 `POST /books`、在 handler 里读请求头、修剪标题、写入数组并返回 JSON。这样的写法在第一天很顺手，但它把几类责任压在了同一个函数里：HTTP 路由、权限、输入处理、业务状态和响应格式。

当接口继续增长时，这种写法会遇到几个典型问题。第一，业务边界靠目录名和口头约定维持，`books` 代码可能随手 import 其他模块内部对象。第二，依赖创建方式不统一，有的 handler 自己 `new` 服务，有的 import 全局单例，测试替换很麻烦。第三，鉴权和输入清理会复制到多个 handler 中，漏掉一次就是线上行为差异。第四，新成员需要先读入口文件和路由注册代码，才能知道某个请求实际经过哪些步骤。

本案例用 NestJS 把这些责任拆开：`AppModule` 表示应用组合了哪些业务模块，`BooksModule` 表示图书模块拥有哪些 controller/provider，`BooksController` 表示 HTTP 入口，`BooksService` 表示业务状态和规则，`ApiKeyGuard` 表示权限前置判断，`TrimTitlePipe` 表示输入规范化。代码文件变多了，但每个文件的变化理由更单一，这就是 NestJS 用结构换长期可维护性的核心价值。

## 设计思想

NestJS 的设计不是“把 Express 包一层装饰器”这么简单，而是把后端服务拆成一组有明确生命周期的对象。

`src/app.module.ts` 体现组合根思想。应用启动时加载 `AppModule`，`AppModule` 决定这个进程启用哪些业务能力。它导入 `BooksModule`，意思是“这个应用包含图书 API”。在裸写服务里，这种组合关系常常藏在 `app.use()` 或路由注册顺序里；NestJS 让它成为模块元数据。

`src/books/books.module.ts` 体现模块边界思想。`controllers: [BooksController]` 说明这个模块的 HTTP 入口，`providers: [BooksService]` 说明这个模块内部可由 DI 容器管理的能力，`exports: [BooksService]` 说明外部模块如果需要图书能力，应该通过服务契约使用，而不是直接访问模块内部文件。真实项目可以继续加入 repository、domain service、policy、mapper，但边界仍由 module 声明。

`src/books/books.controller.ts` 体现协议适配思想。Controller 不保存图书数组，也不决定如何创建图书 ID；它只把 `GET` 和 `POST` 请求映射到内部服务调用。`@Controller("books")`、`@Get()`、`@Post()` 把 HTTP 路由元数据贴近方法本身，`@Body()` 把请求体绑定为 DTO。这让业务逻辑不必知道 Express 的 `req`/`res` 细节。

`src/books/books.service.ts` 体现 Provider 与依赖注入思想。`BooksService` 由 `@Injectable()` 标记，交给 NestJS 容器管理。`BooksController` 通过构造函数声明依赖，而不是自己创建依赖。这样做的收益不是少写几行代码，而是让依赖可替换、可测试、可组合：内存数组可以换成数据库 repository，controller 的路由映射仍然稳定。

`src/common/guards/api-key.guard.ts` 体现 Guard 思想。Guard 回答的问题是“这个请求有没有资格继续执行”。它运行在 controller 方法之前，因此 `POST /books` 不需要在业务方法第一行手写鉴权判断。多个接口需要同样策略时，可以复用同一个 guard；策略变复杂后，也可以把配置、用户解析或权限服务注入进 guard。

`src/common/pipes/trim-title.pipe.ts` 体现 Pipe 思想。Pipe 回答的问题是“交给业务方法之前，输入是否已经是内部希望看到的形状”。这里它把标题首尾空格去掉，真实项目常用 pipe 做 DTO 校验、类型转换和默认值处理。把输入处理放在 pipe 中，能避免 controller 和 service 到处重复 `trim()`、`parseInt()` 或校验分支。

这几层合在一起形成一条请求流水线：底层 HTTP 适配器接收请求，NestJS 根据装饰器匹配 `BooksController.create()`，先运行 `ApiKeyGuard`，再运行 `TrimTitlePipe`，随后 controller 调用 `BooksService.create()`，最后框架序列化返回值。读者理解这条流水线后，就能判断新逻辑应该放在哪里：权限放 guard，输入放 pipe，业务规则放 service，HTTP 绑定放 controller，模块组合放 module。

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

`src/app.module.ts` 是根模块。它导入 `BooksModule`，表示应用启用图书业务能力。模块导入关系是 NestJS 组织大型服务的核心线索，也是区别于裸写路由注册的地方：入口不需要知道每个图书接口的细节，只知道应用需要图书模块。

`src/books/books.module.ts` 声明 `BooksController` 和 `BooksService`。控制器负责 HTTP，服务负责业务数据，模块负责把二者装配起来。`exports: [BooksService]` 表示如果未来有 `ReadingListModule` 需要查询图书，也应该通过导出的服务契约协作，而不是跨目录访问内部状态。

`src/books/books.controller.ts` 使用装饰器声明路由。`findAll()` 响应 `GET /api/books`，`create()` 响应 `POST /api/books`。`@UseGuards(ApiKeyGuard)` 让创建接口先经过守卫，`@UsePipes(TrimTitlePipe)` 让请求体先经过管道。这里的重点是 controller 没有写 `if (apiKey !== ...)`，也没有写 `input.title = input.title.trim()`，它只描述这个路由需要哪些生命周期组件。

`src/books/books.service.ts` 是 Provider。控制器通过构造函数拿到它，而不是自己创建它。换成数据库实现时，可以优先改 service 或进一步引入 repository。测试时也可以给 controller 注入假的 service，只验证 HTTP 参数是否被正确转交。

`src/common/guards/api-key.guard.ts` 读取请求头并决定是否允许继续执行。它把“能不能创建图书”的入口判断从业务方法里拿出来，让权限逻辑可以独立测试和复用。

`src/common/pipes/trim-title.pipe.ts` 修改输入 DTO，把标题规范化后再交给控制器。它展示了 pipe 的最小形态：接收外部输入，返回更适合内部使用的输入。下一步可以把它升级为 class-validator DTO 校验或全局 ValidationPipe。

## 延伸练习

- 给 `GET /api/books/:id` 增加详情接口，并在找不到时抛出 `NotFoundException`。
- 把 `BooksService` 的内存数组替换为 repository 类，再通过 DI 注入 service。
- 增加一个全局异常过滤器或拦截器，统一响应格式和日志。

## 验收

完成后你应该能说明：`Module`、`Controller`、`Provider` 各自负责什么；依赖注入为什么让测试更容易；守卫、管道和业务方法在请求生命周期中的顺序；以及如何把内存数据替换为数据库访问。
