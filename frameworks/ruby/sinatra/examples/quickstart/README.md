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

## 工程结构

```text
.
├── Gemfile
├── app.rb
└── config.ru
```

`app.rb` 目前包含应用类、repository 和 service，便于单文件阅读。真实项目变大后，可以把这些类拆进 `app/repositories`、`app/services`、`app/api.rb`。

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

`TaskApi < Sinatra::Base` 使用 subclass style。相比顶层 DSL，这种写法更适合教学和工程化，因为应用配置、路由、helper 和启动入口都属于一个类，测试时也更容易引用。

`before do content_type :json end` 是一个轻量中间件式钩子。它在每个路由执行前设置响应类型，避免每个路由重复写 header。

`get "/tasks"` 直接返回 repository 中的所有任务。`post "/tasks"` 读取请求体、解析 JSON、调用 service，并用 `status 201` 设置创建成功状态码。路由块处理 HTTP 细节，但不直接管理数据存储。

`TaskService` 负责校验 title 和创建任务。`TaskRepository` 负责保存内存数组。这个拆分让未来替换数据库时只改 repository，而不需要改每个路由。

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
