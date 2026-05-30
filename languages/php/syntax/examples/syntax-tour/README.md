# PHP syntax-tour

## 目标

这个示例用一个小型订单行汇总脚本串起 PHP 的基础语法。读者可以看到 `<?php` 文件入口、`declare(strict_types=1)`、带 `$` 的变量、基础类型、字符串插值、条件分支、`switch`、`foreach`、函数、数组、只读 value object、命名空间导入和异常恢复如何放在同一个标准库脚本里。它不是框架项目，也不依赖 Composer 包；重点是先建立现代 PHP 的语法和运行心智。

## 覆盖语法

- 文件结构：纯 PHP 文件以 `<?php` 开头，不写结束标签，并启用 `strict_types`。
- 变量与常量：`$customerName`、`$lineItems`、`TAX_RATE` 展示变量、局部常量和命名规则。
- 基础类型与字符串：`int`、`float`、`bool`、`string`、`null`、双引号插值和 `sprintf` 格式化。
- 控制流：`if` / `elseif` / `else` 判断折扣等级，`switch` 生成状态文案，`foreach` 遍历列表和映射。
- 函数：带参数类型、返回类型、默认参数和异常抛出的普通函数。
- 集合：列表式数组保存订单行，关联数组按品类汇总金额。
- 数据建模：`readonly class LineItem` 表达不可随意改写的订单行，并在构造器里维护不变量。
- 错误处理：`try` / `catch` 捕获非法数量，恢复成默认赠品行。
- 模块认知：`namespace SyntaxTour;` 和 `use InvalidArgumentException;` 展示命名空间与导入的最小用法。

## 运行

```bash
php main.php
```

如果你在仓库根目录，也可以先进入示例目录再运行：

```bash
cd languages/php/syntax/examples/syntax-tour
php main.php
```

## 观察点

输出会先打印客户名、订单状态、税率和折扣等级，再列出每个订单行、按品类汇总的小计，以及从异常中恢复出的赠品行。`parseQuantity` 故意收到非法字符串 `"two"`，函数会抛出 `InvalidArgumentException`，调用方只在能恢复的边界捕获它，并把数量改成安全默认值。

注意 `LineItem` 是 `readonly class`：构造完成后不能再给它的属性重新赋值，这让订单行更接近 value object。示例里的数组仍然是可变集合，所以可以向 `$lineItems` 追加新的 `LineItem`。这正好体现了 PHP 的常见分层：集合负责组织一批值，对象负责保护单个业务值的不变量。

还可以观察 `foreach ($totalsByCategory as $category => $subtotal)` 的键值遍历。PHP 的 `array` 既能当列表，也能当映射；示例用 `$lineItems` 表达列表，用 `$totalsByCategory` 表达映射，避免在同一个数组里混合两种形态。

## 修改练习

- 给 `LineItem` 增加 `$discountable` 布尔字段，并让不可打折的品类跳过折扣。
- 把 `statusLabel` 的 `switch` 改成 `match` 表达式，比较严格比较和必须覆盖分支带来的差异。
- 把 `"two"` 改成 `"0"`，观察构造器的不变量校验如何继续阻止非法数量。
- 新增一个按 SKU 查找订单行的关联数组，练习 `foreach` 和 `$key => $value`。
- 尝试删除 `declare(strict_types=1);`，再把函数参数传成字符串数字，观察类型行为是否符合你的预期。
