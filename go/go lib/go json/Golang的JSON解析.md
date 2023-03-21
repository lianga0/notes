# Golang的JSON解析

> 2019.07.17

动态语言中觉得解析JSON非常很简单的，往往只需要一行代码就能拿到解析好的JSON对象。

Go语言自带的json包可以让你在程序中方便的读取和写入JSON数据。生成JSON场景相对简单一些，`json.Marshal()`会根据传入的结构体生成JSON数据。解析JSON会把数据解析到结构体中，由于JSON格式的自由组合的特点，并且使用`json.UnMarshal()`解析还需提前定义反序列化的结构体。对于那些结构复杂的JSON数据，声明接受JSON数据的结构体类型就会让新手陷入不知从何下手的困扰。

对于Go来说，其实`json.Marshal()`也不一定要定义结构体，可以使用`interface{}`类型，我们分别就两种情况进行讨论。

## 定义go结构体，强类型解析

例如，请求了手机归属地的接口，json 数据返回如下：

```
{
    "resultcode": "200",
    "reason": "Return Successd!",
    "result": {
        "province": "浙江",
        "city": "杭州",
        "areacode": "0571",
        "zip": "310000",
        "company": "中国移动",
        "card": ""
    }
}
```

go解析思路是这样的：

1. 先写出 json 对应的 struct。

2. 然后 `json.Unmarshal()` 即可。

json 转 struct ，自己手写就太麻烦了，有很多在线的工具可以直接用，我用的这个：

