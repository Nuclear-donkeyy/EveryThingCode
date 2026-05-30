# Sinatra quickstart：任务 API

本案例用一个小型 JSON API 展示 Sinatra 的核心：轻量路由 DSL、Rack 入口、中间件式请求处理，以及由普通 Ruby 对象组成的业务边界。

## 目标

- 理解 Sinatra 如何把 `get`、`post` 等 DSL 映射到 HTTP 路由。
- 理解 `config.ru` 与 Rack 的关系。
- 理解轻量框架中为什么仍然要拆出 service 和 repository。
- 学会用 curl 验证一个最小 Sinatra API。

## 学习重点

这个案例把 Sinatra 思想映射到代码：

- `config.ru`：Rack 入口，负责加载并运行 `TaskApi`。
- `TaskApi < Sinatra::Base`：应用类，声明 before filter、错误处理和路由。
- `TaskRepository`：内存数据访问边界，未来可替换为数据库。
- `TaskService`：业务规则边界，负责校验和创建任务。
- `json` helper：把 Ruby Hash/Array 转成 JSON 响应。

Sinatra 让路由非常直接，但案例仍然避免把业务规则写满路由块。这样读者可以同时学到框架 API 和工程边界。

## 这个案例解决什么问题

如果不用 Sinatra，只用 Rack 写这个 API，需要自己判断 `REQUEST_METHOD`、解析 `PATH_INFO`、读取 `rack.input`、构造 JSON header、处理异常并返回 `[status, headers, body]`。这些代码不难，但很快会把“HTTP 协议适配”和“任务业务逻辑”缠在一起。Sinatra 解决的是这层重复劳动：让路由、状态码、响应格式和请求对象更像普通 Ruby 代码。

这个 quickstart 刻意选择任务 API，而不是页面渲染，是为了聚焦轻量 JSON 服务的常见问题：

- 路由如何从 `GET /tasks`、`POST /tasks` 进入对应 Ruby 代码。
- Rack 入口如何把 `config.ru`、服务器和应用类连起来。
- 每个响应都要 JSON content type 时，如何避免每个路由重复设置 header。
- 创建任务时，JSON 解析、输入校验、业务创建和错误响应如何分层。
- 小项目如何先保持单文件可读，同时保留拆成 service/repository 的演进路径。

## 工程结构

```text
.
├── Gemfile
├── app.rb
└── config.ru
```

`app.rb` 目前包含应用类、repository 和 service，便于单文件阅读。真实项目变大后，可以把这些类拆进 `app/repositories`、`app/services`、`app/api.rb`。

三个文件分别承担不同问题：

- `Gemfile` 解决“运行环境由哪些 gem 组成”的问题，固定 Sinatra、Puma、Rackup 这些运行依赖。
- `config.ru` 解决“Rack 服务器如何找到应用入口”的问题，`run TaskApi` 是整个 HTTP 服务交给 Rack 的地方。
- `app.rb` 解决“请求进入应用后怎么匹配、校验、响应”的问题，同时用普通 Ruby 类保留业务边界。

## 运行前提

- Ruby 4.0.x 或当前受支持 Ruby stable。仓库版本基线见根目录 `versions.yaml`。
- Bundler。
- 可以访问 RubyGems 时，运行 `bundle install` 安装 Sinatra、Puma 和 Rackup。仓库只提供依赖声明，不提交联网安装后的 vendor 目录。

## 运行

```bash
ruby -c app.rb
```

安装 Sinatra 后启动 Rack 应用：

```bash
bundle install
bundle exec rackup -p 4567
```

另开终端请求接口：

```bash
curl http://localhost:4567/health
curl http://localhost:4567/tasks
curl -X POST http://localhost:4567/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Write a Sinatra route"}'
```

## 预期输出

`GET /health` 返回：

```json
{
  "status": "ok"
}
```

`GET /tasks` 返回任务数组；`POST /tasks` 成功时返回 `201 Created` 和新任务。请求体不是合法 JSON 或 title 为空时，会返回 `400` 和错误说明。

## 代码讲解

`config.ru` 是 Rack 的约定入口。`require_relative "app"` 加载应用定义，`run TaskApi` 把应用交给 Rack 服务器。Sinatra 因为兼容 Rack，可以自然接入 Puma、Rackup、中间件和 Rack::Test。

