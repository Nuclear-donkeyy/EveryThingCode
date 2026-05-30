# Prototype Delegation

## 目标

通过 `Object.create`、属性遮蔽和方法提取观察 JavaScript 的原型委托模型。这个例子对应的语言特性是 prototype delegation：对象找不到属性时，会沿着原型链向上查找，而不是从类模板里复制一份方法。

真实工程中，原型模型解释了 `class` 方法为什么共享、对象字面量为什么也能委托行为、以及 `this` 为什么会在方法被拆出来调用时丢失。如果不了解这套机制，代码容易退化成给每个对象重复拷贝函数，或者在回调里遇到 `this` 变成 `undefined` 却不知道原因。

## 特性说明

示例创建了一个 `accountBehavior` 原型对象，再用 `Object.create(accountBehavior)` 创建两个账户。账户实例只保存自己的 `owner` 和 `balance`，`deposit`、`describe` 等方法由原型提供。运行时调用 `checking.deposit(25)` 时，JavaScript 先在 `checking` 自身找 `deposit`，找不到就委托给原型对象。

代码还故意给 `checking.describe` 赋值，形成实例级遮蔽。此时 `checking` 使用自己的 `describe`，`savings` 仍然沿原型链使用共享方法。最后打印 `Object.hasOwn` 和 `Object.getPrototypeOf`，让你直接看到属性到底在实例上还是原型上。

## 设计取舍

原型委托的优势是灵活和节省：共享行为放在原型上，实例只保存差异数据；运行时也可以用组合对象快速建立委托关系。`class` 语法提供了更熟悉的外观，但它没有取消原型链，只是把构造器和原型方法写得更规整。

代价是查找规则和 `this` 绑定需要学习。方法被当作属性取出来后，函数本身不会记住原来的接收者；如果直接调用 `const f = checking.deposit; f(1)`，严格模式下 `this` 会丢失。真实项目通常用箭头函数、显式绑定、类字段或避免方法提取来降低这个风险。

## 运行

```bash
node main.mjs
```

## 观察点

- `checking` 和 `savings` 都没有自己的 `deposit` 属性，但都能调用它，说明行为来自原型委托。
- `checking.describe` 被实例属性遮蔽后，只影响 `checking`，不会改掉原型上的共享方法。
- `Object.getPrototypeOf(checking) === accountBehavior` 输出 `true`，验证对象的委托目标。
- `detached method error` 展示了方法提取后 `this` 丢失的常见问题。
- 原型方法内部通过 `this.balance` 访问接收者状态，因此同一份方法能服务多个实例。

## 延伸练习

删除 `checking.describe = ...` 这一段，观察两个账户是否重新使用同一个原型方法。再把 `accountBehavior.deposit` 改成箭头函数，运行后思考为什么箭头函数不适合放在原型上当依赖 `this` 的方法。

还可以把示例改写成 `class Account`，然后打印 `Account.prototype` 和实例的原型，验证 `class` 只是原型模型的语法外观。这个练习能帮助你把面向对象语法和 JavaScript 的真实运行时连接起来。
