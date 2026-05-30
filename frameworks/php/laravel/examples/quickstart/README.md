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

## 这个案例解决什么问题

这个 quickstart 模拟的是一个最小任务 API，但它真正想展示的不是“如何用 JSON 文件保存任务”，而是 Laravel 如何把 PHP Web/API 项目中最容易失控的几件事放回固定位置。

第一，入口问题。没有框架时，`index.php` 很容易同时负责加载文件、解析 URL、读取 body、处理错误、调用数据库和拼 JSON。这里的 `public/index.php` 只做三件事：加载 Composer autoload、加载 `bootstrap/app.php`、把捕获到的 Request 交给应用。它解决的是入口膨胀问题，也解释了为什么生产 Web 服务器应该只暴露 `public/`。

第二，启动与配置问题。没有统一 bootstrap 时，每个脚本可能自己初始化配置、连接、路由和异常处理。这里的 `bootstrap/app.php` 用 `Application::configure()` 集中声明 API 路由、命令路由、健康检查、中间件和异常处理扩展点。案例没有写复杂配置，但已经保留了真实 Laravel 项目扩展配置、认证、限流、CORS 和错误响应的位置。

第三，路由与响应问题。没有路由层时，路径匹配、参数校验、状态码和 JSON 序列化会散落在条件分支里。这里的 `routes/api.php` 用 `Route::get()`、`Route::post()` 和 `whereNumber('id')` 声明接口形状，用 `validator(...)->validate()` 给非法输入返回 422，用 `response()->json()` 明确响应体与状态码。路由文件把“外部 HTTP 形状”集中在一起，读者可以先看它来理解 API 契约。

第四，依赖创建问题。没有容器时，路由闭包需要自己 `new TaskRepository()`，后续改成数据库、缓存或外部服务时会牵动很多入口。这里的 `TaskRepository $tasks` 直接写在闭包参数里，由 Service Container 根据类型声明解析。它解决的是依赖创建散落问题，也是未来把仓库换成 Eloquent Repository 或接口绑定的入口。

第五，数据边界问题。没有 Repository/Model 边界时，路由会直接读写文件或数据库，验证、业务规则、持久化细节混在一起。这里的 `TaskRepository` 把 `all()`、`find()`、`create()` 放在一个服务类里，路由只关心“列出、创建、查询”。这让案例可以先用 JSON 文件教学，再平滑替换成 Eloquent、Migration 和 SQLite。

第六，脚手架与测试入口问题。`composer.json` 不只是依赖清单，还声明了 `App\\` 的 PSR-4 自动加载和 `serve`、`test` 脚本；`artisan` 不只是一个可执行文件，而是 Laravel 命令行生命周期的入口。未来添加 migration、queue worker、scheduler、feature test 时，都应该通过 Artisan/Composer 这条统一路径进入应用。

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

`composer.json` 先解决“代码如何被找到”的问题。`"App\\": "app/"` 告诉 Composer 使用 PSR-4 自动加载 `App\Services\TaskRepository`，所以路由文件不需要手写 `require app/Services/TaskRepository.php`。`scripts.serve` 和 `scripts.test` 把开发服务器和测试命令变成团队共享入口，避免每个人记一套不同命令。

`artisan` 解决“命令行如何进入同一个应用”的问题。它加载同一个 `vendor/autoload.php` 和 `bootstrap/app.php`，再调用 `$app->handleCommand(...)`。这意味着 `php artisan serve`、`php artisan test`、未来的 `php artisan migrate`、队列 worker 和定时任务，都复用同一套容器、配置和服务绑定，而不是另起一套脚本体系。

`bootstrap/app.php` 使用 `Application::configure(...)` 创建应用。`withRouting(api: ...)` 告诉 Laravel API 路由文件在哪里，`commands` 保留命令路由，`health: '/up'` 提供健康检查入口。`withMiddleware(...)` 和 `withExceptions(...)` 是后续扩展横切逻辑的位置：认证、限流、CORS、日志和统一异常响应都应该从这里进入请求管线，而不是复制到每个路由。

`routes/api.php` 展示三类常见 API：列表查询、创建资源、按 id 查询。闭包参数中的 `TaskRepository` 不是手动 new 出来的，而是由 Service Container 根据类型声明解析。`Request` 也是容器/框架提供的请求对象。这里的 `validator($request->all(), ...)->validate()` 展示了 Laravel 的输入边界：非法输入在进入仓库写入之前就会变成标准 422 响应。

`TaskRepository.php` 使用 JSON 文件模拟持久化。它在第一次访问时写入种子数据，`create()` 会计算新 id 并写回文件。路由层不关心这些细节，因此未来可以把仓库替换成 Eloquent，而 API 的形状基本不变。

验证逻辑放在 POST 路由里是为了让案例短小。真实项目中可以迁移到 Form Request 或专门的 Action/Service，让 Controller/Route 更薄，也更方便复用和测试。

## 思想拆解

| Laravel 思想 | 案例落点 | 解决的问题 |
| --- | --- | --- |
| 约定优于配置 | `public/`、`bootstrap/`、`routes/`、`app/Services/` | 新人不用猜入口、路由、服务类应该放在哪里 |
| Composer + PSR-4 | `composer.json` 的 `autoload` | 不再在入口文件里手写一串 `require` |
| Service Container | `TaskRepository $tasks` 路由参数 | 路由声明依赖，框架负责创建对象 |
| Facade/helper 表达力 | `Route::get()`、`response()->json()`、`validator()` | 路由、响应、验证有统一写法 |
| Middleware 管线 | `bootstrap/app.php` 的 `withMiddleware()` | 认证、限流、CORS、日志等横切逻辑有固定位置 |
| Artisan 生命周期 | `artisan`、`composer run serve`、`composer run test` | Web、测试、迁移、队列、调度共享同一个应用启动流程 |
| 数据访问边界 | `TaskRepository` | 路由不关心数据来自 JSON、数据库还是外部服务 |

## 与完整 Laravel 项目的对应关系

当前案例为了可读性没有加入数据库、队列和完整测试目录，但每个位置都能映射到真实项目：

- `TaskRepository` 可以替换为 `app/Models/Task.php` + `database/migrations/*_create_tasks_table.php`，用 Eloquent 接管查询和持久化。
- POST 验证可以移动到 `app/Http/Requests/StoreTaskRequest.php`，让路由或控制器只处理业务调用。
- 路由闭包可以移动到 `app/Http/Controllers/TaskController.php`，当接口增多时保持路由文件简洁。
- 耗时任务可以移动到 `app/Jobs/*` 并通过 Queue 异步执行，例如任务创建后发送通知。
- API 行为可以写成 `tests/Feature/TaskApiTest.php`，用 `php artisan test` 验证状态码、JSON 结构和持久化结果。
- 认证、限流、CORS 和统一错误格式可以在 `bootstrap/app.php` 的 middleware/exception 扩展点集中注册。

## 延伸练习

- 把 `TaskRepository` 替换为 `Task` Eloquent Model，增加 migration，并用 SQLite 作为本地数据库。
- 新增 `PATCH /api/tasks/{id}`，支持修改 `done` 状态，并处理不存在任务的 404。
- 把路由闭包改为 `TaskController`，比较闭包路由和控制器在大型项目中的可维护性。

## 验收

- 能指出 HTTP 入口、应用启动、路由声明和业务仓库分别在哪个文件。
- 能解释 `TaskRepository` 为什么可以直接写在路由闭包参数中。
- 能运行 `composer validate`，并在安装依赖后用 `curl` 完成列表、创建和查询。
- 能说清本案例为什么不用数据库，以及替换为 Eloquent 时需要新增哪些文件。