`Gemfile` 声明了三类依赖。`sinatra` 提供路由 DSL、request/response helper、filter 和 Rack application；`puma` 是常见的 Rack server，负责监听端口、接收 HTTP 请求并调用应用；`rackup` 提供读取 `config.ru` 并启动 Rack app 的命令。这个拆分也说明 Sinatra 自己不是“服务器”，它是运行在 Rack 服务器之上的应用框架。

`TaskApi < Sinatra::Base` 使用 subclass style。相比顶层 DSL，这种写法更适合教学和工程化，因为应用配置、路由、helper 和启动入口都属于一个类，测试时也更容易引用。以后如果项目里有 `AdminApi`、`WebhookApi` 或不同版本的 API，也可以各自继承 `Sinatra::Base`，再由 Rack 组合。

`configure do set :show_exceptions, false end` 让错误处理更接近真实 API：框架不要在响应里展示调试异常页面，而应由应用返回明确的 JSON 错误。生产项目还会继续配置日志、环境、session、static files 或自定义 middleware。

`before do content_type :json end` 是一个轻量中间件式钩子。它在每个路由执行前设置响应类型，避免每个路由重复写 header。如果以后加认证，可以在 `before` 里检查 token；如果只想影响部分路由，也可以写带路径条件的 filter 或使用 Rack middleware。

`helpers do def json(payload) ... end end` 解决的是 JSON 响应的重复序列化问题。路由只需要写 `json(status: "ok")`，不用在每个路由里记住 `JSON.generate`。helper 适合放“小而稳定、与 HTTP 表达相关”的工具；复杂业务规则不应放 helper，而应放 service。

`get "/tasks"` 直接返回 repository 中的所有任务。`post "/tasks"` 读取请求体、解析 JSON、调用 service，并用 `status 201` 设置创建成功状态码。路由块处理 HTTP 细节，但不直接管理数据存储。

`TaskService` 负责校验 title 和创建任务。`TaskRepository` 负责保存内存数组。这个拆分让未来替换数据库时只改 repository，而不需要改每个路由。

## 设计思想拆解

一次 `POST /tasks` 请求可以按这条链路理解：

1. Puma/Rackup 读取 `config.ru`，加载 `TaskApi`。
2. Rack 把 HTTP 请求转换成环境对象并调用 Sinatra 应用。
3. Sinatra 先执行 `before`，把响应类型设为 JSON。
4. Sinatra 根据方法和路径命中 `post "/tasks"`。
5. 路由读取 `request.body.read` 并用 `JSON.parse` 转成 Ruby Hash。
6. 路由把 `payload["title"]` 交给 `TaskService#create_task`。
7. service 做业务校验，再调用 repository 创建任务。
8. 路由设置 `status 201`，用 `json(task)` 返回响应。
9. JSON 解析错误或业务错误被 rescue 成 `400` JSON 响应。

这条链路体现了 Sinatra 的核心取舍：框架帮你把 Rack、路由、filter、请求对象和响应状态组织好，但不会替你规定领域模型、数据库、目录结构或测试策略。轻量框架的“轻”不是没有架构，而是架构必须更显式地写在你的代码里。

## 与 Rails 对照

Rails 会把同类 API 拆到 routes、controller、model、serializer、migration、test 等约定目录，并内置 Active Record、环境配置、生成器和测试结构。它适合功能面宽、团队协作强、需要完整默认解法的业务系统。

Sinatra 则把路由和 Rack 入口放在更近的位置。这个 quickstart 中，一个 `config.ru` 加一个 `TaskApi` 就能跑起来，读者可以直接看到请求如何进入路由、如何调用 service、如何返回 JSON。它适合小型 API、Webhook、内部工具、框架原理教学和需要高度自定义结构的服务。代价是认证、ORM、迁移、后台任务、配置分层这些能力都要自己选择和组装。

## 延伸练习

1. 用 Rack::Test 添加自动化测试，覆盖 `/health`、`GET /tasks`、`POST /tasks` 和非法输入。
2. 把 `TaskRepository` 改成 SQLite 或 Sequel 实现，保持路由和 service 不变。
3. 增加 `PATCH /tasks/:id`，实现任务完成状态切换。

## 验收

完成本案例后，读者应该能够：

- 说明 Sinatra 路由 DSL 与 HTTP 方法、路径的关系。
- 说明 `config.ru` 为什么是 Rack 应用入口。
- 在不改变路由形状的前提下替换 repository。
- 新增一个路由并返回正确状态码和 JSON。
