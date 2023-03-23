
# Java反射的基本概念

## 问：什么是反射？为什么要使用反射？

答：反射（Reflection）是一种在运行时 动态访问类型信息 的机制。Java 是静态强类型语言，它倾向于在编译时进行类型检查，因此当我们访问一个类时，它必须是编译期已知的，而使用反射机制可以解除这种限制，赋予 Java 语言动态类型的特性。


## 问：什么是强 / 弱类型语言？：

答：强 / 弱类型语言的区分，关键在于变量是否 （倾向于） 类型兼容。例如，Java 是强类型语言，变量有固定的类型，以下代码在 Java 中是非法的：

```
public class MyRunnable {
    public abstract void run();
}

// 编译错误:Incompatible types
java.lang.Runnable runnable = new MyRunnable() { 
    @Override
    public void run() {
        
    }
}
runnable.run(); // X
```

相对地，JavaScript 是弱类型语言，一个变量没有固定的类型，允许接收不同类型的值：

```
function MyRunnable(){
    this.run = function(){
    }
}
function Runnable(){
    this.run = function(){
    }
}
var ss = new MyRunnable();
ss.run(); // 只要对象有相同方法签名的方法即可
ss = new Runnable();
ss.run();
```

更具体地描述，Java的强类型特性体现为：变量仅允许接收相同类型或子类型的值。

## 问：什么是静态 / 动态类型语言？

答：静态 / 动态类型语言的区分，关键在于类型检查是否 （倾向于） 编译时执行。例如， Java & C/C++ 是静态类型语言，而 JavaScript 是动态类型语言。需要注意的是，这个定义并不是绝对的，例如 Java 也存在运行时类型检查的方式，例如 `checkcast` 指令本质上是在运行时检查变量的类型与对象的类型是否相同。



From: https://juejin.cn/post/6889833658669072397
