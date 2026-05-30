# Python 框架学习索引

Python 的框架生态覆盖 Web 后端、异步服务、数据建模、任务队列、测试、命令行工具和数据应用。学习时不要只看“哪个框架最流行”，更应该先判断项目的主路径：是完整业务系统、轻量 API、异步网关、数据管道、自动化脚本，还是面向团队协作的工程平台。

## 常用框架清单

| 框架/库 | 方向 | 本仓库覆盖 | 适合优先学习的原因 |
| --- | --- | --- | --- |
| Django | 全栈 Web、后台管理、ORM、模板、认证 | 已覆盖：[Django](django/) | 代表 Python “batteries included” 思路，适合理解大型业务系统的约定、应用拆分和数据建模。 |
| FastAPI | 类型驱动 API、异步服务、OpenAPI | 已覆盖：[FastAPI](fastapi/) | 代表现代 Python API 开发方式，把类型标注、数据校验、依赖注入和文档生成连在一起。 |
| Flask | 轻量 Web、插件生态、小型服务 | 待扩展 | API 很小，适合理解 WSGI、装饰器路由、请求上下文和“自己组合组件”的风格。 |
| Starlette | ASGI 基础框架、异步 Web 工具箱 | 待扩展 | FastAPI 的底层基础之一，适合理解 ASGI、中间件、路由和异步请求生命周期。 |
| SQLAlchemy | ORM、SQL 表达式、数据库访问 | 待扩展 | Python 数据访问事实标准之一，适合理解 Unit of Work、Session、连接池和迁移边界。 |
| Pydantic | 数据模型、校验、序列化、配置 | 待扩展 | FastAPI 的重要基础，适合理解类型标注如何变成运行时校验和 JSON Schema。 |
| Celery | 分布式任务队列、定时任务、后台作业 | 待扩展 | 适合理解 Web 请求之外的异步任务、重试、幂等、Broker 和 Worker。 |
| pytest | 测试框架、fixture、参数化、插件 | 待扩展 | Python 工程化必学工具，适合理解测试组织、依赖夹具和回归验证。 |
| Typer / Click | 命令行应用 | 待扩展 | Click 强调命令组合，Typer 借助类型标注降低 CLI 样板代码。 |
| Streamlit | 数据应用、内部工具、快速 UI | 待扩展 | 适合把脚本、数据分析和交互式页面快速连起来。 |

补充生态还包括 Scrapy（爬虫）、Airflow/Prefect（工作流编排）、Polars/Pandas（数据处理）、NumPy/SciPy（科学计算）、Ray/Dask（分布式计算）。这些更偏垂直方向，建议在掌握 Web、数据建模和测试之后按项目需要进入。

## 选择思路

大型业务后台优先从 Django 开始。它内置 ORM、Admin、认证、表单、模板、迁移和安全默认值，适合团队在一套约定里交付完整系统。缺点是框架边界较重，单纯做一个薄 API 时可能显得仪式感偏多。

公开 JSON API、微服务、BFF 或异步 I/O 服务优先考虑 FastAPI。它把 Python 类型标注作为接口契约，用 Pydantic 做请求/响应校验，用依赖注入组织认证、数据库 Session 和配置，并自动生成 OpenAPI。缺点是数据访问、后台管理、任务队列等能力需要自己选配。

需要极小 Web 入口或教学 HTTP 基础时，Flask 和 Starlette 更合适。Flask 帮你理解 WSGI、请求上下文和插件组合；Starlette 帮你理解 ASGI、异步中间件和现代 Python Web 栈的底层结构。

数据访问可以把 SQLAlchemy 当作跨框架能力学习。Django 自带 ORM，更贴合 Django 项目；FastAPI/Flask/Starlette 常与 SQLAlchemy、SQLModel 或直接数据库驱动组合。

工程化建议尽早学习 pytest 和 Pydantic。pytest 是验证代码行为的共同语言，Pydantic 是 API、配置、数据边界建模的常见基础。

后台任务用 Celery 或更轻量的队列工具。不要把耗时任务塞进 Web 请求生命周期里；先明确任务是否需要重试、定时、分布式 worker、结果存储和监控。

命令行工具可选 Typer/Click，数据展示可选 Streamlit。前者适合把自动化流程做成团队可复用命令，后者适合把数据分析脚本变成内部可操作界面。

## 学习路线

1. 先读 Python 语言章节，确认包管理、虚拟环境、类型标注、异常、迭代器、上下文管理器和异步基础。
2. 进入 [Django](django/)：理解 batteries included、MTV、URLConf、ORM/Admin 的工程思路，再运行 quickstart。
3. 进入 [FastAPI](fastapi/)：理解类型驱动接口、ASGI、依赖注入、自动 OpenAPI，再运行 quickstart。
4. 对比两者：Django 更像完整平台，FastAPI 更像 API 组装框架；一个优先约定和内建能力，一个优先类型契约和组合。
5. 补齐横向能力：pytest 做测试，Pydantic 做边界模型，SQLAlchemy 做跨框架数据访问，Celery 做请求外任务。
6. 最后按方向扩展 Flask/Starlette、Typer/Click、Streamlit，把不同框架放到真实业务场景中比较。

## 本仓库案例

- [Django quickstart](django/examples/quickstart/)：用内存数据实现 notes API，展示 Django 项目入口、URLConf、View、测试客户端和本地运行方式。
- [FastAPI quickstart](fastapi/examples/quickstart/)：用内存 Repository 实现 books API，展示 Pydantic 模型、依赖注入、OpenAPI、Uvicorn 启动和 pytest 验证。

两个案例都刻意不接数据库：第一轮先看清框架如何接收请求、定位路由、执行业务逻辑、生成响应和完成自动化测试。数据库、认证、任务队列和部署会在后续进阶案例中加入。
