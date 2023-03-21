# go类型断言(Type Assertion)

> 2015-05-19

> https://studygolang.com/articles/3133


go里面的类型断言写法：

```
x.(T)
```

其中`x`为 `interface{}` 类型 `T`是要断言的类型。

类型断言有个非常好的使用场景：
当某个类型为`interface{}`的变量，真实类型为`T`时，才做某件事时，这时可以使用类型断言。

下面有个例子。只有当某个interface{}的类型 存储的是int时才打印出来。

```
package main

import (
    "fmt"
    "math/rand"
    "time"
)

func main() {
    var v interface{}

    r := rand.New(rand.NewSource(time.Now().UnixNano()))
    for i := 0; i < 10; i++{
        v = i 
        if (r.Intn(100) % 2) == 0 { 
            v = "hello"
        }   

        if _, ok := v.(int); ok {
            fmt.Printf("%d\n", v)
        }   
    }   
}
```
