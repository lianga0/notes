## python解析XML时ExpatError: not well-formed (invalid token)错误

> 2018.10.30

python解析从网络上爬取的数据时，总是出现如下错误：

```
ExpatError: not well-formed (invalid token): line 85, column 0
ExpatError: not well-formed (invalid token): line 55, column 13
```

经过搜索，问题原因在于：爬取数据中包含非法字符（XML规范中定义的无效字符）。如`^@, ^Y`等

> From: https://www.w3.org/TR/xml/#charsets

Character Range

```
[2]     Char       ::=      #x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD] | [#x10000-#x10FFFF]  /* any Unicode character, excluding the surrogate blocks, FFFE, and FFFF. */
```

The mechanism for encoding character code points into bit patterns may vary from entity to entity. All XML processors must accept the UTF-8 and UTF-16 encodings of Unicode;

xml中需要过滤的字符分为两类，一类是不允许出现在xml中的字符，这些字符不在xml的定义范围之内。另一类是xml自身要使用的字符，如果内容中有这些字符则需被替换成别的字符。
 
### 不允许出现在XML中的字符

对于这类字符，我们可以通过W3C的XML文档来查看都有哪些字符不被允许出现在xml文档中。
XML允许的字符范围是```#x9 | #xA | #xD | [#x20-#xD7FF] | [#xE000-#xFFFD] | [#x10000-#x10FFFF]```。因此我们可以把这个范围之外的字符过滤掉。

需要过滤的字符的范围为：

```
\\x00-\\x08
\\x0b-\\x0c
\\x0e-\\x1f
```

### xml自身要使用的字符

xml自身要使用的字符一共有5个，如下：

```
字符                HTML字符        字符编码
逻辑与  &           &amp;           &#38;
单引号  '           &apos;          &#39;
双引号  "           &quot;          &#34;
大于号  >           &gt;            &#62;
小于号  <           &lt;            &#60;
```

我们只需要对这个五个字符，进行相应的替换就可以了
 
### 解决上述问题的方法：
 
用正则表达式剔除非法字符即可，如正则表达式 [\\x00-\\x08\\x0b-\\x0c\\x0e-\\x1f]。

From： [xml中的非法字符](https://www.cnblogs.com/Impulse/p/4018720.html)

### 非法字符其他情况，处理非格式良好的XML：

除上述字符外，有时仍然可能出现非法字符（如字符串解码不匹配，或其他异常情况），可以使用`lxml.etree.XMLParser(recover=True) `的recover参数，尽最大努力解析XML。具体代码如下：

```
from lxml import etree
parser = etree.XMLParser(recover=True) 
root = etree.parse(sys.argv[1], parser=parser) 
```

Reference: [Extensible Markup Language (XML) 1.0 (Fifth Edition)](https://www.w3.org/TR/xml/)

[如何使用Python处理lxml中的转义字符串](https://stackoverrun.com/cn/q/3612929)