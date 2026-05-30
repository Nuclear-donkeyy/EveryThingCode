# linq-data-flow

## 目标

把一组报名事件转换成课程报表，观察 LINQ 如何把过滤、分组、排序、投影和聚合连接成声明式数据流。例子也刻意打印一次枚举次数，用来提醒 LINQ 查询通常是延迟执行的。

## 运行

```bash
cd languages/csharp-dotnet/features/examples/linq-data-flow && dotnet run
```

## 观察点

- 查询变量 `activeCourseSummaries` 描述的是转换流程，不是立即生成好的列表。
- `Where`、`GroupBy`、`Select` 和 `OrderByDescending` 让代码强调“要什么结果”。
- `ToList()` 是真正执行查询的位置；如果不缓存，多次枚举可能重复计算。
