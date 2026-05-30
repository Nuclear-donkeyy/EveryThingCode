# C++ syntax-tour

## 目标

这个示例用一个小型任务统计程序展示现代 C++ 基础语法如何组合在一起。它不是 CMake 工程，也不依赖第三方库；重点是让你在一个 `main.cpp` 中看到 `#include`、`main`、变量、函数、类型、容器、控制流和错误处理如何一起工作。

示例使用 C++23 编译，但刻意选择大多数工具链都比较稳定的标准库能力：`std::string`、`std::vector`、`std::map`、`std::optional` 和异常。这样你可以先建立 C++ 的基础心智模型，再去学习更大的工程组织、构建系统和 C API 互操作。

## 覆盖语法

- `#include`、`namespace demo` 和 `int main()` 的最小程序结构。
- `const`、`auto`、基础数值类型、`bool`、`std::string` 和字符串拼接。
- `if`、`switch`、传统 `for`、范围 `for`，以及 `break` 相关的分支习惯。
- 普通函数、按值返回、`const T&` 引用参数、非拥有指针观察值。
- `std::vector` 保存任务列表，`std::map` 统计分类数量。
- `struct` 表达简单数据，`class` 封装统计规则和私有状态。
- `std::optional` 表达可预期缺失，`throw` / `catch` 处理非法输入。
- 局部对象离开作用域自动析构，展示 RAII 的基本直觉。

## 运行

```bash
c++ -std=c++23 main.cpp -o /tmp/cpp-syntax-tour && /tmp/cpp-syntax-tour
```

第一条命令会在当前目录编译并运行 `main.cpp`。如果你在仓库根目录，可以先进入示例目录再执行同一条命令：

```bash
cd languages/c-cpp/syntax/examples/syntax-tour
c++ -std=c++23 main.cpp -o /tmp/cpp-syntax-tour && /tmp/cpp-syntax-tour
```

## 观察点

程序先把原始任务数据解析成 `Task`，其中 `parse_priority` 返回 `std::optional<int>`：缺少优先级是正常情况，所以不用异常。负数优先级会抛出 `std::runtime_error`，调用方在 `main` 里捕获并继续处理后续数据，这展示了异常更适合表达非法输入或无法按当前规则继续的失败。

`TaskBoard` 是一个 `class`，内部持有 `std::vector<Task>`。外部只能通过成员函数添加任务、统计分类和查找最高优先级任务；这比直接暴露可变字段更容易维护不变量。遍历时你会看到 `const auto&`，它表示只读借用，避免复制任务对象。`top_priority` 返回 `const Task*`，这里只是非拥有观察指针，真正的对象仍由 `TaskBoard` 里的 vector 管理。

程序末尾有一个 `ScopeLog` 局部对象。它的析构函数会在离开作用域时自动运行，即使中间出现异常也会触发。这就是 RAII 的核心直觉：把资源或收尾动作绑定到对象生命周期，而不是到处手写清理分支。

## 修改练习

- 给 `raw_tasks` 增加一个负数优先级，观察异常信息如何被捕获，后续任务是否继续处理。
- 给 `Task` 增加 `owner` 字段，并在 `describe` 函数中输出负责人。
- 把 `std::map<std::string, int>` 换成 `std::unordered_map<std::string, int>`，观察输出顺序是否仍然稳定。
- 让 `parse_priority` 支持空字符串以外的文本输入，例如 `"high"`、`"low"`，并决定哪些情况应该返回 `std::nullopt`，哪些情况应该抛异常。
