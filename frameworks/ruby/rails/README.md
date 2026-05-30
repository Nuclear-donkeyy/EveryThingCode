# Rails

Rails 是 Ruby 生态最具代表性的全栈 Web 框架。本章节用一个最小任务 API 展示 Rails 的核心工作方式：通过约定目录组织代码，用路由把请求交给控制器，用模型封装业务数据，再由框架完成启动、加载、响应序列化和环境管理。

## 核心定位

Rails 解决的是“如何把一个 Web 产品快速、稳定地组织起来”的问题。它不仅是路由库，也不仅是 ORM，而是一套产品应用框架：路由、控制器、模型、视图、数据库、任务、邮件、缓存、测试、部署入口都放在同一套约定里。

Rails 不追求把所有选择都暴露成显式配置。它默认认为大多数业务系统有相似结构：请求进入路由，控制器协调输入输出，模型表达领域数据，视图或 JSON 呈现结果，配置按环境区分。对于初学者，最重要的是理解这些约定为什么存在，而不是一开始就绕开它们。

## 设计思想

Rails 的第一条思想是 convention over configuration，也就是“约定优于配置”。类名、文件路径、路由资源、控制器动作、环境配置都有稳定命名规则。框架通过这些规则自动加载代码、推断关系、提供默认行为，让开发者把注意力放在业务表达上。

第二条思想是 MVC。Model 负责数据和业务规则，View 负责展示，Controller 负责把 HTTP 请求翻译成一次业务操作。即便本仓库 quickstart 返回 JSON、没有模板视图，也仍然保留 MVC 的分工：`TasksController` 处理 HTTP，`Task` 表达任务数据。

第三条思想是 batteries included。Rails 集成 Active Record、Action Controller、Action View、Active Job 等组件。真实项目可以只使用其中一部分，但 Rails 的学习价值在于看到一个完整 Web 应用怎样从一个入口启动，并被约定拆成可维护的层次。

## 架构模型

quickstart 采用 Rails 风格最小结构：

- `config.ru` 是 Rack 入口，负责让 Web 服务器启动 Rails 应用。
- `config/application.rb` 定义 `QuickstartApp::Application`，加载 Rails 组件和应用目录。
- `config/routes.rb` 把 HTTP 方法与路径映射到控制器动作。
- `app/controllers/tasks_controller.rb` 是请求协调层，读取参数、调用模型、渲染 JSON。
- `app/models/task.rb` 是教学用内存模型，模拟 Active Record 风格的查询和创建接口。
- `Gemfile` 声明 Rails 依赖，由 Bundler 管理安装。

真实 Rails 项目会继续扩展 `app/views`、`app/jobs`、`app/mailers`、`db/migrate`、`test` 或 `spec`。边界仍然相同：控制器保持薄，模型承载领域行为，配置和启动逻辑留在 `config`。

## 请求/执行生命周期

一次 `GET /tasks` 请求大致经过这些阶段：

1. Rack 服务器读取 `config.ru`，把请求交给 Rails application。
2. Rails 中间件栈处理日志、异常、参数解析、请求 ID 等通用工作。
3. 路由表匹配 `GET /tasks`，找到 `TasksController#index`。
4. 控制器实例读取请求上下文，调用 `Task.all` 获取任务列表。
5. 控制器通过 `render json:` 把 Ruby 对象序列化为 JSON 响应。
6. 响应沿 Rack 协议返回给服务器，再返回给客户端。

一次 `POST /tasks` 请求还会经过参数读取和状态码设置：控制器从 `params[:title]` 取输入，调用 `Task.create`，然后以 `201 Created` 返回新资源。这个流向体现了 Rails 的核心：HTTP 细节在控制器边界处理，业务数据放回模型。

## 工程结构

本仓库案例故意保留少量文件，便于读者看清框架骨架：

```text
examples/quickstart/
├── Gemfile
├── config.ru
├── app/
│   ├── controllers/tasks_controller.rb
│   └── models/task.rb
└── config/
    ├── application.rb
    └── routes.rb
```

当项目变大时，不建议把业务规则继续堆进控制器。可以把复杂流程放入 service object，把跨模型规则放入领域对象，把异步工作放入 job，把数据库结构交给 migration。Rails 的约定目录不是限制，而是提醒团队把不同变化原因的代码分开。

