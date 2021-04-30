## JS中用var声明变量和不用var声明变量的区别

> 数学太陡 2018-09-12 10:17:26

> https://blog.csdn.net/qq_28137309/article/details/82656478

阅前须知：作用域（分为全局和局部），函数会开辟自己的作用域（或"空间"或"过程级"）

### 变量声明

变量在脚本中的第一次出现是在声明中。变量在第一次用到时就设置于内存中，便于后来在脚本中引用。使用变量之前先进行声明。可以使用 var 关键字来进行变量声明。

```
var count;  // 单个声明。
var count, amount, level;  // 用单个 var 关键字声明的多个声明。
var count = 0, amount = 100;  // 一条语句中的变量声明和初始化。
```

如果在 var 语句中没有初始化变量，变量自动取 JScript 值 undefined。尽管并不安全，但声明语句中忽略 var 关键字是合法的 JScript 语法。这时，JScript 解释器给予变量全局范围的可见度。如果，要在过程级中声明一个变量时，它不能用于全局范围；这种情况下，变量声明必须用 var 关键字。

### 1.在函数内部声明变量

**在函数内部用var声明变量和不用的区别是很大的**：用var声明的是局部变量，在函数外部访问是访问不到的；没var声明的变量是全部变量，在函数外部是可以访问到的。

```
function test(){
    var a = 'bbb';
    console.log(a); // bbb
}
test();
console.log(a); // a is not defined
```

如果去掉var声明变量a

```
function test(){
    a = 'bbb';
    console.log(a); // bbb
}
test();
console.log(a); // bbb
```

### 2.在全局作用域内声明变量

在这里用var声明的变量我们之所以认为是全局变量，是因为现在所在的作用域范围是全局，实际上它声明的也是局部变量，只是现在它的局部变量全局而已，所以就相当于起了全局变量的作用。

全局作用域中不用var声明的也是全局变量，那他们俩有啥区别呢？

比较var a=1 和 b=2，前者是变量声明，带不可删除属性，因此无法被删除；后者是全局变量的一个属性，因此可以从全局变量中删除

```
var a=1;
b=2;
console.log(a); // 1
console.log(b); // 2
delete a;
delete b;
console.log(a); // 1
console.log(b); // b is not defined
```

《完》