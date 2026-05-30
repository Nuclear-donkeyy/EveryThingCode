# Spring Boot

Spring Boot 是学习现代 Java 服务端开发最常见的入口。它不是一个单独替代 Spring Framework 的“新框架”，而是在 Spring Framework、Spring MVC、Jackson、Tomcat/Jetty/Netty、JUnit、Actuator 等生态组件之上，提供自动配置、starter 依赖和可独立运行的应用模型。

## 核心定位

Spring Boot 解决的是“如何快速、稳定、可维护地组装一个 Spring 应用”的问题。它把常见 Web 服务需要的 HTTP 服务器、JSON 序列化、配置绑定、日志、测试、健康检查和依赖版本管理整理成一套约定，让学习者不必从大量 XML 或手工 Bean 配置开始。

它不替你解决业务建模、数据库设计、接口语义、分布式一致性或部署平台治理。Spring Boot 可以让应用启动更容易，但项目长期可维护仍取决于清晰的分层、边界、测试和发布流程。

## 解决的问题

没有 Spring Boot 时，写一个 Java Web/Spring 应用并不是只写 Controller。你通常还要自己选择 Spring MVC、Jackson、Servlet 容器、日志、校验、测试框架、监控端点等组件，并确认它们的版本是否互相兼容。很多初学者卡住的地方不是业务逻辑，而是“项目为什么起不来”“为什么 JSON 没有返回”“为什么测试加载不了 Spring 上下文”“为什么本机能跑、部署后端口和配置不对”。

Spring Boot 把这些问题收束成几组明确机制：

- 应用组装痛点：传统 Spring 项目需要显式声明大量 Bean、Servlet、DispatcherServlet、JSON converter 和扫描路径。Boot 通过 `@SpringBootApplication`、组件扫描和自动配置，根据 classpath 与配置自动组装常见基础设施。quickstart 的 `Application.java` 只有一个入口类，但运行时已经拥有 Spring 容器、MVC 分发器和内嵌服务器。
- 依赖版本痛点：Java Web 生态组件很多，手动组合容易出现 Spring、Jackson、Tomcat、JUnit、Mockito 版本不匹配。Boot 用 parent POM 或 BOM 管理经过验证的依赖矩阵，starter 再把一个场景需要的依赖打包给你。quickstart 的 `pom.xml` 不需要逐个写出 MVC、JSON、Tomcat 和 Spring Test 的细碎版本。
- Web 容器痛点：过去常见做法是把 war 放进外部 Tomcat，需要单独安装、配置和排查容器差异。Boot 默认使用内嵌服务器，`mvn spring-boot:run` 或可执行 jar 就能启动完整 HTTP 服务。这样开发、测试、容器部署时启动模型更一致。
- 配置痛点：端口、数据源、日志级别、profile、外部服务地址如果散落在代码和部署脚本里，会很难迁移环境。Boot 提供统一配置模型，把 `application.yml`、环境变量、命令行参数和配置绑定整合起来。默认值让 quickstart 可以零配置启动，后续又能通过配置覆盖端口、日志或数据源。
- 对象协作痛点：如果 Controller 自己 `new` Repository 或 Service，业务对象会和具体实现绑死，测试时难替换，生命周期也难统一管理。Boot 延续 Spring IoC，用构造函数注入显式表达依赖。quickstart 的 `TaskController` 只声明需要 `TaskRepository`，对象创建和装配交给容器。
- 测试痛点：Web API 不只是普通方法调用，还包含路由匹配、参数绑定、JSON 序列化、状态码和异常处理。Boot Test 把 Spring Test、JUnit 和 Web 测试工具组合好。quickstart 的 `TaskControllerTest` 使用 `MockMvc` 验证 HTTP 行为，不需要启动真实端口。
- 监控与运维痛点：生产服务需要健康检查、指标、info、配置可见性和故障定位入口。Boot 可通过 Actuator 提供标准化观测端点。quickstart 为保持最小化没有引入 Actuator，但真实项目通常会把它作为服务上线的基础能力。

