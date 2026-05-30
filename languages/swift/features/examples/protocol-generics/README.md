# Protocols and Generics

## 目标

这个例子展示 Swift 如何用协议描述能力，用泛型复用算法。`Scorable` 只要求一个值能提供标题和分数；`topItem` 不关心具体类型是任务还是课程，只关心元素满足这个能力。

协议让调用方表达需要什么，泛型让函数保留具体类型。这样既能复用逻辑，又不用把所有模型塞进同一个父类。

## 特性说明

Swift 的协议不是只为面向对象继承服务的接口。它更像能力边界：只要一个类型能提供 `title` 和 `score`，它就可以声明符合 `Scorable`。`TaskCard` 和 `Lesson` 的领域含义不同、字段也不同，但它们都能参与同一个评分算法，因为算法真正需要的只是“可评分”这个能力。

泛型把这个能力边界写进函数签名。`topItem<T: Scorable>(from items: [T]) -> T?` 表示：给我一组同一种具体类型的可评分值，我会返回同一种具体类型的最高分项，或者在数组为空时返回 `nil`。调用方拿回 `TaskCard?` 时仍能访问 `owner`，拿回 `Lesson?` 时仍能访问 `durationMinutes`。这就是泛型和把所有东西塞进 `Any` 或父类数组的区别。

如果不用协议和泛型，代码常见退化有两种：一种是为任务、课程、商品分别复制一份 `topTask`、`topLesson`、`topProduct`；另一种是使用字典、元组或 `Any` 抹掉类型，再用字符串键和强制转换拼回信息。前者重复，后者把编译期错误推迟到运行时。Swift 的方案是让抽象仍然保持类型信息。

## 设计取舍

协议和泛型的收益是复用边界清楚、调用方类型不丢失、编译器能检查约束。`Array where Element: Scorable` 的扩展也展示了 Swift 的一个重要设计：算法可以挂在“满足某种能力的集合”上，而不是污染所有数组。

代价是泛型过多会让错误信息变长，也会增加 API 设计成本。不是所有抽象都值得变成协议；如果只有一个具体类型，直接写具体类型通常更清楚。如果你需要把不同具体类型混放在同一个数组里，可能要使用 `any Scorable`，但那会丢失部分静态类型信息。这个例子选择泛型，是因为每次处理的数组元素类型一致，而且调用方需要拿回原来的具体类型。

## 运行

```bash
swift main.swift
```

## 观察点

- `TaskCard` 和 `Lesson` 没有共同父类，但都满足 `Scorable`，因此都能传给 `topItem`。
- `topItem<T: Scorable>` 返回的仍是 `T?`，调用方拿回的是原来的具体类型，而不是丢失信息的通用容器。
- `Array where Element: Scorable` 的扩展只对满足协议约束的数组开放，算法边界写在类型系统里。
- 输出中的 `Top task` 能继续打印 `owner`，`Top lesson` 能继续打印 `durationMinutes`，这验证了泛型没有抹掉具体类型。

## 延伸练习

- 新增一个 `BookReview` 结构体，让它符合 `Scorable`，然后直接复用 `topItem` 和 `averageScore`。
- 把 `topItem` 改成接收 `[any Scorable]`，观察返回值还能不能保留 `owner` 或 `durationMinutes`。
- 给 `Scorable` 增加一个默认实现，例如 `var label: String { "\(title): \(score)" }`，体会协议扩展如何复用行为。
- 把 `score` 从 `Int` 改成 `Double`，观察需要修改哪些类型和算法签名。
