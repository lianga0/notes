# go包和工具

Go语言有超过100个的标准包（译注：可以用`go list std | wc -l`命令查看标准包的具体数目），标准库为大多数的程序提供了必要的基础构件。在Go的社区，有很多成熟的包被设计、共享、重用和改进，目前互联网上已经发布了非常多的Go语言开源包，它们可以通过 `http://godoc.org` 检索。

Go还自带了工具箱，里面有很多用来简化工作区和包管理的小工具。

## 包简介

任何包系统设计的目的都是为了简化大型程序的设计和维护工作，通过将一组相关的特性放进一个独立的单元以便于理解和更新，在每个单元更新的同时保持和程序中其它单元的相对独立性。这种模块化的特性允许每个包可以被其它的不同项目共享和重用，在项目范围内、甚至全球范围统一的分发和复用。

每个包一般都定义了一个不同的名字空间用于它内部的每个标识符的访问。每个名字空间关联到一个特定的包，让我们给类型、函数等选择简短明了的名字，这样可以在使用它们的时候减少和其它部分名字的冲突。

每个包还通过控制包内名字的可见性和是否导出来实现封装特性。通过限制包成员的可见性并隐藏包API的具体实现，将允许包的维护者在不影响外部包用户的前提下调整包的内部实现。通过限制包内变量的可见性，还可以强制用户通过某些特定函数来访问和更新内部变量，这样可以保证内部变量的一致性和并发时的互斥约束。

当我们修改了一个源文件，我们必须重新编译该源文件对应的包和所有依赖该包的其他包。即使是从头构建，Go语言编译器的编译速度也明显快于其它编译语言。Go语言的闪电般的编译速度主要得益于三个语言特性。第一点，所有导入的包必须在每个文件的开头显式声明，这样的话编译器就没有必要读取和分析整个源文件来判断包的依赖关系。第二点，禁止包的环状依赖，因为没有循环依赖，包的依赖关系形成一个有向无环图，每个包可以被独立编译，而且很可能是被并发编译。第三点，编译后包的目标文件不仅仅记录包本身的导出信息，目标文件同时还记录了包的依赖关系。因此，在编译一个包的时候，编译器只需要读取每个直接导入包的目标文件，而不需要遍历所有依赖的的文件（译注：很多都是重复的间接依赖）。

## 导入路径

每个包是由一个全局唯一的字符串所标识的导入路径定位。出现在import语句中的导入路径也是字符串。

```
import (
    "fmt"
    "math/rand"
    "encoding/json"
    "golang.org/x/net/html"
    "github.com/go-sql-driver/mysql"
)
```

Go语言的规范并没有指明包的导入路径字符串的具体含义，导入路径的具体含义是由构建工具来解释的。

我们将深入讨论Go语言工具箱的功能，包括大家经常使用的构建测试等功能。当然，也有第三方扩展的工具箱存在。

如果你计划分享或发布包，那么导入路径最好是全球唯一的。为了避免冲突，所有非标准库包的导入路径建议以所在组织的互联网域名为前缀；而且这样也有利于包的检索。例如，上面的import语句导入了Go团队维护的HTML解析器和一个流行的第三方维护的MySQL驱动。

## 包声明

在每个Go语言源文件的开头都必须有包声明语句。包声明语句的主要目的是确定当前包被其它包导入时默认的标识符（也称为包名）。

例如，`math/rand`包的每个源文件的开头都包含`package rand`包声明语句，所以当你导入这个包，你就可以用`rand.Int`、`rand.Float64`类似的方式访问包的成员。

```
package main
import (
    "fmt"
    "math/rand"
)

func main() {
    fmt.Println(rand.Int())
}
```

通常来说，默认的包名就是包导入路径名的最后一段，因此即使两个包的导入路径不同，它们依然可能有一个相同的包名。例如，`math/rand`包和`crypto/rand`包的包名都是`rand`。稍后我们将看到如何同时导入两个有相同包名的包。

