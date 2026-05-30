# Shelf core ideas example

## 目标

这个示例把 `Shelf` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

Dart 服务端 HTTP 需要轻量处理 Handler、Middleware、Pipeline、Request/Response、JSON、测试和部署 adapter。

## 核心思想到代码

Handler 是函数式入口，Middleware 包裹横切逻辑，Pipeline 顺序组合，adapter 把同一 handler 接到不同运行环境。

```dart
final handler = const Pipeline()
    .addMiddleware(logRequests())
    .addHandler(_router);
```

```dart
Response _router(Request request) {
  if (request.url.path == "tasks") {
    return Response.ok(jsonEncode({"items": tasks}));
  }
  return Response.notFound("not found");
}
```

## 代码位置

- [`pubspec.yaml`](../quickstart/pubspec.yaml)
- [`bin/server.dart`](../quickstart/bin/server.dart)
- [`test/server_test.dart`](../quickstart/test/server_test.dart)

## 运行

先进入 quickstart 目录：

```bash
cd ../quickstart
dart test
```

如果本机缺少对应工具链，可以先运行仓库根目录的 dry-run：

```bash
python3 scripts/run_framework_examples.py --dry-run
```

## 观察点

测试可以直接调用 handler，不需要先启动监听端口。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`Shelf` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
