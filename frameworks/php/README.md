# PHP 框架学习路线

PHP 生态的主线不是“语法糖越来越多”，而是围绕 Web 请求、模板渲染、数据库、包管理和部署方式逐步工程化。现代 PHP 项目通常以 Composer 组织依赖，用框架处理 HTTP 生命周期，用 ORM 或查询构建器管理数据访问，用 PHPUnit 或 Pest 建立反馈。本目录第一版覆盖 Laravel 与 Symfony：前者代表高生产力、强约定的一体化 Web 框架，后者代表组件化、显式配置和长期维护的企业级框架。

## 常用框架清单

| 框架/库/平台 | 主要用途 | 典型思想 | 本仓库状态 |
| --- | --- | --- | --- |
| Laravel | Web 应用、REST API、后台系统、队列任务 | 约定优于配置、Service Container、Eloquent ORM、门面 Facade、Artisan CLI | 已覆盖：[laravel](laravel/) |
| Symfony | 企业 Web、长期维护 API、组件化平台 | HttpKernel、事件分发、服务容器、Bundle、显式配置 | 已覆盖：[symfony](symfony/) |
| Slim | 轻量 API、Webhook、边缘服务 | PSR-7/PSR-15、中间件管线、最小核心 | 待补充 |
| Laminas | 企业应用、组件库、PSR 基础设施 | 组件化、标准接口、可替换实现 | 待补充 |
| CodeIgniter | 小中型 Web、传统 PHP 团队迁移 | 轻量、低门槛、少配置 | 待补充 |
| Yii | CRUD 后台、表单密集型业务 | Active Record、Gii 代码生成、约定式项目结构 | 待补充 |
| Doctrine ORM | 复杂领域模型、关系型数据库持久化 | Data Mapper、Unit of Work、迁移、查询语言 | 待补充，Symfony 进阶重点 |
| Livewire | Laravel 服务端交互 UI | 服务端组件、局部更新、少写 JavaScript | 待补充，Laravel UI 进阶 |
| PHPUnit / Pest | 单元测试、HTTP 测试、行为测试 | 自动化反馈、断言、测试替身、可读测试 DSL | 待补充，当前案例给出测试入口思路 |
| Composer | 依赖管理、自动加载、脚本入口 | Packagist、语义化版本、PSR-4 autoload、项目脚本 | 当前 quickstart 均使用 |

## 选择思路

如果你希望快速完成完整 Web 应用，优先从 Laravel 开始。Laravel 把路由、验证、ORM、队列、缓存、任务调度、邮件、测试和 CLI 整合在一起，适合从业务功能出发学习。它的学习关键不是记住每个 Facade，而是理解“请求进入路由，容器解析依赖，控制器或闭包协调业务，Eloquent 持久化数据，响应返回 JSON/HTML”这条主线。

如果你面对的是长期维护、多人协作、组件边界清晰、需要显式配置的大型系统，Symfony 更适合。Symfony 的优势在于可组合：你可以只使用 HttpFoundation、Routing、Console、DependencyInjection 等组件，也可以使用完整框架。学习它时要优先理解 HttpKernel、事件、服务容器和配置加载，而不是先背 Bundle 名称。

如果目标是非常轻的 API 或 Webhook，Slim 往往比完整框架更直接；如果团队有大量历史 PHP 项目，CodeIgniter 或 Laminas 可能更容易渐进迁移；如果重点是数据模型和事务一致性，Doctrine ORM 值得单独学习；如果你已经在 Laravel 内部，需要少写前端代码实现交互页面，可以再看 Livewire。

测试工具的选择也要贴合团队。PHPUnit 是事实标准，生态集成最广；Pest 在语法上更轻、更接近行为描述，适合教学和业务测试。无论选择哪一个，框架案例都应该至少能验证路由、状态码、JSON 结构和关键业务分支。

## 学习路线

1. 先读 `languages/php/README.md`、PHP 特性案例和语法速览，确认已经理解数组、对象、命名空间、异常、Composer autoload、类型声明和错误处理。
2. 阅读 [Laravel](laravel/)：先建立“强约定项目结构 + 容器解析对象 + Eloquent 管数据”的心智模型，再跑 quickstart。
3. 阅读 [Symfony](symfony/)：把重点放在 HttpKernel、路由属性、服务自动装配和配置导入上，观察它和 Laravel 的差异。
4. 对比两个 quickstart：Laravel 更像“框架给你一套完整路径”，Symfony 更像“组件组合出清晰管线”。两者都用 JSON 文件模拟持久化，避免数据库遮住框架主线。
5. 进阶时再补 Doctrine、队列、缓存、身份认证、表单、模板和容器化部署。真实项目不要一开始就引入所有组件，应围绕业务风险逐步扩展。

## 本仓库案例

- [Laravel quickstart](laravel/examples/quickstart/)：一个最小任务 API，展示入口、路由、中间件位置、Service Container 自动解析、内存/文件仓库和 JSON 响应。
- [Symfony quickstart](symfony/examples/quickstart/)：一个最小任务 API，展示 Runtime 入口、Kernel、属性路由、服务自动装配、控制器和 JSON 响应。
