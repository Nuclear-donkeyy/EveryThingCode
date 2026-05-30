# Rails quickstart：任务 API

本案例是一个最小 Rails 风格项目，用 JSON API 讲清 Rails 的入口、路由、控制器和模型分工。它故意不接数据库，避免第一次学习时被 migration、连接配置和生产部署细节分散注意力。

## 目标

- 理解 Rails 应用如何从 Rack 入口启动。
- 理解 convention over configuration 如何体现在 `config`、`app/controllers`、`app/models` 目录中。
- 理解路由如何把 HTTP 请求交给控制器动作。
- 理解控制器和模型的职责边界。

## 学习重点

这个案例把 Rails 思想映射到代码：

- `config.ru`：Rack 服务器入口，负责加载应用并 `run` 它。
- `config/application.rb`：应用类，负责加载 Rails 和本项目代码。
- `config/routes.rb`：声明资源路由，说明 URL 与控制器动作的关系。
- `TasksController`：处理 HTTP 输入输出，保持尽量薄。
- `Task`：封装任务数据，模拟 Active Record 风格接口。

重点不是“这个内存模型可以生产使用”，而是看清当模型换成数据库后，控制器和路由几乎不需要改变。

## 工程结构

```text
.
├── Gemfile
├── config.ru
├── app/
│   ├── controllers/
│   │   └── tasks_controller.rb
│   └── models/
│       └── task.rb
└── config/
    ├── application.rb
    └── routes.rb
```

## 运行前提

- Ruby 4.0.x 或当前受支持 Ruby stable。仓库版本基线见根目录 `versions.yaml`。
- Bundler。
- 可以访问 RubyGems 时，运行 `bundle install` 安装 Rails。仓库只提供依赖声明，不提交联网安装后的 vendor 目录。

## 运行

```bash
ruby -c app/models/task.rb
```

安装 Rails 后启动 Rack 应用：

```bash
bundle install
bundle exec rackup -p 3000
```

另开终端请求接口：

```bash
curl http://localhost:3000/tasks
curl -X POST http://localhost:3000/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Read Rails routing"}'
curl http://localhost:3000/tasks/1
```

如果你使用完整 Rails 脚手架生成项目，也可以把这些文件迁移到 Rails 项目后用 `bin/rails server` 启动。

## 预期输出

`GET /tasks` 会返回任务数组，例如：

```json
[
  {
    "id": 1,
    "title": "Read Rails guides",
    "done": false
  }
]
```

`POST /tasks` 会返回 `201 Created` 和新任务 JSON。`GET /tasks/1` 会返回单个任务；如果 ID 不存在，会返回 `404`。

## 代码讲解

`config.ru` 是 Rack 标准入口。Rack 服务器并不需要理解 Rails 的目录，它只需要拿到一个可调用的 application。`require_relative "config/application"` 加载应用类，`run QuickstartApp::Application` 把请求交给 Rails。

`config/application.rb` 负责建立 Rails 应用对象。案例使用 `rails/all` 加载常用组件，并设置 `config.eager_load = false` 方便本地学习。真实项目通常还会按环境拆分 development、test、production 配置。

`config/routes.rb` 使用 `resources :tasks, only: [:index, :show, :create]` 声明资源路由。Rails 会把 `GET /tasks` 映射到 `TasksController#index`，把 `POST /tasks` 映射到 `TasksController#create`。这就是 convention over configuration 的一个具体例子：命名和动作有默认含义。

`TasksController` 只负责 HTTP 边界。它从 `params` 读取输入，调用 `Task`，再用 `render json:` 返回响应。控制器不应该知道数据未来是数组、SQLite 还是 PostgreSQL。

`Task` 是教学用内存模型。它暴露 `all`、`find`、`create` 和 `as_json`，模仿 Active Record 对象在控制器中的使用方式。后续替换为真正 Active Record 模型时，路由和控制器的形状可以保持稳定。

## 延伸练习

1. 把 `Task` 改成继承 `ApplicationRecord`，加入 SQLite 数据库和 migration。
2. 为 `POST /tasks` 增加 title 不能为空的验证，并返回 `422 Unprocessable Entity`。
3. 加入请求测试，覆盖成功创建、查询不存在任务和非法输入。

## 验收

完成本案例后，读者应该能够：

- 画出 Rails 请求从 Rack 到路由、控制器、模型再到 JSON 响应的路径。
- 说明 Rails 约定目录如何减少配置。
- 修改 `routes.rb` 新增一个 `PATCH /tasks/:id` 路由。
- 判断哪些代码应该放在控制器，哪些应该放在模型或 service。
