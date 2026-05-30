# Shelf quickstart

这个案例用一个内存 tasks API 展示 Shelf 的真实最小服务端结构。它没有引入路由库、数据库或认证库，目的是把 Shelf 最核心的 `Handler`、`Middleware`、`Pipeline`、`Request` 和 `Response` 看清楚。

## 目标

完成本案例后，你应该能写出一个 Shelf HTTP 服务，能解释请求如何穿过 middleware 进入 handler，能返回 JSON 响应，能用测试直接调用 handler 而不启动真实端口。

案例包含三个接口：`GET /tasks` 列出任务，`POST /tasks` 创建任务，`POST /tasks/<id>/complete` 标记任务完成。所有数据存在内存仓库里，方便聚焦 HTTP 组合。

## 学习重点

- `Handler` 是接收 `Request` 并返回 `Response` 的函数，是 Shelf 的业务入口。
- `Middleware` 包装下游 Handler，用于日志、错误处理、认证、CORS 等横切逻辑。
- `Pipeline` 决定 middleware 顺序，请求按注册顺序进入，响应按相反方向返回。
- Shelf 不强制目录和控制器模型，工程边界需要通过函数、类和包结构主动设计。
- Handler 可直接测试，因此轻量服务不一定需要完整端到端测试才能验证 HTTP contract。

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

`main()` 读取 `PORT` 环境变量，创建 `TaskStore.seeded()`，调用 `buildHandler(store)` 得到完整 Shelf Handler，然后用 `serve()` 监听本地地址。启动代码只负责装配，不直接写业务分支。

`buildHandler()` 是案例的组合入口。它创建 `Pipeline`，先添加 `logRequests()`，再添加 `_jsonErrors()`，最后把请求交给 `_tasksHandler(store)`。这行组合代码就是 Shelf 思想的缩影：HTTP 服务由多个小函数按顺序拼起来。

`_jsonErrors()` 是自定义 middleware。它用 `try/catch` 包住下游 Handler，把未处理异常转换成统一 JSON 500。真实项目里，鉴权、CORS、请求 id、超时、压缩和指标采集也可以用同样模式实现。

`_tasksHandler()` 根据 `request.method` 和 `request.url.pathSegments` 分派请求。为了让初学者看清本质，案例没有引入 `shelf_router`。当路由数量变多时，可以把这里替换成 `Router`，但 Handler 和 Middleware 模型不变。

`TaskStore` 是内存 repository。它隐藏任务列表和 id 递增细节，Handler 只调用 `list()`、`create()`、`complete()`。真实项目可以把它替换成数据库实现，而 HTTP 层代码变化很小。

`server_test.dart` 直接调用 Handler。测试创建 `Request`，等待 `Response`，读取 body 并断言状态码与 JSON 内容。这种测试速度快，也能提醒你把启动监听和业务 handler 分开。

## 延伸练习

1. 引入 `shelf_router`，把手写路径分派改成声明式路由，同时保持 `TaskStore` 不变。
2. 为 `POST /tasks` 增加输入校验：缺少 `title` 时返回 `400` 和 JSON 错误。
3. 把 `TaskStore` 替换成 SQLite 或 Postgres repository，并为测试提供内存实现。

## 验收

- 能说明 `Handler`、`Middleware`、`Pipeline` 的关系和执行顺序。
- 能指出启动入口、业务 handler、内存数据仓库和测试的位置。
- 能新增一个 HTTP 接口，并用 handler 级测试验证状态码和 JSON body。
