# 反射

Go语言提供了一种机制，能够在运行时更新变量和检查它们的值、调用它们的方法和它们支持的内在操作，而不需要在编译时就知道这些变量的具体类型。这种机制被称为反射。反射也可以让我们将类型本身作为第一类的值类型处理。反射是一个复杂的内省技术，不应该随意使用。

## 为何需要反射?

有时候我们需要编写一个函数能够处理一类并不满足普通公共接口的类型的值，也可能是因为它们并没有确定的表示方式，或者是在我们设计该函数的时候这些类型可能还不存在。

一个大家熟悉的例子是`fmt.Fprintf`函数提供的字符串格式化处理逻辑，它可以用来对任意类型的值格式化并打印，甚至支持用户自定义的类型。让我们也来尝试实现一个类似功能的函数。为了简单起见，我们的函数只接收一个参数，然后返回和`fmt.Sprint`类似的格式化后的字符串。我们实现的函数名也叫`Sprint`。

我们首先用`switch`类型分支来测试输入参数是否实现了`String`方法，如果是的话就调用该方法。然后继续增加类型测试分支，检查这个值的动态类型是否是`string`、`int`、`bool`等基础类型，并在每种情况下执行相应的格式化操作。

但是我们如何处理其它类似`[]float64`、`map[string][]string`等类型呢？我们当然可以添加更多的测试分支，但是这些组合类型的数目基本是无穷的。还有如何处理类似`url.Values`这样的具名类型呢？即使类型分支可以识别出底层的基础类型是`map[string][]string`，但是它并不匹配`url.Values`类型，因为它们是两种不同的类型，而且`switch`类型分支也不可能包含每个类似`url.Values`的类型，这会导致对这些库的依赖。

没有办法来检查未知类型的表示方式，我们被卡住了。这就是我们需要反射的原因。

## `reflect.Type` 和 `reflect.Value`

反射是由 `reflect` 包提供的。它定义了两个重要的类型，`Type` 和 `Value`。一个 `Type` 表示一个Go类型。它是一个接口，有许多方法来区分类型以及检查它们的组成部分，例如一个结构体的成员或一个函数的参数等。唯一能反映 `reflect.Type` 实现的是接口的类型描述信息，也正是这个实体标识了接口值的动态类型。

函数 `reflect.TypeOf` 接受任意的 `interface{}` 类型，并以 `reflect.Type` 形式返回其动态类型：

```
t := reflect.TypeOf(3)  // a reflect.Type
fmt.Println(t.String()) // "int"
fmt.Println(t)          // "int"
```

其中 `TypeOf(3)` 调用将值 `3` 传给 `interface{`} 参数。回忆之前小节的将一个具体的值转为接口类型会有一个隐式的接口转换操作，它会创建一个包含两个信息的接口值：操作数的动态类型（这里是 `int`）和它的动态的值（这里是 `3`）。

因为 `reflect.TypeOf` 返回的是一个动态类型的接口值，它总是返回具体的类型。因此，下面的代码将打印`*os.File` 而不是 `io.Writer`。稍后，我们将看到能够表达接口类型的 `reflect.Type`。

```
var w io.Writer = os.Stdout
fmt.Println(reflect.TypeOf(w)) // "*os.File"
```

要注意的是 `reflect.Type` 接口是满足 `fmt.Stringer` 接口的。因为打印一个接口的动态类型对于调试和日志是有帮助的， `fmt.Printf` 提供了一个缩写 `%T` 参数，内部使用 `reflect.TypeOf` 来输出：

```
fmt.Printf("%T\n", 3) // "int"
```

`reflect` 包中另一个重要的类型是 `Value`。一个 `reflect.Value` 可以装载任意类型的值。函数 `reflect.ValueOf`接受任意的 `interface{}` 类型，并返回一个装载着其动态值的 `reflect.Value`。和 `reflect.TypeOf` 类似，`reflect.ValueOf` 返回的结果也是具体的类型，但是 `reflect.Value` 也可以持有一个接口值。

