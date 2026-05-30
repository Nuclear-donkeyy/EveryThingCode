# PHP 基础语法速览

## 读者定位

这份速览面向已经写过 Java、JavaScript、Python、Go、C# 或类似语言，但还没有系统写过 PHP 的读者。PHP 的语法看起来像 C 系语言：花括号、分号、`if`、`switch`、函数和类都很熟悉；真正需要迁移的是它的运行心智。PHP 最初为 Web 页面嵌入而生，现代项目则通常用 Composer、命名空间、自动加载、框架入口和强一些的类型声明来组织。

如果你来自静态类型语言，要把 PHP 理解成“动态语言上叠加了实用的类型护栏”。类型声明能让函数边界更清楚，但数组形状、泛型集合和很多运行时值仍需要靠约定、PHPDoc、静态分析和测试兜住。如果你来自 JavaScript，要注意 PHP 的变量名必须带 `$`，数组同时承担列表和映射角色，字符串插值、相等比较、空值判断和请求生命周期也有自己的坑。

## 运行方式

PHP 文件通常以 `.php` 结尾。纯 PHP 文件以 `<?php` 开头，不需要也不建议写结尾的 `?>`，这样可以避免文件末尾多余空白被提前输出。命令行脚本最小运行方式是：

```bash
php main.php
```

现代 PHP 文件常在开头写：

```php
<?php

declare(strict_types=1);
```

`declare(strict_types=1)` 按文件生效，主要影响标量参数和返回值的类型转换。开启后，把字符串 `"3"` 传给声明为 `int` 的参数会更倾向于暴露错误，而不是悄悄转换。它不是全局开关，也不是完整的运行时类型系统；被哪个文件调用、调用点是否开启 strict types 都会影响标量参数的行为。因此团队项目要统一约定，避免一部分文件严格、一部分文件宽松。

PHP 可以嵌入 HTML，但本章只讨论纯 PHP。真实 Web 项目通常让 `public/index.php` 成为唯一入口，再把请求交给框架或应用内核；业务代码放在 `src/`，依赖和自动加载由 Composer 管理。

## 语法速览

PHP 语句通常以分号结尾，代码块使用花括号。变量名必须以 `$` 开头，例如 `$name`、`$totalPrice`。这不是装饰，而是语法的一部分；函数名、类名、常量名不带 `$`，所以 `$order` 和 `Order` 在视觉上也更容易区分。

```php
$name = "Ada";
$count = 3;
echo "$name has $count tasks\n";
```

文件开头的 `<?php` 告诉解释器后面进入 PHP 代码。纯 PHP 文件省略结束标签是惯例；只有在模板中切回 HTML 时才需要 `?>`。注释可以用 `//`、`#` 或 `/* ... */`。

PHP 的常量可以用 `const` 或 `define`。类内常量和命名空间常量常用 `const`，运行时动态定义才考虑 `define`。变量赋值默认是按值语义，数组赋给另一个变量后修改其中一个通常不会影响另一个；对象变量保存的是对象句柄，多个变量指向同一对象时修改属性会被共享。迁移时不要把 PHP 数组和对象都简单套成“引用”或“复制”，它们的行为不同。

相等比较要格外谨慎。`==` 会做松散转换，`===` 同时比较类型和值。现代业务代码默认使用 `===` 和 `!==`，除非你非常明确地需要 PHP 的转换规则。

## 类型与值

常见基础类型包括 `int`、`float`、`bool`、`string`、`array`、`object`、`null` 和资源类型。函数参数、返回值、类属性都可以写类型：

```php
function total(array $prices): float
{
    return array_sum($prices);
}
```

可空类型写成 `?string`，联合类型写成 `int|float`。`mixed` 表示任意值，适合作为边界上的临时描述，但如果在业务核心到处都是 `mixed`，类型声明就失去了帮助。`void` 表示没有返回值，`never` 表示函数不会正常返回，例如总是抛异常或退出。

字符串有单引号和双引号。单引号几乎不插值，只处理少量转义；双引号会解析变量和常见转义序列：

```php
$user = "Ada";
$message = "Hello, $user\n";
```

