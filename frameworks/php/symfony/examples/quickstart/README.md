# Symfony quickstart

这是一个最小但真实的 Symfony API 项目。它使用 Symfony Runtime 入口、MicroKernelTrait、FrameworkBundle、属性路由和自动装配服务，展示 Symfony 如何把组件组合成一次完整 HTTP 请求处理。

## 目标

完成本案例后，你应该能说明 `public/index.php` 如何创建 Kernel，Kernel 如何注册 Bundle、服务和路由，控制器如何接收 Request 并调用 Service，最后如何返回 JSON 响应。你还应该能把当前 JSON 文件仓库替换成 Doctrine ORM Repository。

## 学习重点

- `composer.json` 声明 Symfony LTS 组件、Runtime 和 PSR-4 自动加载。
- `public/index.php` 不直接 new 控制器，而是返回一个创建 Kernel 的闭包。
- `src/Kernel.php` 是框架组合点：注册 Bundle、配置 FrameworkBundle、加载服务和路由。
- `#[Route]` 属性把 HTTP 路径和方法贴在控制器方法上。
- 服务容器通过 autowire 自动把 `TaskRepository` 注入控制器方法。
- `JsonResponse` 是 Symfony HttpFoundation 对 JSON HTTP 响应的明确表达。

## 这个案例解决什么问题

如果不用 Symfony 写同样的任务 API，最直接的做法是在 `public/index.php` 里读取 `$_SERVER['REQUEST_URI']`、判断请求方法、解析 `php://input`、手写 JSON 响应、创建仓库对象、处理 404/422/500。这个写法能启动，但很快会出现几个问题：路由规则和业务代码混在一起；每个接口重复写输入解析和错误响应；对象依赖靠手动 `new`，测试很难替换；日志、安全、CORS、异常转换这类横切逻辑没有统一入口。

这个 quickstart 用极少文件展示 Symfony 如何拆开这些问题：

- `composer.json` 解决“依赖和自动加载靠手工 require”的问题。Symfony 组件、Runtime、FrameworkBundle 和 `App\` 命名空间都由 Composer 管理。
- `public/index.php` 解决“入口文件承担所有职责”的问题。它只返回 Kernel 工厂，真正的请求处理交给框架生命周期。
- `src/Kernel.php` 解决“框架能力散落初始化”的问题。Bundle、FrameworkBundle 配置、服务扫描和属性路由都在应用组合根声明。
- `TaskController.php` 解决“HTTP 适配和业务混杂”的问题。它只读取请求、选择状态码、返回 JSON，把任务存储交给服务。
- `TaskRepository.php` 解决“数据访问细节污染控制器”的问题。今天用 JSON 文件，明天换 Doctrine，Controller 的路由和状态码逻辑仍然可以保留。

案例故意没有引入数据库、安全组件和复杂目录，是为了让你把注意力放在 Symfony 的核心答案上：请求由 HttpKernel 管，依赖由 Container 管，扩展点由事件管，业务边界由 Service 管。

## 工程结构

```text
.
  composer.json                    # Symfony 依赖、autoload 和脚本
  public/index.php                 # Runtime 入口，创建 Kernel
  src/Kernel.php                   # 注册 Bundle、服务和属性路由
  src/Controller/TaskController.php# 任务 API 控制器
  src/Service/TaskRepository.php   # 文件持久化任务仓库
  var/.gitkeep                     # 教学数据文件运行时会写到这里
```

## 运行前提

- PHP 8.5.x，和根目录 `versions.yaml` 的 PHP 基线一致；Symfony 当前 LTS 线通常支持更低 PHP 版本，但本仓库按统一基线学习。
- Composer 2.x。
- 需要联网访问 Packagist 才能执行 `composer install`；本仓库只提交源码和依赖声明，不提交 `vendor/`。
- Symfony 版本按根目录 `versions.yaml` 使用 latest LTS line；运行当天请以官方发布页刷新 patch。

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
curl -s http://127.0.0.1:8001/tasks
curl -s -X POST http://127.0.0.1:8001/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Learn Symfony HttpKernel","done":false}'
curl -s http://127.0.0.1:8001/tasks/1
curl -i http://127.0.0.1:8001/tasks/999
```

## 预期输出

首次访问列表会看到两条种子任务：

```json
[{"id":1,"title":"Read Symfony HttpKernel flow","done":false},{"id":2,"title":"Inspect service autowiring","done":true}]
```

创建任务会返回 `201 Created`，响应体类似：

```json
{"id":3,"title":"Learn Symfony HttpKernel","done":false}
```

