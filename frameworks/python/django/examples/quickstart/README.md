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

`settings.py` 里最关键的是 `ROOT_URLCONF = "learn_django.urls"` 和 `INSTALLED_APPS = ["notes"]`。前者告诉 Django 根路由在哪里，后者把业务 app 纳入项目。

`learn_django/urls.py` 使用 `include("notes.urls")` 把 `/api/` 下的路径交给 notes app。这样根项目只负责装配，业务 app 自己维护自己的 URL。

`notes/views.py` 中的 `list_notes` 同时处理 GET 和 POST。GET 返回列表，POST 读取 JSON 创建新 note。`note_detail` 处理 GET、PATCH 和 DELETE，展示同一资源路径下如何按 HTTP 方法分派行为。

`notes/tests.py` 用 `Client` 发出请求，不需要真正启动服务器。测试先重置内存数据，再验证列表、创建、修改和 404 行为。

## 延伸练习

- 把内存列表替换为 Django `models.Model`，添加迁移并用 ORM 查询。
- 在 Admin 中注册 Note 模型，比较“自己写 API”和“框架生成后台”的差异。
- 加入 `done=true/false` 查询参数，实现按完成状态过滤。

## 验收

完成后你应该能说明：请求如何从 `learn_django.urls` 进入 `notes.views`；为什么 `settings.py` 是项目装配中心；如何用 Django 测试客户端验证 API；如果要接入数据库，应该把内存数据替换到哪一层。
