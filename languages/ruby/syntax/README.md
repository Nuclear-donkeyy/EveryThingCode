# Ruby 基础语法速览

## 读者定位

这份速览面向已经写过 JavaScript、Python、Java、Go、C# 或类似语言，但第一次系统接触 Ruby 的读者。Ruby 的语法看起来像脚本语言，核心心智模型却是“给对象发送消息”：数字、字符串、数组、类本身甚至 `nil` 都是对象，运算符也多半是方法调用的语法糖。你写 `user.name`、`items.size`、`3.times` 时，本质都是对象响应某个方法。

Ruby 是动态类型语言，不会在变量声明处固定类型。它更依赖 duck typing：对象能不能完成某件事，取决于它是否响应需要的方法，而不是它在声明上属于哪个接口。迁移时不要急着寻找接口关键字或泛型约束，先关注小对象、清楚命名、测试和边界校验。Ruby 的“魔法”通常来自块、开放类、模块混入和动态派发的组合，理解这些机制后，Rails、RSpec、Rake 的 DSL 会更容易读懂。

## 运行方式

Ruby 源文件通常以 `.rb` 结尾。最小运行方式是：

```bash
ruby main.rb
```

本章示例只使用标准库，不需要 `Gemfile` 或第三方 gem。真实项目通常会用 Bundler 管理依赖，并通过 `bundle exec ruby ...` 或框架命令固定运行环境。Ruby 文件被 `require` 时会执行顶层代码，所以可复用文件应把主要逻辑放进方法、类或模块里，并用下面的入口判断保护脚本执行：

```ruby
if __FILE__ == $PROGRAM_NAME
  main
end
```

`__FILE__` 是当前文件路径，`$PROGRAM_NAME` 是启动脚本路径。这个判断类似 Python 的 `if __name__ == "__main__"`：文件被直接运行时执行 `main`，被其他文件 `require` 时只加载定义。

## 语法速览

Ruby 不用分号结束语句，换行通常就是语句边界。代码块用关键字和 `end` 包起来，例如 `if ... end`、`class ... end`、`def ... end`。方法调用的括号很多时候可以省略，但工程代码里建议在参数复杂或会产生歧义时写上括号，让读者少猜。

变量无需声明。Ruby 通过名字形态区分变量种类：`name` 是局部变量或方法调用，`@name` 是实例变量，`@@name` 是类变量，`$name` 是全局变量，`Name` 或 `NAME` 开头的是常量。常量不是绝对不可变，重新赋值会警告；它更多是团队约定和命名信号。

Ruby 的顶层表达式也会被执行，方法最后一个表达式默认作为返回值：

```ruby
def greeting(name)
  "Hello, #{name}"
end
```

这段代码没有显式 `return`，但会返回字符串。显式 `return` 常用于提前退出；如果每个方法末尾都写 `return`，会显得不太 Ruby。

注释使用 `#`。符号 `:ready` 是 Ruby 的常见轻量标识值，常用作哈希键、状态名和方法选项；它不是字符串，但可以按需转换。许多 Ruby API 喜欢返回 `nil` 表示“没有值”，而不是抛异常；因此调用链和空值边界要写清楚。

## 类型与值

Ruby 常见基础值包括 `Integer`、`Float`、`String`、`Symbol`、`true`、`false` 和 `nil`。注意 Ruby 只有 `false` 和 `nil` 是假值，数字 `0`、空字符串 `""`、空数组 `[]` 都是真值。这一点和 JavaScript、Python、PHP 很不同，迁移时不要用 `if items` 判断数组是否为空，应写 `if items.empty?` 或 `unless items.empty?`。

字符串有单引号和双引号。单引号基本只处理少量转义，双引号支持插值和更多转义：

```ruby
name = "Ada"
score = 98.5
message = "#{name} scored #{score.round(1)}"
```

`#{...}` 中可以放表达式。插值适合生成面向人的文本；拼 SQL、shell 命令或协议内容时仍应使用参数化 API，避免把转义问题藏进模板。字符串默认可变，`upcase` 返回新字符串，`upcase!` 这类带 `!` 的方法通常表示可能修改接收者或带有更强副作用。`!` 不是语法规则强制，只是 Ruby 社区非常重要的命名约定。