查询不存在的任务会返回 `404`：

```json
{"message":"Task not found"}
```

如果 POST 请求不是合法 JSON，会返回 `400`；如果 `title` 为空，会返回 `422`。这两个分支展示了 HTTP 适配层应该把输入错误明确映射成状态码。

## 代码讲解

`composer.json` 是第一层工程边界。`symfony/runtime` 让入口文件可以返回一个创建 Kernel 的闭包；`symfony/framework-bundle` 把 HttpKernel、Routing、DependencyInjection、EventDispatcher 等组件组合成 Web 框架；`symfony/config` 与 `symfony/yaml` 支持配置加载；`autoload.psr-4` 把 `App\` 映射到 `src/`。这解决了 PHP 项目早期常见的手工 `require`、隐式全局函数和依赖版本难追踪问题。

`public/index.php` 加载 `vendor/autoload_runtime.php` 后返回一个闭包。Symfony Runtime 会读取 `APP_ENV`、`APP_DEBUG` 等上下文，调用闭包创建 `Kernel`，再把 HTTP 请求交给 Kernel 处理。入口文件因此非常薄：它不判断 URL，不解析 JSON，不创建 Controller，也不连接数据库。它解决的是入口职责膨胀问题。

`src/Kernel.php` 使用 `MicroKernelTrait`，用很少文件表达完整框架配置。`registerBundles()` 启用 `FrameworkBundle`，这相当于把 Symfony 的核心 Web 能力接进应用；`configureContainer()` 配置框架 secret、默认服务自动装配和 `App\` 命名空间扫描；`configureRoutes()` 导入控制器目录中的属性路由。Kernel 是这个案例最重要的文件，因为它说明 Symfony 不是魔法启动，而是通过一个组合根把 Bundle、Container、Routing 和事件系统连接起来。

`TaskController.php` 使用 `#[Route]` 声明路径和 HTTP 方法。属性路由解决的是“路由表和控制器实现来回跳转”的问题：读者看到 `list()` 就知道它处理 `GET /tasks`，看到 `show()` 就知道 `{id<\d+>}` 会先约束为数字路径。控制器方法里的 `TaskRepository $tasks` 不是手动创建的对象，而是由服务容器根据类型自动注入；`Request $request` 则来自 HttpKernel 的参数解析。每个方法返回 `JsonResponse`，让 HTTP 输出边界保持显式。

`TaskRepository.php` 使用 `var/tasks.json` 保存任务。它只是教学仓库，不代表生产数据访问。它存在的价值是隔离 Controller 与存储细节，让你能把 JSON 文件替换为 Doctrine Repository，而不需要重写 HTTP 层。这个类也展示了 Symfony 的服务理念：普通 PHP 类不需要继承框架基类，只要放在被扫描的命名空间下，就能被容器管理和注入。

一次 `POST /tasks` 的执行链路可以这样读：

1. 浏览器或 `curl` 把请求发到 `public/index.php`。
2. Runtime 创建 `Kernel`，Kernel 使用 FrameworkBundle 接入 HttpKernel 管线。
3. 路由系统读取 `TaskController` 上的 `#[Route('/tasks', methods: ['POST'])]`。
4. 参数解析器把当前 `Request` 和容器中的 `TaskRepository` 传给 `create()`。
5. `create()` 解析 JSON，校验 `title`，调用仓库创建任务。
6. `TaskRepository` 写入 `var/tasks.json`，把任务数组返回给控制器。
7. 控制器返回 `201 JsonResponse`，Kernel 触发响应阶段事件后输出给客户端。

这条链路就是 Symfony 思想的缩影：HTTP 生命周期由框架统一管理，业务依赖由容器统一装配，扩展能力可以挂在事件阶段，控制器只保留请求到业务服务的适配逻辑。

## 延伸练习

- 引入 Doctrine ORM，把任务保存到 SQLite，并用 migration 管理表结构。
- 新增 `PATCH /tasks/{id}`，练习路由参数、局部更新和错误状态码。
- 把 Kernel 中的服务和路由配置拆到 `config/services.yaml` 与 `config/routes.yaml`，比较 MicroKernel 与标准项目结构。

## 验收

- 能指出 Runtime 入口、Kernel、Bundle、Controller 和 Service 的职责边界。
- 能解释属性路由和服务自动装配如何减少样板配置。
- 能运行 `composer validate`，并在安装依赖后用 `curl` 完成列表、创建和查询。
- 能说清本案例为什么不用 Doctrine，以及迁移到 Doctrine 时 Controller 可以保持哪些部分不变。
