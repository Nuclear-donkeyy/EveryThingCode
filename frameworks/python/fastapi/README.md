# FastAPI

FastAPI 是现代 Python API 框架，核心卖点是类型驱动、自动校验、自动 OpenAPI 文档和 ASGI 异步能力。它适合构建 JSON API、微服务、BFF、AI/数据服务接口，以及需要清晰接口契约的后端服务。

## 核心定位

FastAPI 解决的是“用 Python 快速构建高质量 HTTP API”的问题。它把函数签名、类型标注、Pydantic 模型、依赖注入和 OpenAPI 文档合在一起，让接口定义本身就能成为校验规则、文档和测试入口。

FastAPI 不试图内置完整后台系统。它没有 Django Admin 那样的官方后台，也不强制 ORM、迁移、模板、认证或任务队列。真实项目会根据需要组合 SQLAlchemy、Pydantic Settings、Alembic、Celery/RQ、pytest、OpenTelemetry 等工具。

## 解决的问题

如果直接用一个轻量 HTTP 框架手写 API，最早遇到的不是“如何返回 JSON”，而是边界规则会散落在很多地方。路径参数要从字符串转成整数，查询参数要判断可选和值域，请求体要检查字段是否存在、类型是否正确、字符串是否为空；这些逻辑如果写在路由函数里，业务代码很快会被 `if`、`try`、字典访问和错误响应淹没。

第二个痛点是接口契约容易漂移。后端代码里写了一套请求规则，前端文档里写了另一套，测试又根据旧行为断言。新增字段、修改响应结构或调整错误码时，代码、文档、客户端和测试很难保持同步。手写 OpenAPI 也能解决一部分问题，但维护成本高，而且经常落后于真实代码。

第三个痛点是序列化和安全边界不清晰。数据库对象、内部领域对象、响应 JSON 往往不是同一个形状。直接 `return dict` 很方便，但容易把内部字段、空值、临时状态或不该暴露的信息返回给调用方；手写转换函数又会在每个接口重复出现。

第四个痛点是横切依赖会污染路由。认证、权限、数据库 session、配置、外部 API client、仓库对象都需要被路由使用。如果在路由里直接创建这些对象，测试替换困难，连接生命周期难管，代码也会把 HTTP 处理、依赖装配和业务规则混在一起。

第五个痛点是异步 I/O 和测试契约。现代 API 经常等待数据库、缓存、消息队列或第三方 HTTP 服务。WSGI 同步模型可以工作，但在高并发 I/O 等待场景下需要更多进程/线程来堆吞吐。另一方面，如果测试必须真的启动端口、拼接 URL、等待服务 ready，反馈速度会很慢，也不利于在单元级验证 API 契约。

FastAPI 的价值就是把这些问题收敛到少数清晰机制：类型标注描述输入输出，Pydantic 负责校验和序列化，`Depends()` 负责请求级依赖装配，OpenAPI 从真实代码生成，Starlette/ASGI 提供异步执行和可直接测试的应用对象。

## 设计思想

第一是类型驱动，把“接口长什么样”放回 Python 函数签名。路径参数 `book_id: int` 不只是给编辑器看的提示，它会让 FastAPI 在请求进入业务函数前完成类型转换和错误处理；请求体 `book: BookCreate` 不只是一个类名，它会触发 Pydantic 校验字段、生成 schema，并把合法 JSON 转成有类型的对象。这样路由函数可以专注于“拿到一个已经合法的输入之后做什么”。

第二是模型即边界。Pydantic 模型不是传统意义上的 ORM model，而是 API 边界对象。`BookCreate` 可以表示客户端允许提交的字段，`BookRead` 可以表示服务端允许返回的字段，`response_model` 会在返回时再次过滤和序列化。这个设计解决了“输入、内部对象、输出混成一团”的问题，也让 schema、文档和测试拥有同一个来源。

第三是显式依赖注入。`Depends()` 可以把认证、配置、数据库 session、仓库对象、权限校验等逻辑声明在函数签名里。它不是大型 IoC 容器，而是围绕请求生命周期工作的轻量依赖解析系统。依赖的好处不是“少写一行构造函数”，而是让路由声明自己需要什么，把创建、复用、清理和测试替换交给框架和应用装配层。

