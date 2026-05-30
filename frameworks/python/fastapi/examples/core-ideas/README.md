# FastAPI core ideas example

## 目标

这个示例把 `FastAPI` 的核心思想落实到 quickstart 的真实代码上。阅读顺序是：先看框架解决了什么问题，再看代码如何承载这个思想，最后运行 quickstart 观察行为。

## 对应的问题

手写 API 容易出现校验重复、文档漂移、序列化不一致和依赖污染。

## 核心思想到代码

类型标注定义 API 契约，Pydantic 负责校验和序列化，Depends 管理依赖，OpenAPI 自动生成文档。

```python
class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
```

```python
@app.post("/books", response_model=BookRead, status_code=201)
def create_book(input: BookCreate, repository: Annotated[BookRepository, Depends(get_repository)]):
    return repository.create(input)
```

## 代码位置

- [`main.py`](../quickstart/main.py)
- [`tests/test_main.py`](../quickstart/tests/test_main.py)

## 运行

先进入 quickstart 目录：

```bash
cd ../quickstart
python3 -m py_compile main.py tests/test_main.py
```

如果本机缺少对应工具链，可以先运行仓库根目录的 dry-run：

```bash
python3 scripts/run_framework_examples.py --dry-run
```

## 观察点

修改 `BookCreate` 字段约束会同时影响运行时校验和 OpenAPI schema。

## 修改练习

- 改动一个路由、组件或 handler，观察测试或 smoke 是否能暴露结构变化。
- 把示例中的内存数据替换成更真实的数据来源，保持入口层代码尽量稳定。
- 在 quickstart README 的 `代码讲解` 中反向定位这里的代码片段，确认每段思想都有源码对应。

## 验收

完成后你应该能用自己的话说明：`FastAPI` 解决了什么重复问题；它的核心抽象在 quickstart 的哪些文件中出现；如果项目变大，哪些代码应该保留在入口层，哪些应该移动到业务或数据边界。