```
v := reflect.ValueOf(3) // a reflect.Value
fmt.Println(v)          // "3"
fmt.Printf("%v\n", v)   // "3"
fmt.Println(v.String()) // NOTE: "<int Value>"
```

和 `reflect.Type` 类似，`reflect.Value` 也满足 `fmt.Stringer` 接口，但是除非 `Value` 持有的是字符串，否则`String` 方法只返回其类型。而使用 `fmt` 包的 `%v` 标志参数会对 `reflect.Values` 特殊处理。

对 `Value` 调用 `Type` 方法将返回具体类型所对应的 `reflect.Type`：

```
t := v.Type()           // a reflect.Type
fmt.Println(t.String()) // "int"
```

`reflect.ValueOf` 的逆操作是 `reflect.Value.Interface` 方法。它返回一个 `interface{}` 类型，装载着与`reflect.Value` 相同的具体值：

```
v := reflect.ValueOf(3) // a reflect.Value
x := v.Interface()      // an interface{}
i := x.(int)            // an int
fmt.Printf("%d\n", i)   // "3"
```

`reflect.Value` 和 `interface{}` 都能装载任意的值。所不同的是，一个空的接口隐藏了值内部的表示方式和所有方法，因此只有我们知道具体的动态类型才能使用类型断言来访问内部的值（就像上面那样），内部值我们没法访问。相比之下，一个 `Value` 则有很多方法来检查其内容(reflect.Value自身是一个struct，reflect.Type自身是一个interface类型)，无论它的具体类型是什么。让我们再次尝试实现我们的格式化函数 `format.Any`。

我们使用 `reflect.Value` 的 `Kind` 方法来替代之前的类型 `switch`。虽然还是有无穷多的类型，但是它们的 `kinds` 类型却是有限的：`Bool`、`String` 和所有数字类型的基础类型；`Array` 和 `Struct` 对应的聚合类型；`Chan`、`Func`、`Ptr`、`Slice` 和 `Map` 对应的引用类型；`interface` 类型；还有表示空值的 `Invalid` 类型。（空的 `reflect.Value` 的 `kind` 即为 Invalid。）

```
package format

import (
    "reflect"
    "strconv"
)

// Any formats any value as a string.
func Any(value interface{}) string {
    return formatAtom(reflect.ValueOf(value))
}

// formatAtom formats a value without inspecting its internal structure.
func formatAtom(v reflect.Value) string {
    switch v.Kind() {
    case reflect.Invalid:
        return "invalid"
    case reflect.Int, reflect.Int8, reflect.Int16, reflect.Int32, reflect.Int64:
        return strconv.FormatInt(v.Int(), 10)
    case reflect.Uint, reflect.Uint8, reflect.Uint16, reflect.Uint32, reflect.Uint64, reflect.Uintptr:
        return strconv.FormatUint(v.Uint(), 10)
    // ...floating-point and complex cases omitted for brevity...
    case reflect.Bool:
        return strconv.FormatBool(v.Bool())
    case reflect.String:
        return strconv.Quote(v.String())
    case reflect.Chan, reflect.Func, reflect.Ptr, reflect.Slice, reflect.Map:
        return v.Type().String() + " 0x" +strconv.FormatUint(uint64(v.Pointer()), 16)
    default: // reflect.Array, reflect.Struct, reflect.Interface
        return v.Type().String() + " value"
    }
}
```

到目前为止，我们的函数将每个值视作一个不可分割没有内部结构的物品，因此它叫 `formatAtom`。对于聚合类型（结构体和数组）和接口，只是打印值的类型，对于引用类型（channels、functions、pointers、slices 和 maps），打印类型和十六进制的引用地址。虽然还不够理想，但是依然是一个重大的进步，并且 Kind 只关心底层表示，format.Any 也支持具名类型。例如：

