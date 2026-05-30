# Laravel quickstart

这是一个最小但真实的 Laravel API 项目。它声明了 Composer 依赖，包含 Laravel 入口、应用启动文件、API 路由和一个由容器自动解析的 `TaskRepository`。案例用 JSON 文件保存任务，避免数据库安装遮住 Laravel 的核心请求链路。

## 目标

完成本案例后，你应该能说明 Laravel 请求如何从 `public/index.php` 进入应用，如何在 `bootstrap/app.php` 注册 API 路由，如何由 Route 闭包接收 `Request` 和业务依赖，最后如何返回 JSON 响应。你还应该能把当前 JSON 文件仓库替换成 Eloquent Model 或数据库 Repository。

## 学习重点

- `composer.json` 负责依赖声明、PSR-4 自动加载和常用脚本。
- `public/index.php` 是 Web 服务器唯一应该暴露的入口目录。
- `bootstrap/app.php` 创建 Laravel Application，并注册路由、中间件和异常处理扩展点。
- `routes/api.php` 用 HTTP 方法和路径声明 API；类型声明让容器自动注入 `Request` 与 `TaskRepository`。
- `TaskRepository` 把数据读写从路由中分离出来，展示未来替换为 Eloquent/数据库的位置。
- `response()->json()` 和验证器把 PHP 数组、状态码、错误信息稳定地转成 HTTP 响应。

## 工程结构

```text
.
  composer.json                  # Laravel 依赖、autoload 和脚本
  artisan                        # Laravel 命令行入口
  bootstrap/app.php              # 创建 Application，注册路由/中间件/异常处理
  public/index.php               # HTTP 入口，接收 Request 并交给框架
  routes/api.php                 # 任务 API 路由
  app/Services/TaskRepository.php# 文件持久化任务仓库
  storage/app/.gitkeep           # 教学数据文件运行时会写到这里
```

## 运行前提

- PHP 8.5.x，和根目录 `versions.yaml` 的 PHP 基线一致；如果本机只有较低版本，请按 Composer 报错调整运行环境。
- Composer 2.x。
- 需要联网访问 Packagist 才能执行 `composer install`；本仓库只提交源码和依赖声明，不提交 `vendor/`。
- Laravel 版本按根目录 `versions.yaml` 使用 latest supported major；运行当天请以官方发布页刷新 patch。

## 运行

先做无网络的依赖声明检查：

```bash
composer validate --no-check-lock --strict
```

安装依赖：

```bash
composer install
```

启动开发服务器：

```bash
composer run serve
```

另开终端验证接口：

```bash
curl -s http://127.0.0.1:8000/api/tasks
curl -s -X POST http://127.0.0.1:8000/api/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Learn Laravel container","done":false}'
curl -s http://127.0.0.1:8000/api/tasks/1
curl -i http://127.0.0.1:8000/api/tasks/999
```

## 预期输出

首次访问列表会看到两条种子任务：

```json
[{"id":1,"title":"Read Laravel routing","done":false},{"id":2,"title":"Trace service container injection","done":true}]
```

创建任务会返回 `201 Created`，响应体类似：

```json
{"id":3,"title":"Learn Laravel container","done":false}
```

查询不存在的任务会返回 `404`，响应体包含：

```json
{"message":"Task not found"}
```

如果 POST 请求缺少 `title`，验证器会返回 `422 Unprocessable Entity`，这说明输入校验应该发生在进入业务写入之前。

## 代码讲解

`public/index.php` 加载 Composer autoload，再加载 `bootstrap/app.php`，最后调用 `$app->handleRequest(Request::capture())`。这一步把 PHP 的全局请求信息封装成 Laravel Request，并交给框架生命周期处理。

`bootstrap/app.php` 使用 `Application::configure(...)` 创建应用。`withRouting(api: ...)` 告诉 Laravel API 路由文件在哪里，`withMiddleware(...)` 和 `withExceptions(...)` 是后续扩展横切逻辑的位置。即使本案例没有复杂中间件，也保留了真实扩展点。

`routes/api.php` 展示三类常见 API：列表查询、创建资源、按 id 查询。闭包参数中的 `TaskRepository` 不是手动 new 出来的，而是由 Service Container 根据类型声明解析。`Request` 也是容器/框架提供的请求对象。

`TaskRepository.php` 使用 JSON 文件模拟持久化。它在第一次访问时写入种子数据，`create()` 会计算新 id 并写回文件。路由层不关心这些细节，因此未来可以把仓库替换成 Eloquent，而 API 的形状基本不变。

验证逻辑放在 POST 路由里是为了让案例短小。真实项目中可以迁移到 Form Request 或专门的 Action/Service，让 Controller/Route 更薄，也更方便复用和测试。

## 延伸练习

- 把 `TaskRepository` 替换为 `Task` Eloquent Model，增加 migration，并用 SQLite 作为本地数据库。
- 新增 `PATCH /api/tasks/{id}`，支持修改 `done` 状态，并处理不存在任务的 404。
- 把路由闭包改为 `TaskController`，比较闭包路由和控制器在大型项目中的可维护性。

## 验收

- 能指出 HTTP 入口、应用启动、路由声明和业务仓库分别在哪个文件。
- 能解释 `TaskRepository` 为什么可以直接写在路由闭包参数中。
- 能运行 `composer validate`，并在安装依赖后用 `curl` 完成列表、创建和查询。
- 能说清本案例为什么不用数据库，以及替换为 Eloquent 时需要新增哪些文件。
