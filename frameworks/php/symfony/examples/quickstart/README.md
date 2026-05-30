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

`public/index.php` 加载 `vendor/autoload_runtime.php` 后返回一个闭包。Symfony Runtime 会读取环境变量，调用闭包创建 `Kernel`，再把 HTTP 请求交给 Kernel 处理。入口文件因此非常薄，真正的框架组合发生在 Kernel。

`src/Kernel.php` 使用 `MicroKernelTrait`，用很少文件表达完整框架配置。`registerBundles()` 启用 `FrameworkBundle`；`configureContainer()` 配置框架 secret、默认服务自动装配和 `App\` 命名空间扫描；`configureRoutes()` 导入控制器目录中的属性路由。

`TaskController.php` 使用 `#[Route]` 声明路径。每个方法返回 `JsonResponse`，这比返回裸数组更显式。`create()` 方法读取 JSON、做基本校验、调用仓库，然后返回 `201`；`show()` 方法把不存在的任务映射为 `404`。

`TaskRepository.php` 使用 `var/tasks.json` 保存任务。它只是教学仓库，不代表生产数据访问。它存在的价值是隔离 Controller 与存储细节，让你能把 JSON 文件替换为 Doctrine Repository，而不需要重写 HTTP 层。

## 延伸练习

- 引入 Doctrine ORM，把任务保存到 SQLite，并用 migration 管理表结构。
- 新增 `PATCH /tasks/{id}`，练习路由参数、局部更新和错误状态码。
- 把 Kernel 中的服务和路由配置拆到 `config/services.yaml` 与 `config/routes.yaml`，比较 MicroKernel 与标准项目结构。

## 验收

- 能指出 Runtime 入口、Kernel、Bundle、Controller 和 Service 的职责边界。
- 能解释属性路由和服务自动装配如何减少样板配置。
- 能运行 `composer validate`，并在安装依赖后用 `curl` 完成列表、创建和查询。
- 能说清本案例为什么不用 Doctrine，以及迁移到 Doctrine 时 Controller 可以保持哪些部分不变。
