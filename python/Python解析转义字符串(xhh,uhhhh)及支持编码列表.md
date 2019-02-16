## Python解析 \x 和 \u 转义字符及支持编码列表

> 2019.2.16

Python中使用反斜杠来引入特殊的字节编码，我们称之转义序列。

如果Python没有作为一个合法的转义编码识别出在"\"后的字符，那么它就直接在最终的字符串中保留反斜杠。

Python 2.7

```
>>> x = "c:\py\code"
>>> x
'c:\\py\\code'
>>len(x)
10
>>> y = '\u2121'
>>> y
'\\u2121'
>>> len(y)
6
```

Python3.x

```
>>> x = "c:\py\code"
>>> x
'c:\\py\\code'
>>> len(x)
10
>>> y = '\u2121'
>>> y
'℡'
>>> len(y)
1
```


### \xHH转义

在处理日志时，往往会碰到文本文件中类似`AirStation\xC0\xDF\xC4\xEA \xC7\xA7\xBE\xDA\xA5\xA8\xA5\xE9\xA1\xBC<br>`的转义字符串。Python提供了快速将转义字符转化为原始字节的方法，示例代码如下：

Python 2.7

```
>>> x = "AirStation\\xC0\\xDF\\xC4\\xEA \\xC7\\xA7\\xBE\\xDA\\xA5\\xA8\\xA5\\xE9\\xA1\\xBC<br>"
>>> x
'AirStation\\xC0\\xDF\\xC4\\xEA \\xC7\\xA7\\xBE\\xDA\\xA5\\xA8\\xA5\\xE9\\xA1\\xBC<br>'
>>> len(x)
71
>>> y = x.decode("string-escape")
>>> y
'AirStation\xc0\xdf\xc4\xea \xc7\xa7\xbe\xda\xa5\xa8\xa5\xe9\xa1\xbc<br>'
>>> len(y)
29
>>> print(y.decode('EUC-JP')) # 我们知道Log中该字符串原始字节流对应的编码方式为EUC-JP
AirStation設定 認証エラー<br>
```

Python 3.x代码

```
>>> x = "AirStation\\xC0\\xDF\\xC4\\xEA \\xC7\\xA7\\xBE\\xDA\\xA5\\xA8\\xA5\\xE9\\xA1\\xBC<br>"
>>> x  # Python3字符串默认为Unicode字符串，我们假定获取到的字符串是这个样子的
'AirStation\\xC0\\xDF\\xC4\\xEA \\xC7\\xA7\\xBE\\xDA\\xA5\\xA8\\xA5\\xE9\\xA1\\xBC<br>'
>>> y = x.encode("ASCII")
>>> y  # 因为转义了，所以应该是可以用ASCII解码，从而转为字节序列（其实，latin_1编发方式来解码最贴切）。
b'AirStation\\xC0\\xDF\\xC4\\xEA \\xC7\\xA7\\xBE\\xDA\\xA5\\xA8\\xA5\\xE9\\xA1\\xBC<br>'
>>> z = y.decode("unicode_escape")
>>> z
'AirStationÀßÄê Ç§¾Ú¥¨¥é¡¼<br>'
>>> zz = z.encode("latin_1")
>>> zz
b'AirStation\xc0\xdf\xc4\xea \xc7\xa7\xbe\xda\xa5\xa8\xa5\xe9\xa1\xbc<br>'
>>> zzz = zz.decode("EUC-JP")
>>> zzz
'AirStation設定 認証エラー<br>'
>>> print(x.encode("ASCII").decode("unicode_escape").encode("latin_1").decode("EUC-JP"))
AirStation設定 認証エラー<br>
>>>
```

### unicode转义\uHHHH

Python2.x中，因为字符串默认并不是Unicode类型的，所以下面代码中，Python2.x处理"\uhhhh"有些小状况。样例代码如下：

```
>>> print(x)
\u2121
>>> x = '\u2121'
>>> print(x)
\u2121
>>> y = u'\u2121'
>>> print(y)
℡
>>> z = '\\u2121'  # 构建原始字符串
>>> z
'\\u2121'
>>> z.decode("unicode-escape")  # 解码Unicode转义字符序列
u'\u2121'
>>> print(z.decode("unicode-escape"))
℡
```

Python3.x中代码如下：

```
>>> x = '\u2121'
>>> print(x)
℡
>>> y = '\\u2121'
>>> y.encode('ASCII')
b'\\u2121'
>>> y.encode('ASCII').decode("unicode-escape")
'℡'
```

### Python decode支持的编码列表

Python的`codecs `模块是处理Python编码的基础模块，其官方文档中有列出Python支持的所有编码方式的名称。

> codecs — Codec registry and base classes

> This module defines base classes for standard Python codecs (encoders and decoders) and provides access to the internal Python codec registry which manages the codec and error handling lookup process.

Strings are stored internally as sequences of code points in range `0x0–0x10FFFF`. (See [PEP 393](https://www.python.org/dev/peps/pep-0393) for more details about the implementation.) Once a string object is used outside of CPU and memory, endianness and how these arrays are stored as bytes become an issue. As with other codecs, serialising a string into a sequence of bytes is known as encoding, and recreating the string from the sequence of bytes is known as *decoding*. There are a variety of different text serialisation codecs, which are collectivity referred to as [text encodings](https://docs.python.org/3/library/codecs.html#standard-encodings).

Reference:

[【整理】Python中，如何将反斜杠u类型（\uXXXX）的字符串，转换为对应的unicode的字符](https://www.crifan.com/python_decode_slash_u_unicode_escape_string_into_unicode_chars/)

[python解析 \x 和 \u "乱码"](https://blog.csdn.net/qyt0147/article/details/83214671)

[Get a list of all the encodings Python can encode to](https://stackoverflow.com/questions/1728376/get-a-list-of-all-the-encodings-python-can-encode-to)

[Python2.7 Standard Encodings](https://docs.python.org/2.7/library/codecs.html#standard-encodings)

[Python3.7 Encodings and Unicode](https://docs.python.org/3/library/codecs.html#encodings-and-unicode)