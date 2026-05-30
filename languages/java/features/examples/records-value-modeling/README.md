# records-value-modeling

## 目标

这个例子展示 Java `record` 如何用于 value modeling。订单行、金额和订单摘要都被建模为值：它们由字段决定身份，构造后不可变，适合在集合、日志和并发代码中传递。例子还用紧凑构造器检查数量和单价，说明 record 不是“没有规则的数据袋”。

## 运行

```bash
javac Main.java && java Main
```

## 观察点

- 两个字段完全相同的 `LineItem` 会被认为相等，因此放进 `Set` 后只保留一个。
- `record` 自动生成可读的 `toString`，输出适合调试，但真实项目仍要注意敏感字段。
- 构造器中的校验把非法状态挡在对象创建阶段，后续计算就不需要反复检查数量是否为负。
