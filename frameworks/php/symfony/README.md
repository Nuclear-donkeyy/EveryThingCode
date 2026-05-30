# Symfony

Symfony 是 PHP 生态中最重要的组件化框架之一。它既可以作为完整 Web 框架使用，也可以拆成 HttpFoundation、Routing、Console、DependencyInjection、EventDispatcher、Validator、Messenger 等独立组件嵌入其他项目。学习 Symfony 的核心，是理解一个 HTTP 请求如何被 HttpKernel 管线接住，如何通过路由找到控制器，如何由服务容器装配依赖，最后如何返回 Response。

## 核心定位

Symfony 解决的是可组合、可维护、可显式演进的 PHP 工程问题。它适合大型 Web 应用、企业 API、长期维护平台、需要清晰服务边界和配置治理的团队。Symfony 的很多组件也是其他框架的基础，理解它能反过来帮助你读懂 Laravel、Drupal、API Platform、Shopware 等生态。

Symfony 不追求把所有能力都包装成最短语法。相比 Laravel，它通常更显式：服务定义、Bundle、配置文件、Kernel、事件订阅器、编译期容器都需要读者理解。这个成本换来的是边界清楚、可替换性强、组件生命周期明确。

## 解决的问题

PHP 企业 Web/API 的第一个长期痛点，是“入口能跑，但系统边界越来越糊”。小项目可以在 `public/index.php` 里解析请求、连接数据库、判断路由、输出 JSON；业务增长后，同一个文件或同一批全局函数会同时负责 HTTP、认证、日志、配置、错误处理和数据访问。Symfony 把入口压缩到只创建 Kernel，把请求处理交给 HttpKernel 管线，把业务协作交给服务容器，让应用从一开始就有明确边界。

第二个痛点是组件化不足。企业项目常常需要复用路由、控制台命令、校验、事件、消息队列、模板、安全、缓存等能力。如果每个能力都和框架核心绑死，替换和测试会很困难。Symfony 把很多能力拆成独立组件：你可以只用 HttpFoundation 表达 Request/Response，只用 Routing 做路由匹配，只用 DependencyInjection 构建容器，也可以把它们组合成完整框架。这个设计解决的是“既要统一工程模型，又不想被单体黑盒锁死”的问题。

第三个痛点是对象创建和配置散落。Controller 需要 Repository，Repository 需要 Client 或数据库连接，Subscriber 需要 Logger，命令需要业务 Service；如果到处 `new` 对象，测试替换和环境配置都会失控。Symfony 的 Container 在编译阶段读取服务定义、类型声明、参数和环境变量，构建一张可缓存的依赖图。普通场景用 autowire 自动装配，复杂场景用 YAML/PHP/XML 或 Bundle Extension 显式声明，既减少样板，也保留治理能力。

第四个痛点是横切逻辑很难放对位置。认证、CORS、缓存头、异常转换、审计日志、性能追踪、调试工具栏都不是某一个 Controller 的业务，但又必须参与请求生命周期。Symfony 用 HttpKernel 事件和 EventDispatcher 暴露 `kernel.request`、`kernel.controller`、`kernel.response`、`kernel.exception` 等扩展点，让这些能力以监听器/订阅器接入，而不是散落在每个控制器方法里。

第五个痛点是大型团队缺少约定。路由写在哪里、配置如何区分环境、第三方包如何注册服务、测试应该启动多少框架能力，如果没有统一模型，项目会很快变成个人风格集合。Symfony 通过 Kernel、Bundle、属性/配置路由、`config/` 目录、测试基类和 Composer 生态给出稳定约定，让长期维护、升级和代码审查更可控。

## 设计思想

Symfony 的第一层思想是组件化。框架由多个独立组件组成：HttpFoundation 抽象 Request/Response，Routing 做路由匹配，HttpKernel 定义请求处理核心流程，DependencyInjection 构建服务容器，EventDispatcher 连接生命周期扩展点。完整框架只是把这些组件组合成默认工程形态。这样做解决了组件复用和框架可替换性问题：当你只需要 HTTP 对象或路由匹配时，不必启动整个应用；当你使用完整框架时，又能获得一套一致的生命周期。

第二层思想是 Kernel 作为应用组合根。`public/index.php` 不应该知道有哪些控制器、服务和 Bundle，它只负责把环境信息交给 Kernel。Kernel 注册 Bundle，加载容器配置，加载路由，并在运行时把 Request 交给 HttpKernel。这个模型解决了“入口文件越来越厚”的问题，也让测试、缓存预热、命令行和 HTTP 入口共享同一套应用装配方式。

