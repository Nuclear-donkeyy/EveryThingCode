# Django

Django 是 Python 生态最具代表性的全栈 Web 框架之一。它的核心价值不是“能写 HTTP 接口”，而是把业务系统常见能力放进同一套工程模型：URL 路由、视图、模板、ORM、迁移、Admin、认证、表单、安全中间件、测试工具和部署入口。

## 核心定位

Django 解决的是完整 Web 应用和后台业务系统的交付问题。它适合处理模型清晰、数据驱动、需要后台管理、权限、表单、模板页面或稳定工程约定的项目，例如内容管理、运营后台、内部系统、交易管理和传统服务端渲染网站。

Django 不试图成为最薄的 HTTP 工具箱。只想暴露几个 JSON 接口时，FastAPI、Flask 或 Starlette 可能更轻；需要极致异步 I/O 管道时，也通常会把 Django 放在业务后台侧，而不是所有网络边界的最前面。

## 设计思想

Django 的第一关键词是 batteries included。框架把常见 Web 能力作为官方内建能力提供，而不是要求开发者从零组合一堆插件。这样做的好处是团队协作成本低、文档统一、安全默认值更稳定；代价是你需要理解 Django 的约定和项目组织方式。

第二个关键词是 MTV。Django 常说 Model、Template、View，而不是传统 MVC：Model 表示数据模型和业务数据边界，Template 负责展示，View 负责接收请求、调用模型或服务并返回响应。URLConf 把 URL 映射到 View，因此路由配置也是 Django 架构的一等公民。

第三个关键词是显式应用拆分。真实 Django 项目通常由多个 app 组成，例如 `accounts`、`billing`、`catalog`。每个 app 拥有自己的模型、视图、URL、测试和管理后台注册逻辑。项目配置负责把这些 app 装配起来。

第四个关键词是 Admin 与 ORM 的联动。Django ORM 不只是查询数据库，它还驱动迁移、表单、验证和 Admin 后台。很多后台系统可以先从模型定义开始，再快速得到管理界面和基础 CRUD。

## 架构模型

一个典型 Django 项目可以分成三层：

- 项目层：`settings.py`、根 `urls.py`、`asgi.py`、`wsgi.py`，负责全局配置、入口和应用装配。
- 应用层：每个业务 app 拥有自己的 `models.py`、`views.py`、`urls.py`、`tests.py`、`admin.py`。
- 外部边界：数据库、缓存、消息队列、对象存储、第三方 API，由配置和业务服务接入。

本仓库 quickstart 使用 `learn_django` 作为项目层，使用 `notes` 作为应用层。为了突出 URLConf 和 View 的关系，案例暂时把数据放在内存列表里，没有引入 ORM 和迁移。

## 请求/执行生命周期

一次 Django HTTP 请求通常这样流动：

1. 请求进入 WSGI 或 ASGI 入口，Django 创建请求对象。
2. 请求经过中间件链，例如安全、会话、CSRF、认证等。
3. 根 URLConf 根据路径匹配具体 view。
4. view 读取请求参数或 JSON，调用模型、服务或表单逻辑。
5. view 返回 `HttpResponse`、`JsonResponse`、重定向或渲染后的模板。
6. 响应再次经过中间件链，最终交给服务器返回给客户端。

理解这个生命周期后，再看 ORM、Admin 和模板会更容易：它们不是孤立功能，而是 view 在处理请求时调用的框架能力。

## 工程结构

quickstart 的结构如下：

```text
examples/quickstart/
├── manage.py
├── requirements.txt
├── learn_django/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── notes/
    ├── __init__.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

真实项目扩展时，建议把复杂业务逻辑从 `views.py` 中抽出到 service、domain 或 repository 层；把数据模型放入 `models.py`；把后台注册放入 `admin.py`；把跨请求配置放入环境变量或 settings 分层文件。不要让 view 同时承担路由、校验、业务规则、数据访问和第三方调用。

## 配置方式

Django 配置集中在 `settings.py`。常见配置包括 `INSTALLED_APPS`、`MIDDLEWARE`、`DATABASES`、`TEMPLATES`、`STATIC_URL`、`ALLOWED_HOSTS` 和安全相关开关。

本案例为了保持最小化，只启用 `notes` 应用，不启用数据库和模板。真实项目中建议通过环境变量区分开发、测试和生产配置，例如数据库 URL、密钥、调试开关、缓存地址和外部服务凭据。

## 模块与依赖管理

Django 通过 app 组织模块。一个 app 是否参与项目，由 `INSTALLED_APPS` 决定；URL 是否暴露，由根 URLConf 是否 `include()` 它决定。这个双层装配很重要：安装 app 让 Django 能发现模型、测试、模板、静态文件等；挂载 URL 让外部请求能进入它。

Django 没有像某些框架那样内置通用依赖注入容器。依赖通常通过显式导入、函数参数、类属性、settings 配置或工厂函数组织。这样更接近 Python 的常规模块系统，也要求开发者在项目变大时主动控制边界。

## 数据访问

Django 的标准数据访问方式是 ORM：用 Python 类描述表结构，用 QuerySet 表达查询，用 migration 管理 schema 演进。Admin、ModelForm、认证和权限系统都能围绕模型工作。

quickstart 使用内存列表实现 notes CRUD，是为了让第一眼看到的是 URL 和 view 如何工作。进入真实项目后，可以把内存仓库替换为 Django model，再加入迁移、事务、索引、分页和权限控制。

## 测试方式

Django 自带测试框架，常用入口是 `python manage.py test`。它提供测试客户端、请求构造、数据库测试隔离、override settings 等能力。

quickstart 使用 `django.test.SimpleTestCase` 和 `Client` 验证 JSON API。因为案例不访问数据库，所以不需要测试数据库创建过程。真实项目中建议为模型、表单、view、权限和集成 API 分层写测试。

## 部署方式

开发环境可用 `python manage.py runserver`。生产环境通常由 Gunicorn/uWSGI/Daphne/Uvicorn 等服务器承载 WSGI 或 ASGI 应用，再由 Nginx、负载均衡器或平台网关负责 TLS、静态文件和反向代理。

Django 部署前需要特别关注 `DEBUG=False`、`ALLOWED_HOSTS`、密钥、数据库连接、静态文件收集、迁移执行、日志、健康检查和安全 Header。容器化时通常把依赖安装、静态文件构建、迁移和应用启动拆成清晰步骤。

## 适用场景与取舍

优先选择 Django 的场景：

- 需要完整后台、权限、管理界面和稳定工程约定。
- 数据模型是系统中心，CRUD、表单、查询和报表占比高。
- 团队希望用官方内建方案降低插件拼装成本。
- 项目生命周期长，需要成熟文档、社区和升级路径。

可以考虑其他框架的场景：

- 只是很薄的 API 网关或异步 I/O 服务，FastAPI/Starlette 更轻。
- 想完全自由组合组件，Flask 更灵活。
- 前端完全独立，后端只需要少量类型驱动接口，FastAPI 学习成本更低。

## 案例索引

- [quickstart](examples/quickstart/)：用内存 notes API 演示 Django 项目结构、URLConf、View、测试客户端和本地启动命令。

## 版本来源

- 语言基线：Python 3.14.5，策略为 latest supported stable，本仓库记录在 `versions.yaml`。
- 框架基线：Django 5.2 LTS，策略为 latest LTS。
- 官方来源：https://docs.djangoproject.com/en/stable/releases/
- 校验日期：2026-05-30
