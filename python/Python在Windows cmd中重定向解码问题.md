## Python在Windows cmd中重定向解码问题

### 问题

Python3在Windows平台中的CMD中使用重定向时，会出现`illegal multibyte sequence`问题。

非常简单的Python3代码如下：

```
print("中国☀ ")
```

在CMD中以命令`python t.py > t.txt`运行会出现如下错误：

```
Traceback (most recent call last):
  File "t.py", line 1, in <module>
    print("中国☀ ")
UnicodeEncodeError: 'gbk' codec can't encode character '\u2600' in position 2: illegal multibyte sequence
```

### 解决方案

为Windows的CMD添加环境变量`PYTHONIOENCODING`即可。

> PYTHONIOENCODING
If this is set before running the interpreter, it overrides the encoding used for stdin/stdout/stderr, in the syntax `encodingname:errorhandler`. Both the `encodingname` and the `:errorhandler` parts are optional and have the same meaning as in `str.encode().`

For stderr, the `:errorhandler` part is ignored; the handler will always be `'backslashreplace'`.

Changed in version 3.4: The encodingname part is now optional.

Changed in version 3.6: On Windows, the encoding specified by this variable is ignored for interactive console buffers unless `PYTHONLEGACYWINDOWSSTDIO` is also specified. Files and pipes redirected through the standard streams are not affected.

相关问题：

## 解决Python在windows平台默认编码(encoding)为gbk所导致的open()函数报错及其他编码问题

> From: https://juejin.im/post/5bd2b6d5e51d45735c3c0453

在windows平台下使用python3内置函数 open() 时发现，当不传递encoding参数时，会自动采用gbk(cp936)编码打开文件，而当下很大部分文件的编码都是UTF-8。

我们当然可以通过每次手动传参encoding='utf-8'，但是略显冗余，而且有很多外国的第三方包，里面调用的内置open()函数并没有提供接口让我们指定encoding，这就会导致这些包在windows平台上使用时，常会出现如 "UnicodeDecodeError: 'gbk' codec can't decode byte 0x91 in position 209: illegal multibyte sequence" 的报错

通过查看python文档分析原因：

> if encoding is not specified the encoding used is platform dependent: locale.getpreferredencoding(False) is called to get the current locale encoding. (For reading and writing raw bytes use binary mode and leave encoding unspecified.)

可以发现当open不传递encoding参数时，是默认调用`locale.getpreferredencoding()`方法来获取当前平台的“默认编码类型”,继续查看相关文档，发现有两种方法可以指定windows平台下Python运行时的“默认编码类型”。

1. 指定`sys.flags.utf8_mode`(推荐)
通过运行脚本是添加命令行参数 `-X utf8`（注意是跟在python.exe后面的interpreter option,不是跟在要运行脚本后面的parameters!）
指定`sys.flags.utf8_mode`参数之后，Python运行时会在很多场景下自动使用utf-8编码，而不是win默认的gbk(cp936)编码。

2. 直接重写_locale(兼容老版本)

```
import _locale
_locale._getdefaultlocale = (lambda *args: ['en_US', 'utf8'])
```

复制代码python解释器会取`_getdefaultlocale()[1]`作为默认编码类型，重写后，会改变当前运行环境下的所有模块的默认编码。

总之，使用以上两种方法后，windows平台下，open()函数会默认用utf-8编码打开文件，其实不止open()方法，跨模块、全局改变python解释器的默认编码为utf-8,会带来很多使用上的便利，而不需要被gbk编码报错的噩梦所纠缠。

Reference:

[解决Python在windows平台默认编码(encoding)为gbk所导致的open()函数报错及其他编码问题](https://juejin.im/post/5bd2b6d5e51d45735c3c0453)

[从根本解决python3 open的UnicodeDecodeError: 'gbk' codec问题](https://blog.csdn.net/blmoistawinde/article/details/87717065)