所以，Spring Boot 解决的不是“怎样写一个业务功能”，而是把 Java 服务端项目从手工装配基础设施，推进到围绕业务代码、配置和测试组织工程。

## 设计思想

Spring Boot 的设计不是“把注解藏起来变魔法”，而是把 Spring 生态里最常见、最容易重复出错的组合方式固化成可观察、可替换的默认路径。学习它时，可以把每个注解和 starter 都追问成两个问题：它省掉了哪段基础设施代码？它把默认行为放在哪里，并允许我如何覆盖？

第一层思想是“约定优于配置”。约定不是限制，而是为常见场景给出默认答案。例如 quickstart 把 `Application.java` 放在 `dev.everythingcode.springboot` 包下，`TaskController` 和 `TaskRepository` 也在这个包下面。`@SpringBootApplication` 默认从启动类所在包向下扫描组件，因此不需要额外写 `@ComponentScan`。这种约定让小项目结构清楚，中大型项目也可以按业务包组织，只要理解扫描边界即可。

第二层思想是“自动配置是有条件的默认值”。Boot 会查看 classpath、配置属性、已经存在的 Bean 和运行环境，再决定启用哪些配置。引入 Web starter 后，classpath 上出现 Spring MVC 与内嵌服务器相关类，Boot 才会配置 MVC、`DispatcherServlet`、JSON 消息转换器和错误处理基础设施。如果你自己声明了同类型 Bean，或者写了更具体的配置，默认行为就会让位。自动配置的关键价值是：先给你能工作的默认组合，再保留明确的覆盖点。

第三层思想是“starter 表达场景能力”。starter 不是运行时容器，也不是神秘语法，它是依赖组合和版本协同。`spring-boot-starter-webmvc` 表示“我要做传统阻塞式 Spring MVC Web API”，所以它带来 MVC、JSON、内嵌服务器等能力；`spring-boot-starter-test` 表示“我要以 Boot 风格测试应用”，所以它带来 JUnit、Spring Test、MockMvc 等工具。quickstart 的 `TaskControllerTest` 能直接使用 `MockMvc`，背后就是测试 starter 和 Boot 测试集成在工作。

第四层思想是“IoC 管理对象协作，而不是只减少 new”。`TaskController` 通过构造函数声明 `TaskRepository`，`TaskRepository` 通过 `@Repository` 进入容器。这样 Controller 只关心“我需要任务仓库”，不关心仓库何时创建、是否单例、以后是否换成 JPA 实现。依赖关系在构造函数上可读、可测试、可替换，比在方法里到处 `new` 具体类更适合长期演进。

第五层思想是“Web 框架处理协议细节，业务代码表达意图”。`@GetMapping`、`@PostMapping`、`@PathVariable`、`@RequestBody` 和 `ResponseEntity` 把 HTTP 的路径、方法、请求体、状态码映射到 Java 方法。`TaskController.findById` 返回 `Optional` 分支对应的 `200 OK` 或 `404 Not Found`，这比手写 Servlet 时直接操作 request/response 更接近业务语义，也更容易通过 MockMvc 测试。

第六层思想是“默认值可观察、可覆盖、可测试”。Boot 的好用来自默认值，但成熟项目不能停留在“能跑”。当默认 JSON 格式、错误响应、端口、日志、数据源或健康检查不符合要求时，应通过配置属性、显式 Bean、profile 或测试覆盖它们。quickstart 保持默认端口和默认 JSON 序列化，是为了让学习者先看清主链路；随后可以加入 `application.yml`、校验、异常处理或 Actuator，观察默认行为如何被替换。

## 架构模型

一个典型 Spring Boot Web API 可以理解为四层：

