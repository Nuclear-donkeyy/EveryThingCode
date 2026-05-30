# Django quickstart

这个案例用最少文件实现一个 notes JSON API，帮助读者把 Django 的项目入口、URLConf、View、测试客户端和本地启动流程串起来。案例故意使用内存数据，不引入数据库和迁移，让第一轮学习聚焦框架请求生命周期。

## 目标

- 能看懂一个 Django 项目由项目配置和业务 app 共同组成。
- 能说明根 URLConf 如何把请求转发到 app URLConf，再进入 view。
- 能用 `JsonResponse` 实现最小 CRUD 风格 API。
- 能用 Django 测试客户端验证请求和响应。

## 学习重点

Django 的核心不是单个函数，而是一套约定：`manage.py` 找到配置，`settings.py` 装配应用，`urls.py` 决定请求进入哪个 view，view 负责读取请求并返回响应。后续引入 ORM、模板或 Admin 时，它们都会接到这条主线上。

本案例把 `notes.views` 当作业务入口，把内存列表当作数据层。这样可以清楚看到“框架结构”和“数据持久化”是两个不同问题。

## 解决的问题

如果不用 Django，而是直接用纯 Python 或一个很轻的 HTTP 框架实现这个 notes API，最小版本并不难：写两个函数、判断路径、读写一个列表即可。难点会在需求继续增长时出现：

- 路由组织：路径越来越多后，`/api/notes/`、`/api/notes/<id>/`、后台页面和静态资源如果没有统一 URL 约定，会散落在多个文件和装饰器里。
- 配置入口：开发、测试、生产的密钥、Host、数据库、模板、静态文件、安全开关需要集中管理，否则排查运行环境会很痛苦。
- 数据访问：内存列表只能教学，真实业务需要数据库、迁移、索引、事务、查询组合和测试隔离。
- 后台管理：运营人员通常需要直接管理数据；自己从零写 Admin 会重复很多列表、筛选、编辑和权限逻辑。
- 安全与中间件：CSRF、会话、认证、Host 校验、安全 Header 这类横切逻辑不应该散落到每个 view。
- 测试方式：如果只能启动真实服务器再测，每次验证都会更慢；如果只测函数，又容易漏掉 URLConf、请求解析和响应状态码。

这个 quickstart 用一个故意简化的内存 API 展示 Django 的解决路径：项目有统一 settings，路由按项目层和 app 层拆分，view 只关心请求到响应，测试用 Django `Client` 从 HTTP 行为切入。把内存列表换成 ORM、把 JSON 响应换成 template、把手写管理接口换成 Admin，仍然是在同一套结构里扩展。

## 设计思想

Django 的设计思想可以从本案例的四个文件读出来。

`learn_django/settings.py` 体现 batteries included 的装配思想。Django 不要求你在每个模块里临时拼接框架能力，而是把 `INSTALLED_APPS`、`ROOT_URLCONF`、`MIDDLEWARE`、`ALLOWED_HOSTS` 这类运行选项集中放在 settings 中。本案例只安装 `notes`，并把 `MIDDLEWARE` 设为空，是为了先看到最短请求链；真实项目会在这里打开数据库、模板、安全中间件、认证 app 和静态文件能力。

`learn_django/urls.py` 和 `notes/urls.py` 体现 URLConf 的边界思想。根 URLConf 只做应用装配：`path("api/", include("notes.urls"))`。业务 app 的 URLConf 再决定 `notes/` 和 `notes/<int:note_id>/` 分别进入哪个 view。这样增长到多个 app 时，项目层不会被每个业务细节塞满。

`notes/views.py` 体现 MTV 中 View 的职责：接收 `HttpRequest`，读取方法、路径参数和 JSON body，调用数据层或业务逻辑，返回 `JsonResponse`。案例里的 `NOTES` 和 `NEXT_ID` 是教学用内存仓库；在真实 Django 中，它们应当被 `models.Model`、QuerySet 和 migration 替代。替换后，URLConf 和测试的整体结构仍然不需要重写。

`notes/tests.py` 体现框架级测试约定。`Client` 不需要启动真实 HTTP 服务器，却会经过 Django URL 匹配和 view 调用。测试中的 `self.client.post("/api/notes/", ...)` 验证的是“外部调用者看到的行为”，而不是某个内部函数的实现细节。

从思想上说，Django 倾向于把基础设施问题提前标准化：配置在哪里、URL 怎样挂载、数据怎样建模、请求如何经过中间件、测试如何发请求。业务代码因此少做框架拼装，多表达业务规则。

## 工程结构

