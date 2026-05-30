# Laravel core ideas example

## 目标

这个示例把 `Laravel` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

PHP 业务应用常重复处理路由、容器、配置、ORM、迁移、队列、中间件、测试和脚手架。

## 核心思想到代码

约定目录降低决策成本，Service Container 装配依赖，Facade 提供门面入口，Artisan 统一工程命令。

```php
Route::get("/tasks", fn (TaskRepository $tasks) => response()->json(["items" => $tasks->all()]));
```

```php
return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(api: __DIR__."/../routes/api.php")
    ->create();
```

## 代码位置

- [`composer.json`](../quickstart/composer.json)
- [`artisan`](../quickstart/artisan)
- [`bootstrap/app.php`](../quickstart/bootstrap/app.php)
- [`routes/api.php`](../quickstart/routes/api.php)
- [`app/Services/TaskRepository.php`](../quickstart/app/Services/TaskRepository.php)

## 运行

先进入 quickstart 目录：

```bash
cd ../quickstart
composer validate --no-check-lock --strict
```

如果本机缺少对应工具链，可以先运行仓库根目录的 dry-run：

```bash
python3 scripts/run_framework_examples.py --dry-run
```

## 观察点

路由闭包直接声明 TaskRepository，容器负责解析依赖。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`Laravel` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