关于默认包名一般采用导入路径名的最后一段的约定也有三种例外情况。第一个例外，包对应一个可执行程序，也就是`main`包，这时候`main`包本身的导入路径是无关紧要的。名字为`main`的包是给`go build`构建命令一个信息，这个包编译完之后必须调用连接器生成一个可执行程序。

第二个例外，包所在的目录中可能有一些文件名是以`_test.go`为后缀的Go源文件（译注：前面必须有其它的字符，因为以`_`或`.`开头的源文件会被构建工具忽略），并且这些源文件声明的包名也是以`_test`为后缀名的。这种目录可以包含两种包：一种是普通包，另一种则是测试的外部扩展包。所有以`_test`为后缀包名的测试外部扩展包都由`go test`命令独立编译，普通包和测试的外部扩展包是相互独立的。测试的外部扩展包一般用来避免测试代码中的循环导入依赖。

第三个例外，一些依赖版本号的管理工具会在导入路径后追加版本号信息，例如`gopkg.in/yaml.v2`。这种情况下包的名字并不包含版本号后缀，而是`yaml`。

## 导入声明

可以在一个Go语言源文件包声明语句之后，其它非导入声明语句之前，包含零到多个导入包声明语句。每个导入声明可以单独指定一个导入路径，也可以通过圆括号同时导入多个导入路径。下面两个导入形式是等价的，但是第二种形式更为常见。

```
import "fmt"
import "os"
import (
    "fmt"
    "os"
)
```

导入的包之间可以通过添加空行来分组；通常将来自不同组织的包独自分组。包的导入顺序无关紧要，但是在每个分组中一般会根据字符串顺序排列。（gofmt和goimports工具都可以将不同分组导入的包独立排序。）

如果我们想同时导入两个有着名字相同的包，例如`math/rand`包和`crypto/rand`包，那么导入声明必须至少为一个同名包指定一个新的包名以避免冲突。这叫做导入包的重命名。

```
import (
    "crypto/rand" 
    mrand "math/rand"// alternative name mrand avoids conflict
)
```

导入包的重命名只影响当前的源文件。其它的源文件如果导入了相同的包，可以用导入包原本默认的名字或重命名为另一个完全不同的名字。

导入包重命名是一个有用的特性，它不仅仅只是为了解决名字冲突。如果导入的一个包名很笨重，特别是在一些自动生成的代码中，这时候用一个简短名称会更方便。选择用简短名称重命名导入包时候最好统一，以避免包名混乱。选择另一个包名称还可以帮助避免和本地普通变量名产生冲突。例如，如果文件中已经有了一个名为`path`的变量，那么我们可以将`path`标准包重命名为`pathpkg`。

每个导入声明语句都明确指定了当前包和被导入包之间的依赖关系。如果遇到包循环导入的情况，Go语言的构建工具将报告错误。

## 包的匿名导入

如果只是导入一个包而并不使用导入的包将会导致一个编译错误。但是有时候我们只是想利用导入包而产生的副作用：它会计算包级变量的初始化表达式和执行导入包的`init`初始化函数。这时候我们需要抑制`unused import`编译错误，我们可以用下划线`_`来重命名导入的包。像往常一样，下划线`_`为空白标识符，并不能被访问。

```
import _ "image/png"// register PNG decoder
```

这个被称为包的匿名导入。它通常是用来实现一个编译时机制，然后通过在main主程序入口选择性地导入附加的包。首先，让我们看看如何使用该特性，然后再看看它是如何工作的。

标准库的image图像包包含了一个`Decode`函数，用于从`io.Reader`接口读取数据并解码图像，它调用底层注册的图像解码器来完成任务，然后返回`image.Image`类型的图像。使用`image.Decode`很容易编写一个图像格式的转换工具，读取一种格式的图像，然后编码为另一种图像格式

