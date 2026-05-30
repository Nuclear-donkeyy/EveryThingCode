# Rails

Rails 是 Ruby 生态最具代表性的全栈 Web 框架。本章节用一个最小任务 API 展示 Rails 的核心工作方式：通过约定目录组织代码，用路由把请求交给控制器，用模型封装业务数据，再由框架完成启动、加载、响应序列化和环境管理。

## 核心定位

Rails 解决的是“如何把一个 Web 产品快速、稳定地组织起来”的问题。它不仅是路由库，也不仅是 ORM，而是一套产品应用框架：路由、控制器、模型、视图、数据库、任务、邮件、缓存、测试、部署入口都放在同一套约定里。

Rails 不追求把所有选择都暴露成显式配置。它默认认为大多数业务系统有相似结构：请求进入路由，控制器协调输入输出，模型表达领域数据，视图或 JSON 呈现结果，配置按环境区分。对于初学者，最重要的是理解这些约定为什么存在，而不是一开始就绕开它们。

## 解决的问题

Ruby 适合写表达力很强的业务代码，但只靠 Ruby 标准库搭 Web 产品时，团队很快会遇到一组重复问题：路由表如何维护、请求参数在哪里校验、控制器是否会膨胀、数据库表结构如何演进、测试如何组织、邮件和后台任务放在哪里、上线脚本怎样保持一致。Rails 的价值不是“替你写业务”，而是把这些每个产品都会遇到的工程问题放进一套默认结构。

第一类问题是 HTTP 和页面/API 的组织。如果每个接口都手写路径匹配、参数读取、JSON 序列化和状态码，很快会出现命名不统一、错误响应不统一、列表/详情/创建动作不统一的问题。Rails 用 `config/routes.rb`、RESTful resources 和控制器动作约定，把 `GET /tasks`、`POST /tasks`、`GET /tasks/:id` 这类资源操作映射到稳定命名的 action。学习者不需要先发明一套路由风格，团队也更容易在不同模块之间移动。

第二类问题是业务代码的归属。没有框架约定时，数据查询、输入校验、权限判断、响应拼装容易混在同一个函数里。Rails 用 MVC 把变化原因拆开：Controller 处理 HTTP 边界，Model 管数据和领域规则，View 或 JSON serializer 负责呈现。即使 quickstart 没有模板视图，`TasksController` 与 `Task` 的分工仍然展示了 Rails 想解决的核心问题：让 HTTP 代码不要吞掉业务模型。

第三类问题是数据持久化和演进。真实产品离不开数据库、关联、校验、事务和 schema 变更。手写 SQL 和迁移脚本可以工作，但很难保证团队都按同一方式做。Rails 的 Active Record 把表、对象、验证、关联、查询和 migration 连接起来，让 `Task.create!` 这类模型操作既表达业务，又能落到数据库结构。quickstart 用内存 `Task` 模拟这个接口，是为了先看懂控制器如何依赖模型，再替换成真正的 `ApplicationRecord`。

第四类问题是产品周边能力。邮件、异步任务、缓存、文件上传、环境配置、日志、测试和生成器都不是“业务核心”，但每个成熟产品都需要。Rails 用 Action Mailer、Active Job、Active Storage、缓存、Minitest、generators 和统一目录解决这些周边复杂度；开发者可以先沿着默认路径交付，再在确有需要时替换组件。

第五类问题是扩展和复用。大型 Rails 应用往往需要把管理后台、支付、认证、内部平台能力拆成可维护模块。Rails 通过 Railties 和 engines 允许 gem 挂载自己的配置、路由、任务、生成器和初始化逻辑。也就是说，Rails 的“约定”不只服务单个应用，也服务生态组件之间的集成。

## 设计思想

Rails 的第一条思想是 convention over configuration，也就是“约定优于配置”。类名、文件路径、路由资源、控制器动作、环境配置都有稳定命名规则。`TasksController` 放在 `app/controllers/tasks_controller.rb`，`Task` 放在 `app/models/task.rb`，Rails 就能按常量名和路径推断加载关系；`resources :tasks` 也能推导出 `index`、`show`、`create` 等动作。框架通过这些规则减少样板配置，让开发者把注意力放在业务表达上。

第二条思想是 MVC。Model 负责数据和业务规则，View 负责展示，Controller 负责把 HTTP 请求翻译成一次业务操作。即便本仓库 quickstart 返回 JSON、没有模板视图，也仍然保留 MVC 的分工：`TasksController` 处理 `params`、状态码和 `render json:`，`Task` 表达任务数据、查找和创建规则。这个分工的收益是，当数据层从内存数组换成数据库时，路由和 HTTP 边界不需要被重写。

第三条思想是 Active Record 优先。Rails 默认相信多数业务系统的核心复杂度在数据模型及其关系上，所以把 ORM、验证、关联、迁移、事务和查询接口放在一条主线上。对初学者来说，重要的不是记住所有 Active Record API，而是理解“模型是业务语言的中心”：控制器发起用例，模型维护数据规则，migration 记录结构变化。

第四条思想是 RESTful resources。Rails 鼓励把 URL 看成资源集合和资源成员，而不是随意命名的函数调用。`resources :tasks, only: [:index, :show, :create]` 让列表、详情、创建动作有统一形状，也让测试、权限、文档和前端调用更容易约定。

第五条思想是 batteries included 与可替换边界并存。Rails 集成 Active Record、Action Controller、Action View、Action Mailer、Active Job 等组件，真实项目可以只使用其中一部分，也可以替换模板引擎、队列适配器或测试工具。Rails 的学习价值在于看到一个完整 Web 应用怎样从一个 Rack 入口启动，并被约定拆成可维护层次。

第六条思想是通过 Railties 和 engines 组织生态。Rails 自身的组件就是通过 Railtie 接入应用生命周期；第三方 gem 也可以添加 initializer、rake task、generator、路由挂载和配置项。这样，认证、后台管理、支付、监控等能力可以以 Rails 风格融入应用，而不是要求团队为每个库手写胶水代码。

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

- [core-ideas](examples/core-ideas/)：把上一节“解决的问题”和“设计思想”映射到 quickstart 的关键代码片段。
- [quickstart](examples/quickstart/)：最小 Rails 风格任务 API，展示 Rack 入口、应用配置、路由、控制器和模型。

## 版本来源

- 语言基线：Ruby 4.0.x，策略为 latest stable / 无官方 LTS。
- 框架基线：Rails latest supported series，策略为 latest stable or supported。
- 官方来源：https://rubyonrails.org/
- 版本记录：见仓库根目录 `versions.yaml`。
- 校验日期：2026-05-30
