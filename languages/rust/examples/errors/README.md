# Rust / errors

## 目标

通过一个最小案例观察 Rust 在 `errors` 场景下的惯用写法。

## 运行

```bash
rustc main.rs -o /tmp/rust-example && /tmp/rust-example
```

## 预期输出

输出应包含 `Hello`、`total minutes` 或 `recover` 之一，分别对应最小程序、数据流和错误恢复案例。

## 观察点

- 源文件：`main.rs`
- 版本基线：1.96.x
- 包管理：Cargo
