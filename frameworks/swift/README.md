# Swift 框架与常用库

Swift 的生态横跨 Apple 平台客户端、服务端 API、命令行工具和系统库封装。学习 Swift 框架时，建议先把语言层的值类型、协议、泛型、错误处理、并发模型、属性包装器和包管理理解清楚，再进入框架。SwiftUI、Vapor、ArgumentParser 等框架并不是彼此孤立的技术点，它们都在用 Swift 的类型系统把“状态、依赖、生命周期和副作用”表达得更明确。

## 常用框架清单

| 方向 | 框架/库 | 常见用途 | 本仓库状态 |
| --- | --- | --- | --- |
| 声明式 UI | [SwiftUI](swiftui/) | iOS、macOS、watchOS、visionOS 的声明式界面、状态驱动渲染 | 已覆盖 |
| 传统 UI | UIKit / AppKit | 成熟 Apple 平台 UI、复杂手势、系统控件深度定制 | 待扩展 |
| 服务端 Web | [Vapor](vapor/) | JSON API、Web 服务、Middleware、Fluent 数据访问 | 已覆盖 |
| 服务端 Web | Hummingbird | 轻量服务端 Swift、插件化、AsyncHTTPClient 生态 | 待扩展 |
| CLI | ArgumentParser | 命令行工具、子命令、参数解析、帮助文档生成 | 待扩展 |
| 状态与响应式 | Combine / Observation | 事件流、状态观察、SwiftUI 数据刷新 | 待扩展 |
| 数据持久化 | Core Data / SwiftData | Apple 平台本地数据、对象图、持久化模型 | 待扩展 |
| 测试 | XCTest / Swift Testing | 单元测试、异步测试、包测试、UI 测试入口 | 待扩展 |
| 底层与系统 | Foundation / Network / CryptoKit | 文件、URL、日期、网络、加密、系统集成 | 待扩展 |

## 选择思路

如果目标是 Apple 平台应用，优先从 [SwiftUI](swiftui/) 入手。SwiftUI 用 `View`、状态属性包装器和环境对象把界面描述成状态的函数，适合新项目、跨 Apple 设备体验和与 Observation/SwiftData 组合的现代应用。遇到复杂系统控件、老项目迁移或 UIKit/AppKit 已有大量投资时，可以采用 SwiftUI 与 UIKit/AppKit 混合的方式，而不是一次性重写。

如果目标是服务端 API，可以从 [Vapor](vapor/) 开始。Vapor 展示了 Swift 在服务端的常见形态：路由、请求/响应、Middleware、async/await、依赖注入式的 `Application` 配置，以及通过 Fluent 接入数据库。Hummingbird 更轻量，适合想更接近底层 HTTP 组件和插件组合的读者。

如果目标是工具链或自动化，ArgumentParser 是最值得先学的库，因为它把命令、参数、校验和帮助输出组合成类型安全的结构。数据访问方面，Apple 客户端优先理解 Core Data/SwiftData；服务端优先理解 Fluent、SQLKit 或直接使用 PostgreSQL/MySQL 驱动。测试方面，先用 XCTest 覆盖可隔离的模型和服务，再按平台加入 UI 测试或 HTTP 集成测试。

## 学习路线

1. 先读 Swift 语言章节，重点关注 `struct`/`class`、协议、泛型、属性包装器、错误处理、`async`/`await` 和 Swift Package Manager。
2. 阅读 [SwiftUI](swiftui/)：理解声明式 UI、状态绑定、环境传值、视图生命周期，以及为什么业务状态应从视图树中清晰抽离。
3. 运行 [SwiftUI quickstart](swiftui/examples/quickstart/)：观察 `@State`、`@Binding`、`@Observable` 风格的职责边界，并尝试改造一个列表交互。
4. 阅读 [Vapor](vapor/)：理解 Router、Request/Response、Middleware、服务注册和 Fluent 的数据建模思路。
5. 运行 [Vapor quickstart](vapor/examples/quickstart/)：用内存仓储写一个任务 API，再把仓储替换成 Fluent 或外部服务。
6. 扩展到真实工程：客户端加入 SwiftData、网络层和 UI 测试；服务端加入数据库迁移、配置、日志、容器部署和 CI。

## 本仓库案例

- [SwiftUI quickstart](swiftui/examples/quickstart/)：一个 Swift Package 形式的最小 SwiftUI app，展示状态驱动列表、绑定、环境值和组件拆分。
- [Vapor quickstart](vapor/examples/quickstart/)：一个最小 Vapor API Package，展示路由分组、中间件、内存 repository、JSON 请求/响应和 async handler。