常量用大写开头，常见写法是 `DEFAULT_LIMIT = 10`。数组和哈希赋给常量后，引用本身不应重新绑定，但对象内容仍可能被改动；需要更强保护时可使用 `freeze`。Ruby 变量保存的是对象引用，给另一个变量赋值不会复制对象：

```ruby
tags = ["ruby"]
alias_tags = tags
alias_tags << "syntax"
# tags 现在也是 ["ruby", "syntax"]
```

## 控制流

`if` / `elsif` / `else` 是基本条件分支，注意 Ruby 写 `elsif`，不是 `elseif` 或 `elif`。条件表达式本身会返回值，因此常见写法是把分支结果赋给变量：

```ruby
label =
  if done
    "done"
  elsif urgent
    "urgent"
  else
    "open"
  end
```

`unless` 表示“如果不”，适合短条件，例如 `return if name.empty?` 或 `puts "missing" unless found`。复杂否定条件不要硬塞进 `unless`，否则读者需要在脑中反转逻辑。

`case` 常用来替代多段等值判断，也能配合范围、正则和类匹配：

```ruby
case priority
when 1
  "low"
when 2..3
  "normal"
else
  "high"
end
```

集合遍历优先使用迭代器和块，而不是手写索引循环。`each` 做副作用遍历，`map` 做转换，`select` 做过滤，`reduce` / `sum` 做汇总。`for item in items` 也存在，但 Ruby 社区更常用 `items.each do |item| ... end`，因为它和 Enumerable 方法链保持一致。

循环控制有 `break`、`next` 和 `redo`。`next` 类似其他语言的 `continue`。范围 `1..3` 包含右边界，`1...3` 不包含右边界，边界差异常出现在下标和分页逻辑里。

## 函数与模块

Ruby 用 `def` 定义方法。顶层 `def` 实际会定义在 `Object` 的私有方法上；项目代码更常把方法放进类或模块，避免污染全局语义。参数可以有默认值、关键字参数和可变参数：

```ruby
def format_task(title, owner: "team", done: false)
  status = done ? "done" : "open"
  "#{title} (#{owner}, #{status})"
end
```

Ruby 的块是理解语言的关键。方法可以接收一个临时代码块，用 `yield` 调用它，或者用 `&block` 把它转成对象：

```ruby
def around(label)
  puts "start #{label}"
  result = yield
  puts "end #{label}"
  result
end
```

调用时可写 `{ ... }` 或 `do ... end`。单行表达式常用花括号，多行块常用 `do ... end`。块是闭包，可以读取外层局部变量。许多 Ruby API 的资源管理和 DSL 都依赖块，例如 `File.open(path) { |file| ... }` 会在块结束后自动关闭文件。

模块 `module` 有两种常见用途：命名空间和 mixin。作为命名空间时，它把相关类、常量、方法放在同一前缀下；作为 mixin 时，`include` 把模块实例方法加入类的实例，`extend` 把模块方法加入某个对象或类本身。Ruby 没有传统接口语法，模块和 duck typing 一起承担了“共享行为”和“协议约定”的角色。

`require` 用来加载标准库、gem 或项目文件。加载标准库时写 `require "json"`；加载相对当前文件的本地文件常用 `require_relative "helper"`。`require` 通常只加载一次，`load` 每次都会重新执行，入门阶段优先使用 `require` / `require_relative`。

## 集合与数据建模

数组 `Array` 是有序、可变集合。常用操作包括 `<<` 追加、`first` / `last` 取元素、`each` 遍历、`map` 转换、`select` 过滤、`compact` 去掉 `nil`。Ruby 方法名常用问号表达谓词，例如 `empty?`、`include?`、`nil?`；问号同样是命名约定，不是布尔返回的强制检查。

哈希 `Hash` 是键值映射，现代 Ruby 保持插入顺序。符号键很常见：

```ruby
task = { title: "Read guide", priority: 2, done: false }
puts task[:title]
```

