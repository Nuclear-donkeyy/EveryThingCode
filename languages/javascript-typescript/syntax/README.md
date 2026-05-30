# JavaScript / TypeScript 基础语法速览

## 读者定位

这份速览面向已经写过至少一门编程语言，但第一次系统接触 JavaScript / TypeScript 的读者。你可以把 JavaScript 理解为“对象和函数都很轻量、运行时很动态、异步 I/O 很常见”的语言；TypeScript 则是在 JavaScript 之上增加开发期类型检查，但不会改变最终运行时行为。

迁移时最重要的心智分离是：JS 决定代码真的怎么跑，TS 决定编辑器和编译器在运行前能帮你发现多少问题。`type`、`interface`、泛型、类型标注最后都会被擦除，来自 JSON、环境变量、表单、数据库的数据仍然需要运行时校验。

## 运行方式

本仓库的语法示例使用 Node.js 的 ES Module：

```bash
cd languages/javascript-typescript/syntax/examples/syntax-tour
node main.mjs
```

`.mjs` 文件默认按 ESM 运行，可以直接写 `import` / `export`。在真实项目里也常见 `.js` 配合 `package.json` 的 `"type": "module"`，或 `.ts` 交给 TypeScript 工具链编译后再运行。入门阶段先把运行时的 JavaScript 语义跑清楚，再补 TypeScript 配置会更稳。

## 语法速览

现代 JS/TS 代码的基础形状通常是：用 `const` 声明不会重新绑定的名字，用 `let` 声明会重新绑定的名字；用对象字面量和数组表达数据；用函数和箭头函数组织行为；用 `import` / `export` 拆分模块；用 `Promise`、`async`、`await` 表达异步结果。

和许多静态语言不同，JavaScript 的变量名本身没有固定类型，值才有类型。同一个 `let value` 可以先指向字符串再指向数字，虽然这通常不利于维护。TypeScript 的类型系统会尽量约束这种变化，但它约束的是源码，不是已经运行的进程。

## 类型与值

JavaScript 的基础值包括 `number`、`bigint`、`string`、`boolean`、`symbol`、`undefined`、`null`，其他大多是对象。数组、函数、日期、正则、Map、Set 都属于对象体系。`typeof null` 返回 `"object"` 是历史包袱，不要用它判断空值。

`let` 和 `const` 都是块级作用域。`const` 只表示“绑定不可重新赋值”，不表示对象深度不可变：

```js
const user = { name: "Ada" };
user.name = "Grace"; // 可以，变的是对象内容
// user = {}          // 不可以，变的是绑定
```

TypeScript 的常见心智是“给边界加约束，让内部靠推断”。例如函数参数、API 响应、公共对象结构适合写类型；局部变量往往让 TS 自动推断即可。`unknown` 表示“我还不知道类型，使用前要收窄”，`any` 表示“关闭检查”，迁移项目时宁愿多用 `unknown`，少用 `any`。

模板字符串用反引号包裹，支持插值和多行文本：`` `hello ${name}` ``。插值会调用值的字符串化逻辑，适合日志和展示；构造 SQL、Shell 命令或 HTML 时仍要使用对应的安全 API，不能把模板字符串当成自动转义。

## 控制流

`if` / `else`、`switch`、`for`、`while` 都存在，但现代 JS 更常见 `for...of` 遍历可迭代对象：

```js
for (const item of items) {
  console.log(item);
}
```

`for...in` 遍历对象键名，容易误用于数组；数组遍历优先用 `for...of` 或数组方法。`switch` 默认会向下穿透，除非 `break`、`return` 或 `throw`，所以多个分支合并时要明确写出来。条件判断里 `0`、`""`、`false`、`null`、`undefined`、`NaN` 都是假值；不要用简单的 truthy 判断替代业务上对“空字符串”和“缺失”的区分。

TS 会根据控制流做类型收窄。例如先判断 `typeof value === "string"`，后续分支里就能按字符串使用。这个能力很像把运行时检查变成类型信息，但前提是你真的写了检查。

## 函数与模块

函数是一等值，可以赋给变量、作为参数传入，也可以作为返回值。普通函数声明会提升，箭头函数通常作为表达式使用：

```js
function double(n) {
  return n * 2;
}

const triple = (n) => n * 3;
```