```
// The jpeg command reads a PNG image from the standard input
// and writes it as a JPEG image to the standard output.

package main

import (
    "fmt"
    "image"
    "image/jpeg"
    _ "image/png"// register PNG decoder
    "io"
    "os"
)

func main() {
    if err := toJPEG(os.Stdin, os.Stdout); err != nil {
        fmt.Fprintf(os.Stderr, "jpeg: %v\n", err)
        os.Exit(1)
    }
}

func toJPEG(in io.Reader, out io.Writer) error {
    img, kind, err := image.Decode(in)
    if err != nil {
        return err
    }
    fmt.Fprintln(os.Stderr, "Input format =", kind)
    return jpeg.Encode(out, img, &jpeg.Options{Quality: 95})
}
```

上述代码将解码输入的PNG格式图像，然后转换为JPEG格式的图像输出。

```
$ go build gopl.io/ch10/jpeg
$ cat test.jpg | ./jpeg > mandelbrot.jpg
Input format = png
```

要注意image/png包的匿名导入语句。如果没有这一行语句，程序依然可以编译和运行，但是它将不能正确识别和解码PNG格式的图像：

```
$ go build gopl.io/ch10/jpeg
$ cat test.jpg | ./jpeg > mandelbrot.jpg
jpeg: image: unknown format
```

下面的代码演示了它的工作机制。标准库还提供了GIF、PNG和JPEG等格式图像的解码器，用户也可以提供自己的解码器，但是为了保持程序体积较小，很多解码器并没有被全部包含，除非是明确需要支持的格式。`image.Decode`函数在解码时会依次查询支持的格式列表。每个格式驱动列表的每个入口指定了四件事情：格式的名称；一个用于描述这种图像数据开头部分模式的字符串，用于解码器检测识别；一个`Decode`函数用于完成解码图像工作；一个`DecodeConfig`函数用于解码图像的大小和颜色空间的信息。每个驱动入口是通过调用`image.RegisterFormat`函数注册，一般是在每个格式包的`init`初始化函数中调用，例如`image/png`包是这样注册的：

```
package png // image/png

func Decode(r io.Reader) (image.Image, error)
func DecodeConfig(r io.Reader) (image.Config, error)

func init() {
    const pngHeader = "\x89PNG\r\n\x1a\n"
    image.RegisterFormat("png", pngHeader, Decode, DecodeConfig)
}
```

最终的效果是，主程序只需要匿名导入特定图像驱动包就可以用`image.Decode`解码对应格式的图像了。

数据库包`database/sql`也是采用了类似的技术，让用户可以根据自己需要选择导入必要的数据库驱动。例如：

```
import (
    "database/sql"
    _ "github.com/lib/pq"// enable support for Postgres
    _ "github.com/go-sql-driver/mysql"// enable support for MySQL
)

db, err = sql.Open("postgres", dbname) // OK
db, err = sql.Open("mysql", dbname)    // OK
db, err = sql.Open("sqlite3", dbname)  // returns error: unknown driver "sqlite3"
```

## 包和命名

关于Go语言独特的包和成员命名的约定。当创建一个包，一般要用短小的包名，但也不能太短导致难以理解。标准库中最常用的包有bufio、bytes、flag、fmt、http、io、json、os、sort、sync和time等包。

尽可能让命名有描述性且无歧义。例如，类似`imageutil`或`ioutilis`的工具包命名已经足够简洁了，就无须再命名为`util`了。要尽量避免包名使用可能被经常用于局部变量的名字，这样可能导致用户重命名导入包，例如前面看到的`path`包。

包名一般采用单数的形式。标准库的`bytes`、`errors`和`strings`使用了复数形式，这是为了避免和预定义的类型冲突，同样还有`go/types`是为了避免和`type`关键字冲突。

