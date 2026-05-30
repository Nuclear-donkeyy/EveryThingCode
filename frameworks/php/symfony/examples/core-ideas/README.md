# Symfony core ideas example

## 目标

这个示例把 `Symfony` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

PHP 企业项目需要组件化入口、服务容器、路由、事件、配置和测试，而不是把逻辑塞进入口文件。

## 核心思想到代码

HttpKernel 管请求生命周期，Container 管服务，Attributes/配置声明路由，组件可独立使用也可组合成完整框架。

```php
#[Route("/tasks", methods: ["GET"])]
public function list(TaskRepository $tasks): JsonResponse
{
    return $this->json(["items" => $tasks->all()]);
}
```

```php
$request = Request::createFromGlobals();
$response = $kernel->handle($request);
$response->send();
```

## 代码位置

- [`composer.json`](../quickstart/composer.json)
- [`public/index.php`](../quickstart/public/index.php)
- [`src/Kernel.php`](../quickstart/src/Kernel.php)
- [`src/Controller/TaskController.php`](../quickstart/src/Controller/TaskController.php)
- [`src/Service/TaskRepository.php`](../quickstart/src/Service/TaskRepository.php)

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

public/index.php 只负责交给 Kernel，业务处理进入 Controller 和 Service。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`Symfony` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