```
var x int64 = 1
var d time.Duration = 1 * time.Nanosecond
fmt.Println(format.Any(x))                  // "1"
fmt.Println(format.Any(d))                  // "1"
fmt.Println(format.Any([]int64{x}))         // "[]int64 0x8202b87b0"
fmt.Println(format.Any([]time.Duration{d})) // "[]time.Duration 0x8202b87e0"
```

## 一个递归的值打印器示例

接下来，让我们看看如何改善聚合数据类型的显示。我们并不想完全克隆一个fmt.Sprint函数，我们只是构建一个用于调试用的Display函数：给定任意一个复杂类型 x，打印这个值对应的完整结构，同时标记每个元素的发现路径。

你应该尽量避免在一个包的API中暴露涉及反射的接口。我们将定义一个未导出的`display`函数用于递归处理工作，导出的是`Display`函数，它只是`display`函数简单的包装以接受`interface{}`类型的参数：

```
func Display(name string, x interface{}) {
    fmt.Printf("Display %s (%T):\n", name, x)
    display(name, reflect.ValueOf(x))
}
```

在display函数中，我们使用了前面定义的打印基础类型——基本类型、函数和`chan`等——元素值的`formatAtom`函数，但是我们会使用`reflect.Value`的方法来递归显示复杂类型的每一个成员。在递归下降过程中，`path`字符串，从最开始传入的起始值（这里是“e”），将逐步增长来表示是如何达到当前值（例如“e.args[0].value”）的。

因为我们不再模拟`fmt.Sprint`函数，我们将直接使用`fmt`包来简化我们的例子实现。

```
func display(path string, v reflect.Value) {
    switch v.Kind() {
    case reflect.Invalid:
        fmt.Printf("%s = invalid\n", path)
    case reflect.Slice, reflect.Array:
        for i := 0; i < v.Len(); i++ {
            display(fmt.Sprintf("%s[%d]", path, i), v.Index(i))
        }
    case reflect.Struct:
        for i := 0; i < v.NumField(); i++ {
            fieldPath := fmt.Sprintf("%s.%s", path, v.Type().Field(i).Name)
            display(fieldPath, v.Field(i))
        }
    case reflect.Map:
        for _, key := range v.MapKeys() {
            display(fmt.Sprintf("%s[%s]", path,formatAtom(key)), v.MapIndex(key))
        }
    case reflect.Ptr:
        if v.IsNil() {
            fmt.Printf("%s = nil\n", path)
        } else {
            display(fmt.Sprintf("(*%s)", path), v.Elem())
        }
    case reflect.Interface:
        if v.IsNil() {
            fmt.Printf("%s = nil\n", path)
        } else {
            fmt.Printf("%s.type = %s\n", path, v.Elem().Type())
            display(path+".value", v.Elem())
        }
    default: // basic types, channels, funcs
        fmt.Printf("%s = %s\n", path, formatAtom(v))
    }
}
```

让我们针对不同类型分别讨论。

**Slice和数组**：两种的处理逻辑是一样的。`Len`方法返回slice或数组值中的元素个数，`Index(i)`获得索引i对应的元素，返回的也是一个`reflect.Value`；如果索引`i`超出范围的话将导致`panic`异常，这与数组或`slice`类型内建的`len(a)`和`a[i]`操作类似。`display`针对序列中的每个元素递归调用自身处理，我们通过在递归处理时向path附加`[i]`来表示访问路径。

虽然`reflect.Value`类型带有很多方法，但是只有少数的方法能对任意值都安全调用。例如，`Index`方法只能对`Slice`、数组或字符串类型的值调用，如果对其它类型调用则会导致`panic`异常。

**结构体**： `NumField`方法报告结构体中成员的数量，`Field(i)`以`reflect.Value`类型返回第`i`个成员的值。成员列表也包括通过匿名字段提升上来的成员。为了在path添加`.f`来表示成员路径，我们必须获得结构体对应的`reflect.Type`类型信息，然后访问结构体第`i`个成员的名字。

**Maps**: `MapKeys`方法返回一个`reflect.Value`类型的`slice`，每一个元素对应map的一个key。和往常一样，遍历map时顺序是随机的。`MapIndex(key)`返回map中key对应的value。我们向path添加`[key]`来表示访问路径。

