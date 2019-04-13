## 【python】lxml处理命名空间及在XPath查询时使用空命名空间


### XML 命名空间提供避免元素命名冲突的方法。

#### 命名冲突

在 XML 中，元素名称是由开发者定义的，当两个不同的文档使用相同的元素名时，就会发生命名冲突。

例如，下面这个 XML 文档携带着某个表格中的信息：

```
<table>
   <tr>
      <td>Apples</td>
      <td>Bananas</td>
   </tr>
</table>
```

而下面这个 XML 文档携带有关桌子的信息（一件家具）：

```
<table>
   <name>African Coffee Table</name>
   <width>80</width>
   <length>120</length>
</table>
```

假如这两个 XML 文档被一起使用，由于两个文档都包含带有不同内容和定义的 `<table>` 元素，就会发生命名冲突。

XML解析器无法确定如何处理这类冲突。

#### 使用前缀来避免命名冲突

此文档带有某个表格中的信息：

```
<h:table>
   <h:tr>
      <h:td>Apples</h:td>
      <h:td>Bananas</h:td>
   </h:tr>
</h:table>
```

此 XML 文档携带着有关一件家具的信息：

```
<f:table>
   <f:name>African Coffee Table</f:name>
   <f:width>80</f:width>
   <f:length>120</f:length>
</f:table>
```

现在，命名冲突不存在了，这是由于两个文档都使用了不同的名称来命名它们的 `<table>` 元素 (`<h:table>` 和 `<f:table>`)。

通过使用前缀，我们创建了两种不同类型的 `<table>` 元素。

#### 使用命名空间（Namespaces）

这个 XML 文档携带着某个表格中的信息：

```
<h:table xmlns:h="http://www.w3.org/TR/html4/" >
   <h:tr>
      <h:td>Apples</h:td>
      <h:td>Bananas</h:td>
   </h:tr>
</h:table>
```

此 XML 文档携带着有关一件家具的信息：

```
<f:table xmlns:f="http://www.w3school.com.cn/furniture">
   <f:name>African Coffee Table</f:name>
   <f:width>80</f:width>
   <f:length>120</f:length>
</f:table>
```

与仅仅使用前缀不同，我们为 `<table>` 标签添加了一个 `xmlns` 属性，这样就为前缀赋予了一个与某个命名空间相关联的限定名称。


#### XML Namespace (xmlns) 属性

XML 命名空间属性被放置于元素的开始标签之中，并使用以下的语法：

```
xmlns:namespace-prefix="namespaceURI"
```

当命名空间被定义在元素的开始标签中时，所有带有相同前缀的子元素都会与同一个命名空间相关联。

> 注释：用于标示命名空间的地址不会被解析器用于查找信息。其惟一的作用是赋予命名空间一个惟一的名称。不过，很多公司常常会作为指针来使用命名空间指向实际存在的网页，这个网页包含关于命名空间的信息。