第三层思想是显式配置与自动装配并存。现代 Symfony 默认使用 autowire/autoconfigure，普通 Service 只要写构造函数或控制器参数的类型声明即可被容器解析；同时它保留 YAML/PHP/XML/PHP DSL 配置，让你能在复杂系统中精确控制参数、服务、环境差异和第三方 Bundle。自动装配解决日常样板，显式配置解决多实现、条件装配、环境隔离和团队治理。

第四层思想是 HttpKernel 请求管线。一次请求不是直接跳进控制器，而是经过 Kernel、事件、路由、参数解析、控制器调用、响应事件和异常处理。RouterListener 在 `kernel.request` 阶段匹配路由，ArgumentResolver 把路由参数和服务变成控制器实参，异常监听器把错误转成响应，响应监听器再补充 header 或调试信息。这个模型让日志、安全、缓存、调试工具栏、异常页面等横切能力可以通过事件和中间层接入。

第五层思想是 Bundle 与配置扩展。Bundle 可以注册服务、加载配置、暴露命令、接入事件和提供资源。`FrameworkBundle` 把 HttpKernel、Routing、DependencyInjection、EventDispatcher 等组件接成默认 Web 应用；DoctrineBundle 接入 ORM；SecurityBundle 接入认证授权。应用自身不一定要拆很多 Bundle，但理解 Bundle 能帮助你明白第三方包为什么安装后可以改变框架行为。

第六层思想是属性与配置并用。属性路由让“URL 属于哪个控制器方法”靠近代码，适合快速理解和局部修改；集中配置适合跨模块策略、环境差异和第三方包选项。Symfony 没有把一种方式推到极端，而是允许项目根据规模选择：小型 API 可以用属性和 MicroKernelTrait，复杂平台可以把服务、路由和 Bundle 选项拆到 `config/`。

## 架构模型

一个典型 Symfony 应用可以看成六个部分：

- 入口层：`public/index.php` 通过 Symfony Runtime 创建 Kernel。
- Kernel 层：`src/Kernel.php` 注册 Bundle、加载容器配置、加载路由。
- 路由层：属性路由、YAML/PHP 路由或 XML 路由把请求映射到 Controller。
- 控制器层：Controller 接收 Request，调用 Service，返回 Response/JsonResponse。
- 服务层：Service、Repository、Message Handler、Event Subscriber 承担业务逻辑。
- 配置层：`config/` 或 Kernel 内配置把参数、环境、Bundle 选项和服务装配起来。

quickstart 使用 MicroKernelTrait，把配置和路由导入写在 `src/Kernel.php` 中，减少文件数量，同时保留真实 Symfony 框架结构。它用属性路由声明 API，用 `TaskRepository` 模拟数据访问，用 JSON 文件保存状态。

把 quickstart 对应到这些思想，可以看到 Symfony 的分层非常具体：`composer.json` 决定组件和自动加载边界；`public/index.php` 保持薄入口；`src/Kernel.php` 是应用组合根；`TaskController` 只处理 HTTP 适配；`TaskRepository` 封装任务数据。框架帮你解决“如何接住请求、如何找到控制器、如何创建依赖、如何返回响应”，业务代码只需要表达“任务如何被查询和创建”。

## 请求/执行生命周期

一次 Symfony HTTP 请求通常这样流动：

1. `public/index.php` 加载 `vendor/autoload_runtime.php`。
2. Symfony Runtime 根据环境变量创建 `Kernel`。
3. Kernel 启动时注册 Bundle，构建或读取缓存后的服务容器。
4. `handle()` 接收 Request，并触发 `kernel.request` 等事件。
5. RouterListener 根据路径和方法匹配路由，把控制器信息写入 Request attributes。
6. Argument Resolver 根据控制器签名解析 `Request`、路由参数和服务。
7. Controller 调用业务服务并返回 `Response` 或 `JsonResponse`。
8. Kernel 触发 `kernel.response`，让监听器修改 header、缓存策略或调试信息。
9. 如果抛出异常，异常监听器会把错误转成响应。

命令行、Messenger 消息、事件订阅器也复用同一套容器。理解生命周期后，你会知道扩展行为应该放在哪里：请求前后放事件监听器，业务流程放 Service，HTTP 适配放 Controller，基础设施注册放配置。

## 工程结构

quickstart 的结构如下：

```text
examples/quickstart/
  composer.json
  public/index.php
  src/Kernel.php
  src/Controller/TaskController.php
  src/Service/TaskRepository.php
  var/.gitkeep
```

真实项目通常会增加 `config/packages`、`config/routes`、`src/Entity`、`src/Repository`、`src/MessageHandler`、`src/EventSubscriber`、`migrations`、`templates` 和 `tests`。边界建议是：Controller 不写复杂业务；Service 表达用例；Repository 管数据访问；Event Subscriber 处理生命周期扩展；配置描述基础设施，而不是散落到业务代码里。