箭头函数没有自己的 `this`，这让它很适合回调和数组方法；需要对象方法动态接收调用者时，普通方法语法更清晰。参数可以有默认值，返回多个值通常用对象或数组，并配合解构。

ES Module 用静态 `import` / `export` 组织文件。命名导出适合工具函数和多个能力，默认导出适合一个文件只有一个主要概念。模块有自己的作用域，顶层变量不会自动挂到全局。`import` 会被提前解析，因此路径、扩展名、ESM/CJS 兼容是 Node 项目里常见的第一批坑。

## 集合与数据建模

数组用于有序列表，对象字面量用于轻量记录，`Map` 适合任意键或频繁增删的映射，`Set` 适合去重和成员关系。对象属性访问有点号和方括号两种：`user.name` 适合固定属性，`user[field]` 适合动态键。

对象和数组常与展开语法配合，形成“复制并修改”的风格：

```js
const nextUser = { ...user, active: true };
const nextItems = [...items, newItem];
```

这只是浅拷贝，嵌套对象仍然共享引用。TS 中常用 `type` 或 `interface` 描述对象形状。它是结构化类型系统：只要属性形状匹配，就不要求显式继承同一个类。这对 JSON 风格数据非常自然，也意味着“名字相同但语义不同”的结构要靠更明确的字段、品牌类型或封装来区分。

解构是 JS/TS 的高频写法：`const { id, name } = user` 从对象取字段，`const [first] = items` 从数组取位置。它能减少样板代码，但不要在函数签名里解构过深，否则调用方很难看出需要传什么。

## 错误处理

同步错误用 `throw` 抛出，用 `try...catch...finally` 捕获和清理。推荐抛 `Error` 或自定义错误对象，不要抛字符串，因为堆栈、`cause` 和错误分类都会变差。

异步错误通常藏在 `Promise` 里。`async` 函数总是返回 Promise；在其中 `throw` 会变成 rejected Promise，`return` 会变成 resolved Promise。调用时要么 `await` 并在边界 `try...catch`，要么返回 Promise 让上层处理。常见误解是“调用了异步函数就已经捕获错误”，但如果忘记 `await`，外层 `try...catch` 捕不到后续 rejection。

对业务上可预期的失败，也可以返回 `{ ok: true, value }` / `{ ok: false, error }` 这样的 Result 风格对象，让调用方显式分支。异常更适合不可继续、跨层传播或真正意外的失败。

## 惯用写法

常见现代写法包括：

- 默认用 `const`，只有需要重新绑定时用 `let`。
- 用 `===` / `!==`，避免 `==` 的隐式转换。
- 用可选链 `user.profile?.email` 读取可能缺失的深层字段。
- 用空值合并 `value ?? fallback`，只在 `null` 或 `undefined` 时兜底。
- 用解构、展开、模板字符串减少机械样板，但保持边界清楚。
- 数据转换小而直白时用 `map` / `filter` / `reduce`，流程较复杂时用 `for...of`。
- 异步顺序流程用 `await`，并发流程用 `Promise.all` 或 `Promise.allSettled` 明确收敛。
- TS 里优先表达业务边界，避免把所有局部变量都手写类型，也避免用 `any` 绕过真正的问题。

一句话总结：JS/TS 的代码常把数据当轻量对象流动，把函数当组合单元，把异步结果当值传递。写得清楚比写得炫更重要。

## 可运行示例

示例位于 [examples/syntax-tour/](examples/syntax-tour/)：

```bash
cd languages/javascript-typescript/syntax/examples/syntax-tour
node main.mjs
```

它只使用 Node 标准库，覆盖变量、模板字符串、控制流、函数、数组、对象、Map/Set、错误处理、Promise 和 ESM 导入导出的基本心智。你可以先直接运行，再按示例 README 的修改练习改变输入数据，观察输出和错误路径。

## 学习检查

读完后可以用下面的问题自测：

- 什么时候用 `const`，什么时候才需要 `let`？
- `const obj = {}` 为什么仍然能修改 `obj.name`？
- TypeScript 类型为什么不能替代 JSON 输入校验？
- `for...of` 和 `for...in` 分别遍历什么？
- 箭头函数和普通函数在 `this` 上有什么差异？
- `async` 函数抛错后，调用方为什么需要 `await` 或返回 Promise？
- `??` 和 `||` 在处理空字符串、数字 `0` 时有什么不同？