更多详细内容请访问 [HTML 4.01 Specification -W3C Recommendation 24 December 1999 superseded 27 March 2018](http://www.w3.org/TR/html4/)。

#### 统一资源标识符（Uniform Resource Identifier (URI)）

统一资源标识符是一串可以标识因特网资源的字符。最常用的 URI 是用来标示因特网域名地址的统一资源定位器(URL)。另一个不那么常用的 URI 是统一资源命名(URN)。

#### 默认的命名空间（Default Namespaces）

为元素定义默认的命名空间可以让我们省去在所有的子元素中使用前缀的工作。

请使用下面的语法：

```
xmlns="namespaceURI"
```

这个 XML 文档携带着某个表格中的信息：

```
<table xmlns="http://www.w3.org/TR/html4/">
   <tr>
      <td>Apples</td>
      <td>Bananas</td>
   </tr>
</table>
```

此 XML 文档携带着有关一件家具的信息：

```
<table xmlns="http://www.w3school.com.cn/furniture">
   <name>African Coffee Table</name>
   <width>80</width>
   <length>120</length>
</table>
```

众所周知，XmlDocument可以进行XPath查询，但实际上这里所说的XPath查询仅限于没有命名空间（没有xmlns属性）的XML，一旦遇到有命名空间的XML，对应XPath查询都会无结果。Python中lxml库提供的XPath查询同样如此。

比如下面这个XML

```
<a xmlns="mgen.cnblogs.com">
    <b>ccc</b>
</a>
```
 
XPath查询*/a/b*会返回null，而如果没有xmlns的话，会返回节点b。

为什么会这样呢？MSDN的相应函数有解释（参考：http://msdn.microsoft.com/en-us/library/system.xml.xmlnode.selectsinglenode.aspx）

> If the XPath expression does not include a prefix, it is assumed that the namespace URI is the empty namespace. If your XML includes a default namespace, you must still add a prefix and namespace URI to the XmlNamespaceManager; otherwise, you will not get any nodes selected

意思就是如果XPath表达式没有加前缀（如*namespace-prefix:tag-a*中前缀是*namespace-prefix*），那么所查询节点（注意属性也可以是节点）的命名空间URI就应该是空值（也是默认值，没有xmlns属性），否则XPath不会返回结果。

上面的XML, 因为节点*a*和*b*实际上都有命名空间值，自然XPath查询不会有结果。（上面英文还提到如果节点有默认命名空间，那么还得手动向XmlNamespaceManager添加前缀和命名空间值，这个在后面会讲的）

在看解决方案前，首先需要能够辨识XML命名空间，当然辨识XML命名空间值还是很容易的，参考如下XML（这个XML在后面程序中也会用到）

```
<?xml version="1.0" encoding="utf-8"?>
<root xmlns="dotnet" xmlns:w="wpf">
  <a>data in a</a>                
  <w:b>data in b</w:b>         
  <c xmlns="silverlight">
    <w:d>                             
      <e>data in e</e>              
    </w:d>
  </c>
</root>
```

它的所有XML节点的命名空间如下所示：

```
<?xml version="1.0" encoding="utf-8"?>
<root xmlns="dotnet" xmlns:w="wpf">       <!-- xmlns: dotnet -->
    <a>data in a</a>                        <!-- xmlns: dotnet -->
    <w:b>data in b</w:b>                    <!-- xmlns: wpf -->
    <c xmlns="silverlight">                 <!-- xmlns: silverlight -->
        <w:d>                                  <!-- xmlns: wpf -->
            <e>data in e</e>                     <!-- xmlns: silverlight -->
        </w:d>
    </c>
</root>
```

如果识别XML命名空间没有问题，那么后面的操作就相当简单了，你需要记住：**在XmlDocument中用XPath查询某一节点时，只要它的命名空间值不是空值，那么你必须给它一个前缀， 用这个前缀代表这个节点的命名空间值！**这些前缀是通过XmlNamespaceManager类添加的，使用时将XmlNamespaceManager 传入SelectNodes或SelectSingleNode中即可。这也是为什么上面说“如果节点有默认命名空间，那么还得手动向 XmlNamespaceManager添加前缀和命名空间值”的原因。 

下面我们步入代码，比如说查询上面XML中的节点e，分析位置节点e位于：root->c->d->e，然后将所需命名空间值加入到 XmlNamespaceManager中(前缀名称无所谓，只要在XPath一致即可)，查询即可成功，如下代码：

```
/*
  * 假设上面XML文件在C:\a.txt中
  * 下面代码会查询目标节点e，并输出数据：data in e
  * */
var xmlDoc = new XmlDocument();
xmlDoc.Load(@"C:\a.txt");
//加入命名空间和前缀
var xmlnsm = new XmlNamespaceManager(xmlDoc.NameTable);
xmlnsm.AddNamespace("d", "dotnet");
xmlnsm.AddNamespace("s", "silverlight");
xmlnsm.AddNamespace("w", "wpf");

var node = xmlDoc.SelectSingleNode("/d:root/s:c/w:d/s:e", xmlnsm);
Console.WriteLine(node.InnerText);

//输出：data in e
```

### python lxml处理命名空间

#### 查看xml的tag

```
# encoding=utf8
from lxml import etree
str_xml = """
<A xmlns="http://This/is/a/namespace">
    <B>dataB1</B>
    <B>dataB2</B>
    <B>
        <C>dataC</C>
    </B>
</A>
"""

xml = etree.fromstring(str_xml)
for node in xml.iter():
    print node.tag
```

运行结果为：

```
{http://This/is/a/namespace}A
{http://This/is/a/namespace}B
{http://This/is/a/namespace}B
{http://This/is/a/namespace}B
{http://This/is/a/namespace}C
```

可以看到，跟普通xml的tag相比每个tag前面都多出了一个命名空间。

#### xmlns命名空间

```
from lxml import etree

str_xml = """
<A xmlns="http://This/is/a/namespace">
    <B>dataB1</B>
    <B>dataB2</B>
    <B>
        <C>dataC</C>
    </B>
</A>
"""

xml = etree.fromstring(str_xml)
ns = xml.nsmap
print ns
print ns[None]
```

运行结果为：

```
{None: 'http://This/is/a/namespace'}
http://This/is/a/namespace
```

ns[None]获取的是默认命名空间，ns会显示所有的命名空间

#### 在XPath中使用默认命名空间

从上述例子中可以看到，python的lxml库使用None做为默认命名空间的Key，但由于Python语法的限制，不能在XPath的查询字符串中指定None，所以需要像如下代码一样进行处理：

```
import lxml.etree as et

str_xml = """
<A xmlns="http://This/is/a/namespace">
    <B>dataB1</B>
    <B>dataB2</B>
    <B>
        <C>dataC</C>
    </B>
</A>
"""

ns = {"default-namespace": "http://This/is/a/namespace"}
tree = et.fromstring(str_xml)
for node in tree.xpath('//default-namespace:C', namespaces=ns):
    print(node)

# or use this method
for node in tree.xpath("//*[local-name() = 'C']"):
    print(node)
```

运行结果为：

```
<Element {http://This/is/a/namespace}C at 0x202593509c8>
<Element {http://This/is/a/namespace}C at 0x202593509c8>
```

也可以参照：http://lxml.de/xpathxslt.html#namespaces-and-prefixes.

#### 在findall中使用默认命名空间


```
import lxml.etree as et

str_xml = """
<A xmlns="http://This/is/a/namespace">
    <B>dataB1</B>
    <B>dataB2</B>
    <B>
        <C>dataC</C>
    </B>
</A>
"""

tree = et.fromstring(str_xml)
for item in tree.findall('{http://This/is/a/namespace}B'): 
    print(item)
```

运行结果为：

```
<Element {http://This/is/a/namespace}B at 0x1dc61a34a08>
<Element {http://This/is/a/namespace}B at 0x1dc61a34a88>
<Element {http://This/is/a/namespace}B at 0x1dc61a34ac8>
```

Reference: [XML 命名空间（XML Namespaces）介绍以及节点读取方法](https://blog.csdn.net/yi412/article/details/70158876)

[【python】lxml处理命名空间](https://www.cnblogs.com/dplearning/p/5954005.html)

[how do I use empty namespaces in an lxml xpath query?](https://stackoverflow.com/questions/8053568/how-do-i-use-empty-namespaces-in-an-lxml-xpath-query)