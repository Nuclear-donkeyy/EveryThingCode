# Sinatra

Sinatra 是 Ruby 生态里最经典的轻量 Web 框架之一。它不试图提供完整产品框架，而是用极小 DSL 把 HTTP 方法、路径、参数和响应写成直接可读的 Ruby 代码。学习 Sinatra 很适合建立 Ruby Web 的底层直觉：Rack 是什么，中间件如何串联，路由怎样命中处理逻辑。

## 核心定位

Sinatra 解决的是“用最少结构写一个 HTTP 应用”的问题。它提供路由 DSL、请求/响应对象、渲染辅助、配置和 Rack 集成，但不会强制 MVC、ORM、目录布局或数据库方案。

它不适合直接承担大型全栈框架的全部职责。真实项目如果变复杂，需要开发者主动拆分 service、repository、配置、测试和部署结构。也正因为如此，Sinatra 是学习框架本质的好材料：没有太多自动约定遮挡，请求如何流动一眼可见。

## 解决的问题

轻量 Ruby API 最容易遇到的第一个问题是路由入口散乱。如果直接用 Rack 或手写 `case env["PATH_INFO"]`，HTTP 方法、路径匹配、参数读取和响应构造会混在一起，新增一个端点就要重复判断方法、解析 body、设置 header。Sinatra 用 `get "/tasks"`、`post "/tasks"` 这样的 DSL 把“哪种请求进入哪段代码”写成接近自然语言的 Ruby，路由表不需要额外配置文件也能保持可读。

第二个问题是 Rack 入口和应用代码之间缺少清晰边界。Rack 只规定应用对象要响应 `call(env)` 并返回 `[status, headers, body]`，这很强大，但直接编写会让初学者过早面对底层协议细节。Sinatra 保留 Rack compatibility，让 `config.ru`、Puma、Rackup、Rack middleware 和 Rack::Test 都能直接接入，同时把常见的请求对象、响应状态、header、helper 封装成更好读的 API。

第三个问题是横切逻辑会快速重复。JSON API 通常每个路由都要设置 `Content-Type`、解析 JSON、处理错误、记录日志或检查认证。如果每个路由块都手写这些逻辑，代码会变得短期直接、长期松散。Sinatra 提供 `before` filter、`helpers`、错误处理和 Rack middleware 接口，把“每个请求都要做”的事情从单个路由里拿出来。

第四个问题是轻量框架容易把业务逻辑全部写进路由。Sinatra 不强制 MVC，也不内置 service/repository 目录，这给小项目很高自由度，但也要求开发者主动拆分。quickstart 把 `TaskRepository`、`TaskService` 和 `TaskApi` 放在同一个文件里教学，是为了展示边界：路由负责 HTTP，service 负责业务规则，repository 负责数据访问。项目变大后，这些类应拆到独立文件，而不是让路由块继续膨胀。

第五个问题是测试入口不稳定。直接启动真实端口做测试慢且容易受环境影响；只测纯 Ruby 对象又覆盖不到 HTTP 状态码和响应头。Sinatra 因为是 Rack 应用，可以用 Rack::Test 直接向 `TaskApi` 发请求，不需要启动服务器，同时也能绕过 HTTP 直接测试 service。这让轻量 API 仍然可以保留分层测试策略。

## 设计思想

Sinatra 的核心思想是用 DSL 把 HTTP 协议翻译成 Ruby 代码，而不是把应用放进一套完整产品框架。`get "/tasks"` 表示处理 `GET /tasks`，`post "/tasks"` 表示处理创建请求，代码和 HTTP 语义几乎一一对应。对已经会编程但没写过 Ruby Web 的读者来说，这种写法能快速建立“路由就是入口，返回值就是响应 body”的直觉。

第二个思想是 Rack first。Sinatra 应用本质上仍然是 Rack application，可以被 `config.ru` 暴露给 Puma、Rackup 或其他 Rack 服务器。这样做解决了两层问题：向下兼容 Ruby Web 的共同协议，向上给开发者更舒适的路由、helper、filter API。你可以先用 Sinatra 的 DSL 学会请求流，再逐步理解底层 Rack middleware 和 response triple。

