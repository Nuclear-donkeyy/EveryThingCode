# Laravel

Laravel 是现代 PHP 中最常见的一体化 Web 框架之一。它提供路由、控制器、验证、ORM、迁移、队列、缓存、任务调度、认证、测试、CLI 和部署工具，并用统一的项目结构把这些能力连接起来。学习 Laravel 时，最重要的是理解它如何通过约定和 Service Container 把“写业务功能”变成一条稳定流程。

## 核心定位

Laravel 解决的是 Web 应用从入口到上线的完整工程问题：如何声明 HTTP 路由，如何把请求数据验证后交给业务服务，如何访问数据库，如何组织配置，如何运行队列和定时任务，如何写测试以及如何部署。它尤其适合业务迭代快、功能面广、团队希望少做基础设施粘合的项目。

Laravel 不替你消除架构设计问题。复杂领域仍然需要清晰的 Service、DTO、Policy、事件和事务边界；高并发场景仍然要关注数据库连接、缓存、队列吞吐和 PHP-FPM/Octane 的部署模型。把所有逻辑塞进路由闭包或 Eloquent Model，短期很快，长期会让项目难以测试。

## 设计思想

Laravel 的第一层思想是约定优于配置。默认目录、默认命名、默认配置和 Artisan 命令让项目开局非常快。例如路由放在 `routes/`，服务放在 `app/`，公共入口在 `public/index.php`，配置来自 `.env` 与 `config/`。你可以覆盖这些约定，但先顺着它走更容易理解生态文档。

第二层思想是 Service Container。容器负责创建对象、解析构造函数依赖、管理绑定和生命周期。控制器或路由闭包可以直接声明 `Request`、Repository、Service 等参数，Laravel 会尝试自动解析。这个机制让业务代码少写工厂和全局变量，也让测试更容易替换依赖。

第三层思想是表达力。Route、Validator、Eloquent、Collection、Queue、Event、Notification、Policy 等 API 都追求可读性。Facade 看起来像静态调用，本质上通常是访问容器中的服务。学习时不要只停在“语法优雅”，要追问：这个调用背后解析了哪个服务，依赖在哪里绑定，错误如何冒泡。

第四层思想是围绕数据模型构建应用。Eloquent 使用 Active Record 风格，把表、记录、关系、查询和持久化行为放到 Model 附近。它适合多数 CRUD 与后台系统，但在复杂领域里要避免让 Model 承担所有业务规则，可以把流程编排放进 Service 或 Action。

路由和中间件是 Laravel Web 层的核心。路由把 URL 与处理函数绑定，中间件在请求到达业务前后处理认证、限流、会话、CSRF、日志、跨域等横切逻辑。读 Laravel 项目时，先看路由，再看中间件栈，最后看 Controller/Service/Model，会比从任意类开始读更稳。

## 架构模型

一个典型 Laravel 应用可以看成五层：

- 入口层：`public/index.php` 接收 Web 请求，`artisan` 接收命令行任务。
- 框架启动层：`bootstrap/app.php` 创建 Application，注册路由、中间件、异常处理和服务提供者。
- HTTP 层：`routes/`、Controller、Form Request、中间件负责把外部请求转成业务调用。
- 业务层：Service、Action、Event、Job、Policy 表达业务流程和权限规则。
- 数据层：Eloquent Model、Repository、Migration、Seeder、外部 API Client 负责持久化和集成。

本仓库 quickstart 保留真实入口、真实路由和一个 `TaskRepository`。它没有接入数据库，而是用 JSON 文件模拟持久化，目的是让读者先看清 Laravel 的请求流、容器解析和响应构造。真实项目中，`TaskRepository` 可以被 Eloquent Model、Query Builder 或外部服务替换。

## 请求/执行生命周期

一次 HTTP 请求通常这样流动：

1. Web 服务器把请求转给 `public/index.php`。
2. 入口加载 Composer autoload，再加载 `bootstrap/app.php` 创建 Laravel Application。
3. Application 注册路由、中间件、异常处理和服务提供者，并把请求交给 HTTP Kernel。
4. 中间件按顺序执行，例如信任代理、CORS、认证、限流、请求转换等。
5. 路由匹配 URL 与 HTTP 方法，Laravel 用容器解析闭包或控制器需要的参数。
6. 业务代码读取请求、验证数据、调用 Service/Repository/Eloquent。
7. 返回值被转成 Response；数组和模型通常被序列化为 JSON。
8. 响应离开时，中间件可以继续追加 header、写日志或清理资源。

命令行任务的生命周期类似，但入口是 `artisan`。队列 Worker、调度任务、迁移和测试都通过 Console Kernel/命令系统进入应用，再复用同一套容器和配置。

## 工程结构

quickstart 的结构如下：

```text
examples/quickstart/
  composer.json
  artisan
  bootstrap/app.php
  public/index.php
  routes/api.php
  app/Services/TaskRepository.php
  storage/app/.gitkeep
```

