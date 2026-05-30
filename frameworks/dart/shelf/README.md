# Shelf

Shelf 是 Dart 服务端 HTTP 的基础框架之一。它的 API 刻意保持很小：请求进入 `Handler`，横切逻辑由 `Middleware` 包装，多个中间件通过 `Pipeline` 组合。相比 batteries included 的后端框架，Shelf 更像一套可组合的 HTTP 函数工具箱。

## 核心定位

Shelf 解决的是“如何用 Dart 明确处理 HTTP 请求并返回响应”的问题。它定义了 `Request`、`Response`、`Handler`、`Middleware` 等抽象，让你可以把路由、日志、鉴权、错误处理、CORS、静态文件和业务处理组合成一条清晰的请求链。

Shelf 不内建 ORM、模板系统、配置中心、认证体系或应用目录规范。它适合轻量 API、Webhook、边缘服务、内部工具、教学示例和作为更高层框架的基础。需要更完整约定时，可以在 Shelf 之上引入 `shelf_router`、Dart Frog 或自己沉淀项目模板。

本仓库版本基线是 Shelf latest stable，语言基线是 Dart 3.12.x，策略是 latest stable / officially supported，无官方 LTS 标记。

## 设计思想

Shelf 的核心思想是函数组合。`Handler` 本质上是接收 `Request`、返回 `Response` 或 `Future<Response>` 的函数。业务代码可以先从一个普通函数开始，再逐步拆出 repository、service 和 JSON 编码逻辑。

`Middleware` 是对 Handler 的包装：它接收下一个 Handler，返回一个新的 Handler。日志中间件可以在请求前后打印信息，鉴权中间件可以在调用下游前拒绝请求，错误处理中间件可以捕获异常并统一转换成 JSON 响应。这个模型让横切逻辑不必混进每个路由。

`Pipeline` 把多个 Middleware 按顺序串起来。请求进入 pipeline 的第一个中间件，再层层进入最终 Handler；响应则沿相反方向返回。理解这个进入和返回方向，是读懂日志、异常处理、认证和压缩中间件顺序的关键。

Shelf 鼓励显式 HTTP 组合。它不会自动扫描控制器，也不会把隐式上下文注入到方法里。你能在代码里直接看到端口从哪里来、handler 如何创建、middleware 如何排序、请求路径如何分派。这种透明度很适合学习服务端基础，也要求工程纪律。

## 架构模型

一个 Shelf 服务通常由三块组成：启动入口、HTTP 组合层、业务处理层。启动入口读取配置并调用 `serve()`；组合层创建 `Pipeline`，挂载 middleware，再连接到 app handler；业务层处理路径、方法、请求体、内存或数据库数据，并返回 `Response`。

quickstart 中，`bin/server.dart` 同时包含启动入口和一个小型 app factory：`buildHandler()` 返回完整 Handler，方便测试直接调用；`_tasksHandler()` 负责具体 API 分派；`TaskStore` 作为内存 repository；`jsonResponse()` 统一 JSON 输出。

真实项目可以把这些拆成 `lib/server.dart`、`lib/routes/`、`lib/middleware/`、`lib/repositories/`、`lib/models/` 和 `bin/server.dart`。`bin/` 只放启动，`lib/` 放可测试业务代码，这样测试不必真的占用端口。

## 请求/执行生命周期

一次请求从 Dart I/O server 接入，Shelf 把底层 HTTP 信息包装成 `Request`。`serve(handler, address, port)` 把你的 Handler 连接到监听 socket。请求到来后，先进入 Pipeline 最外层 middleware。

以 quickstart 为例，请求先经过 `logRequests()`，这个 middleware 记录方法、路径、状态码和耗时；然后进入 `_jsonErrors()`，它捕获下游抛出的异常并转成 JSON 500；最后进入业务 Handler。业务 Handler 根据 `request.method` 和 `request.url.pathSegments` 判断应该执行 list、create、complete 还是 not found。

Handler 返回 `Response`。如果响应体是 JSON，案例会通过 `jsonEncode` 转成字符串，并设置 `content-type: application/json`。响应再沿中间件链返回，日志 middleware 得到状态码后输出日志，最终由底层 HTTP server 写回客户端。

异步 I/O 通过 Dart 的 Future/async 完成。读取请求体是异步的，访问数据库或外部 API 也应该是异步的。Shelf 不强迫你使用某种并发模型，但所有耗时 I/O 都应该避免阻塞 event loop。

## 工程结构

quickstart 使用最小 Shelf 工程：

```text
examples/quickstart/
├── pubspec.yaml
├── bin/
│   └── server.dart
└── test/
    └── server_test.dart
```

`pubspec.yaml` 声明 Dart SDK、Shelf 和测试依赖。`bin/server.dart` 包含启动入口、handler factory、middleware、内存数据和 JSON 工具函数。`test/server_test.dart` 不启动真实端口，而是直接构造 `Request` 调用 Handler，验证 HTTP 行为。

真实项目建议把启动和业务拆开：`bin/server.dart` 只负责读取环境变量、创建依赖和监听端口；`lib/app.dart` 创建 handler；`lib/routes/` 放路径分派；`lib/repositories/` 放数据访问；`lib/middleware/` 放日志、鉴权和错误处理。这样命令行启动、单元测试和容器部署会更干净。