第四是 OpenAPI 从代码派生，而不是另写一份文档。只要路径操作、参数、状态码和模型写清楚，`/docs` 和 `/openapi.json` 就能自动反映 API 契约。团队可以用它对齐前后端、生成客户端、做契约测试和接口审查。文档仍然需要人来解释业务语义，但字段结构、必填规则和响应模型不再靠手工同步。

第五是 ASGI 原生。FastAPI 构建在 Starlette 之上，天然支持 async view、中间件、WebSocket、后台任务和现代异步服务器。即使你写同步函数，FastAPI 也能处理；但当服务需要等待数据库、HTTP 客户端或消息系统时，async/await 会更自然。更重要的是，应用本身就是 ASGI callable，因此 `TestClient` 可以直接调用应用对象，测试不必启动真实网络端口。

## 架构模型

一个典型 FastAPI 服务通常包含：

- 应用入口：创建 `FastAPI()`，注册路由、中间件、异常处理和生命周期事件。
- 路由层：声明 HTTP 方法、路径、参数、请求体、响应模型和状态码。
- 模型层：用 Pydantic 描述输入、输出和配置。
- 依赖层：用 `Depends()` 注入配置、认证、仓库、数据库 session 或外部服务客户端。
- 业务层：放置不依赖 HTTP 的业务规则，便于复用和测试。
- 测试层：使用 `TestClient` 或异步客户端直接调用 ASGI 应用。

本仓库 quickstart 用 `main.py` 放入口、模型、依赖和内存仓库；真实项目变大后应拆成 `routers/`、`schemas/`、`services/`、`repositories/`、`settings.py` 和 `tests/`。

在 quickstart 里，`BookCreate` 是写入契约，`BookRead` 是读取契约，`BookRepository` 是数据访问边界，`get_repository()` 是依赖装配入口，三个路由函数只描述 HTTP 行为。这个拆分虽小，但已经包含真实项目的核心形状：API 层不直接关心存储细节，数据层不关心 HTTP，请求校验和响应序列化由模型统一承担。

## 请求/执行生命周期

一次 FastAPI 请求通常这样流动：

1. Uvicorn 等 ASGI 服务器接收请求，把 scope、receive、send 交给应用。
2. Starlette/FastAPI 中间件按顺序处理请求。
3. 路由系统匹配路径和 HTTP 方法。
4. FastAPI 解析路径、查询、Header、Cookie 和请求体。
5. Pydantic 根据类型标注校验数据，失败时自动返回 422。
6. 依赖系统解析 `Depends()`，可以递归调用依赖并缓存同一请求内结果。
7. 路径操作函数执行，返回 dict、Pydantic 模型、Response 或其他可序列化对象。
8. FastAPI 根据 `response_model` 过滤和序列化输出，再返回响应。

这个生命周期解释了为什么 FastAPI 代码看起来像普通函数，但运行时可以得到校验、依赖、文档和响应转换。

以 `POST /books` 为例，请求体先被解析成 `BookCreate`。如果 `title` 为空，Pydantic 会在进入 `create_book()` 之前返回 422；如果数据合法，`Depends(get_repository)` 会拿到仓库实例，路由调用 `repository.create(book)` 得到 `BookRead`，最后 `response_model=BookRead` 决定响应 JSON 的公开形状。你写的是一个普通函数，框架在函数前后补上了 API 边界工作。

## 工程结构

quickstart 的结构如下：

```text
examples/quickstart/
├── main.py
├── requirements.txt
└── tests/
    └── test_main.py
```

真实项目建议按边界拆分：

- `app/main.py`：应用入口。
- `app/routers/`：按资源或业务域拆分路由。
- `app/schemas/`：Pydantic 输入输出模型。
- `app/services/`：业务规则。
- `app/repositories/`：数据库或外部 API 访问。
- `app/dependencies.py`：认证、配置、数据库 session 等依赖。
- `tests/`：API、服务和依赖替换测试。

