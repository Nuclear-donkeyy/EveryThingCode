# Spring Boot quickstart

这是一个最小但真实的 Spring Boot REST API。它没有连接数据库，而是用内存仓库存储任务，方便把学习重点放在应用入口、路由、依赖注入、JSON 响应和 HTTP 测试上。

## 目标

完成本案例后，你应该能读懂一个 Spring Boot API 项目的基本结构，知道请求如何从 HTTP 路由进入 Controller，再调用 Repository 返回 JSON；也能用 Maven 运行测试、启动服务，并用 `curl` 验证接口。

## 学习重点

- `@SpringBootApplication` 是启动入口，也是组件扫描的默认根包。
- `@RestController` 把 Java 方法暴露为 HTTP endpoint，并自动把返回对象序列化为 JSON。
- 构造函数注入让 Controller 明确声明它依赖 `TaskRepository`，测试时也更容易替换依赖。
- `ConcurrentHashMap` 只是教学用内存存储，展示 Repository 边界，不代表生产级数据访问。
- `MockMvc` 可以不启动真实端口就测试 HTTP 路由、状态码和 JSON 字段。

## 工程结构

```text
.
  pom.xml
  src/main/java/dev/everythingcode/springboot/
    Application.java        # 应用入口，创建 Spring 容器和内嵌 Web 服务器
    Task.java               # REST API 返回和接收的任务数据模型
    TaskController.java     # HTTP 路由，处理任务查询与创建
    TaskRepository.java     # 内存数据仓库，封装存取逻辑
  src/test/java/dev/everythingcode/springboot/
    TaskControllerTest.java # 使用 MockMvc 验证 API 行为
```

## 运行前提

- JDK 25，和根目录 `versions.yaml` 的 Java 基线一致。
- Maven 3.9+。
- 能访问 Maven Central 下载依赖。
- Spring Boot 版本按根目录 `versions.yaml` 使用 4.0.x。当前目录的 `pom.xml` 写入了一个教学用 patch；如果运行当天官方已有更新 patch，请优先按官方页面与 `versions.yaml` 策略调整。

## 运行

在本目录执行：

```bash
mvn test
```

启动服务：

```bash
mvn spring-boot:run
```

另开一个终端验证接口：

```bash
curl -s http://localhost:8080/tasks
curl -s -X POST http://localhost:8080/tasks \
  -H 'Content-Type: application/json' \
  -d '{"title":"Learn Spring Boot","done":false}'
curl -s http://localhost:8080/tasks/1
```

打包并运行可执行 jar：

```bash
mvn package
java -jar target/spring-boot-quickstart-0.1.0-SNAPSHOT.jar
```

## 预期输出

`mvn test` 应通过 `TaskControllerTest` 中的 HTTP 行为验证。启动服务后，首次访问列表会得到示例数据：

```json
[{"id":1,"title":"Read Spring Boot guide","done":false},{"id":2,"title":"Run quickstart tests","done":true}]
```

创建任务时会返回 `201 Created`，响应体类似：

```json
{"id":3,"title":"Learn Spring Boot","done":false}
```

查询不存在的任务会返回 `404 Not Found`，这来自 Controller 中对 `Optional` 的显式处理。

## 代码讲解

`Application.java` 是整个应用的入口。`@SpringBootApplication` 组合了组件扫描、自动配置和配置类能力；`SpringApplication.run(...)` 会创建 Spring 应用上下文，并启动内嵌 Web 服务器。这个文件很短，正是 Spring Boot 的核心价值之一：你不需要手写 Servlet 初始化、MVC 分发器、JSON 转换器和 Web 容器启动脚本，Boot 会根据 starter 和 classpath 给出默认装配。

`Task.java` 使用 Java record 表达不可变数据载体。对于简单 DTO，record 比传统 JavaBean 更短，也天然带有构造方法、访问器、`equals` 和 `hashCode`。

`TaskRepository.java` 用 `@Repository` 注册为 Spring Bean。它内部用 `ConcurrentHashMap` 保存数据，并用 `AtomicLong` 生成 id。Controller 不知道存储细节，只依赖 `findAll`、`findById` 和 `create` 这些方法，这就是数据访问边界。这个边界解决的是“控制器和存储实现绑死”的问题：今天仓库是内存 Map，明天可以替换成 JPA Repository、MyBatis Mapper 或远程 API client，而 Controller 的 HTTP 语义可以尽量保持稳定。

`TaskController.java` 用 `@RequestMapping("/tasks")` 设置统一路径前缀，`@GetMapping` 和 `@PostMapping` 分别声明查询与创建接口。方法返回 `ResponseEntity` 时，可以同时控制状态码和响应体。这里体现了 Spring MVC 解决的问题：不用直接处理底层 `HttpServletRequest` 和 `HttpServletResponse`，而是把“读取路径变量”“解析 JSON body”“返回 201 Created”“不存在时返回 404”表达成清晰的 Java 方法。

`TaskController` 的构造函数接收 `TaskRepository`，而不是在方法里 `new TaskRepository()`。这体现了 IoC 的价值：对象的创建、生命周期和依赖装配交给 Spring 容器，业务代码只声明协作关系。等到项目变大时，你可以给 Repository 加配置、事务、缓存或替换实现，而不需要在每个 Controller 里改对象创建逻辑。

`TaskControllerTest.java` 使用 `MockMvc` 发起模拟 HTTP 请求。它验证的不只是 Java 方法返回值，而是包括路由匹配、JSON 序列化和 HTTP 状态码在内的 Web 层行为。`@SpringBootTest` 会加载应用上下文，`MockMvcBuilders.webAppContextSetup(context)` 则复用真实 MVC 配置，所以测试能覆盖“Boot 自动配置 + Controller + Repository”的主链路，同时避免真实端口、外部服务器和手工启动步骤。

这个 quickstart 故意没有加入数据库、认证、全局异常处理和 Actuator。它的教学重点是先看清 Spring Boot 如何解决基础设施装配问题：starter 负责依赖组合，自动配置负责默认基础设施，IoC 负责对象协作，Spring MVC 负责 HTTP 映射，Boot Test 负责把这些能力放进可重复运行的测试里。

## 延伸练习

- 给 `Task` 增加 `priority` 字段，并更新 POST 请求、测试和预期输出。
- 把内存仓库替换为 Spring Data JPA，使用 H2 或 PostgreSQL 保存任务。
- 增加 `PATCH /tasks/{id}/done`，练习路径变量、局部更新和 404 分支测试。

## 验收

- 能说清 `Application`、`TaskController`、`TaskRepository` 和测试各自职责。
- 能运行 `mvn test` 并解释 MockMvc 测试验证了哪些 HTTP 行为。
- 能启动服务并用 `curl` 完成列表查询、创建任务和按 id 查询。
- 能说明为什么本案例用内存仓库教学，以及生产项目为什么要替换为数据库或外部服务。