要避免包名有其它的含义。例如，之前我们的温度转换包最初使用了temp包名，虽然并没有持续多久。但这是一个糟糕的尝试，因为temp几乎是临时变量的同义词。然后我们有一段时间使用了temperature作为包名，显然名字并没有表达包的真实用途。最后我们改成了和strconv标准包类似的tempconv包名，这个名字比之前的就好多了。

现在让我们看看如何命名包的成员。由于是通过包的导入名字引入包里面的成员，例如`fmt.Println`，同时包含了包名和成员名信息。因此，我们一般并不需要关注Println的具体内容，因为fmt包名已经包含了这个信息。当设计一个包的时候，需要考虑包名和成员名两个部分如何很好地配合。下面有一些例子：

```
bytes.Equal    
flag.Int    
http.Get    
json.Marshal
```


我们可以看到一些常用的命名模式。strings包提供了和字符串相关的诸多操作：

```
package strings

func Index(needle, haystack string)int

type Replacer struct{ /* ... */ }
func NewReplacer(oldnew ...string) *Replacer

type Reader struct{ /* ... */ }
funcNewReader(s string) *Reader
```


包名strings并没有出现在任何成员名字中。因为用户会这样引用这些成员strings.Index、strings.Replacer等。

其它一些包，可能只描述了单一的数据类型，例如`html/template`和`math/rand`等，只暴露一个主要的数据结构和与它相关的方法，还有一个以`New`命名的函数用于创建实例。

```
package rand // "math/rand"

type Rand struct{ /* ... */ }
func New(source Source) *Rand
```

这可能导致一些名字重复，例如`template.Template`或`rand.Rand`，这就是这些种类的包名往往特别短的原因之一。

在另一个极端，还有像`net/http`包那样含有非常多的名字和种类不多的数据类型，因为它们都是要执行一个复杂的复合任务。尽管有将近二十种类型和更多的函数，但是包中最重要的成员名字却是简单明了的：Get、Post、Handle、Error、Client、Server等。

## 工具

Go语言的工具箱集合了一系列功能的命令集。它可以看作是一个包管理器（类似于`Linux`中的`apt`和`rpm`工具），用于包的查询、计算包的依赖关系、从远程版本控制系统下载它们等任务。它也是一个构建系统，计算文件的依赖关系，然后调用编译器、汇编器和链接器构建程序，虽然它故意被设计成没有标准的make命令那么复杂。它也是一个单元测试和基准测试的驱动程序。

为了达到零配置的设计目标，Go语言的工具箱很多地方都依赖各种约定。例如，根据给定的源文件的名称，Go语言的工具可以找到源文件对应的包，因为每个目录只包含了单一的包，并且包的导入路径和工作区的目录结构是对应的。给定一个包的导入路径，Go语言的工具可以找到与之对应的存储着实体文件的目录。它还可以根据导入路径找到存储代码的仓库的远程服务器URL。

## 下载包

使用Go语言工具箱的go命令，不仅可以根据包导入路径找到本地工作区的包，甚至可以从互联网上找到和更新包。

使用命令`go get`可以下载一个单一的包或者用`...`下载整个子目录里面的每个包。Go语言工具箱的go命令同时计算并下载所依赖的每个包，这也是前一个例子中`golang.org/x/net/html`自动出现在本地工作区目录的原因。

一旦`go get`命令下载了包，然后就是安装包或包对应的可执行的程序。第一个命令是获取`golint`工具，它用于检测Go源代码的编程风格是否有问题。第二个命令是用`golint`命令对之前的`gopl.io/ch2/popcount`包代码进行编码风格检查。它友好地报告了忘记了包的文档：

```
$ go get github.com/golang/lint/golint
$ $GOPATH/bin/golint gopl.io/ch2/popcount
src/gopl.io/ch2/popcount/main.go:1:1:
  package comment should be of the form "Package popcount ..."
```

`go get`命令支持当前流行的托管网站`GitHub`、`Bitbucket`和`Launchpad`，可以直接向它们的版本控制系统请求代码。对于其它的网站，你可能需要指定版本控制系统的具体路径和协议，例如 `Git`或`Mercurial`。运行`go help importpath`获取相关的信息。

