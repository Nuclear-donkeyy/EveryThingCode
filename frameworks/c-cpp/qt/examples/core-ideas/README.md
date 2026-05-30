# Qt core ideas example

## 目标

这个示例把 `Qt` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

跨平台 GUI 要处理事件循环、控件层级、对象生命周期、信号/槽和平台差异。

## 核心思想到代码

QApplication 管事件循环，QObject 树管理生命周期，signals/slots 解耦事件，moc 扩展元对象能力，CMake AUTOMOC 接入构建。

```cpp
class TaskBoard : public QWidget {
    Q_OBJECT
public:
    explicit TaskBoard(QWidget *parent = nullptr);
};
```

```cpp
QObject::connect(button, &QPushButton::clicked, this, [this] {
    statusLabel->setText("Task completed");
});
```

## 代码位置

- [`CMakeLists.txt`](../quickstart/CMakeLists.txt)
- [`src/main.cpp`](../quickstart/src/main.cpp)

## 运行

先进入 quickstart 目录：

```bash
cd ../quickstart
cmake -S . -B build -DCMAKE_PREFIX_PATH=/path/to/Qt
```

如果本机缺少对应工具链，可以先运行仓库根目录的 dry-run：

```bash
python3 scripts/run_framework_examples.py --dry-run
```

## 观察点

按钮点击不直接调用全局函数，而是通过信号/槽把 UI 事件连接到状态更新。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`Qt` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
