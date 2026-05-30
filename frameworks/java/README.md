# Java 框架学习路线

Java 生态的框架通常围绕三个问题展开：如何组织大型业务代码，如何把 HTTP、事务、数据库、消息队列等基础设施接入工程，以及如何在长期演进中保持可测试、可部署、可观测。本目录先覆盖 Spring Boot，因为它是当代 Java Web 与企业应用最常见的入口；后续可以按使用场景继续补 Quarkus、Micronaut、Jakarta EE、Vert.x、Hibernate/JPA 与 MyBatis 等专题。

## 常用框架清单

| 框架/库/平台 | 主要用途 | 典型思想 | 本仓库状态 |
| --- | --- | --- | --- |
| Spring Boot | Web API、企业服务、微服务、批处理入口 | 自动配置、约定优于配置、IoC 容器、starter 依赖 | 已覆盖：[spring-boot](spring-boot/) |
| Spring Framework / Spring MVC | IoC、AOP、事务、Web MVC 基础设施 | 依赖注入、声明式事务、分层 MVC | 待补充，当前通过 Spring Boot 案例间接学习 |
| Jakarta EE | 企业级标准 API，如 Servlet、JPA、CDI、JAX-RS | 标准优先、容器托管、规范与实现分离 | 待补充 |
| Quarkus | 云原生、容器、Kubernetes、GraalVM 原生镜像 | 构建期增强、快速启动、低内存占用 | 待补充 |
| Micronaut | 轻量服务、Serverless、微服务 | 编译期依赖注入、低反射、快速启动 | 待补充 |
| Hibernate / JPA | ORM 与关系型数据库持久化 | 实体映射、工作单元、脏检查、声明式事务 | 待补充，适合作为 Spring Boot 数据访问进阶 |
| MyBatis | SQL 映射与半自动 ORM | 显式 SQL、Mapper 接口、结果映射 | 待补充，适合 SQL 可控的业务系统 |
| Vert.x | 高并发异步服务、事件驱动系统 | Event Loop、非阻塞 I/O、响应式组合 | 待补充 |
| Maven / Gradle | 构建、依赖管理、插件生命周期 | 声明式构建、仓库解析、任务编排 | 待补充，当前 quickstart 使用 Maven |
| JUnit / Mockito / Testcontainers | 单元、集成和外部依赖测试 | 自动化反馈、替身对象、真实依赖容器化 | 待补充，当前 quickstart 使用 JUnit 与 MockMvc |

## 选择思路

如果目标是传统 Web API、后台管理、企业服务或微服务，优先从 Spring Boot 开始。它把 Spring MVC、校验、JSON、测试、配置、监控等常见能力整合为 starter，学习成本主要在理解 Spring 容器和自动配置。一旦掌握它，再回看 Spring Framework / Spring MVC 会更容易理解底层机制。

如果团队更重视云原生冷启动、容器密度和原生镜像，可以比较 Quarkus 与 Micronaut。它们把一部分运行时扫描和反射成本前移到编译期，适合 Serverless、Kubernetes 和资源敏感场景，但生态通用性通常不如 Spring Boot。

如果系统以标准规范、应用服务器和供应商兼容为核心，Jakarta EE 更合适。它强调 API 规范与实现分离，常见于金融、电信、政企等生命周期很长的项目。

数据访问不要只按“流行度”选择。Hibernate/JPA 适合领域模型清晰、希望减少样板 SQL 的系统；MyBatis 适合 SQL 需要精细控制、报表查询复杂、DBA 与开发协作紧密的系统。真实项目中也经常组合使用：核心交易走显式 SQL，普通 CRUD 走 ORM。

Vert.x 适合你明确需要事件驱动、非阻塞 I/O 和高并发连接管理的场景。它不是 Spring Boot 的直接替代品，而是把编程模型从“每个请求进入控制器”推向“事件在多个异步处理器之间流动”。

## 学习路线

1. 先读 `languages/java/README.md` 与 Java 语法/特性案例，确保理解 class、interface、record、exception、generic、stream、thread/virtual thread、module、Maven 依赖这些基础。
2. 阅读 [Spring Boot](spring-boot/) 的核心定位、设计思想和请求生命周期，先建立“容器管理对象、自动配置装配基础设施、控制器处理 HTTP”的心智模型。
3. 跑通 [Spring Boot quickstart](spring-boot/examples/quickstart/)，观察一个 REST API 从 `Application` 启动类到 `TaskController`、再到内存仓库和测试的完整链路。
4. 进阶到数据访问：在 quickstart 中把内存仓库替换为 JPA 或 MyBatis，理解事务边界、连接池、迁移脚本和测试数据库。
5. 再比较 Quarkus、Micronaut、Jakarta EE 与 Vert.x：不要先背 API，而是比较它们的组件生命周期、配置方式、启动模型和部署目标。

## 本仓库案例

- [Spring Boot quickstart](spring-boot/examples/quickstart/)：一个最小但真实的 REST API 项目，包含 Maven 依赖、应用入口、Controller、内存 Repository 和 MockMvc 测试。

