# FastAPI quickstart

这个案例用一个 books JSON API 展示 FastAPI 的核心工作方式：函数签名定义接口，Pydantic 模型定义输入输出，`Depends()` 注入仓库，OpenAPI 文档自动生成，pytest 直接测试 ASGI 应用。

## 目标

- 能看懂 FastAPI 如何通过类型标注理解请求参数、请求体和响应体。
- 能用 Pydantic 模型表达 API 边界。
- 能用 `Depends()` 把路由和数据访问解耦。
- 能用 `TestClient` 验证 API 行为和 OpenAPI 文档。

## 学习重点

FastAPI 的教学主线是“类型即契约”。你在函数签名里写的路径参数、查询参数、请求体模型和返回模型，会同时用于运行时校验、响应序列化和 OpenAPI 生成。

本案例用内存 `BookRepository` 模拟数据层。路由函数只声明自己需要一个仓库，而不关心仓库来自数据库、缓存还是测试替身。这就是 FastAPI 依赖注入在小项目里的价值。

## 工程结构

```text
.
├── main.py
├── requirements.txt
└── tests/
    └── test_main.py
```

- `main.py`：创建 FastAPI 应用、定义 Pydantic 模型、内存仓库、依赖函数和路由。
- `tests/test_main.py`：使用 `TestClient` 覆盖创建、列表、详情、错误和 OpenAPI。
- `requirements.txt`：声明 FastAPI、Uvicorn、pytest 和 HTTPX。

## 运行前提

- Python 3.14.5，或当前机器上可用的 Python 3.11+。
- 能创建虚拟环境并通过 pip 安装依赖。
- 本仓库版本基线为 FastAPI latest stable。

## 运行

先进入案例目录：`cd frameworks/python/fastapi/examples/quickstart`。

```bash
python3 -m py_compile main.py tests/test_main.py
```

安装 FastAPI 后运行完整测试和开发服务器：

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
pytest
uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

另开一个终端访问 API：

```bash
curl http://127.0.0.1:8001/books
curl -X POST http://127.0.0.1:8001/books \
  -H 'Content-Type: application/json' \
  -d '{"title":"Designing Data-Intensive Applications","author":"Martin Kleppmann"}'
curl http://127.0.0.1:8001/docs
```

## 预期输出

`pytest` 应看到类似输出：

```text
4 passed
```

列表接口会返回内置示例数据：

```json
[{"id":1,"title":"FastAPI type driven APIs","author":"EveryThingCode"}]
```

创建接口会返回 `201 Created` 和新书：

```json
{"id":2,"title":"Designing Data-Intensive Applications","author":"Martin Kleppmann"}
```

浏览器打开 `http://127.0.0.1:8001/docs` 可以看到自动生成的 Swagger UI。`/openapi.json` 中会包含 `BookCreate` 和 `BookRead` schema。

## 代码讲解

`app = FastAPI(...)` 创建 ASGI 应用。Uvicorn 启动时加载 `main:app`，测试时 `TestClient(app)` 直接调用同一个应用对象。

`BookCreate` 描述请求体，`BookRead` 描述响应体。`Field(min_length=1)` 会变成运行时校验规则，也会出现在 OpenAPI schema 中。

`BookRepository` 是内存数据仓库，负责创建、列表和查询。路由函数不直接操作全局字典，而是通过 `repository: Annotated[BookRepository, Depends(get_repository)]` 获取依赖。

`@app.get("/books", response_model=list[BookRead])` 声明了路径、HTTP 方法和响应模型。FastAPI 会根据 `response_model` 过滤输出字段并生成文档。

`read_book` 在找不到数据时抛出 `HTTPException(status_code=404)`。这是 FastAPI/Starlette 中表达 HTTP 错误的常见方式。

`tests/test_main.py` 不需要启动真实端口。它直接调用 ASGI 应用，适合快速验证 API 契约和业务行为。

## 延伸练习

- 用 `APIRouter` 把 books 路由拆到 `routers/books.py`。
- 用 SQLAlchemy 或 SQLModel 替换内存仓库，并通过依赖管理数据库 session。
- 给 `POST /books` 加入重复标题校验，并为 409 错误补充测试。

## 验收

完成后你应该能说明：FastAPI 如何从类型标注生成校验和 OpenAPI；`Depends()` 如何把路由与数据访问解耦；为什么测试可以不启动服务器；如果要接入数据库，应替换哪个依赖和仓库实现。
