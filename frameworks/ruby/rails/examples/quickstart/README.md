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

## 这个案例解决什么问题

如果不用 Rails，最小任务 API 看起来也不复杂：写一个 Rack app，判断 `PATH_INFO`，解析请求体，手写 JSON，维护数组，再补状态码。但真实项目不会停在三个接口：很快会加入详情页、创建、编辑、权限、数据库、测试、邮件通知和后台任务。Rails 先把这些变化放进稳定位置，让小项目从第一天就拥有可扩展的形状。

本案例用 `GET /tasks`、`POST /tasks`、`GET /tasks/:id` 展示 Rails 如何把常见 Web 产品问题拆开：

- 路由问题：`config/routes.rb` 用 `resources :tasks` 统一资源 URL，不需要在入口文件里手写路径分支。
- MVC 问题：`TasksController` 管 HTTP，`Task` 管数据和规则，避免把参数解析、业务规则和响应拼装塞进一个函数。
- 约定目录问题：`app/controllers`、`app/models`、`config` 的位置本身就是文档，新成员能从目录猜到代码职责。
- ORM 迁移问题：示例先用内存模型模拟 Active Record 接口，后续换成数据库时可以加入 `ApplicationRecord` 和 `db/migrate`，控制器形状保持稳定。
- 测试问题：稳定路由和控制器动作让请求测试可以围绕“状态码 + JSON 契约”编写，模型测试可以独立验证创建和校验规则。
- 产品周边问题：完整 Rails 项目还会把后台任务放入 `app/jobs`，邮件放入 `app/mailers`，生成器负责创建这些约定文件；本案例保留最小骨架，让你先看清主线。

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

`config/application.rb` 负责建立 Rails 应用对象。案例使用 `rails/all` 加载常用组件，说明 Rails 不是单个路由库，而是由 Action Controller、Active Record、Action Mailer、Active Job 等组件组成的应用平台。`config.api_only = true` 表示这个 quickstart 走 API 模式，保留请求处理、路由、参数和 JSON 响应能力，同时不引入模板、静态资产等页面应用才需要的默认配置。`config.eager_load = false` 方便本地学习；真实项目通常还会按 environment 拆分 development、test、production 配置。

`config/routes.rb` 使用 `resources :tasks, only: [:index, :show, :create]` 声明资源路由。Rails 会把 `GET /tasks` 映射到 `TasksController#index`，把 `POST /tasks` 映射到 `TasksController#create`，把 `GET /tasks/:id` 映射到 `TasksController#show`。这就是 convention over configuration 与 RESTful resources 的具体例子：资源名、HTTP 方法、路径和 action 名称有默认含义。随着项目扩大，你通常继续使用 `resources`、`namespace`、`scope` 和嵌套路由组织产品模块，而不是让 URL 变成临时字符串集合。

`TasksController` 只负责 HTTP 边界。`index` 调用 `Task.all` 后直接渲染 JSON；`show` 从 `params[:id]` 读取路径参数，找不到数据时返回 `404`；`create` 读取 `params[:title]`，捕获模型抛出的 `ArgumentError`，把非法输入翻译成 `422 Unprocessable Entity`。控制器不应该知道数据未来是数组、SQLite 还是 PostgreSQL，它只需要协调请求、模型调用和响应。

`Task` 是教学用内存模型。它暴露 `all`、`find`、`create`，模仿 Active Record 对象在控制器中的使用方式，并把“标题不能为空”的规则放在模型侧。后续替换为真正 Active Record 模型时，`Task.create(title: params[:title])` 可以演进为 `Task.create!`、validation、database transaction 和 migration，但路由和控制器的形状可以保持稳定。

Rails 生成器和约定目录在完整项目里会继续放大这种收益。`bin/rails generate model Task title:string done:boolean` 会创建模型和 migration；`bin/rails generate controller Tasks` 会创建控制器和测试入口；`bin/rails generate job NotifyTaskCreated` 会把异步任务放到 `app/jobs`；`bin/rails generate mailer TaskMailer` 会把邮件模板和投递逻辑放到 `app/mailers`。这些工具解决的不是“少敲几行代码”，而是让团队默认把相同类型的变化放在相同位置。

## 请求链路拆解

一次 `POST /tasks` 可以这样读：

1. Rack 服务器执行 `config.ru`，拿到 `QuickstartApp::Application`。
2. Rails application 载入中间件栈、路由表和自动加载路径。
3. `resources :tasks` 匹配 `POST /tasks`，选择 `TasksController#create`。
4. 控制器从 `params[:title]` 读取输入，并调用 `Task.create`。
5. `Task.create` 归一化标题，拒绝空标题，创建任务数据。
6. 控制器把模型结果交给 `render json:`，Rails 序列化并返回 `201 Created`。

这个链路体现了 Rails 的核心取舍：框架接管重复基础设施，应用代码表达资源、动作和领域规则。

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
