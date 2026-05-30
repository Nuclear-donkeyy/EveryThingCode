# C# / .NET / data-flow

## 目标

通过一个最小案例观察 C# / .NET 在 `data-flow` 场景下的惯用写法。

## 运行

```bash
dotnet new console --force && dotnet run
```

## 预期输出

输出应包含 `Hello`、`total minutes` 或 `recover` 之一，分别对应最小程序、数据流和错误恢复案例。

## 观察点

- 源文件：`Program.cs`
- 版本基线：.NET 10.0.8 LTS
- 包管理：NuGet