[JSON-to-Go Convert JSON to Go struct](https://mholt.github.io/json-to-go/)

在左边贴上 json 后面就生成 struct 对应的go代码了，使用超级方便。

全部测试代码实现下：

```
type MobileInfo struct {
    Resultcode string `json:"resultcode"`
    Reason     string `json:"reason"`
    Result     struct {
        Province string `json:"province"`
        City     string `json:"city"`
        Areacode string `json:"areacode"`
        Zip      string `json:"zip"`
        Company  string `json:"company"`
        Card     string `json:"card"`
    } `json:"result"`
}

func main() {
    jsonStr := `
        {
            "resultcode": "200",
            "reason": "Return Successd!",
            "result": {
                "province": "浙江",
                "city": "杭州",
                "areacode": "0571",
                "zip": "310000",
                "company": "中国移动",
                "card": ""
            }
        }
    `

    var mobile MobileInfo
    err := json.Unmarshal([]byte(jsonStr), &mobile)
    if err != nil {
        fmt.Println(err.Error())
    }
    fmt.Println(mobile.Resultcode)
    fmt.Println(mobile.Reason)
    fmt.Println(mobile.Result.City)
}
```

运行输出：

```
200
Return Successd!
杭州
```

完美解析。

到这问题还没结束，思考下这些问题：

如果 json 格式的数据类型不确定怎么办？

如果 json 格式的数据 result 中参数不固定怎么办？

思路是这样的：去 github 上找开源类库，比如大家常用的[mapstructure](https://github.com/mitchellh/mapstructure)

## 数据类型不确定，mapstructure.WeakDecode弱类型解析方法

咱们一起学习下，先解决第一个问题，数据类型不确定怎么办？

先定义一个 string 类型的 resultcode，json 却返回了 int 类型的 resultcode。

看文档有一个弱类型解析的方法 `WeakDecode()`，咱们试一下：

```
type MobileInfo struct {
    Resultcode string `json:"resultcode"`
}

func main() {
    jsonStr := `
        {
            "resultcode": 200
        }
    `

    var result map[string]interface{}
    err := json.Unmarshal([]byte(jsonStr), &result)
    if err != nil {
        fmt.Println(err.Error())
    }

    var mobile MobileInfo
    err = mapstructure.WeakDecode(result, &mobile)
    if err != nil {
        fmt.Println(err.Error())
    }

    fmt.Println(mobile.Resultcode)
}
```

输出：

```
200
```

第一个问题已解决。

## 参数名称不固定，mapstructure Embedded Structs and Squashing

再解决第二个问题，result 中参数不固定怎么办？

这个就不用上面的例子了，看下官方提供的例子 [Embedded Structs and Squashing](https://pkg.go.dev/github.com/mitchellh/mapstructure#hdr-Embedded_Structs_and_Squashing)。

```
type Family struct {
    LastName string
}
type Location struct {
    City string
}
type Person struct {
    Family    `mapstructure:",squash"`
    Location  `mapstructure:",squash"`
    FirstName string
}

func main() {
    input := map[string]interface{}{
        "FirstName": "Mitchell",
        "LastName":  "Hashimoto",
        "City":      "San Francisco",
    }

    var result Person
    err := mapstructure.Decode(input, &result)
    if err != nil {
        panic(err)
    }

    fmt.Println(result.FirstName)
    fmt.Println(result.LastName)
    fmt.Println(result.City)
}
```

输出：

```
Mitchell
Hashimoto
San Francisco
```

使用的是 `mapstructure` 包，`struct tag` 标识不要写 `json`，要写 `mapstructure`。

其他情况自己探索吧[mapstructure](https://pkg.go.dev/github.com/mitchellh/mapstructure)。

# 不定义解构体，`json.Marshal()`直接使用`interface{}`对象解析json字符串

示例代码1：

```
package main

import (
    "encoding/json"
    "fmt"
)

func main() {
    jsonStr := `
        {
            "resultcode": 200
        }`
    var m1 interface{}
    _ = json.Unmarshal([]byte(jsonStr), &m1)
    fmt.Println(m1)
}
```

上述代码输出：

```
map[resultcode:200]

```

示例代码2：
```
package main

import (
    "encoding/json"
    "fmt"
)

func main() {
    jsonStr := `[
        {
            "resultcode": 200
        }]`
    var m1 interface{}
    _ = json.Unmarshal([]byte(jsonStr), &m1)
    fmt.Println(m1)
}
```

上述代码输出：
```
[map[resultcode:200]]
```

interface{}类型通过json.Unmarshal之后的类型，一句话总结：所有JSON数值类型一律解析为float64类型，需手动转换；对于map类型需判断是否为nil再转换为所需类型。

`interface{}`类型在`json.Unmarshal`时，会自动将JSON转换为对应的数据类型：

- JSON的`boolean` 转换为`bool`
- JSON的数值 转换为`float64`
- JSON的字符串 转换为`string`
- JSON的`Array` 转换为`[]interface{}`
- JSON的`Object` 转换为`map[string]interface{}`，也可以转为本身类型
- JSON的`null` 转换为`nil`

```
package main

import (
    "encoding/json"
    "fmt"
)

type Person struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
    Addr string `json:"addr,omitempty"`
}

func main() {
    var m map[string]interface{}     
    m = make(map[string]interface{}) //分配内存
    m["name"] = "simon"
    var age int = 12
    m["age"] = age
    m["addr"] = "China"
    fmt.Println(m)
    fmt.Println()

    data, _ := json.Marshal(m)

    m1 := make(map[string]interface{})
    _ = json.Unmarshal(data, &m1)
    fmt.Println(m1)
    fmt.Println()

    if m1["name"] != nil {
        fmt.Println(m1["name"].(string))
    }
    if m1["type"] != nil {
        fmt.Println(m1["type"].(string))
    } else {
        fmt.Println("there is not the key of type")
    }
    fmt.Println()

    p := Person{"simon", 22, "China"}
    data, _ = json.Marshal(p)
    p1 := Person{}
    _ = json.Unmarshal(data, &m1)
    _ = json.Unmarshal(data, &p1)
    fmt.Println("map m1:", m1)
    fmt.Println("person:", p1)
    fmt.Println(m1["name"], m1["age"], m1["addr"])
    fmt.Println(p1.Name, p1.Age, p1.Addr)
}
```

上述代码输出结果

```
map[addr:China age:12 name:simon]

map[addr:China age:12 name:simon]

simon
there is not the key of type

map m1: map[addr:China age:22 name:simon]
person: {simon 22 China}
simon 22 China
simon 22 China
```


[细说Golang的JSON解析](https://juejin.cn/post/6844903891344048141)

[学会用Go解析复杂JSON的思路](https://mp.weixin.qq.com/s?__biz=MzUzNTY5MzU2MA==&mid=2247484337&idx=1&sn=d43944a3ec55cfdd52b1513eb2133e86&chksm=fa80d226cdf75b308dc793c2730696f4f7842a81e1f0fffc4e9f496dc10dd43d09cbc055cc20&token=137161257&lang=zh_CN#rd)

[Go - 如何解析 JSON 数据？](https://segmentfault.com/a/1190000021487147)

[interface{}类型通过json.Unmarshal之后的类型](https://blog.csdn.net/Nick_666/article/details/79809358)

