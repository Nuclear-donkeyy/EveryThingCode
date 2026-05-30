# Shelf quickstart

这个案例用一个内存 tasks API 展示 Shelf 的真实最小服务端结构。它没有引入路由库、数据库或认证库，目的是把 Shelf 最核心的 `Handler`、`Middleware`、`Pipeline`、`Request` 和 `Response` 看清楚。

## 目标

完成本案例后，你应该能写出一个 Shelf HTTP 服务，能解释请求如何穿过 middleware 进入 handler，能返回 JSON 响应，能用测试直接调用 handler 而不启动真实端口。

案例包含三个接口：`GET /tasks` 列出任务，`POST /tasks` 创建任务，`POST /tasks/<id>/complete` 标记任务完成。所有数据存在内存仓库里，方便聚焦 HTTP 组合。

## 这个案例解决什么问题

这个 quickstart 不是为了展示一个功能复杂的任务系统，而是为了回答 Dart 服务端入门时最容易混在一起的几个问题：

- HTTP 请求如何从底层 socket 变成业务函数能读懂的对象。
- 日志和错误处理为什么不应该写进每个接口分支。
- JSON 响应为什么需要统一状态码、body 和 `content-type`。
- handler 为什么应该可以不启动端口就被测试。
- 一个 Dart 服务端项目如何和 Flutter 项目保持边界。

`bin/server.dart` 把这些问题压缩在一个文件里：`main()` 只做启动和环境变量读取，`buildHandler()` 组装 middleware 链，`_tasksHandler()` 处理 HTTP contract，`TaskStore` 保存业务数据，`jsonResponse()` 统一 JSON 输出。这样读者可以看到 Shelf 解决的是服务端 HTTP 组合问题，而不是 UI、数据库或后台管理问题。

## 学习重点

- `Handler` 是接收 `Request` 并返回 `Response` 的函数，是 Shelf 的业务入口。
- `Middleware` 包装下游 Handler，用于日志、错误处理、认证、CORS 等横切逻辑。
- `Pipeline` 决定 middleware 顺序，请求按注册顺序进入，响应按相反方向返回。
- Shelf 不强制目录和控制器模型，工程边界需要通过函数、类和包结构主动设计。
- Handler 可直接测试，因此轻量服务不一定需要完整端到端测试才能验证 HTTP contract。
- `shelf_io` 是 adapter，它把 Handler 接到 `dart:io` server；测试则可以绕过 adapter 直接调用 Handler。
- Shelf 与 Flutter 共享 Dart 语言，但职责不同：Shelf 管请求/响应，Flutter 管界面/交互。

## 工程结构

```text
.
├── pubspec.yaml
├── bin/
│   └── server.dart
└── test/
    └── server_test.dart
```

- `pubspec.yaml`：声明 Dart SDK、`shelf`、`shelf_io` 和 `test`。
- `bin/server.dart`：启动入口、handler factory、middleware、内存任务仓库和 JSON 工具。
- `test/server_test.dart`：构造 Shelf `Request`，直接调用 `buildHandler()` 返回的 Handler。

这个结构故意没有 `lib/`、路由库和数据库。真实项目变大后，可以把 `TaskStore`、handler factory、middleware 和模型移进 `lib/`，让 `bin/server.dart` 只负责读取环境变量、创建依赖和调用 `serve()`。

## 运行前提

- Dart 3.12.x 或与仓库基线兼容的最新 stable。
- 当前 shell 可以运行 `dart --version`。
- 首次运行前在本目录执行 `dart pub get` 安装依赖。

## 运行

```bash
dart test
```

启动 HTTP 服务：

```bash
dart pub get
dart run bin/server.dart
```

另开一个终端验证接口：

```bash
curl http://localhost:8080/tasks
curl -X POST http://localhost:8080/tasks -H 'content-type: application/json' -d '{"title":"Read Shelf docs"}'
curl -X POST http://localhost:8080/tasks/1/complete
```

## 预期输出

`dart test` 应通过三类断言：列表接口返回 JSON 数组，创建接口返回 `201` 和新任务，未知路径返回 `404`。

启动服务后，终端会输出监听地址，例如 `Serving at http://localhost:8080`。访问 `GET /tasks` 会返回类似：

```json
[
  {"id":1,"title":"Read Dart async model","done":false},
  {"id":2,"title":"Map a Shelf pipeline","done":false}
]
```

创建任务后，响应状态码是 `201`，body 是新任务 JSON。完成任务后，`done` 字段会变为 `true`。

## 代码讲解

`pubspec.yaml` 定义这个服务的运行边界。`shelf` 提供 `Request`、`Response`、`Handler`、`Middleware` 和 `Pipeline`；`shelf_io` 提供把 Handler 接到本机 HTTP server 的 adapter；`test` 提供普通 Dart 测试入口。这里没有 Flutter SDK 依赖，因为服务端不需要 Widget、渲染树、平台通道或设备模拟器。

`main()` 读取 `PORT` 环境变量，创建 `TaskStore.seeded()`，调用 `buildHandler(store)` 得到完整 Shelf Handler，然后用 `serve()` 监听本地地址。启动代码只负责装配，不直接写业务分支。

`buildHandler()` 是案例的组合入口。它创建 `Pipeline`，先添加 `logRequests()`，再添加 `_jsonErrors()`，最后把请求交给 `_tasksHandler(store)`。这行组合代码就是 Shelf 思想的缩影：HTTP 服务由多个小函数按顺序拼起来。