`go get`命令获取的代码是真实的本地存储仓库，而不仅仅只是复制源文件，因此你依然可以使用版本管理工具比较本地代码的变更或者切换到其它的版本。例如`golang.org/x/net`包目录对应一个`Git`仓库：

```
$ cd $GOPATH/src/golang.org/x/net
$ git remote -v
origin  https://go.googlesource.com/net (fetch)
origin  https://go.googlesource.com/net (push)
```

需要注意的是导入路径含有的网站域名和本地Git仓库对应远程服务地址并不相同，真实的Git地址是`go.googlesource.com`。这其实是Go语言工具的一个特性，可以让包用一个自定义的导入路径，但是真实的代码却是由更通用的服务提供，例如`googlesource.com`或`github.com`。因为页面`https://golang.org/x/net/html` 包含了如下的元数据，它告诉Go语言的工具当前包真实的Git仓库托管地址：

```
$ go build gopl.io/ch1/fetch
$ ./fetch https://golang.org/x/net/html | grep go-import
<meta name="go-import" content="golang.org/x/net git https://go.googlesource.com/net">
```

如果指定`-u`命令行标志参数，`go get`命令将确保所有的包和依赖的包的版本都是最新的，然后重新编译和安装它们。如果不包含该标志参数的话，而且如果包已经在本地存在，那么代码将不会被自动更新。

`go get -u`命令只是简单地保证每个包是最新版本，如果是第一次下载包则是比较方便的；但是对于发布程序则可能是不合适的，因为本地程序可能需要对依赖的包做精确的版本依赖管理。通常的解决方案是使用`vendor`的目录用于存储依赖包的固定版本的源代码，对本地依赖的包的版本更新也是谨慎和持续可控的。在Go1.5之前，一般需要修改包的导入路径，所以复制后`golang.org/x/net/html`导入路径可能会变为`gopl.io/vendor/golang.org/x/net/html`。最新的Go语言命令已经支持vendor特性，但限于篇幅这里并不讨论vendor的具体细节。不过可以通过`go help gopath`命令查看`Vendor`的帮助文档。

(译注：墙内用户在上面这些命令的基础上，还需要学习用翻墙来`go get`。)


## 构建包

`go build`命令编译命令行参数指定的每个包。如果包是一个库，则忽略输出结果；这可以用于检测包是可以正确编译的。如果包的名字是`main`，`go build`将调用链接器在当前目录创建一个可执行程序；以导入路径的最后一段作为可执行程序的名字。

由于每个目录只包含一个包，因此每个对应可执行程序或者叫Unix术语中的命令的包，会要求放到一个独立的目录中。这些目录有时候会放在名叫`cmd`目录的子目录下面，例如用于提供Go文档服务的`golang.org/x/tools/cmd/godoc`命令就是放在cmd子目录。

每个包可以由它们的导入路径指定，就像前面看到的那样，或者用一个相对目录的路径名指定，相对路径必须以`.`或`..`开头。如果没有指定参数，那么默认指定为当前目录对应的包。下面的命令用于构建同一个包，虽然它们的写法各不相同：

```
$ cd $GOPATH/src/gopl.io/ch1/helloworld
$ go build
```

或者：

```
$ cd anywhere
$ go build gopl.io/ch1/helloworld
```

或者：

```
$ cd $GOPATH
$ go build ./src/gopl.io/ch1/helloworld
```

但不能这样：

```
$ cd $GOPATH
$ go build src/gopl.io/ch1/helloworld
Error: cannot find package "src/gopl.io/ch1/helloworld".
```

也可以指定包的源文件列表，这一般只用于构建一些小程序或做一些临时性的实验。如果是`main`包，将会以第一个`Go`源文件的基础文件名作为最终的可执行程序的名字。