复杂表达式建议用拼接、`sprintf` 或先计算变量，而不是把太多逻辑塞进字符串。面向 HTML、SQL、shell 或 JSON 时不要手写转义；优先使用模板引擎转义、PDO 参数绑定、`escapeshellarg`、`json_encode` 等对应 API。

PHP 的 truthy/falsy 规则和其他动态语言不完全一样。`false`、`0`、`0.0`、空字符串、字符串 `"0"`、空数组和 `null` 都是假值。特别是 `"0"` 为假经常让表单、配置和 ID 判断出错。需要区分缺失和空值时，用 `array_key_exists`、`isset`、`=== null` 或更明确的验证逻辑。

## 控制流

`if` / `elseif` / `else` 是基本分支。条件表达式不要求是布尔值，但惯用代码会尽量让条件本身表达清楚，避免依赖松散转换。

```php
if ($score >= 90) {
    $grade = "A";
} elseif ($score >= 60) {
    $grade = "pass";
} else {
    $grade = "retry";
}
```

`switch` 使用松散比较，这和很多语言的 `switch` 不同。如果 case 值可能来自用户输入或混合类型，优先考虑 `match` 表达式；`match` 使用严格比较、必须覆盖或提供 `default`，并返回一个值。不过 `switch` 仍常见于兼容旧版本或需要贯穿复杂语句的代码，写它时要留意 `break`。

循环包括 `for`、`while`、`do while` 和最常用的 `foreach`。PHP 数组既可以是列表也可以是映射，所以 `foreach` 有两种常见形式：

```php
foreach ($names as $name) {
    echo $name;
}

foreach ($scores as $name => $score) {
    echo "$name: $score";
}
```

`foreach` 默认按值遍历。按引用遍历需要 `&$value`，但容易留下引用变量污染后续逻辑，入门阶段尽量避免。需要过滤、映射和求和时，可以用普通循环，也可以用 `array_map`、`array_filter`、`array_reduce`；当转换逻辑超过一两行，普通循环往往更可读。

## 函数与模块

函数用 `function` 定义，参数默认值、类型和返回类型都写在签名上：

```php
function formatPrice(float $amount, string $currency = "USD"): string
{
    return sprintf("%s %.2f", $currency, $amount);
}
```

PHP 函数没有强制 `return`，但声明了返回类型后必须返回兼容值。参数默认值需要是常量表达式。数组和对象传参的表现不同：数组修改通常不会影响调用方，除非显式按引用传参；对象属性修改会影响同一个对象。按引用参数写作 `function fill(array &$items): void`，它是很强的信号，应该少用并清楚说明副作用。

PHP 的模块化核心是命名空间和 Composer 自动加载。文件可以声明命名空间：

```php
namespace App\Service;

use App\Model\Order;
use RuntimeException;
```