## 配置方式

Symfony 支持 YAML、PHP、XML 多种配置格式。现代项目常见结构是 `config/packages/*.yaml` 配 Bundle 选项，`config/services.yaml` 配服务装配，`config/routes.yaml` 或属性路由配 URL。环境变量通过 `%env()%` 注入配置，生产环境会缓存容器和路由以提升启动速度。

quickstart 为了教学把配置写进 `src/Kernel.php`：启用 `FrameworkBundle`，配置 `framework.secret`，对 `App\` 命名空间开启 autowire/autoconfigure，并导入 `src/Controller` 的属性路由。这样文件更少，但思想和真实项目一致。后续扩展时，可以把这些配置拆回 `config/` 目录。

## 模块与依赖管理

Symfony 用 Composer 管理依赖，用 Flex 或手写配置把包接入项目。服务容器是模块协作中心：普通类通过构造函数声明依赖，容器根据类型自动装配；需要多实现、标记服务、环境参数或工厂创建时，再显式配置。

Bundle 是更高层的模块机制。`FrameworkBundle` 接入核心框架能力；DoctrineBundle 接入 ORM；TwigBundle 接入模板；SecurityBundle 接入认证授权。Bundle 可以在编译期修改容器，因此 Symfony 项目有一个很重要的概念：很多依赖关系不是运行时临时找出来的，而是在容器编译阶段确定并缓存。

## 数据访问

Symfony 本身不强制 ORM。最常见组合是 Doctrine ORM：Entity 表达领域对象，Repository 封装查询，Migration 管 schema 变化，EntityManager 管事务和 Unit of Work。也可以直接用 DBAL、PDO、外部 API Client 或消息系统。

quickstart 的 `TaskRepository` 使用 `var/tasks.json` 做极小持久化，目的是让数据访问边界可见。Controller 只知道它能调用 `all()`、`find()`、`create()`，并不关心存储介质。迁移到 Doctrine 时，可以保留 Controller 形状，把 Repository 改成注入 Doctrine Repository 或 EntityManager。

## 测试方式

Symfony 测试通常分三类：单元测试直接实例化 Service；KernelTestCase 启动容器验证服务配置和集成；WebTestCase 使用测试客户端发 HTTP 请求，验证路由、状态码、响应体和数据库变化。对于 Messenger、Console、Event Subscriber，也有对应的集成测试入口。

quickstart 先提供 `composer validate` 和手动 `curl` 验证路径，避免仓库在没有网络和没有 PHP 工具链的机器上误执行安装。依赖安装后，可以加入 `symfony/test-pack` 或 `phpunit/phpunit`，再写 WebTestCase 覆盖 `GET /tasks`、`POST /tasks`、`GET /tasks/{id}` 和错误分支。

## 部署方式

Symfony 生产部署通常包括安装无 dev 依赖、设置 `.env.local` 或平台环境变量、预热缓存、迁移数据库、把 Web 根目录指向 `public/`，并由 Nginx/Apache + PHP-FPM 或容器平台承载。生产环境应关闭 debug，启用 opcode cache，并把日志、缓存目录和上传目录纳入运维策略。

Symfony 也适合容器化和平台部署。容器里常见做法是构建阶段 `composer install --no-dev --optimize-autoloader`，运行阶段由 PHP-FPM 或 FrankenPHP 提供服务。长期项目还要关注缓存清理、零停机迁移、队列 Worker 重启和配置变更回滚。

## 适用场景与取舍

优先选择 Symfony 的场景：大型 API、企业平台、需要细粒度配置、组件复用、多团队协作、长期维护、复杂认证授权或领域边界清晰的系统。它的显式性让复杂项目更容易被分析和重构。

需要权衡的场景：极快交付的中小业务系统可能 Laravel 更省心；非常小的 API 可能 Slim 足够；不熟悉容器和配置的团队会觉得 Symfony 初期概念多。Symfony 的优势通常在项目规模和生命周期拉长后显现。

## 案例索引

- [core-ideas](examples/core-ideas/)：把上一节“解决的问题”和“设计思想”映射到 quickstart 的关键代码片段。
- [quickstart](examples/quickstart/)：最小任务 API，包含 Symfony Runtime 入口、Kernel、FrameworkBundle、属性路由、自动装配服务和可复制运行命令。

## 版本来源

- PHP 基线：PHP 8.5.x，见根目录 `versions.yaml`。
- Symfony 基线：latest LTS line；quickstart 使用 LTS 主线约束，运行当天应按官方发布页刷新 patch。
- 官方来源：https://symfony.com/releases
- 校验日期：2026-05-30