- 启动层：`Application` 使用 `@SpringBootApplication` 标记根配置类，并调用 `SpringApplication.run(...)` 创建应用上下文。
- 接入层：`@RestController` 声明 HTTP 路由，把请求参数、路径变量和 JSON body 转换为 Java 对象。
- 业务层：`@Service` 或普通类承载用例逻辑，避免控制器直接堆业务流程。
- 数据层：`@Repository`、JPA Repository、MyBatis Mapper 或外部客户端负责持久化与远程调用。

本仓库 quickstart 为了让核心链路更清楚，暂时使用内存 `TaskRepository`。真实工程扩展时，可以把 Repository 换成 JPA、MyBatis、Redis 或 HTTP client，但 Controller 和测试入口不需要大幅改动。

## 请求/执行生命周期

一次 HTTP 请求进入 Spring Boot MVC 应用时，大致经历以下步骤：

1. 内嵌服务器接收连接，例如 Tomcat 接收 `GET /tasks`。
2. 请求交给 Spring MVC 的 `DispatcherServlet`，它是 MVC 应用的前端控制器。
3. `DispatcherServlet` 根据路径、HTTP 方法、参数条件匹配到某个 `@RequestMapping` / `@GetMapping` 方法。
4. Spring MVC 执行参数绑定，把 path variable、query string、header 或 JSON body 转成 Java 参数。
5. Controller 调用业务或数据组件。依赖通过构造函数注入，调用关系是显式的。
6. Controller 返回对象或 `ResponseEntity`，消息转换器通常使用 Jackson 把对象序列化为 JSON。
7. 框架写回 HTTP status、headers 和 body。测试中可以用 MockMvc 不启动真实端口也验证这条链路。

理解这个生命周期后，很多常见问题会变得可定位：404 通常是路由没匹配，400 通常是参数绑定或校验失败，500 通常是业务异常未处理或依赖初始化失败。

## 工程结构

quickstart 使用真实 Maven 工程结构：

```text
examples/quickstart/
  pom.xml
  src/main/java/dev/everythingcode/springboot/
    Application.java
    Task.java
    TaskController.java
    TaskRepository.java
  src/test/java/dev/everythingcode/springboot/
    TaskControllerTest.java
```

小项目可以按技术角色分文件；中大型项目更推荐按业务域组织，例如 `task/TaskController.java`、`task/TaskService.java`、`task/TaskRepository.java`。核心原则是：入口、业务规则、数据访问、配置、测试各有边界，不把所有代码放进启动类或控制器。

## 配置方式

Spring Boot 配置主要有四类来源：

- Maven/Gradle 构建配置：决定 Java 版本、依赖、插件和打包方式。
- `application.properties` 或 `application.yml`：配置端口、数据源、日志、序列化、Actuator 等运行时属性。
- 环境变量和命令行参数：适合部署时覆盖，如 `SERVER_PORT=8081` 或 `--spring.profiles.active=prod`。
- Java 配置类：用 `@Configuration` 和 `@Bean` 明确声明需要交给容器管理的对象。

quickstart 为了降低噪音，没有额外放 `application.properties`。默认端口是 `8080`，默认 JSON 序列化由 Web starter 提供。学习时可以先跑通默认配置，再逐步加入端口、日志和 profile。

## 模块与依赖管理

Spring Boot 项目通常通过 parent POM 或 BOM 管理依赖版本，避免每个 starter 都手写兼容版本。quickstart 使用 `spring-boot-starter-parent`，并声明 Java 25 与 Spring Boot 4.0.x 基线。

依赖管理的关键不是“越少越好”或“starter 越多越好”，而是每个 starter 都应该对应一个明确能力：Web MVC、数据访问、校验、测试、监控等。引入依赖后要知道它带来了哪些自动配置、哪些传递依赖，以及是否影响启动时间、安全面或运行内存。

