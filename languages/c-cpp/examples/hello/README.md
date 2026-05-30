# C / C++ / hello

## 目标

通过一个最小案例观察 C / C++ 在 `hello` 场景下的惯用写法。

## 运行

```bash
c++ -std=c++23 main.cpp -o /tmp/cpp-example && /tmp/cpp-example
```

## 预期输出

输出应包含 `Hello`、`total minutes` 或 `recover` 之一，分别对应最小程序、数据流和错误恢复案例。

## 观察点

- 源文件：`main.cpp`
- 版本基线：C23 / C++23
- 包管理：CMake / Conan / vcpkg
