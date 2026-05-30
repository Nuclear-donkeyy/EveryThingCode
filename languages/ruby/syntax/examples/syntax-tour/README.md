# Ruby syntax-tour

## 目标

这个示例把 Ruby 基础语法串成一个小型“任务汇总”脚本。读者可以在一个文件里看到变量、常量、字符串插值、条件分支、`case`、`each`、方法、块、数组、哈希、类、模块 mixin、异常和 `ensure` 如何一起工作。它不是 Rails 项目，也不引入第三方 gem，重点是先看清 Ruby 语言本身的日常表达方式。

## 覆盖语法

- 变量与常量：`DEFAULT_OWNER`、局部变量、实例变量和常量冻结。
- 基础类型与字符串：`Integer`、`String`、`Symbol`、`true` / `false`、`nil`、双引号插值。
- 控制流：`if` / `elsif` / `else`、`case`、范围、`each`、`next`。
- 方法与 block：普通方法、关键字参数、默认参数、`yield` 包装输出。
- 集合：`Array` 保存任务，`Hash` 统计状态，`map` / `select` / `sum` / `uniq` 组合数据流。
- 数据建模：`class Task`、`initialize`、`attr_reader`、谓词方法 `done?`。
- 模块认知：`module Taggable` 通过 `include` 混入实例方法，并使用 `require "json"` 加载标准库。
- 错误处理：自定义异常、`rescue` 处理非法优先级、`ensure` 清理临时文件。

## 运行

```bash
ruby main.rb
```

如果你在仓库根目录，也可以先进入示例目录再运行：

```bash
cd languages/ruby/syntax/examples/syntax-tour
ruby main.rb
```

## 观察点

输出会先打印任务摘要，再打印按状态统计的哈希、去重后的标签数组和 JSON 格式报告。`parse_priority` 会故意收到非法字符串 `"high"`，捕获 `ArgumentError` 后回退到默认优先级；这展示了 Ruby 中常见的“在边界处转换，失败时处理具体异常”的写法。

注意 `Task#status` 使用 `if` 返回最后一个表达式，`priority_label` 使用 `case` 和范围表达多分支。`with_section` 通过 `yield` 执行调用方传入的块，类似许多标准库 API 的结构。脚本最后手动创建临时文件并在 `ensure` 中删除，是为了直接观察清理边界；真实文件读写更常用 `File.open(path) { |file| ... }` 这类块形式 API。

## 修改练习

- 给 `Task` 增加 `estimate_hours` 字段，并用 `sum` 输出总工时。
- 把 `status_counts` 的初始化改成 `Hash.new(0)`，比较和显式键初始化的差异。
- 在任务列表里加入空标题，观察自定义异常 `InvalidTask` 的报错。
- 把 `priority_label` 的范围 `2..3` 改成 `2...3`，确认右边界差异。
- 增加一个模块方法并用 `extend` 挂到单个对象上，比较它和 `include` 的区别。
