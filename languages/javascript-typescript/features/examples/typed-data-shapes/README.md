# Typed Data Shapes

## 目标

把 TypeScript 的结构化类型思想翻译成可运行的 JavaScript：程序关心的是对象形状是否满足契约，而不是对象来自哪个类。示例同时强调运行时边界：从 JSON 得到的值必须先验证，再进入业务逻辑。

## 运行

```bash
node main.mjs
```

## 观察点

- `parseOrder` 先把 JSON 当作未知运行时值处理，没有假设它已经符合类型。
- `isOrder` 检查字段形状，对应 TypeScript 中 `Order` 接口会描述的结构。
- `summarizeOrder` 只接收验证后的订单对象，业务代码因此可以更直接。
- 修改第二条输入里的字段，例如把 `quantity` 改成字符串，可以观察边界校验如何阻止坏数据继续流动。