**指针**： Elem方法返回指针指向的变量，依然是`reflect.Value`类型。即使指针是`nil`，这个操作也是安全的，在这种情况下指针是`Invalid`类型，但是我们可以用`IsNil`方法来显式地测试一个空指针，这样我们可以打印更合适的信息。

**接口**：再一次，我们使用`IsNil`方法来测试接口是否是`nil`，如果不是，我们可以调用`v.Elem()`来获取接口对应的动态值，并且打印对应的类型和值。

反射能够访问到结构体中未导出的成员。需要当心的是这个例子的输出在不同操作系统上可能是不同的，并且随着标准库的发展也可能导致结果不同。（这也是将这些成员定义为私有成员的原因之一！）我们甚至可以用Display函数来显示`reflect.Value` 的内部构造。

对于目前的实现，如果遇到对象图中含有回环，Display将会陷入死循环，例如下面这个首尾相连的链表：

```
// a struct that points to itself
type Cycle struct{ Value int; Tail *Cycle }
var c Cycle
c = Cycle{42, &c}
Display("c", c)
```

Display会永远不停地进行深度递归打印：

```
Display c (display.Cycle):
c.Value = 42
(*c.Tail).Value = 42
(*(*c.Tail).Tail).Value = 42
(*(*(*c.Tail).Tail).Tail).Value = 42
...ad infinitum...
```

许多Go语言程序都包含了一些循环的数据。让Display支持这类带环的数据结构需要些技巧，需要额外记录迄今访问的路径；相应会带来成本。通用的解决方案是采用 unsafe 的语言特性，我们将在后续小节看到具体的解决方案。

带环的数据结构很少会对`fmt.Sprint`函数造成问题，因为它很少尝试打印完整的数据结构。例如，当它遇到一个指针的时候，它只是简单地打印指针的数字值。在打印包含自身的`slice`或`map`时可能卡住，但是这种情况很罕见，不值得付出为了处理回环所需的开销。


## 通过`reflect.Value`修改值

到目前为止，反射还只是程序中变量的另一种读取方式。然而，在本节中我们将重点讨论如何通过反射机制来修改变量。

回想一下，Go语言中类似`x`、`x.f[1]`和`*p`形式的表达式都可以表示变量，但是其它如`x + 1`和`f(2)`则不是变量。一个变量就是一个可寻址的内存空间，里面存储了一个值，并且存储的值可以通过内存地址来更新。

对于`reflect.Values`也有类似的区别。有一些`reflect.Values`是可取地址的；其它一些则不可以。考虑以下的声明语句：

```
x := 2// value   type    variable?
a := reflect.ValueOf(2)  // 2       int     no
b := reflect.ValueOf(x)  // 2       int     no
c := reflect.ValueOf(&x) // &x      *int    no
d := c.Elem()            // 2       int     yes (x)
```

其中a对应的变量不可取地址。因为a中的值仅仅是整数2的拷贝副本。b中的值也同样不可取地址。c中的值还是不可取地址，它只是一个指针`&x`的拷贝。实际上，所有通过`reflect.ValueOf(x)`返回的`reflect.Value`都是不可取地址的。但是对于d，它是c的解引用方式生成的，指向另一个变量，因此是可取地址的。我们可以通过调用`reflect.ValueOf(&x).Elem()`，来获取任意变量`x`对应的可取地址的`Value`。

我们可以通过调用`reflect.Value`的`CanAddr`方法来判断其是否可以被取地址：

```
fmt.Println(a.CanAddr()) // "false"
fmt.Println(b.CanAddr()) // "false"
fmt.Println(c.CanAddr()) // "false"
fmt.Println(d.CanAddr()) // "true"
```

