# Go - Scope Rules

> https://www.tutorialspoint.com/go/go_scope_rules.htm

A scope in any programming is a region of the program where a defined variable can exist and beyond that the variable cannot be accessed. There are three places where variables can be declared in Go programming language −

- Inside a function or a block (local variables)

- Outside of all functions (global variables)

- In the definition of function parameters (formal parameters)

Let us find out what are local and global variables and what are formal parameters.


## Local Variables

Variables that are declared inside a function or a block are called local variables. They can be used only by statements that are inside that function or block of code. Local variables are not known to functions outside their own. The following example uses local variables. Here all the variables `a`, `b`, and `c` are local to the `main() `function.

```
package main

import "fmt"

func main() {
   /* local variable declaration */
   var a, b, c int 

   /* actual initialization */
   a = 10
   b = 20
   c = a + b

   fmt.Printf ("value of a = %d, b = %d and c = %d\n", a, b, c)
}
```

When the above code is compiled and executed, it produces the following result −

```
value of a = 10, b = 20 and c = 30
```


### 局部变量初始化`(:=)`

Golang中有一种局部变量初始化方法，即使用冒号和等号的组合`:=`来进行变量声明和初始化,这使得我们在使用局部变量时很方便。

初始化一个局部变量的代码可以这样写：

```
v := 10
```

等效于

```
var v = 10
```

指定类型已不再是必需的，Go编译器可以从初始化表达式的右值推导出该变量应该声明为哪种类型，这让Go语言看起来有点像动态类型语言，尽管Go语言实际上是不折不扣的强类型语言（静态类型语言）。


### Short variable declarations

Inside a function, the `:=` short assignment statement can be used in place of a var declaration with implicit type.

Outside a function, every statement begins with a keyword (`var`, `func`, and so on) and so the `:=` construct is not available.


## Global Variables

全局变量声明到函数外部，整个包都可以访问。

如果全局变量首字母大写，跨包也可以访问。

在golang的main包中，main包定义的全局变量无法被其他包引用。

Global variables are defined outside of a function, usually on top of the program. Global variables hold their value throughout the lifetime of the program and they can be accessed inside any of the functions defined for the program.

A global variable can be accessed by any function. That is, a global variable is available for use throughout the program after its declaration. The following example uses both global and local variables −

```
import "fmt"
 
/* global variable declaration */
var g int
 
func main() {
   /* local variable declaration */
   var a, b int

   /* actual initialization */
   a = 10
   b = 20
   g = a + b

   fmt.Printf("value of a = %d, b = %d and g = %d\n", a, b, g)
}
```

When the above code is compiled and executed, it produces the following result −

```
value of a = 10, b = 20 and g = 30
```

A program can have the same name for local and global variables but the value of the local variable inside a function takes preference. For example −

```
package main

import "fmt"
 
/* global variable declaration */
var g int = 20
 
func main() {
   /* local variable declaration */
   var g int = 10
 
   fmt.Printf ("value of g = %d\n",  g)
}
```

When the above code is compiled and executed, it produces the following result −

```
value of g = 10
```


## Formal Parameters

Formal parameters are treated as local variables with-in that function and they take preference over the global variables. For example −

```
package main

import "fmt"
 
/* global variable declaration */
var a int = 20;
 
func main() {
   /* local variable declaration in main function */
   var a int = 10
   var b int = 20
   var c int = 0

   fmt.Printf("value of a in main() = %d\n",  a);
   c = sum( a, b);
   fmt.Printf("value of c in main() = %d\n",  c);
}
/* function to add two integers */
func sum(a, b int) int {
   fmt.Printf("value of a in sum() = %d\n",  a);
   fmt.Printf("value of b in sum() = %d\n",  b);

   return a + b;
}
```

When the above code is compiled and executed, it produces the following result −

```
value of a in main() = 10
value of a in sum() = 10
value of b in sum() = 20
value of c in main() = 30
```

## Initializing Local and Global Variables

Local and global variables are initialized to their default value, which is 0; while pointers are initialized to `nil`.
