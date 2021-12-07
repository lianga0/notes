# Golang —unsafe.Pointer和uintptr

> 2021-02-03

如果你看go的源码，尤其是runtime的部分的源码，你一定经常会发现`unsafe.Pointer`和`uintptr`这两个函数，例如下面就是runtime里面的map源码实现里面的一个函数：

```
func (b *bmap) overflow(t *maptype) *bmap {
    return *(**bmap)(add(unsafe.Pointer(b), uintptr(t.bucketsize)-sys.PtrSize))
}
```

那么这两个方法有什么用呢？下面我们来重点介绍一下。

## Go中的指针及与指针对指针的操作主要有以下三种：

一普通的指针类型，例如 `var intptr *T`，定义一个`T`类型指针变量。

二内置类型`uintptr`，本质是一个无符号的整型，它的长度是跟平台相关的，它的长度可以用来保存一个指针地址。

三是`unsafe`包提供的`Pointer`，表示可以指向任意类型的指针。

## 1.普通的指针类型

```
count := 1
Counter(&count)
fmt.Println(count)

func Counter(count *int) {
    *count++
}
```

普通指针可以通过引用来修改变量的值，这个跟C语言指针有点像。

## 2.uintptr类型

- 一个足够大的无符号整型， 用来表示任意地址。

- 可以进行数值计算。

因为它是整型，所以很容易计算出下一个指针所指向的位置。uintptr在builtin包中定义，定义如下：

```
// uintptr is an integer type that is large enough to hold the bit pattern of any pointer.
// uintptr是一个能足够容纳指针位数大小的整数类型
type uintptr uintptr
```

虽然`uintpr`保存了一个指针地址，但它只是一个值，不引用任何对象。因此使用的时候要注意以下情况：

1. 如果`uintptr`地址相关联对象移动，则其值也不会更新。例如`goroutine`的堆栈信息发生变化

2. `uintptr`地址关联的对象可以被垃圾回收。GC不认为`uintptr`是活引用，因此unitptr地址指向的对象可以被垃圾收集。

一个`uintptr`可以被转换成`unsafe.Pointer`,同时`unsafe.Pointer`也可以被转换为`uintptr`。可以使用使用`uintptr + offset`计算出地址，然后使用`unsafe.Pointer`进行转换，格式如下：`p = unsafe.Pointer(uintptr(p) + offset)`

一个`uintptr`是一个整数，不是一个引用。把一个`Pointer`转换为`uintptr`后，实际是剥离了原有的指针的语义，只取了地址的整数值。但是，即使`uintptr`保存了某些对象的地址值，当对象发生移动，GC并不会去更新`uintprt`的值， GC也还是可能会对对象进行垃圾回收。作为对比，在指针指向对象时，GC是不会去对此对象进行垃圾回收的。

```
n := 10

b := make([]int, n)
for i:= 0;i< n;i++ {
    b[i] = i
}
fmt.Println(b)
// [0 1 2 3 4 5 6 7 8 9]

// 取slice的最后的一个元素
end := unsafe.Pointer(uintptr(unsafe.Pointer(&b[0])) + 9 * unsafe.Sizeof(b[0]))
// 等价于unsafe.Pointer(&b[9])
fmt.Println(*(*int)(end))
// 9
```

## 3.unsafe.Pointer

- 代表一个可以指向任意类型的指针。

- 不可以进行数值计算。

- 有四种区别于其他类型的特殊操作：

1. 任意类型的指针值均可转换为 Pointer。
2. Pointer 均可转换为任意类型的指针值。
3. uintptr 均可转换为 Pointer。
4. Pointer 均可转换为 uintptr。

所以unsafe.Pointer做的主要是用来进行桥接，用于不同类型的指针进行互相转换。

## 4.`unsafe.Pointer`,`uintptr`与普通指针的互相转换

### unsafe.Pointer和普通指针的相互转换

```
var f float64 = 1.0
fmt.Println(Float64bits(f))
// 4607182418800017408

func Float64bits(f float64) uint64 {
    return *((*uint64)(unsafe.Pointer(&f)))
}
```

借助`unsafe.Pointer`指针，实现`float64`转换为`uint64`类型。当然，我们不可以直接通过`*p`来获取`unsafe.Pointer`指针指向的真实变量的值，因为我们并不知道变量的具体类型。另外一个重要的要注意的是，在进行普通类型转换的时候，要注意转换的前后的类型要有相同的内存布局，下面两个结构也能完成转换，就因为他们有相同的内存布局

```
type s1 struct {
    id int
    name string
}

type s2 struct {
    field1 *[5]byte
    filed2 int
}

b := s1{name:"123"}
var j s2
j = *(*s2)(unsafe.Pointer(&b))
fmt.Println(j)
```

### unsafe.Pointer和uintrptr的互相转换及配合

`uintptr`类型的主要是用来与`unsafe.Pointer`配合使用来访问和操作`unsafe`的内存。`unsafe.Pointer`不能执行算术操作。要想对指针进行算术运算必须这样来做：

1. 将`unsafe.Pointer`转换为`uintptr`

2. 对`uintptr`执行算术运算

3. 将`uintptr`转换回`unsafe.Pointer`,然后访问`uintptr`地址指向的对象

**需要小心的是，上面的步骤对于垃圾收集器来说应该是原子的，否则可能会导致问题。**

例如，在第1步之后，引用的对象可能被收集。如果在步骤3之后发生这种情况，指针将是一个无效的Go指针，并可能导致程序崩溃。

因此，在uintptr转换回`Pointer`前，不能将`uintptr`的值保存到临时变量中。

```
// INVALID: uintptr cannot be stored in variable
// before conversion back to Pointer.
u := uintptr(p)
p = unsafe.Pointer(u + offset)
```

因为某些GC会把变量进行搬移来进行内存整理，这种类型的GC称为“移动的垃圾回收器”。当一个变量在内存中移动后，所有指向旧地址的指针都应该更新，并指向新地址。`uintptr`只是个数值，它的值不会变动。上面的代码使得GC无法通过临时变量`u`了解它背后的指针。当转换执行的时候，`p`可以已经发生了移动，这个时候`u`中的值就不再是原来`p`的位置了。

unsafe.Pointer和uintrptr的转换

```
package main

import (
    "fmt"
    "unsafe"
)

type Person struct {
    age int
    name string
}
func main() {
    p := &Person{age: 30, name: "Bob"}
    
   //获取到struct s中b字段的地址
    p := unsafe.Pointer(uintptr(unsafe.Pointer(p)) + unsafe.Offsetof(p.name))
    
    //将其转换为一个string的指针，并且打印该指针的对应的值
    fmt.Println(*(*string)(p))
}
```

From:

[Golang学习笔记--unsafe.Pointer和uintptr](https://studygolang.com/articles/33151)

[Golang学习笔记（一）—unsafe.Pointer和uintptr](http://www.manongjc.com/article/50416.html)
