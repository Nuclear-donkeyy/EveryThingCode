# Dart 框架学习索引

Dart 生态最重要的两个方向是跨平台客户端和轻量服务端。Flutter 让 Dart 成为面向移动端、桌面端、Web 和嵌入式 UI 的完整应用平台；Shelf 则代表 Dart 服务端里“显式组合 HTTP 处理链”的基础风格。学习 Dart 框架时，建议把语言的异步、类型、包管理和测试工具先串起来，再进入 Widget tree、Handler/Middleware、状态管理和工程边界。

## 常用框架清单

| 框架/库 | 方向 | 本仓库覆盖 | 适合优先学习的原因 |
| --- | --- | --- | --- |
| Flutter | 跨平台 UI、移动端、桌面端、Web、嵌入式 | 已覆盖：[Flutter](flutter/) | Dart 最主流应用平台，能系统理解 Widget tree、声明式 UI、布局、渲染、状态和平台集成。 |
| Shelf | HTTP 服务器、Middleware、轻量 API | 已覆盖：[Shelf](shelf/) | Dart 服务端基础库之一，适合理解 Handler、Middleware、Pipeline 和显式请求处理。 |
| Dart Frog | 服务端 Web/API、文件路由、middleware | 待扩展 | 建立在 Shelf 之上，提供更接近现代 Web 框架的路由、依赖注入和项目结构。 |
| Aqueduct | 历史上的 Dart 后端框架 | 历史/替代 | 已停止维护，不建议新项目使用；可作为理解 Dart 后端生态演进的参考，替代方向通常是 Shelf、Dart Frog 或通用云函数平台。 |
| Riverpod | 状态管理、依赖注入、可测试状态 | 待扩展 | 适合中大型 Flutter 项目，把状态、缓存、异步加载和依赖关系从 Widget 中拆出来。 |
| Bloc | 事件驱动状态管理、业务流程建模 | 待扩展 | 适合复杂交互和团队协作，强调事件、状态、Reducer-like 转换和可追踪流程。 |
| Provider | 轻量状态共享、依赖传递 | 待扩展 | Flutter 生态常见入门状态管理工具，适合理解 InheritedWidget 风格的依赖向下传递。 |
| freezed / json_serializable | 不可变模型、联合类型、JSON 序列化、代码生成 | 待扩展 | 适合把 API DTO、领域对象和状态对象做成清晰可比较、可序列化的数据结构。 |
| Mockito / test / flutter_test | 单元测试、Mock、Widget 测试 | 待扩展 | Dart/Flutter 工程化基础，帮助把业务逻辑、HTTP handler 和 Widget 行为纳入回归验证。 |

补充生态还包括 drift（本地数据库）、dio/http（HTTP 客户端）、go_router（声明式路由）、melos（多包仓库管理）、build_runner（代码生成入口）和 integration_test（端到端测试）。它们不一定是第一天就要学的框架，但在真实 Flutter 工程中非常常见。

## 选择思路

做跨平台产品、移动端应用、桌面工具或需要高度自定义 UI 的业务，优先从 Flutter 开始。Flutter 自带渲染、布局、手势、动画、主题、国际化、测试和打包工具，学习收益最高。它的代价是你需要理解 Widget tree、BuildContext、状态生命周期和平台适配，而不能把它只当作“Dart 版网页框架”。

做轻量 HTTP API、Webhook、教学服务端基础或内部工具时，Shelf 更适合作为第一站。Shelf 的 API 很薄：一个请求进入 Handler，Middleware 决定横切逻辑，Pipeline 把多个步骤组合成最终服务。它不会替你规定目录、ORM、认证和配置中心，因此更适合学习 HTTP 本质，也更需要你自己设计工程边界。

如果你想要更完整的 Dart 后端项目结构，可以在理解 Shelf 后再看 Dart Frog。它把路由、middleware、依赖作用域和生成工具组织得更像常见 Web 框架，但底层思想仍然离不开 Shelf。

Flutter 状态管理不要急着一上来追库。小项目先用 `StatefulWidget`、`ValueNotifier` 和显式传参理解状态在哪里、谁拥有状态、谁触发重建；再进入 Provider、Riverpod 或 Bloc。Riverpod 更偏组合和可测试依赖，Bloc 更偏事件流和业务流程，Provider 更轻量但在复杂依赖上容易变得隐式。

模型和序列化建议和 API 需求一起学习。简单案例可以手写 `fromJson`/`toJson`，中大型项目再引入 `freezed`、`json_serializable` 和 `build_runner`，用代码生成降低样板代码和状态比较错误。

测试方向可以分三层：纯 Dart 逻辑用 `test`，Flutter Widget 行为用 `flutter_test`，服务端 Handler 用 `shelf` 的请求对象直接调用。Mock 工具如 Mockito 适合外部服务边界，但第一版案例优先用内存仓库，避免 Mock 把核心思想遮住。

## 学习路线

1. 先读 Dart 语言章节，确认类型系统、Future/Stream、异常、包管理、空安全和测试基础。
2. 进入 [Flutter](flutter/)：先理解 Widget tree、声明式 UI、布局约束、状态拥有者和测试方式，再运行 Flutter quickstart。
3. 进入 [Shelf](shelf/)：理解 Handler、Middleware、Pipeline、请求对象和响应对象，再运行 Shelf quickstart。
4. 对比两者：Flutter 的核心问题是“状态变化后如何描述下一帧 UI”；Shelf 的核心问题是“HTTP 请求如何经过一组显式函数得到响应”。
5. 补齐常见横向能力：Flutter 项目补状态管理、路由、本地存储、网络请求和 Widget 测试；Shelf 项目补配置、日志、认证、数据库和容器部署。
6. 再按方向扩展 Dart Frog、Riverpod、Bloc、freezed/json_serializable、Mockito/test，把“框架能力”落到真实产品结构里。

## 本仓库案例

- [Flutter quickstart](flutter/examples/quickstart/)：一个学习任务面板，展示 `runApp`、`MaterialApp`、`StatefulWidget`、状态更新、布局和 Widget 测试。
- [Shelf quickstart](shelf/examples/quickstart/)：一个内存 tasks API，展示 `Handler`、`Middleware`、`Pipeline`、JSON 响应和 handler 级测试。

两个案例都刻意使用内存数据。第一轮先看清框架如何接收事件或请求、定位代码入口、更新状态或执行业务逻辑、输出 UI/HTTP 响应和完成自动化测试。持久化、鉴权、路由库、状态管理库和部署流水线会在后续进阶案例中加入。
