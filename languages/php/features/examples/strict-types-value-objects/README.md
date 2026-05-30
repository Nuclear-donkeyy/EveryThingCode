# strict-types-value-objects

## 目标

理解 `declare(strict_types=1)`、参数/返回类型和值对象如何一起工作。例子用 `Money` 表示金额：类型签名负责拦截错误参数，构造函数负责保护业务不变量，例如金额不能为负、货币代码必须是三位大写字母。

## 运行

```bash
php main.php
```

## 观察点

- 正常路径会输出订单小计，说明核心函数只接收明确的对象和值。
- 字符串 `"2"` 传给 `int $quantity` 时会触发 `TypeError`，这是 `strict_types=1` 对标量参数的影响。
- 负金额会触发 `InvalidArgumentException`，说明类型系统能说明“这是整数”，但业务规则仍需要值对象自己校验。
