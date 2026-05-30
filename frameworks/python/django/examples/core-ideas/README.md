# Django core ideas example

## 目标

这个示例把 `Django` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

业务后台经常重复搭建 ORM、Admin、URL、配置、安全、中间件和测试约定。

## 核心思想到代码

项目配置负责装配，app 承载业务，URLConf 分派请求，View 返回响应，后续 ORM/Admin 可以接入同一结构。

```python
urlpatterns = [
    path("api/", include("notes.urls")),
]
```

```python
def list_notes(request):
    if request.method == "GET":
        return JsonResponse({"items": NOTES})
```

## 代码位置

- [`manage.py`](../quickstart/manage.py)
- [`learn_django/settings.py`](../quickstart/learn_django/settings.py)
- [`learn_django/urls.py`](../quickstart/learn_django/urls.py)
- [`notes/urls.py`](../quickstart/notes/urls.py)
- [`notes/views.py`](../quickstart/notes/views.py)
- [`notes/tests.py`](../quickstart/notes/tests.py)

## 运行

先进入 quickstart 目录：

```bash
cd ../quickstart
python3 -m py_compile manage.py learn_django/settings.py learn_django/urls.py notes/views.py notes/tests.py
```

如果本机缺少对应工具链，可以先运行仓库根目录的 dry-run：

```bash
python3 scripts/run_framework_examples.py --dry-run
```

## 观察点

根 URL 只做装配，notes app 自己维护业务路由和视图。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`Django` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