`_jsonErrors()` 是自定义 middleware。它用 `try/catch` 包住下游 Handler，把未处理异常转换成统一 JSON 500。真实项目里，鉴权、CORS、请求 id、超时、压缩和指标采集也可以用同样模式实现。

`_tasksHandler()` 根据 `request.method` 和 `request.url.pathSegments` 分派请求。为了让初学者看清本质，案例没有引入 `shelf_router`。当路由数量变多时，可以把这里替换成 `Router`，但 Handler 和 Middleware 模型不变。

`TaskStore` 是内存 repository。它隐藏任务列表和 id 递增细节，Handler 只调用 `list()`、`create()`、`complete()`。真实项目可以把它替换成数据库实现，而 HTTP 层代码变化很小。

`server_test.dart` 直接调用 Handler。测试创建 `Request`，等待 `Response`，读取 body 并断言状态码与 JSON 内容。这种测试速度快，也能提醒你把启动监听和业务 handler 分开。

## 思想拆解

| 文件/代码 | 解决的问题 | Shelf 思想 |
| --- | --- | --- |
| `pubspec.yaml` | 明确服务端依赖，避免把 Flutter UI 运行时带进后端 | Dart package 边界清晰，按需组合 |
| `main()` | 启动逻辑和业务分支混在一起会让测试困难 | adapter 只负责把 Handler 接到网络 |
| `buildHandler(TaskStore store)` | 日志、错误处理和业务分派缺少统一装配点 | Handler factory 让依赖和 middleware 顺序显式 |
| `Pipeline().addMiddleware(...)` | 横切逻辑复制到每个接口会失控 | Middleware 链按顺序进入、反向返回 |
| `_jsonErrors()` | 未捕获异常可能泄漏栈信息或返回非 JSON | 用 middleware 统一错误响应格式 |
| `_tasksHandler()` | 路由、方法、请求体和响应状态码需要清楚表达 | Handler 是 HTTP contract 的边界 |
| `TaskStore` | HTTP 层直接管理数据细节会难以替换数据库 | repository 隔离业务数据访问 |
| `jsonResponse()` | 每个接口手写 header 和编码容易不一致 | 响应生成集中到一个小函数 |
| `server_test.dart` | 端到端测试启动慢，端口冲突会带来噪声 | 直接测试 `Request -> Handler -> Response` |

理解这张表后，再引入 `shelf_router`、数据库、JWT 或配置库时，心智模型不会变：新能力只是替换或扩展某一层，而不是推翻 Shelf 的 Handler/Middleware/Pipeline 模型。

## 请求链路拆解

以 `POST /tasks` 为例，请求进入 `serve()` 绑定的 handler 后，先经过 `logRequests()`。它不关心业务，只记录方法、路径、状态码和耗时。接着进入 `_jsonErrors()`，这个 middleware 用 `try/catch` 包住下游，确保未处理异常会变成统一 JSON 500。

随后请求进入 `_tasksHandler(store)`。handler 根据 `request.method` 和 `request.url.pathSegments` 判断这是创建任务接口，调用 `_readJsonObject(request)` 异步读取 body，再检查 `title` 是否存在且非空。校验失败返回 `400`，成功则调用 `store.create(title.trim())`，最后通过 `jsonResponse(task.toJson(), statusCode: 201)` 输出 JSON。

响应沿着相反方向回到 middleware。`_jsonErrors()` 如果没有异常就原样返回，`logRequests()` 得到最终状态码后写日志，底层 `shelf_io` adapter 再把 Shelf `Response` 转成真实 HTTP 响应。测试中的调用少了真实网络层，但保留了 middleware、handler、JSON 和状态码，因此足够验证大多数 HTTP 行为。

## 与 Flutter 的边界对照

| 关注点 | Shelf 服务端 | Flutter 客户端 |
| --- | --- | --- |
| 入口 | `main()` 创建 Handler 并监听端口 | `main()` 调用 `runApp()` 创建 Widget tree |
| 核心对象 | `Request`、`Response`、`Handler`、`Middleware` | `Widget`、`State`、`BuildContext`、`Element` |
| 主要问题 | HTTP contract、JSON、鉴权、日志、部署 | UI 布局、交互、状态展示、平台适配 |
| 测试方式 | `package:test` 直接调用 Handler | `flutter_test` 渲染 Widget 并模拟交互 |
| 部署产物 | Dart JIT 或 `dart compile exe` 的服务进程 | Android/iOS/Web/Desktop 应用包 |

同一个产品可以同时使用 Flutter 和 Shelf：Flutter 调用 Shelf 暴露的 HTTP API，二者共享 Dart 语法和部分数据模型。但 Flutter 的 UI 状态不应依赖 Shelf 的 `Request`，Shelf 的业务服务也不应依赖 Flutter 的 Widget。

## 延伸练习

1. 引入 `shelf_router`，把手写路径分派改成声明式路由，同时保持 `TaskStore` 不变。
2. 为 `POST /tasks` 增加输入校验：缺少 `title` 时返回 `400` 和 JSON 错误。
3. 把 `TaskStore` 替换成 SQLite 或 Postgres repository，并为测试提供内存实现。
4. 增加一个 `authMiddleware()`，要求写接口携带 `authorization` header，并用测试覆盖 `401`。
5. 把 `jsonResponse()` 扩展为统一错误模型，让 `validation_error`、`not_found` 和 `internal_error` 都包含 `code` 与 `message`。

## 验收

- 能说明 `Handler`、`Middleware`、`Pipeline` 的关系和执行顺序。
- 能指出启动入口、业务 handler、内存数据仓库和测试的位置。
- 能新增一个 HTTP 接口，并用 handler 级测试验证状态码和 JSON body。