`{ title: "Read guide" }` 是 `{ :title => "Read guide" }` 的简写。访问缺失键默认返回 `nil`，这很方便，也可能隐藏拼写错误；当缺失代表程序错误时，可以用 `fetch(:title)` 让错误显式暴露，或提供默认值 `fetch(:owner, "team")`。

简单数据建模可以先用类。`initialize` 是构造方法，实例变量以 `@` 开头，`attr_reader` / `attr_accessor` 用来生成读取或读写方法：

```ruby
class Task
  attr_reader :title, :priority

  def initialize(title, priority:)
    @title = title
    @priority = priority
  end
end
```

Ruby 类是开放的，同一个类可以在多个地方继续添加方法。这让扩展非常灵活，也让全局猴子补丁有风险。应用代码应谨慎修改核心类，优先用自己的类、模块或 refinements 限定影响范围。

## 错误处理

Ruby 使用异常表达失败，基本结构是 `begin` / `rescue` / `ensure`。`rescue` 默认捕获 `StandardError` 及其子类，不会捕获所有系统级异常。惯用做法是捕获自己能处理的具体异常，补充上下文后返回默认值或重新抛出：

```ruby
def parse_priority(raw)
  Integer(raw)
rescue ArgumentError
  1
end
```

`ensure` 无论是否发生异常都会执行，适合释放锁、关闭连接、清理临时状态。不过 Ruby 标准库和许多 gem 提供块形式 API，把清理逻辑封装好了：

```ruby
File.open("report.txt", "w") do |file|
  file.puts "hello"
end
```

这比手写 `file = File.open(...)` 加 `ensure file.close` 更不容易漏掉边界。自定义异常通常继承 `StandardError`，例如 `class InvalidTask < StandardError; end`。不要随手 `rescue Exception`，那会吞掉中断、退出等不应被业务代码处理的信号。

## 惯用写法

Ruby 代码通常追求“读起来像在描述对象和业务动作”。常见惯用写法包括：

- 用 `each`、`map`、`select`、`sum` 处理集合，少写手动索引循环。
- 用 `?` 结尾命名谓词方法，例如 `done?`、`valid?`。
- 用 `!` 结尾提醒调用方这个方法更危险、会修改对象或失败方式更强，例如 `save!`、`sort!`。
- 用 `nil` 表达缺失值，但在边界处用 `fetch`、显式校验或异常避免静默失败。
- 用块形式 API 管理资源和表达流程包装。
- 用 `module` 提取共享行为，用组合和 mixin 替代过深继承。
- 用 `require_relative` 加载本地文件，用 Bundler 管理外部 gem。

Ruby 社区也偏好小而清楚的方法。由于最后一个表达式会返回值，方法常可以写得很短；但不要为了“像 DSL”而省略所有括号或堆叠元编程。可读的 Ruby 往往是动态能力和明确边界的平衡：对象协议灵活，错误和资源边界清楚，集合转换一眼能看懂。

## 可运行示例

本章示例位于：

- [syntax-tour](examples/syntax-tour/)：一个任务汇总脚本，演示变量和常量、字符串插值、`if` / `case` / `each`、方法与块、数组和哈希、类、模块 mixin、`require` 标准库、异常和 `ensure`。

运行：

```bash
cd languages/ruby/syntax/examples/syntax-tour
ruby main.rb
```

示例只使用 Ruby 标准库。它故意把语法组合放在一个文件里，便于第一次阅读时从上到下观察 Ruby 的对象模型、块和集合风格。

## 学习检查

读完并运行示例后，可以用这些问题确认自己是否掌握了迁移重点：

- 为什么说 Ruby 中运算符和属性访问多半也是方法调用？
- `false`、`nil`、`0`、`""`、`[]` 在条件判断中分别是真还是假？
- 局部变量、实例变量和常量如何从名字上区分？
- 双引号字符串插值 `#{...}` 适合什么场景，什么场景应避免直接拼接？
- `each`、`map`、`select` 和 `sum` 的意图分别是什么？
- 方法最后一个表达式默认返回值会怎样影响代码风格？
- `include` 和 `extend` 在模块 mixin 中有什么区别？
- 什么时候使用 `require`，什么时候使用 `require_relative`？
- 为什么 `ensure` 和块形式资源 API 能减少泄漏风险？
