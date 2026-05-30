# 框架学习总览

这一层用于从“语言生态”进入“框架实践”。每个语言目录先列出该生态最常用的框架、库和平台，再对本仓库覆盖的代表性框架做深入讲解，并提供最小可运行项目。

## 学习方式

1. 先阅读对应语言的 `frameworks/<language>/README.md`，理解该生态常见框架的分工。
2. 选择一个代表性框架进入 `frameworks/<language>/<framework>/README.md`，重点看设计思想、生命周期和工程结构。
3. 运行 `examples/quickstart/` 中的最小项目，把路由、组件、依赖、配置和数据流串起来。
4. 再回到语言特性章节，对比框架为什么采用这种抽象方式。

## 语言入口

| 语言 | 框架入口 | 本仓库首批覆盖 |
| --- | --- | --- |
| Java | [frameworks/java/](java/) | Spring Boot |
| JavaScript / TypeScript | [frameworks/javascript-typescript/](javascript-typescript/) | Next.js、NestJS |
| Python | [frameworks/python/](python/) | Django、FastAPI |
| Go | [frameworks/go/](go/) | net/http、Gin |
| Rust | [frameworks/rust/](rust/) | Axum、Actix Web |
| C# / .NET | [frameworks/csharp-dotnet/](csharp-dotnet/) | ASP.NET Core |
| Kotlin | [frameworks/kotlin/](kotlin/) | Ktor、Compose Multiplatform |
| PHP | [frameworks/php/](php/) | Laravel、Symfony |
| C / C++ | [frameworks/c-cpp/](c-cpp/) | CMake、Qt、Boost |
| Ruby | [frameworks/ruby/](ruby/) | Rails、Sinatra |
| Swift | [frameworks/swift/](swift/) | SwiftUI、Vapor |
| Dart | [frameworks/dart/](dart/) | Flutter、Shelf |

## 验证

```bash
python3 scripts/verify_framework_modules.py
python3 scripts/run_framework_examples.py --dry-run
```

`run_framework_examples.py --execute` 只会在本机工具链存在时尝试运行命令。多数框架案例依赖外部包管理器下载依赖，离线环境下以结构校验和 dry run 为主。