模块机制上，Spring Boot 主要依赖 Spring IoC 容器组织 Bean。组件扫描会从 `Application` 所在包向下寻找组件，所以示例把所有类放在 `dev.everythingcode.springboot` 包下。真实项目中，如果组件不在扫描路径下，需要显式 `@ComponentScan` 或调整包结构。

## 数据访问

本案例使用内存 `ConcurrentHashMap` 保存任务，目的是突出 HTTP 路由、依赖注入和测试链路。它适合教学，不适合生产：进程重启数据会丢失，也没有事务、索引、查询优化或并发写入语义保证。

接入关系型数据库时，常见路径有两条：

- Spring Data JPA + Hibernate：适合实体关系清晰、CRUD 多、希望少写样板 SQL 的系统。重点学习 `@Entity`、Repository、事务、懒加载和迁移脚本。
- MyBatis：适合 SQL 需要强控制、复杂查询多、希望 SQL 与 Java 映射清晰分离的系统。重点学习 Mapper、参数绑定、结果映射和事务边界。

无论使用哪条路径，都建议把数据访问隐藏在 Repository/Mapper 后面，让 Controller 不直接接触数据库细节。

## 测试方式

Spring Boot 测试可以分层：

- 单元测试：直接 new 业务类，使用假仓库或 Mockito，速度最快。
- Web 切片测试：用 `@WebMvcTest` 只加载 MVC 层，适合验证路由、参数绑定、JSON 和 HTTP 状态。
- 集成测试：用 `@SpringBootTest` 加载完整应用上下文，必要时配合 Testcontainers 启动真实数据库。

quickstart 使用 `@SpringBootTest` 加载应用上下文，并从 `WebApplicationContext` 构建 `MockMvc`。这样可以验证从 MVC 到内存 Repository 的完整路径，又不需要真实监听端口。学习者可以先运行 `mvn test`，再启动应用用 `curl` 做手动验证。

## 部署方式

Spring Boot 应用通常打成可执行 jar：

```bash
mvn package
java -jar target/spring-boot-quickstart-0.1.0-SNAPSHOT.jar
```

生产部署时可以进一步加入 Dockerfile、分层镜像、健康检查、Actuator、外部配置和日志采集。容器部署不应该把密码、数据库地址等写死在 jar 内，而应通过环境变量、配置文件挂载或平台 secret 注入。

## 适用场景与取舍

优先选择 Spring Boot 的场景包括：企业内部系统、REST API、微服务、后台任务、需要成熟数据访问和测试生态的长期项目、团队成员 Java/Spring 经验较多的项目。

需要谨慎评估的场景包括：极端冷启动要求、非常小的 Serverless 函数、强事件驱动且不需要 MVC 模型的网关层、只需单文件脚本的自动化任务。此时可以比较 Quarkus、Micronaut、Vert.x、原生 Java HTTP Server 或其他语言生态。

Spring Boot 的优势是生态稳定、资料多、企业集成能力强；代价是抽象层较厚，初学者容易把自动配置当魔法。学习时要不断把注解背后的运行链路还原出来。

## 案例索引

- [core-ideas](examples/core-ideas/)：把上一节“解决的问题”和“设计思想”映射到 quickstart 的关键代码片段。
- [quickstart](examples/quickstart/)：最小 REST API 项目，包含任务列表查询、创建任务、按 id 查询、MockMvc 测试和可复制运行命令。

## 版本来源

- 语言基线：Java 25 LTS，见根目录 `versions.yaml`。
- 框架基线：Spring Boot 4.0.x，策略为 latest stable / supported，见根目录 `versions.yaml`。
- 官方来源：https://spring.io/projects/spring-boot
- 校验日期：2026-05-30
- 说明：本仓库离线编写时无法联网刷新具体 patch 与 Maven 仓库可用性；运行前应以官方页面和 `versions.yaml` 的版本策略为准，把 `pom.xml` 中的 Spring Boot patch 调整到当前 4.0.x 可用版本。