每当我们通过指针间接地获取的`reflect.Value`都是可取地址的，即使开始的是一个不可取地址的`Value`。在反射机制中，所有关于是否支持取地址的规则都是类似的。例如，`slice`的索引表达式`e[i]`将隐式地包含一个指针，它就是可取地址的，即使开始的`e`表达式不支持也没有关系。以此类推，`reflect.ValueOf(e).Index(i)`对应的值也是可取地址的，即使原始的`reflect.ValueOf(e)`不支持也没有关系。

要从变量对应的可取地址的`reflect.Value`来访问变量需要三个步骤。第一步是调用`Addr()`方法，它返回一个`Value`，里面保存了指向变量的指针。然后是在`Value`上调用`Interface()`方法，也就是返回一个`interface{}`，里面包含指向变量的指针。最后，如果我们知道变量的类型，我们可以使用类型的断言机制将得到的`interface{}`类型的接口强制转为普通的类型指针。这样我们就可以通过这个普通指针来更新变量了：

```
x := 2
d := reflect.ValueOf(&x).Elem()   // d refers to the variable x
px := d.Addr().Interface().(*int) // px := &x
*px = 3                           // x = 3
fmt.Println(x)                    // "3"
```

或者，不使用指针，而是通过调用可取地址的`reflect.Value`的`reflect.Value.Set`方法来更新对应的值：

```
d.Set(reflect.ValueOf(4))
fmt.Println(x) // "4"
```

`Set`方法将在运行时执行和编译时进行类似的可赋值性约束的检查。以上代码，变量和值都是`int`类型，但是如果变量是`int64`类型，那么程序将抛出一个`panic`异常，所以关键问题是要确保改类型的变量可以接受对应的值：

```
d.Set(reflect.ValueOf(int64(5))) // panic: int64 is not assignable to int
```

同样，对一个不可取地址的`reflect.Value`调用`Set`方法也会导致`panic`异常：

```
x := 2
b := reflect.ValueOf(x)
b.Set(reflect.ValueOf(3)) // panic: Set using unaddressable value
```

这里有很多用于基本数据类型的`Set`方法：`SetIn`t、`SetUint`、`SetString`和`SetFloat`等。

```
d := reflect.ValueOf(&x).Elem()
d.SetInt(3)
fmt.Println(x) // "3"
```

从某种程度上说，这些`Set`方法总是尽可能地完成任务。以`SetInt`为例，只要变量是某种类型的有符号整数就可以工作，即使是一些命名的类型、甚至只要底层数据类型是有符号整数就可以，而且如果对于变量类型值太大的话会被自动截断。但需要谨慎的是：对于一个引用`interface{}`类型的`reflect.Value`调用`SetInt`会导致`panic`异常，即使那个`interface{}`变量对于整数类型也不行。

```
x := 1
rx := reflect.ValueOf(&x).Elem()
rx.SetInt(2)                     // OK, x = 2
rx.Set(reflect.ValueOf(3))       // OK, x = 3
rx.SetString("hello")            // panic: string is not assignable to int
rx.Set(reflect.ValueOf("hello")) // panic: string is not assignable to int

var y interface{}
ry := reflect.ValueOf(&y).Elem()
ry.SetInt(2)                     // panic: SetInt called on interface Value
ry.Set(reflect.ValueOf(3))       // OK, y = int(3)
ry.SetString("hello")            // panic: SetString called on interface Value
ry.Set(reflect.ValueOf("hello")) // OK, y = "hello"
```

反射可以越过Go语言的导出规则的限制读取结构体中未导出的成员，比如在类Unix系统上`os.File`结构体中的`fd int`成员。然而，利用反射机制并不能修改这些未导出的成员：

```
stdout := reflect.ValueOf(os.Stdout).Elem() // *os.Stdout, an os.File var
fmt.Println(stdout.Type())                  // "os.File"
fd := stdout.FieldByName("fd")
fmt.Println(fd.Int()) // "1"
fd.SetInt(2)          // panic: unexported field
```