## 配置方式

Rails 配置分为三层：

- 依赖配置：`Gemfile` 说明需要 Rails，由 Bundler 安装并生成 lockfile。
- 应用配置：`config/application.rb` 定义应用类、加载路径和框架组件。
- 运行配置：环境变量、`RAILS_ENV`、服务器端口、数据库连接等决定本地、测试、生产环境行为。

quickstart 只保留最小应用配置和依赖声明，避免数据库、资产管线和认证配置掩盖 Rails 主干。真实项目通常还会有 `config/environments/development.rb`、`config/database.yml`、credentials 和 deployment 配置。

## 模块与依赖管理

Rails 通过 Ruby 常量、目录约定和自动加载组织模块。`TasksController` 放在 `app/controllers/tasks_controller.rb`，`Task` 放在 `app/models/task.rb`，Rails 可以根据常量名和路径加载它们。依赖关系不依赖显式容器注入，而是依靠约定、模块命名和少量配置组合起来。

外部依赖由 Bundler 管理。`Gemfile` 声明 `rails`，学习者运行 `bundle install` 后，Bundler 会把依赖解析到本机或 lockfile。应用启动时一般通过 `bundle exec rackup` 或 `bin/rails server` 保证使用项目指定的 gem 版本。

## 数据访问

真实 Rails 项目默认使用 Active Record。Active Record 把数据库表映射为 Ruby 类，把一行记录映射为对象，并提供验证、关联、查询、迁移、事务等能力。例如真实项目中 `Task.create!(title: "Read docs")` 可能会写入 `tasks` 表。

quickstart 为了降低运行门槛，使用内存数组实现 `Task.all` 与 `Task.create`。这不是推荐的生产数据层，而是为了突出控制器如何调用模型。学习者理解请求流后，可以把 `Task` 改成继承 `ApplicationRecord`，再加入 SQLite/PostgreSQL 和 migration。

## 测试方式

Rails 常见测试入口包括：

- 模型测试：验证领域规则、校验、查询和方法行为。
- 控制器或请求测试：验证路由、状态码、JSON 响应和权限边界。
- 系统测试：驱动浏览器验证完整用户流程。

quickstart 的第一验收以启动服务和 curl 请求为主。后续可加入 Minitest 或 RSpec，请求测试应覆盖 `GET /tasks` 和 `POST /tasks`，模型测试应覆盖 `Task.create` 的数据形状和默认状态。

## 部署方式

本地运行通常使用 `bundle exec rackup` 或 `bin/rails server`。生产部署时，需要固定 Ruby 和 Rails 版本，安装 gems，设置 `RAILS_ENV=production`，配置数据库、日志、密钥和反向代理。Rails 可以部署到容器、PaaS、虚拟机或传统应用服务器。

如果项目使用数据库，部署流程还应包含 migration；如果使用资产管线或前端构建，还要加入 assets precompile；如果使用后台任务，还需要独立运行 job worker。Rails 的优势是这些环节都有成熟约定和生态工具。

## 适用场景与取舍

优先选择 Rails 的场景：

- 业务需要快速交付 CRUD、后台管理、表单、认证和数据模型。
- 团队愿意接受统一约定，用框架默认结构换取开发速度。
- 项目需要成熟生态，比如 ORM、邮件、任务、测试、部署和插件。

需要谨慎的场景：

- 只需要几个极小接口，Rails 可能显得过重，Sinatra 或 Roda 更直接。
- 团队想严格手写所有边界和依赖注入，Rails 的自动加载与约定可能需要适应。
- 极端性能场景需要更细粒度控制时，要评估 Rack、中间件和 ORM 成本。

## 案例索引

- [quickstart](examples/quickstart/)：最小 Rails 风格任务 API，展示 Rack 入口、应用配置、路由、控制器和模型。

## 版本来源

- 语言基线：Ruby 4.0.x，策略为 latest stable / 无官方 LTS。
- 框架基线：Rails latest supported series，策略为 latest stable or supported。
- 官方来源：https://rubyonrails.org/
- 版本记录：见仓库根目录 `versions.yaml`。
- 校验日期：2026-05-30
