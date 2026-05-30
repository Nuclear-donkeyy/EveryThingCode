# namespaces-autoload-manual

## 目标

用 `namespace`、`use` 和 `spl_autoload_register` 手写一个极小自动加载器，理解 Composer autoload 背后的语言机制。这个例子不依赖 Composer，但模拟了“类名映射到文件路径”的核心思想。

## 特性说明

命名空间解决的是大型 PHP 项目中类名冲突和组织边界的问题。没有 namespace 时，`User`、`Order`、`Logger` 这类名字很容易在不同模块或依赖中撞车；有了 `App\Domain\OrderId`，类名就携带了所在上下文。

自动加载解决的是手写 `require` 的问题。`spl_autoload_register` 会在类第一次被使用但尚未加载时触发回调。Composer 的 PSR-4 自动加载就是在这个机制上建立映射：命名空间前缀对应目录，类名剩余部分对应文件。

## 设计取舍

手写 autoload 能帮助理解原理，但真实项目应该交给 Composer。手写版本容易遗漏边界情况，例如大小写、多个前缀、依赖包路径和性能优化。Composer 的价值不只是少写 `require`，还在于把依赖、版本和自动加载规则统一放进项目元数据。

这个例子把类文件写成临时文件，是为了保持单个 `main.php` 可复制运行。真实项目会把 `OrderId` 放在 `src/Domain/OrderId.php`，并由 Composer 生成 `vendor/autoload.php`。

## 运行

```bash
php main.php
```

## 观察点

- `use App\Domain\OrderId` 让调用处不用写完整命名空间。
- 类第一次被实例化时，autoload 回调才会加载对应文件。
- 输出中的订单号来自被加载的类，说明类定义不是预先手写 require 进来的。
- autoload 是工程组织能力，不是业务逻辑能力。

## 延伸练习

- 把命名空间前缀从 `App\\` 改成 `Learning\\`，同步修改路径映射。
- 新增一个 `App\Service\OrderPrinter` 类，观察 autoload 是否能加载多个类。
- 阅读 Composer 的 PSR-4 配置格式，比较它和这个手写映射的相似处。