## 配置方式

FastAPI 本身主要通过代码配置：创建应用、注册路由、声明依赖和中间件。项目配置通常使用环境变量和 Pydantic Settings 管理，例如数据库地址、密钥、日志级别、CORS 白名单和外部服务 endpoint。

quickstart 没有引入配置文件，只用内存仓库。真实项目应避免在路由函数里硬编码密钥和外部地址，而是通过 settings 对象和依赖注入传入。

## 模块与依赖管理

FastAPI 的模块组织围绕路由和依赖。`APIRouter` 用来拆分 API 模块，`include_router()` 用来装配模块；`Depends()` 用来声明某个路径操作需要哪些依赖。

依赖可以是普通函数、类实例、生成器函数或异步函数。生成器依赖常用于数据库 session：请求开始时创建，响应结束后关闭。测试时可以通过 `app.dependency_overrides` 替换依赖，这是 FastAPI 非常实用的可测试性设计。

## 数据访问

FastAPI 不绑定 ORM。常见组合包括 SQLAlchemy/SQLModel + Alembic，或者 asyncpg、psycopg、MongoDB、Redis、外部 HTTP 客户端等。

quickstart 使用内存 `BookRepository`，重点是展示“路由不直接管理存储细节，而是通过依赖拿到仓库”。把它替换成数据库时，路由函数可以基本保持不变，只需要调整依赖和仓库实现。

这也是 FastAPI 依赖系统解决的核心工程问题：路由层稳定表达 HTTP 契约，仓库层可以从内存字典演进到 SQLAlchemy session、Redis、Elasticsearch 或外部 REST client。测试时可以继续用内存仓库，也可以用 `app.dependency_overrides[get_repository] = fake_repository_factory` 把依赖替换成隔离数据源。

## 测试方式

FastAPI 常用 `fastapi.testclient.TestClient` 做同步测试，也可以用 HTTPX 的异步客户端测试 async 场景。因为 FastAPI 应用本身就是 ASGI callable，测试不需要真的启动网络端口。

quickstart 使用 pytest 调用 `TestClient`，覆盖创建、列表、详情、404 和 OpenAPI 生成。真实项目还应测试依赖替换、认证失败、请求体校验、数据库事务和外部服务 mock。

## 部署方式

开发环境可以用：

```bash
uvicorn main:app --reload
```

生产环境通常使用 Uvicorn、Granian 或 Gunicorn + Uvicorn worker，前面接反向代理、负载均衡器或平台网关。需要关注 worker 数量、超时、日志、健康检查、指标、追踪、CORS、限流和安全 Header。

容器化时建议使用非 root 用户、固定依赖版本、分层构建、健康检查，并把配置全部放到环境变量或 secret 管理系统中。

## 适用场景与取舍

优先选择 FastAPI 的场景：

- 对外 JSON API、微服务、BFF 或内部平台 API。
- 希望类型标注直接驱动校验、文档和客户端契约。
- 需要 async/await 处理大量 I/O 等待。
- 需要灵活组合数据库、认证、任务队列和观测工具。

可以考虑其他框架的场景：

- 需要完整后台管理、表单、模板和 ORM 一体化，Django 更省心。
- 只是极小 HTTP 服务或教学底层机制，Flask/Starlette 更轻。
- API 很少且项目主要是数据页面，Streamlit 或简单脚本可能更快。

## 案例索引

- [core-ideas](examples/core-ideas/)：把上一节“解决的问题”和“设计思想”映射到 quickstart 的关键代码片段。
- [quickstart](examples/quickstart/)：用内存 books API 演示 Pydantic 模型、依赖注入、OpenAPI、Uvicorn 启动和 pytest 验证。

## 版本来源

- 语言基线：Python 3.14.5，策略为 latest supported stable，本仓库记录在 `versions.yaml`。
- 框架基线：FastAPI latest stable，策略为 latest stable / officially supported。
- 官方来源：https://fastapi.tiangolo.com/
- 校验日期：2026-05-30