第三个思想是 filter/helper 组合。`before` 适合放每个请求都要执行的动作，例如设置 JSON content type、认证、请求 ID 或日志上下文；`helpers` 适合放路由之间共享的小函数，例如 `json(payload)`。它们解决的是重复代码和横切逻辑污染路由的问题，但不会把应用变成隐式魔法：代码仍然在类里，执行顺序也很短。

第四个思想是 subclass style。Sinatra 支持顶层 DSL，也支持 `class TaskApi < Sinatra::Base`。本仓库选择 subclass style，是因为它更适合教学和工程化：应用配置、helper、filter、路由都属于一个明确的类，`config.ru` 可以 `run TaskApi`，测试也可以直接引用 `TaskApi`。当一个进程里有多个 API 或多个 Rack app 时，subclass style 的边界更稳。

第五个思想是显式结构。Sinatra 可以把所有代码写在一个文件里，但本仓库案例刻意拆出 repository 与 service，让读者看到轻量框架并不等于把业务逻辑塞进路由；框架越轻，工程边界越需要开发者主动维护。Sinatra 负责让 HTTP 入口清楚，应用自己的领域模型、持久化、验证和测试策略仍然要由团队设计。

## 架构模型

quickstart 使用 subclass style：

- `app.rb` 定义 `TaskApi < Sinatra::Base`，包含配置、中间件、路由和错误处理。
- `TaskRepository` 管理内存数据，模拟持久化边界。
- `TaskService` 承载创建任务的业务规则。
- `config.ru` 是 Rack 入口，`run TaskApi` 把应用交给 Rack 服务器。
- `Gemfile` 声明 Sinatra、Rackup、Puma 等运行依赖。

这个结构保留了 Sinatra 的轻量表达，同时避免把所有状态和逻辑混在路由块里。真实项目可以继续把 repository、service、serializers、settings、tests 拆到独立目录。

与 Rails 对照看，Sinatra 更像“把 HTTP 服务所需的最小工具交给你”：路由、请求、响应、filter、helper、Rack 入口。Rails 更像“把产品级 Web 应用的默认解法交给你”：MVC、ORM、migration、assets、mailers、jobs、generators、environments、测试目录。Sinatra 的优势是请求路径短、学习成本低、结构自由；代价是很多工程约定需要自己建立。Rails 的优势是默认能力完整、团队协作约定强；代价是框架层更多，理解请求流需要穿过更多抽象。

## 请求/执行生命周期

一次 `GET /tasks` 请求大致经过这些阶段：

1. Rack 服务器读取 `config.ru`，加载 `app.rb`。
2. Rack 把环境哈希传给 `TaskApi`。
3. Sinatra 执行 before filter，例如设置响应 `content_type :json`。
4. Sinatra 根据 HTTP 方法和路径匹配 `get "/tasks"`。
5. 路由块调用 repository，返回 JSON 字符串。
6. Sinatra 把状态码、响应头和 body 交回 Rack。

一次 `POST /tasks` 请求会额外读取 JSON body。案例中 `request.body.read` 取得原始请求体，`JSON.parse` 转为 Hash，再交给 service 创建任务。如果输入不合法，路由返回 `400`；如果创建成功，返回 `201`。

这条链路能看到 Sinatra 的边界：Rack 负责把 HTTP 请求交给应用，Sinatra 负责匹配路由并提供请求/响应 helper，业务对象负责规则和数据。框架没有替你隐藏这些层，因此很适合用来学习 Web 框架到底在“省掉哪些重复劳动”。

## 工程结构

```text
examples/quickstart/
├── Gemfile
├── app.rb
└── config.ru
```

这个结构已经足够展示 Sinatra 的主要边界：`config.ru` 负责启动协议，`app.rb` 负责应用逻辑。项目扩大时可以演进为：

```text
app/
├── api.rb
├── repositories/task_repository.rb
├── services/task_service.rb
└── serializers/task_serializer.rb
config.ru
spec/
```

