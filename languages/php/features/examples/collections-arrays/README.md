# collections-arrays

## 目标

理解 PHP 数组和对象各自适合的位置。例子把请求中的购物车行项目先当关联数组处理，因为它们来自外部边界；筛选和汇总后，再把有效行转换成 `CartLine` 对象，让核心逻辑使用明确属性和方法。

真实项目中，`CartLine` 通常会放在 `src/Domain/CartLine.php`，再由 Composer 根据 PSR-4 自动加载。这里不引入 Composer，只保留同一个文件，重点观察建模思想。

## 运行

```bash
php main.php
```

## 观察点

- `array_filter` 适合在边界上丢弃无效输入，但过滤条件要写清楚，否则会把业务规则藏在匿名函数里。
- `array_map` 把松散数组转换成对象后，后续代码可以读 `$line->sku`，不用反复记字符串键。
- `array_reduce` 对对象集合求总价，表达的是“对已经验证过的行项目汇总”，而不是继续信任原始请求。