默认情况下，`go build`命令构建指定的包和它依赖的包，然后丢弃除了最后的可执行文件之外所有的中间编译结果。依赖分析和编译过程虽然都是很快的，但是随着项目增加到几十个包和成千上万行代码，依赖关系分析和编译时间的消耗将变的可观，有时候可能需要几秒种，即使这些依赖项没有改变。

`go install`命令和`go build`命令很相似，但是它会保存每个包的编译成果，而不是将它们都丢弃。被编译的包会被保存到`$GOPATH/pkg`目录下，目录路径和`src`目录路径对应，可执行程序被保存到`$GOPATH/bin`目录。（很多用户会将`$GOPATH/bin`添加到可执行程序的搜索列表中。）还有，`go install`命令和`go build`命令都不会重新编译没有发生变化的包，这可以使后续构建更快捷。为了方便编译依赖的包，`go build -i`命令将安装每个目标所依赖的包。

因为编译对应不同的操作系统平台和CPU架构，`go install`命令会将编译结果安装到`GOOS`和`GOARCH`对应的目录。例如，在Mac系统，`golang.org/x/net/html`包将被安装到`$GOPATH/pkg/darwin_amd64`目录下的`golang.org/x/net/html.a`文件。

针对不同操作系统或CPU的交叉构建也是很简单的。只需要设置好目标对应的`GOOS`和`GOARCH`，然后运行构建命令即可。下面交叉编译的程序将输出它在编译时的操作系统和CPU类型：

```
func main() {
    fmt.Println(runtime.GOOS, runtime.GOARCH)
}
```

下面以64位和32位环境分别编译和执行：

```
$ go build gopl.io/ch10/cross
$ ./cross
darwin amd64
$ GOARCH=386 go build gopl.io/ch10/cross
$ ./cross
darwin 386
```

有些包可能需要针对不同平台和处理器类型使用不同版本的代码文件，以便于处理底层的可移植性问题或为一些特定代码提供优化。如果一个文件名包含了一个操作系统或处理器类型名字，例如net_linux.go或asm_amd64.s，Go语言的构建工具将只在对应的平台编译这些文件。还有一个特别的构建注释参数可以提供更多的构建过程控制。例如，文件中可能包含下面的注释：

```
// +build linux darwin
```

在包声明和包注释的前面，该构建注释参数告诉`go build`只在编译程序对应的目标操作系统是Linux或Mac OS X时才编译这个文件。下面的构建注释则表示不编译这个文件：

```
// +build ignore
```

更多细节，可以参考go/build包的构建约束部分的文档。

```
$ go doc go/build
```


## 包文档

Go语言的编码风格鼓励为每个包提供良好的文档。包中每个导出的成员和包声明前都应该包含目的和用法说明的注释。

Go语言中的文档注释一般是完整的句子，第一行通常是摘要说明，以被注释者的名字开头。注释中函数的参数或其它的标识符并不需要额外的引号或其它标记注明。例如，下面是fmt.Fprintf的文档注释。

```
// Fprintf formats according to a format specifier and writes to w.
// It returns the number of bytes written and any write error encountered.
func Fprintf(w io.Writer, format string, a ...interface{}) (int, error)
```

`Fprintf`函数格式化的细节在`fmt`包文档中描述。如果注释后紧跟着包声明语句，那注释对应整个包的文档。包文档对应的注释只能有一个（译注：其实可以有多个，它们会组合成一个包文档注释），包注释可以出现在任何一个源文件中。如果包的注释内容比较长，一般会放到一个独立的源文件中；`fmt`包注释就有300行之多。这个专门用于保存包文档的源文件通常叫`doc.go`。

好的文档并不需要面面俱到，文档本身应该是简洁但不可忽略的。事实上，Go语言的风格更喜欢简洁的文档，并且文档也是需要像代码一样维护的。对于一组声明语句，可以用一个精炼的句子描述，如果是显而易见的功能则并不需要注释。