拆分标准不是文件数量，而是变化原因：路由变更、业务规则变更、数据存储变更、序列化格式变更应尽量互不影响。

## 配置方式

Sinatra 配置可以写在应用类里，例如 `set :bind, "0.0.0.0"`、`set :port, 4567`、`set :show_exceptions, false`。也可以从环境变量读取端口、数据库 URL、日志级别等运行时设置。

quickstart 只在 `Gemfile` 声明依赖，在 `config.ru` 指定 Rack 入口，并在 `app.rb` 里配置 JSON content type。真实项目可以把配置拆到 `config/settings.rb`，或者用 dotenv、ENV、容器环境变量管理不同环境。

## 模块与依赖管理

Sinatra 没有 Rails 那样强约定的自动加载结构，也没有内置依赖注入容器。依赖管理通常靠普通 Ruby 对象组合：路由块调用 service，service 持有 repository，repository 负责数据读写。这样做的好处是关系清楚，代价是需要开发者自己维护构造和生命周期。

Gem 依赖由 Bundler 管理。`bundle install` 安装 `sinatra`、`puma`、`rackup` 等依赖；`bundle exec rackup` 确保运行时使用当前项目的 gem 集合。Sinatra 的插件机制也很常见，真实项目可以注册日志、验证、模板、认证或 JSON helper。

## 数据访问

quickstart 使用内存 repository。它让 `TaskService` 不直接关心数据放在哪里，只调用 `repository.all` 和 `repository.create`。这是一种教学用端口边界：后续可以把 repository 替换为 SQLite、PostgreSQL、Redis 或 HTTP 客户端。

Sinatra 本身不绑定 ORM。常见选择包括 Active Record、Sequel 或 ROM。小项目可以直接用 Sequel；已有 Rails 生态经验的团队也可能选择 Active Record；更复杂项目则应显式处理连接池、迁移、事务和测试数据。

## 测试方式

Sinatra 最常见的测试方式是 Rack::Test。它不需要启动真实端口，而是直接把请求送入 Rack application，然后断言状态码、响应头和 body。对于本案例，测试应覆盖：

- `GET /health` 返回健康状态。
- `GET /tasks` 返回数组。
- `POST /tasks` 成功创建任务并返回 `201`。
- 空 title 返回 `400`。

业务规则也可以绕过 HTTP，直接测试 `TaskService`。这能让测试更快，并且避免每个业务分支都必须通过路由触发。

## 部署方式

本地可用 `bundle exec rackup -p 4567` 启动。生产环境通常用 Puma 运行 Rack app，并放在 Nginx、Caddy、负载均衡器或平台路由之后。部署时需要固定 Ruby 版本、安装 gems、设置环境变量、配置日志和健康检查。

Sinatra 应用很适合容器化：镜像中安装依赖，启动命令运行 `bundle exec rackup --host 0.0.0.0 -p $PORT`。如果使用数据库，要额外管理连接池和 migration；如果有后台任务，则需要独立进程或外部队列。

## 适用场景与取舍

优先选择 Sinatra 的场景：

- 小型 JSON API、Webhook、内部工具、健康检查服务。
- 教学或原型阶段，需要快速看懂请求如何进入应用。
- 希望显式设计目录和依赖，而不是接受完整全栈约定。

需要谨慎的场景：

- 大型业务系统需要认证、ORM、邮件、任务、管理后台和复杂测试时，Rails 可能更省心。
- 团队缺少工程边界经验时，Sinatra 项目容易退化成超大的路由文件。
- 需要大量框架默认能力时，轻量框架的“自由”会变成额外决策成本。

## 案例索引

- [quickstart](examples/quickstart/)：最小 Sinatra 任务 API，展示 Rack 入口、轻量 DSL、中间件、显式 service/repository 边界。

## 版本来源

- 语言基线：Ruby 4.0.x，策略为 latest stable / 无官方 LTS。
- 框架基线：Sinatra latest stable，策略为 latest stable or supported。
- 官方来源：https://sinatrarb.com/
- 版本记录：见仓库根目录 `versions.yaml`。
- 校验日期：2026-05-30
