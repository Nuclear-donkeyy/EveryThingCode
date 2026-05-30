# Ruby 框架与常用库

Ruby 生态的框架很重视表达力：用少量代码描述意图，把大量 Web、数据访问、测试、后台任务细节交给框架和约定处理。本目录面向已经会编程、但没有系统使用 Ruby Web 生态的读者，先列出常用框架和库，再进入 Rails 与 Sinatra 的可运行教学案例。

## 常用框架清单

| 名称 | 类型 | 本仓库状态 | 适合解决的问题 |
| --- | --- | --- | --- |
| [Rails](rails/) | 全栈 Web 框架 | 已覆盖 | 中大型 Web 应用、CRUD 后台、传统服务端渲染、JSON API、快速业务迭代 |
| [Sinatra](sinatra/) | 轻量 Web DSL | 已覆盖 | 小型 API、Webhook、内部工具、教学示例、需要显式结构的服务 |
| Hanami | 模块化 Web 框架 | 待扩展 | 希望比 Rails 更显式、更强调边界和干净架构的 Web 项目 |
| Roda | 路由树 Web 工具包 | 待扩展 | 极高性能、细粒度路由控制、插件式扩展 |
| Grape | API 框架 | 待扩展 | REST API、版本化 API、参数声明和文档化接口 |
| Sidekiq | 后台任务 | 待扩展 | 异步任务、队列、邮件发送、耗时工作、重试和定时任务 |
| Active Record | ORM / 数据映射 | Rails 案例中涉及 | 数据表映射、查询构造、迁移、验证、事务 |
| RSpec | 测试框架 | 待扩展 | 行为驱动测试、可读性强的测试描述、Rails 项目常见测试栈 |
| Minitest | 测试框架 | Rails 默认生态常见 | 标准库风格、轻量单元测试、低依赖测试 |
| Bundler | 依赖管理 | quickstart 均使用 | 管理 Gemfile、安装依赖、固定运行环境 |

## 选择思路

如果目标是完整业务系统，优先从 Rails 开始。Rails 把路由、控制器、模型、视图、任务、测试、数据库迁移、环境配置组织成一个统一工程，适合学习 Ruby 生态的主线工作方式。它的重点不是让每个文件都显式配置，而是用稳定约定让团队少做重复决策。

如果目标是理解 Ruby Web 的最小模型，或者只需要几个接口，优先看 Sinatra。Sinatra 把 HTTP 方法和路径直接写成 Ruby DSL，背后运行在 Rack 之上。它更适合观察一次请求怎样进入 Rack、经过中间件、命中路由并返回响应，也适合把依赖和目录边界显式写出来。

如果项目需要更强的架构边界，可以继续研究 Hanami；如果非常关注路由性能和插件组合，可以看 Roda；如果已有 Rails 应用但 API 层希望更声明式，可以引入 Grape；如果有耗时任务，通常补 Sidekiq；数据访问常见选择是 Active Record；测试则根据团队风格选择 RSpec 或 Minitest。

## 学习路线

1. 先阅读 Ruby 语言章节，理解 block、module、class、异常、迭代器和 Gem 生态。
2. 阅读 [Sinatra](sinatra/)：用最少概念建立 HTTP、Rack、中间件、路由和响应的直觉。
3. 运行 [Sinatra quickstart](sinatra/examples/quickstart/)：观察一个内存任务 API 如何拆分 app、repository、service 和 Rack 入口。
4. 阅读 [Rails](rails/)：把 Sinatra 中手写的结构映射到 Rails 的约定目录、MVC 和 Active Record 思想。
5. 运行 [Rails quickstart](rails/examples/quickstart/)：观察路由、控制器、模型和配置如何协作。
6. 后续扩展数据库、认证、后台任务和测试框架时，再引入 Active Record 迁移、Sidekiq、RSpec/Minitest 等专题案例。

## 本仓库案例

- [Rails quickstart](rails/examples/quickstart/)：用最小 Rails 风格项目讲解 convention over configuration、MVC、路由、控制器和内存模型。
- [Sinatra quickstart](sinatra/examples/quickstart/)：用 Rack 应用讲解轻量 DSL、显式依赖、中间件和 JSON API。