首先是`go doc`命令，该命令打印其后所指定的实体的声明与文档注释，该实体可能是一个包，或者是某个具体的包成员，或者是一个方法。

该命令并不需要输入完整的包导入路径或正确的大小写。下面的命令将打印`encoding/json`包的`(*json.Decoder).Decode`方法的文档：

```
go doc json.decode

func (dec *Decoder) Decode(v any) error
    Decode reads the next JSON-encoded value from its input and stores it in the
    value pointed to by v.

    See the documentation for Unmarshal for details about the conversion of JSON
    into a Go value.
```

第二个工具，名字也叫`godoc`，它提供可以相互交叉引用的HTML页面，但是包含和`go doc`命令相同以及更多的信息。godoc的在线服务 https://godoc.org ，包含了成千上万的开源包的检索工具。

你也可以在自己的工作区目录运行godoc服务。运行下面的命令，然后在浏览器查看http://localhost:8000/pkg 页面：

```
$ godoc -http :8000
```

其中`-analysis=type`和`-analysis=pointer`命令行标志参数用于打开文档和代码中关于静态分析的结果。如果你电脑显示找不到godoc命令，可以使用如下命令安装一下:

```
go install golang.org/x/tools/cmd/godoc@latest
```

## 内部包

在Go语言程序中，包是最重要的封装机制。没有导出的标识符只在同一个包内部可以访问，而导出的标识符则是面向全宇宙都是可见的。

有时候，一个中间的状态可能也是有用的，标识符对于一小部分信任的包是可见的，但并不是对所有调用者都可见。例如，当我们计划将一个大的包拆分为很多小的更容易维护的子包，但是我们并不想将内部的子包结构也完全暴露出去。同时，我们可能还希望在内部子包之间共享一些通用的处理包，或者我们只是想实验一个新包的还并不稳定的接口，暂时只暴露给一些受限制的用户使用。

为了满足这些需求，Go语言的构建工具对包含internal名字的路径段的包导入路径做了特殊处理。这种包叫`internal`包，一个`internal`包只能被和`internal`目录有同一个父目录的包所导入。例如，`net/http/internal/chunked`内部包只能被`net/http/httputil`或`net/http`包导入，但是不能被`net/url`包导入。不过`net/url`包却可以导入`net/http/httputil`包。

```
net/http
net/http/internal/chunked
net/http/httputil
net/url
```

## 查询包

`go list`命令可以查询可用包的信息。其最简单的形式，可以测试包是否在工作区并打印它的导入路径

```
$ go list github.com/go-sql-driver/mysql
github.com/go-sql-driver/mysql
```

`go list`命令的参数还可以用`...`表示匹配任意的包的导入路径。我们可以用它来列出工作区中的所有包

或者是特定子目录下的所有包

```
$ go list gopl.io/ch3/...
gopl.io/ch3/basename1
gopl.io/ch3/basename2
```

或者是和某个主题相关的所有包:

```
$ go list ...xml...
encoding/xml
gopl.io/ch7/xmlselect
```

`go list`命令还可以获取每个包完整的元信息，而不仅仅只是导入路径，这些元信息可以以不同格式提供给用户。其中`-json`命令行参数表示用JSON格式打印每个包的元信息。

`go list`命令行参数`-f`则允许用户使用`text/template`包的模板语言定义输出文本的格式。下面的命令将打印`strconv`包的依赖的包，然后用`join`模板函数将结果链接为一行，连接时每个结果之间用一个空格分隔：

```
$ go list -f '{{join .Deps " "}}' strconv
errors math runtime unicode/utf8 unsafe
```

译注：上面的命令在Windows的命令行运行会遇到`template: main:1: unclosed action`的错误。产生这个错误的原因是因为命令行对命令中的" "参数进行了转义处理。可以按照下面的方法解决转义字符串的问题：

```
$ go list -f "{{join .Deps \" \"}}" strconv
```
