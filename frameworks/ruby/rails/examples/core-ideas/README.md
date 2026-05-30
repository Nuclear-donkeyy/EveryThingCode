# Rails core ideas example

## 目标

这个示例把 `Rails` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

Web 产品要反复处理路由、MVC、ORM、迁移、目录约定、测试、邮件和后台任务。

## 核心思想到代码

Convention over configuration 降低选择成本，MVC 分层请求，Active Record 统一数据模型，RESTful resources 统一资源入口。

```ruby
resources :tasks, only: [:index, :show, :create]
```

```ruby
class TasksController < ActionController::API
  def index
    render json: Task.all
  end
end
```

## 代码位置

- [`config.ru`](../quickstart/config.ru)
- [`config/application.rb`](../quickstart/config/application.rb)
- [`config/routes.rb`](../quickstart/config/routes.rb)
- [`app/controllers/tasks_controller.rb`](../quickstart/app/controllers/tasks_controller.rb)
- [`app/models/task.rb`](../quickstart/app/models/task.rb)

## 运行

先进入 quickstart 目录：

```bash
cd ../quickstart
ruby -c app/models/task.rb
```

如果本机缺少对应工具链，可以先运行仓库根目录的 dry-run：

```bash
python3 scripts/run_framework_examples.py --dry-run
```

## 观察点

routes.rb 一行 resources 约定出多个 HTTP 入口，控制器按动作承接。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`Rails` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