## 配置方式

Shelf 自身没有配置系统。端口、主机、日志级别、数据库连接串、外部 API 地址通常通过环境变量、Dart 常量、配置文件或你选择的配置库注入。quickstart 用 `PORT` 环境变量控制端口，默认监听 `8080`。

依赖配置通过 `pubspec.yaml` 完成。应用项目建议提交 `pubspec.lock`，服务端部署时使用 `dart pub get` 还原依赖，再用 `dart run` 或 `dart compile exe` 启动/打包。

Middleware 顺序也是配置的一部分。错误处理通常放在靠外层的位置，日志可以在最外层观察最终状态码，鉴权要放在业务 handler 之前，CORS 要根据浏览器访问需求处理预检请求。Shelf 的优势是这些顺序都写在代码里。

## 模块与依赖管理

Shelf 使用普通 Dart package 管理模块。一个服务可以只依赖 `shelf`，也可以逐步加入 `shelf_router`、`shelf_static`、数据库驱动、JWT、日志库和配置库。依赖越多，越需要明确哪些是框架组合层，哪些是业务层。

Shelf 没有内建依赖注入容器。常见做法是用构造函数显式传入依赖：`buildHandler(TaskStore store, Clock clock, Logger logger)`。这让测试替换依赖非常直接，也让应用启动时的对象创建顺序一目了然。

在大型服务里，可以把 Handler 当作边界适配器：它解析 HTTP 请求、调用 service、把结果转成 Response。业务 service 不应该依赖 Shelf 的 `Request` 或 `Response`，否则后续想复用到 CLI、队列 worker 或测试中会更困难。

## 数据访问

quickstart 使用 `TaskStore` 内存仓库保存任务，避免数据库连接和迁移配置掩盖 Shelf 的请求处理思想。它展示了 list、create、complete 三种典型 API 操作，也让测试可以在没有外部服务的情况下运行。

真实项目接入数据库时，可以在 repository 层封装 postgres、sqlite、mysql、redis 或外部 HTTP API。Handler 不直接拼 SQL，而是把请求数据转换成 command/query，交给 service 或 repository。这样错误处理、事务、连接池和重试策略都有明确位置。

JSON 模型可以先手写 Map，复杂后再引入代码生成或数据类模式。无论采用哪种方式，都要在 HTTP 边界处理输入校验、字段缺失、类型错误和业务错误，避免内部异常直接泄露给客户端。

## 测试方式

Shelf 的 Handler 是普通函数，因此非常适合直接测试。你可以构造 `Request('GET', Uri.parse('http://localhost/tasks'))`，调用 `handler(request)`，再断言 `response.statusCode`、headers 和 body。这样不需要启动真实端口，测试速度快且稳定。

quickstart 的测试覆盖了列表接口、创建接口和不存在路径。它验证的是 HTTP contract，而不是内部实现细节：给定方法、路径和 JSON body，应返回什么状态码和响应内容。

当服务变复杂后，可以分层测试：纯业务 service 做单元测试；handler 做 HTTP contract 测试；需要验证真实网络、数据库或容器配置时，再做集成测试。CI 中至少应运行 `dart test` 和静态分析。

## 部署方式

本地开发可以使用 `dart run bin/server.dart`，端口通过 `PORT=9090 dart run bin/server.dart` 覆盖。生产环境可以直接运行 Dart JIT，也可以用 `dart compile exe bin/server.dart -o build/server` 编译成本地可执行文件。

容器化时常见做法是用 Dart SDK 镜像构建依赖和可执行文件，再用更小的 runtime 镜像运行产物。服务端还需要处理健康检查、优雅关闭、日志输出到 stdout/stderr、环境变量注入和反向代理超时。

Shelf 本身没有部署平台绑定，可以部署到 VM、容器、Kubernetes、Cloud Run、Fly.io、Render 或任何能运行 Dart 的环境。部署选择更多取决于项目的网络、扩缩容、数据库和运维要求。

## 适用场景与取舍

优先选择 Shelf 的场景包括：轻量 API、Webhook、内部服务、边缘 HTTP 适配、教学服务端基础、需要显式控制 middleware 顺序的小型系统，以及想在 Dart 生态中构建自定义框架风格的项目。

谨慎选择 Shelf 的场景包括：团队需要完整后台管理、ORM、认证、迁移、模板、代码生成和强约定项目结构；这时 Shelf 需要你自己组合很多能力，Dart Frog 或其他更完整框架可能更合适。

和 Express/Koa、Go `net/http`、Python Starlette 相比，Shelf 的共同点是轻量和组合；差异在于 Dart 的类型系统、async/Future、package 生态和部署成熟度。它适合喜欢显式函数边界的团队，但不适合期待“一装即有全套后台平台”的场景。

## 案例索引

- [quickstart](examples/quickstart/)：内存 tasks API，展示 `Handler`、`Middleware`、`Pipeline`、JSON 响应、环境变量端口和 handler 级测试。

## 版本来源

- 语言基线：Dart 3.12.x
- 框架基线：Shelf latest stable
- 版本策略：latest stable / officially supported，无官方 LTS
- 官方来源：https://pub.dev/packages/shelf
- 校验日期：2026-05-30
