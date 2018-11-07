### python json.dumps 参数详解

```
json.dumps(obj, skipkeys=False, ensure_ascii=True, check_circular=True, allow_nan=True, cls=None, indent=None, separators=None, encoding="utf-8", default=None, sort_keys=False, **kw)
```

通过转换表将`obj`对象序列化为一个JSON格式的字符串（str）。

> 注意：因为JSON的key/value键值对中key的取值必须总是字符串。当Python中的字典序列化为JSON时，字典中所有的key都将被强制转化为string类型。所有，当把一个字典转化为JSON格式的字符串，而后再使用该结果字符串反序列化出Python的字典对象，新字典对象可能与原始字典对象并不相等，即`loads(dumps(x)) != x if x has non-string keys`。

**如果`ensure_ascii`的值为`false`，那么结果可能包含非ASCII字符，所以`json.dumps`返回值可能是一个`unicode`对象。** 如果`ensure_ascii`的值为`true`（默认值），那么所有待返回的非ASCII字符都会被转义为`\uXXXX`序列，最终`json.dumps`返回的是一个仅包含ASCII字符的`str`对象。

`encoding`参数指示`json.dumps`解析`obj`对象中的str实例时所使用的编码类型，默认值为`utf-8`。而不是指示`json.dumps`返回字符串的编码类型。`json.dumps`返回结果字符串的编码由`ensure_ascii`参数控制，结果要么是转义后的ASCII字符串，否则就是`unicode`对象。

例如，如下样例代码可说明上述两个参数的效果：
```
#coding:utf-8
import json

origin_str = "移动"
unicode_str = origin_str.decode("utf-8")
gbk_str = unicode_str.encode("gbk")
x = {
    "uft-8": origin_str,
    "gbk": gbk_str
}

y = json.dumps(x, encoding="gbk")
print type(y)
print y

z = json.dumps(x, ensure_ascii=False, encoding="gbk")
print type(z)
print z
```

windows 10中Python 2.7输出结果如下：

```
<type 'str'>
{"uft-8": "\u7ec9\u8bf2\u59e9", "gbk": "\u79fb\u52a8"}
<type 'unicode'>
{"uft-8": "绉诲姩", "gbk": "移动"}
```

<完>