```text
.
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

- `manage.py`：Django 命令入口，用来运行测试、启动开发服务器和执行管理命令。
- `learn_django/settings.py`：项目配置，声明安装的 app、URL 入口和基础运行选项。
- `learn_django/urls.py`：根 URLConf，把 `/api/` 前缀交给 `notes.urls`。
- `notes/urls.py`：业务 app URLConf，把具体路径映射到 view。
- `notes/views.py`：处理请求、维护内存数据并返回 JSON。
- `notes/tests.py`：使用 Django `Client` 做 HTTP 行为验证。

## 运行前提

- Python 3.14.5，或当前机器上可用的 Python 3.11+。
- 能创建虚拟环境并通过 pip 安装依赖。
- 本仓库版本基线为 Django 5.2 LTS。

## 运行

先进入案例目录：`cd frameworks/python/django/examples/quickstart`。

```bash
python3 -m py_compile manage.py learn_django/settings.py learn_django/urls.py notes/views.py notes/tests.py
```

安装 Django 后运行完整测试和开发服务器：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python manage.py test
python manage.py runserver 127.0.0.1:8000
```

另开一个终端访问 API：

```bash
curl http://127.0.0.1:8000/api/notes/
curl -X POST http://127.0.0.1:8000/api/notes/ \
  -H 'Content-Type: application/json' \
  -d '{"title":"learn Django URLConf"}'
curl http://127.0.0.1:8000/api/notes/1/
```

## 预期输出

测试命令应看到类似输出：

```text
Found 4 test(s).
...
OK
```

首次列表请求会返回内置示例数据：

```json
{"items":[{"id":1,"title":"Read Django request lifecycle","done":false}]}
```

创建请求会返回 `201 Created`，响应体包含新的 note：

```json
{"id":2,"title":"learn Django URLConf","done":false}
```

## 代码讲解

`manage.py` 通过 `DJANGO_SETTINGS_MODULE` 指向 `learn_django.settings`。这是 Django 命令行和运行时找到项目配置的方式。

`settings.py` 里最关键的是 `ROOT_URLCONF = "learn_django.urls"` 和 `INSTALLED_APPS = ["notes"]`。前者告诉 Django 根路由在哪里，后者把业务 app 纳入项目。`ALLOWED_HOSTS` 展示了 Django 对 Host 校验的安全意识；`MIDDLEWARE = []` 则是教学取舍，目的是让第一版案例不被会话、认证、CSRF 等横切能力分散注意力。

`learn_django/urls.py` 使用 `include("notes.urls")` 把 `/api/` 下的路径交给 notes app。这样根项目只负责装配，业务 app 自己维护自己的 URL。等项目出现 `accounts`、`billing`、`admin` 等模块时，每个 app 都可以按同样方式挂载，而不是把所有路径堆在根文件里。

`notes/views.py` 中的 `list_notes` 同时处理 GET 和 POST。GET 返回列表，POST 读取 JSON 创建新 note。`note_detail` 处理 GET、PATCH 和 DELETE，展示同一资源路径下如何按 HTTP 方法分派行为。这里用 `JsonResponse` 表示 API 输出，用 `HttpResponseNotAllowed` 表示方法不被允许；这些响应对象让 view 的意图比手写状态码字符串更清楚。

案例中的 `@csrf_exempt` 是为了方便用 `curl` 直接发送 JSON POST/PATCH。真实面向浏览器表单的 Django 页面通常不应随意关闭 CSRF，而应使用 Django 的 CSRF 中间件和模板标签；面向外部 API 时，则通常会配合 token、session、OAuth 或专门 API 框架处理认证与防护。

内存变量 `_INITIAL_NOTES`、`NOTES`、`NEXT_ID` 只是为了让教学案例能在没有数据库的环境里运行。引入 ORM 后，你会定义 `Note(models.Model)`，运行 `makemigrations` 和 `migrate`，再把 `NOTES.append(note)` 替换成 `Note.objects.create(...)`，把 `_find_note` 替换成 `get_object_or_404(Note, pk=note_id)` 或 QuerySet 查询。Django 的价值在于：数据层升级后，请求入口、URLConf、测试客户端仍然沿用同一套框架约定。

`notes/tests.py` 用 `Client` 发出请求，不需要真正启动服务器。测试先重置内存数据，再验证列表、创建、修改和 404 行为。

这四个测试分别覆盖了 Django 框架给应用提供的关键边界：URL 能进入正确 view，JSON 请求能被处理，响应状态码和响应体符合预期，缺失资源能得到 404。真实项目继续扩展时，可以把测试分成 model 测试、view 测试、form 测试、Admin 权限测试和端到端 API 测试。

## 延伸练习

- 把内存列表替换为 Django `models.Model`，添加迁移并用 ORM 查询。
- 在 Admin 中注册 Note 模型，比较“自己写 API”和“框架生成后台”的差异。
- 加入 `done=true/false` 查询参数，实现按完成状态过滤。

## 验收

完成后你应该能说明：请求如何从 `learn_django.urls` 进入 `notes.views`；为什么 `settings.py` 是项目装配中心；如何用 Django 测试客户端验证 API；如果要接入数据库，应该把内存数据替换到哪一层。