一个可取地址的`reflect.Value`会记录一个结构体成员是否是未导出成员，如果是的话则拒绝修改操作。因此，`CanAddr`方法并不能正确反映一个变量是否是可以被修改的。另一个相关的方法`CanSet`是用于检查对应的`reflect.Value`是否是可取地址并可被修改的：

```
fmt.Println(fd.CanAddr(), fd.CanSet()) // "true false"
```

当然，Go使用反射也是可以修改 "非导出" 属性的值，这需要用到go的"unsafe"包和`reflect.NewAt`结合实现。


## 获取结构体字段标签

结构体成员标签可用于设置对应JSON对应的名字。其中json成员标签让我们可以选择成员的名字和抑制零值成员的输出。在本节，我们将看到如何通过反射机制类获取成员标签。

`reflect.Type`的`Field`方法将返回一个`reflect.StructField`，里面含有每个成员的名字、类型和可选的成员标签等信息。其中成员标签信息对应`reflect.StructTag`类型的字符串，并且提供了`Get`方法用于解析和根据特定`key`提取的子串。

## 显示一个类型的方法集

我们的最后一个例子是使用`reflect.Type`来打印任意值的类型和枚举它的方法：

```
// Print prints the method set of the value x.
func Print(x interface{}) {
    v := reflect.ValueOf(x)
    t := v.Type()
    fmt.Printf("type %s\n", t)
    
    for i := 0; i < v.NumMethod(); i++ {
        methType := v.Method(i).Type()
        fmt.Printf("func (%s) %s%s\n", t, t.Method(i).Name,strings.TrimPrefix(methType.String(), "func"))
    }
}
```

`reflect.Type`和`reflect.Value`都提供了一个`Method`方法。每次`t.Method(i)`调用将一个`reflect.Method`的实例，对应一个用于描述一个方法的名称和类型的结构体。每次`v.Method(i)`方法调用都返回一个`reflect.Value`以表示对应的值，也就是一个方法是绑到它的接收者的。使用`reflect.Value.Call`方法（我们这里没有演示），将可以调用一个`Func`类型的`Value`，但是这个例子中只用到了它的类型。


## 几点忠告

虽然反射提供的API远多于我们讲到的，我们前面的例子主要是给出了一个方向，通过反射可以实现哪些功能。反射是一个强大并富有表达力的工具，但是它应该被小心地使用，原因有三。

第一个原因是，基于反射的代码是比较脆弱的。对于每一个会导致编译器报告类型错误的问题，在反射中都有与之相对应的误用问题，不同的是编译器会在构建时马上报告错误，而反射则是在真正运行到的时候才会抛出panic异常，可能是写完代码很久之后了，而且程序也可能运行了很长的时间。

避免这种因反射而导致的脆弱性的问题的最好方法，是将所有的反射相关的使用控制在包的内部，如果可能的话避免在包的API中直接暴露`reflect.Value`类型，这样可以限制一些非法输入。如果无法做到这一点，在每个有风险的操作前指向额外的类型检查。以标准库中的代码为例，当`fmt.Printf`收到一个非法的操作数时，它并不会抛出`panic`异常，而是打印相关的错误信息。程序虽然还有BUG，但是会更加容易诊断。

```
fmt.Printf("%d %s\n", "hello", 42) // "%!d(string=hello) %!s(int=42)"
```

反射同样降低了程序的安全性，还影响了自动化重构和分析工具的准确性，因为它们无法识别运行时才能确认的类型信息。

避免使用反射的第二个原因是，即使对应类型提供了相同文档，但是反射的操作不能做静态类型检查，而且大量反射的代码通常难以理解。总是需要小心翼翼地为每个导出的类型和其它接受`interface{}`或`reflect.Value`类型参数的函数维护说明文档。

第三个原因，基于反射的代码通常比正常的代码运行速度慢一到两个数量级。对于一个典型的项目，大部分函数的性能和程序的整体性能关系不大，所以当反射能使程序更加清晰的时候可以考虑使用。测试是一个特别适合使用反射的场景，因为每个测试的数据集都很小。但是对于性能关键路径的函数，最好避免使用反射。