真实项目会继续增加 `app/Models`、`app/Http/Controllers`、`app/Http/Requests`、`database/migrations`、`tests`、`config`、`resources/views` 等目录。扩展时的关键边界是：路由只负责映射入口，Controller 只负责 HTTP 适配，Service/Action 负责业务流程，Model/Repository 负责数据访问，测试覆盖行为而不是复述实现。

## 配置方式

Laravel 配置通常由三部分协作：`.env` 放环境变量，`config/*.php` 把环境变量组织成框架配置，代码通过 `config()` 或类型化配置对象读取。生产环境通常会执行 `php artisan config:cache`，把配置缓存成 PHP 文件，避免每次请求解析大量配置。

quickstart 为了保持最小体积，没有放完整 `config/` 目录，只依赖 Laravel 默认配置和 `bootstrap/app.php` 中的路由声明。真实项目中应把数据库、缓存、队列、日志、邮件、第三方服务密钥放进配置系统，而不是硬编码在 Controller 或 Service 中。

## 模块与依赖管理

Laravel 使用 Composer 管理包，用 PSR-4 autoload 加载 `App\` 命名空间。框架内部通过 Service Provider 注册服务，应用层可以在 Provider 中绑定接口到实现、注册单例、扩展验证规则或发布配置。现代 Laravel 项目也常用自动发现，让包在安装后自动注册 Provider。

Service Container 是模块协作的核心。简单类可以自动装配；需要接口、多实现或特殊构造参数时，可以显式绑定。Facade、helper、事件监听器、队列任务、命令和中间件最终也会回到容器和应用生命周期。读项目时，要学会从类型声明追踪依赖，而不是被 Facade 的静态外观迷惑。

## 数据访问

Laravel 默认数据访问中心是 Eloquent。它把数据库表映射到 Model，支持关系、查询作用域、访问器/修改器、事件、工厂、迁移和 Seeder。对于常见 CRUD，Eloquent 的表达力很高；对于复杂报表和性能敏感 SQL，可以使用 Query Builder 或原生 SQL。

quickstart 用 `TaskRepository` 写入 `storage/app/tasks.json`，展示数据访问边界。这个仓库类的意义不是推荐生产使用 JSON 文件，而是让你看到 Controller/Route 不应该知道数据存在哪里。下一步可以把它替换成 `Task` Eloquent Model：创建 migration，定义 fillable 字段，把 `all/find/create` 改为数据库调用，再补 HTTP 测试。

## 测试方式

Laravel 测试通常分为三层：纯 PHP 单元测试验证 Service/Value Object；Feature Test 通过 `$this->getJson()`、`postJson()` 验证路由、状态码和数据库变化；浏览器测试或端到端测试验证真实页面流程。数据库相关测试常用迁移、事务回滚、Model Factory 和 Seeder。

quickstart README 给出 `composer validate`、`composer install`、`php artisan serve` 和 `curl` 验证命令。依赖安装后，可以继续添加 `tests/Feature/TaskApiTest.php`，验证 `GET /api/tasks`、`POST /api/tasks` 和 404 分支。学习阶段不要只点浏览器，应该把最关键的 API 行为变成自动化测试。

## 部署方式

传统部署会把 Laravel 运行在 Nginx/Apache + PHP-FPM 后面，入口目录指向 `public/`。上线流程通常包含安装依赖、生成 `.env`、迁移数据库、缓存配置、缓存路由、重启队列 Worker。容器化部署会把这些步骤写入 Dockerfile 和启动脚本。

Laravel 生态还提供 Forge、Vapor、Octane、Horizon 等工具。Forge 偏服务器管理，Vapor 面向 Serverless，Octane 用长驻进程提升吞吐，Horizon 管理 Redis 队列。它们不是入门必需品，但在生产场景会影响配置、生命周期和资源管理。

## 适用场景与取舍

优先选择 Laravel 的场景：中小型到大型业务系统、后台管理、API 服务、团队希望快速交付、项目需要队列/缓存/邮件/认证/测试等完整能力。它的生态一致性强，资料多，招聘和协作成本低。

需要谨慎的场景：极小型 Webhook 可能用 Slim 更轻；高度组件化或长期企业平台可能更适合 Symfony；需要极致运行时性能时，要评估 PHP-FPM、Octane、缓存和数据库瓶颈；复杂领域模型不要让 Eloquent Model 无限膨胀。

## 案例索引

- [quickstart](examples/quickstart/)：最小任务 API，包含 Composer 依赖声明、Laravel 入口、API 路由、容器解析的 Repository 和可复制运行命令。

## 版本来源

- PHP 基线：PHP 8.5.x，见根目录 `versions.yaml`。
- Laravel 基线：latest supported major；本 quickstart 的 `composer.json` 使用当前教学基线的主版本约束，运行当天应按官方发布页刷新 patch。
- 官方来源：https://laravel.com/docs/releases
- 校验日期：2026-05-30
