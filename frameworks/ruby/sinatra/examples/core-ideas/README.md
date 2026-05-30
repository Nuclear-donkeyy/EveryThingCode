# Sinatra core ideas example

## 目标

这个示例把 `Sinatra` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

轻量 API 需要快速声明路由、接入 Rack、中间件、JSON 和业务对象边界。

## 核心思想到代码

DSL 直接表达 HTTP，Rack compatibility 接入服务器，before/helper 处理横切逻辑，subclass style 让应用可测试可组合。

```ruby
class TaskApi < Sinatra::Base
  before { content_type :json }
  get "/tasks" do
    json repository.all
  end
end
```

```ruby
run TaskApi
```

## 代码位置

- [`Gemfile`](../quickstart/Gemfile)
- [`config.ru`](../quickstart/config.ru)
- [`app.rb`](../quickstart/app.rb)

## 运行

先进入 quickstart 目录：

```bash
cd ../quickstart
ruby -c app.rb
```

如果本机缺少对应工具链，可以先运行仓库根目录的 dry-run：

```bash
python3 scripts/run_framework_examples.py --dry-run
```

## 观察点

config.ru 只运行 Rack app，app.rb 内部再拆 repository/service，保持轻量但不失边界。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`Sinatra` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