`namespace` 给类、函数和常量一个逻辑前缀，避免全局名字冲突。`use` 只是导入名字或设置别名，不会像某些语言那样执行模块加载逻辑。现代项目一般在 `composer.json` 中配置 PSR-4 自动加载，把 `App\` 映射到 `src/`；代码里引用 `App\Service\Checkout` 时，Composer 的 autoloader 根据类名找到对应文件。心智模型是“类名到文件路径的约定映射”，不是到处手写 `require`。

## 集合与数据建模

PHP 的 `array` 是有序映射，可以同时当列表和字典：

```php
$list = ["draft", "review", "done"];
$map = ["draft" => 2, "done" => 5];
```

当键是连续整数时，它像列表；当键是字符串或非连续整数时，它像映射。混用两种形态会让 JSON 编码、遍历和静态分析变得别扭。团队中通常会用变量名、PHPDoc 或专门值对象表达意图，例如 `$users` 是列表，`$usersById` 是映射。

数据建模不应全靠关联数组。现代 PHP 支持构造器属性提升、只读属性和只读类，适合表达不可随意改动的 value object：

```php
readonly class Money
{
    public function __construct(
        public int $cents,
        public string $currency,
    ) {}
}
```

`readonly` 表示属性初始化后不能再被重新赋值，能减少“对象创建后被远处代码改坏”的风险。它不是深度不可变：如果只读属性里放的是可变对象，对象内部仍可能改变。值对象通常还会在构造器中校验不变量，例如金额不能为负、币种不能为空。

类使用 `class`，对象用 `new` 创建，成员访问用 `->`，静态成员和类常量用 `::`。构造器名固定为 `__construct`。PHP 没有内建泛型，复杂集合常写 PHPDoc，例如 `/** @var list<Money> $prices */`，再交给 PHPStan 或 Psalm 检查。

## 错误处理

现代 PHP 的可捕获顶层接口是 `Throwable`，它下面主要有 `Exception` 和 `Error`。业务规则失败通常抛 `InvalidArgumentException`、`DomainException`、`RuntimeException` 或自定义异常；类型错误、调用不存在方法等通常属于 `Error` 体系。

```php
try {
    $price = parsePrice($input);
} catch (InvalidArgumentException $error) {
    $price = null;
} finally {
    // release resources here
}
```

`try` / `catch` / `finally` 应该围绕真正能恢复的边界。不要把大段业务代码全包进 `catch (Throwable $e)` 后静默继续，那会隐藏程序错误。Web 应用里通常让框架统一捕获异常、记录日志并转换成 HTTP 响应；业务层只负责抛出有语义的异常。

PHP 仍有传统错误、警告和通知。现代版本中很多致命问题已经变成 `Error`，但标准库函数仍可能通过返回 `false` 表示失败。处理这类 API 时要用严格比较检查 `false`，不要写 `if (!$result)` 把合法的 `0`、空字符串或空数组误判为失败。

## 惯用写法

现代 PHP 的惯用写法不是把脚本零散 `include` 到一起，而是围绕 Composer、PSR 规范和清晰边界组织：

- 每个纯 PHP 文件以 `<?php` 开头，通常紧跟 `declare(strict_types=1);`。
- 变量用 `$camelCase`，类名用 `PascalCase`，常量多用 `UPPER_SNAKE_CASE` 或类常量。
- 默认使用 `===`、`!==`，避免松散比较和隐式转换。
- 用 `foreach` 直接遍历数组；需要键和值时写 `$key => $value`。
- 用 `DateTimeImmutable` 处理时间，避免共享可变日期对象。
- 用值对象和 DTO 承载结构化数据，不要让大型关联数组穿透整个系统。
- 用 Composer autoload 组织类文件，避免在业务代码里散落 `require_once`。
- 在边界校验输入，在核心代码里依赖清晰类型和不变量。

Composer 的心智很重要：`composer.json` 声明依赖、平台约束、脚本和 autoload；`composer.lock` 固定解析后的版本；`vendor/autoload.php` 注册自动加载器。框架项目通常只在入口文件引入一次 autoload，然后类按命名空间自动解析。学习基础语法时可以只跑单文件脚本，但进入真实项目后，要尽早理解 `composer install`、PSR-4 和 `vendor/` 的职责。

## 可运行示例

本章示例位于：

- [syntax-tour](examples/syntax-tour/)：一个订单行汇总脚本，演示 `<?php`、`strict_types`、`$` 变量、基础类型、字符串、`if` / `switch` / `foreach`、函数、数组、`readonly class` value object、命名空间、`use` 和异常恢复。

运行：

```bash
cd languages/php/syntax/examples/syntax-tour
php main.php
```

示例只使用标准库。它故意保持在一个文件里，方便观察语法组合；真实项目会把类放到 `src/`，通过 Composer autoload 按命名空间加载。

## 学习检查

读完并运行示例后，可以用这些问题确认自己是否抓住了 PHP 的迁移重点：

- 为什么纯 PHP 文件通常省略结尾的 `?>`？
- `declare(strict_types=1)` 解决了什么问题，又为什么不能替代完整校验？
- `$order`、`Order`、`ORDER_STATUS` 在 PHP 里分别可能代表什么？
- 为什么业务代码默认应该用 `===` 而不是 `==`？
- PHP 中字符串 `"0"` 在条件判断里有什么特别之处？
- `foreach ($items as $key => $value)` 适合什么数组形态？
- `switch` 和 `match` 在比较规则上有什么差异？
- 什么时候用关联数组就够了，什么时候应该建 value object 或 class？
- `namespace`、`use` 和 Composer autoload 各自负责什么？
- 捕获 `Throwable`、`Exception` 和具体业务异常的边界应该如何选择？
