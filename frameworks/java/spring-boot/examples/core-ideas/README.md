# Spring Boot core ideas example

## 目标

这个示例把 `Spring Boot` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

把 Web 容器、MVC 路由、JSON、依赖注入、配置和测试从手工装配变成默认可运行的应用骨架。

## 核心思想到代码

自动配置负责基础设施，starter 负责依赖组合，IoC 容器负责对象生命周期，Controller/Repository 把 HTTP 边界和数据边界分开。

```java
@SpringBootApplication
public class Application {
  public static void main(String[] args) {
    SpringApplication.run(Application.class, args);
  }
}
```

```java
@RestController
@RequestMapping("/tasks")
class TaskController {
  private final TaskRepository repository;

  TaskController(TaskRepository repository) {
    this.repository = repository;
  }
}
```

## 代码位置

- [`src/main/java/dev/everythingcode/springboot/Application.java`](../quickstart/src/main/java/dev/everythingcode/springboot/Application.java)
- [`src/main/java/dev/everythingcode/springboot/TaskController.java`](../quickstart/src/main/java/dev/everythingcode/springboot/TaskController.java)
- [`src/main/java/dev/everythingcode/springboot/TaskRepository.java`](../quickstart/src/main/java/dev/everythingcode/springboot/TaskRepository.java)
- [`src/test/java/dev/everythingcode/springboot/TaskControllerTest.java`](../quickstart/src/test/java/dev/everythingcode/springboot/TaskControllerTest.java)

## 运行

先进入 quickstart 目录：

```bash
cd ../quickstart
mvn test
```

如果本机缺少对应工具链，可以先运行仓库根目录的 dry-run：

```bash
python3 scripts/run_framework_examples.py --dry-run
```

## 观察点

运行测试时观察 MockMvc 不启动真实端口也能穿过 MVC 路由、参数绑定和 Repository。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`Spring Boot` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
