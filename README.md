# 主流编程语言与框架学习仓库

这个仓库用于系统学习主流编程语言及其代表性框架。第一版采用中文文档、统一章节模板和最小可运行案例，目标是让学习者能横向比较语言特性，也能纵向进入框架工程实践。

## 版本策略

- 有官方 LTS 或 Active LTS 的生态，优先使用当前最新 LTS。
- 没有官方 LTS 概念的生态，使用官方最新 stable 或受支持分支，并在 [`versions.yaml`](versions.yaml) 标注为 `latest-stable-no-lts` 或 `latest-supported-stable`。
- 本仓库的版本基线最后校验日期为 2026-05-30。实际安装时请以各官方页面和包管理器解析结果为准。

## 学习路线

1. 先阅读一门语言的 `languages/<language>/README.md`，理解类型系统、错误处理、并发模型和工程化方式。
2. 运行该语言的 3 个基础案例：`hello`、`data-flow`、`errors`。
3. 再进入 [`frameworks/`](frameworks/) 和 `frameworks/<language>/<framework>/README.md`，学习框架核心思想和最小项目结构。
4. 横向比较不同语言在同一类问题上的表达方式，例如数据建模、错误恢复、HTTP API。

## 语言目录

| 语言 | 版本基线 | 策略 | 典型场景 |
| --- | --- | --- | --- |
| [Java](languages/java/) | 25 LTS | latest-lts | 企业服务、Android 生态、数据平台、中间件 |
| [JavaScript / TypeScript](languages/javascript-typescript/) | Node.js 24.16.0 LTS | latest-active-lts | Web 前端、Node 服务、全栈应用、工具链 |
| [Python](languages/python/) | 3.14.5 | latest-supported-stable | 自动化、AI/数据、Web API、脚本工具 |
| [Go](languages/go/) | 1.26.3 | latest-supported-stable | 云原生、微服务、CLI、基础设施 |
| [Rust](languages/rust/) | 1.96.x | latest-stable-no-lts | 系统编程、性能服务、嵌入式、WebAssembly |
| [C# / .NET](languages/csharp-dotnet/) | .NET 10.0.8 LTS | latest-lts | 企业后端、桌面、游戏、云服务 |
| [Kotlin](languages/kotlin/) | 2.3.x | latest-stable-no-lts | Android、服务端、跨平台 UI |
| [PHP](languages/php/) | 8.5.x | latest-supported-stable | Web 应用、CMS、电商、业务后台 |
| [C / C++](languages/c-cpp/) | C23 / C++23 | latest-published-standards | 系统、游戏、音视频、数据库、性能核心 |
| [Ruby](languages/ruby/) | 4.0.x | latest-stable-no-lts | Web 产品、自动化、DSL、脚本工具 |
| [Swift](languages/swift/) | 6.3.x | latest-stable-no-lts | Apple 平台、服务端、CLI、系统工具 |
| [Dart](languages/dart/) | 3.12.x | latest-stable-no-lts | Flutter 应用、跨平台 UI、客户端工具 |

## 框架目录

| 框架 | 语言 | 版本基线 | 第一案例 |
| --- | --- | --- | --- |
| [Spring Boot](frameworks/java/spring-boot/) | Java | 4.0.x | REST API |
| [Next.js](frameworks/javascript-typescript/nextjs/) | JavaScript / TypeScript | 16.x Active LTS | App Router 页面 |
| [NestJS](frameworks/javascript-typescript/nestjs/) | JavaScript / TypeScript | latest stable | 模块化 API |
| [Django](frameworks/python/django/) | Python | 5.2 LTS | CRUD 后台 |
| [FastAPI](frameworks/python/fastapi/) | Python | latest stable | JSON API |
| [net/http](frameworks/go/net-http/) | Go | Go standard library | HTTP 服务 |
| [Gin](frameworks/go/gin/) | Go | latest stable | REST API |
| [Axum](frameworks/rust/axum/) | Rust | latest stable | 异步 API |
| [Actix Web](frameworks/rust/actix-web/) | Rust | latest stable | REST API |
| [ASP.NET Core](frameworks/csharp-dotnet/aspnet-core/) | C# / .NET | .NET 10.0.8 LTS | Minimal API |
| [Ktor](frameworks/kotlin/ktor/) | Kotlin | latest stable | JSON API |
| [Compose Multiplatform](frameworks/kotlin/compose-multiplatform/) | Kotlin | latest stable | 计数器 UI |
| [Laravel](frameworks/php/laravel/) | PHP | latest supported major | CRUD API |
| [Symfony](frameworks/php/symfony/) | PHP | latest LTS line | 控制器 API |
| [CMake](frameworks/c-cpp/cmake/) | C / C++ | latest stable | CLI 构建 |
| [Qt](frameworks/c-cpp/qt/) | C / C++ | latest LTS | 窗口应用 |
| [Boost](frameworks/c-cpp/boost/) | C / C++ | latest stable | 算法/工具库 |
| [Rails](frameworks/ruby/rails/) | Ruby | latest supported series | 资源控制器 |
| [Sinatra](frameworks/ruby/sinatra/) | Ruby | latest stable | 微服务 API |
| [SwiftUI](frameworks/swift/swiftui/) | Swift | latest stable | 列表 UI |
| [Vapor](frameworks/swift/vapor/) | Swift | latest stable | JSON API |
| [Flutter](frameworks/dart/flutter/) | Dart | 3.44 stable | 计数器 UI |
| [Shelf](frameworks/dart/shelf/) | Dart | latest stable | HTTP 服务 |

## 验证

```bash
python3 scripts/verify_versions.py
python3 scripts/run_smoke_tests.py --dry-run
python3 scripts/verify_framework_modules.py
python3 scripts/run_framework_examples.py --dry-run
```

`run_smoke_tests.py` 默认只检查案例结构和运行命令；加上 `--execute` 后会尝试运行本机已经安装的语言工具链案例。
