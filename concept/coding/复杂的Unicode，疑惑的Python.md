### 复杂的Unicode，疑惑的Python

> 2011-12-03 00:04:30

> From: http://blog.chinaunix.net/uid-7570132-id-3033204.html

Python 3000决定采用Unicode作为字符的默认编码。这不是什么新闻了，也是国际化的大势所趋。但实际上似乎没有那么简单。最近python-dev邮件列表吵的一个问题就很有意思。

7月2日，一个叫Jeroen Ruigrok van der Werven的人以UCS2/UCS4 default 为标题说了问题。Python虽然采用unicode作为默认字符，但语言内部用什么方法表示unicode字符串并没有一致的规定。在编译的时候可以选择用UCS2或者UCS4编码。作者说，随着unicode中的CJK象形字扩展B（CJK ideographs extension B)已经加入最新的unicode规范，扩展C已经在投票表决阶段，扩展D已经在开发，使用UCS2编码已经不能满足预期未来的应用了。所以应该默认使用UCS4编码。而且作者认为允许UCS2和UCS4两种编码会产生编程一致性的问题。比如，在用UCS2编码的python 3中：

```
len("\N{MUSICAL SYMBOL G CLEF}")
2
```

而在用USC4编码中的python 3中：

```
len("\N{MUSICAL SYMBOL G CLEF}")
1
```

然后这个问题就引起了一场大混战。这个问题到底是什么问题呢？到底为什么会允许那么奇怪的事情发生：同一个字符串在不同的编译版本中长度不一样呢？其实这个问题根植在unicode复杂的规范和历史中。

Unicode的一个中文名字叫“万国码”。这个翻译很明确指出了Unicode的任务，为人类使用的文字都编一个号码，解决他们在计算机中共存的问题，消除计算机世界里面万码奔腾的兼容性问题。现在unicode 5.1规范已经于2008-04-04发布，而且也确实很大部分消除了计算机世界里面兼容问题，成为了事实规范。现在哪个稍大的新程序不支持Unicode，是说不过去的。不过这不表示unicode里面没有什么犄角旮旯影响着大家的使用。

##### 第一个问题是，unicode到底要给什么编号？

对中文来说，当然是给字编号——在中文里面是这样，但unicode并不是中文编码，这个世界的书写文字五花八门，中文概念里面的字在其他书写文字里面并不一定存在。在这里要澄清的两个概念是glyph和character。Glyph是文字的图像，是我们书写的最小单元，是屏幕上看到的，打印机上打出来的最小单元。Character是一种逻辑上和语言学上的描述，它并不完全等同于Glyph。Glyph和Character之间有多种组合发生。一种情况是一个Glyph代表多个character。举中文里面的多音字说明，比如“没”字，它有两个读音，而且意义完全不一样，但只有一个表现形式。“没”代表着一个glyph，代表着两个character。如果再加上日语和韩语，这种同一个glyph却有多个character的情况就更多了。还有一个情况是多个character才能组成一个glyph。主要是一些字母的音调问题。中文里面也有这个问题，比如“e”和“ˊ”这两个character可以组成一个glyph“é”。还有一种我们不太熟悉的情况是多个glyph只是一个character，主要出现在阿拉伯文中。在阿拉伯文中，一个字母在不同的书写情况下可能有不同的表现形式（glyph）。还有一种情况是，character没有对应的glyph，比如我们常见的回车符。事实上，unicode并没有给出一个标准的说法说明到底给什么编号，它走的是务实主义。Unicode大致可以说的是给character编号，但也会照顾到各种语言的现实，会给glyph编号。对于编程，一个简单的计算字符串长度就会发生歧义。到底我们是计算unicode字符串的character数量还是glyph数量？在ascii编码中没有这个问题，因为它的character和glyph是统一的。Unicode解决这个问题的方法是不仅仅给character编号，还给每个character编订了unicode character property。软件可以计算character数量，也可以根据character查询属性，用于计算和显示glyph。

##### 第二个问题是，unicode到底打算使用多少个编号？

现在的Unicode使用了21bit的数字去编号。目前看来21bit在可预见的将来是足够使用的——除非人类发现了外星人文明，需要为他们编号。现在的unicode编号从0x0-0x10FFFF分为17个Plane，编号从0-16。从0x0-0xFFFD为BMP（Basic Multilingual Plane)，也就是前16bit，集中了大多现代书写系统；从0x10000-0x1FFFD为SMP（Supplementary Mulitilingual Plane），包括了大多在历史上曾经使用的书写系统；从0x20000-0x2FFFD为SIP（Supplementary Ideographic Plane），用于每年新增加的象形文字；然后11个plane尚未使用；Plane 14（0xE0000-0xEFFFD）为SSP（Supplementary Special-Purpose Plane），存放一些争议性比较大的字符（语义上比较模糊或者会给文字处理带来麻烦），使用这些字符都需要多加小心；后面两个Plane 15（0xF0000-0xFFFFD)和Plane 16（0x100000-0x10FFFD）为保留区，任何人都可以私自定义这个区域，当然Unicode规范也不保证这些区域可以在异构系统上顺利交换。还有一个特殊字符编号0xFEFF是BOM（Byte Order Mark），包括它对判断Byte Order有特殊用途，所以它的另外一面0xFFFE也就被规定为非Unicode字符（也就是为什么Plane的结束都是0xFFFD的原因）。上面的说法看起来没有什么太大的问题，但这不是故事的全部。最开始的Unicode只打算用16bit的数字，也就是现在的BMP去实现它的目的，这个跟当年的兼容和效率考量有关。但这显然是不够的，尤其对于庞大的CJK象形文字——至今Unicode已经包含了7万多个CJK象形文字。这是个不幸的历史。所以早期的Unicode实现中，并没有考虑到16bit以外的问题。比如大量使用的Windows和Java构建的系统。Unix系统倒是塞翁失马焉知非福，对Unicode的支持比较晚，所以大多都是用32bit去表示21bit的unicode编号。历史的悲剧就这么产生了，虽然都是Unicode，但历史遗留系统和现代系统的不同表示还是给所有希望实现Portability的应用带来尴尬的处境。Python的UCS2/UCS4问题就是其中之一，但这不是造成这个问题的全部原因，还有下一个原因。

##### 第三个问题是，unicode到底是什么？

这是个很严肃的问题。Unicode只是字符编号，字符编号的属性，以及相关说明的集合。Unicode不是平常所说的编码（Encoding）。Unicode规范只是规定了每个字符的编号（Code Point)。虽然它是为计算机设计的规范，但这个编号和计算机如何存储，如何表示这些字符没有直接关系。在这一层，叫做CCS（Coded Character Set）。理论上如何表示Unicode字符是应用程序的自由，喜欢怎么表示就怎么表示，只要你的表示方法能找到字符对应的Code Point就行。当然，大家不能让这种混乱出现，所以有了CEF（Character Encoding Form）这一层。这一层关注的是在计算机理论上如何从数字到映射Code Point，也就是如何在8bit为单位的计算机系统中表示21bit的Unicode Code Point。其中UCS2，UCS4，UTF32，UTF16，UTF8等等都是实际上使用的方案。理论上映射和实践上映射不完全一样，实践上还要考虑异构系统的可交换特性，也就是解决大小端问题的CES（Character Encoding Scheme）。所以又会有UTF32-LE，UTF32-BE，UTF16-BE，UTF16-LE，UTF8。还有最后一层，是TES（Transfer Encoding Syntax）。这一层解决的问题是在特定传输环境中的编码问题，比如把UTF8字符串再用base64编码用于电子邮件传输。跟Python有关的是CEF这一层。前面说过，历史上Unicode的code point是16bit的，所以无论是UCS2，UCS4，UTF32，UTF16，UTF8都可以相安无事。对于前四者来说，都是一个code unit对应一个code point（code unit是CEF的最小单位，对于UCS4和UTF32是32bit，对于UCS2和UTF16是16bit，对于UTF8是8bit）；对于UTF8来说是1到3个code unit对应一个code point。这时候的UCS4和UTF32是等价的，UCS2和UTF16是等价的。后来unicode扩展为21位了。对于UCS4和UTF32来说，还是一个code unit对应一个code point，对应用程序来说变化不大。而对于UTF8来说，变成了1-4个code unit对应一个code point（为什么是扩展到21bit这么奇怪的数字呢？我猜测是为了UTF8的效率，因为UTF8中4个code unit正好最多可以表示21bit的code point），因为UTF8本来就是长度可变的编码，问题也不大。但对UCS2和UTF16来说，问题就比较头疼了。UCS2和UTF16本来是固定长度编码，但现在无论如何也不可能用16bit的存储表示21bit的code point。UCS2和UTF16在这里就分道扬镳了。UCS2的处理方法很暴力，只保留低16位信息，忽略高5位的信息，也就是只兼容BMP中的code point。而UTF16就变成了可变长度编码。解决方法是在BMP中划分出两个保留区域，分别是0xD800-0xDBFF的High Surrogate Area和0xDC00-0xDFFF的Low Surrogate Area。编码方案是，假如有一个大于0xFFFF的code point是X，那么让Y=X-0x10000；Y显然是介于0x00和0xFFFFF之间的20bit数据（这也就是为什么unicode虽然扩展到21bit，但只有17个plane——理论上21bit可以表示32个plane）。假如Y这个数字的分隔为高10bit和低10bit（假如是xxxxxxxxxxyyyyyyyyyy)，那么X的UTF16编码110110xxxxxxxxxx 110111yyyyyyyyyy，正好落在Surrogate Area里面。就这样UTF16变成了长度可变编码。用Python表示就是：

```
high = ((X-0x10000)>>10)&0x3FF+0xD800low = (X-0x10000)&0x3FF+0xDC00
```

但对使用UTF16编码的程序来说，一个字符串的code point数量（也就是unicode character的数量）和code unit的数量不再是恒等的——如果代码里面曾经简单的恒等这两个数量，代码就出错了。

回到Python的问题上，由于历史原因，现有的系统即有使用UCS2（Windows，Java——Java从1.5开始改为支持UTF16）也有使用UCS4（Unix/Linux)的。为了在各个系统上的最大兼容性，Python的Unicode字符串在内存中的表示方式一直都有两种，在编译的时候指定（有--with-wide-unicode的时候用UCS4)。对于同一个不在BMP范围内的字符"\N{MUSICAL SYMBOL G CLEF}"，UCS4的Python内部表示成一个UCS4 code unit，计算长度的时候自然就是等于一，因为code unit的数量和code point的数量是恒等的；但UCS2的Python为了不丢失信息，首先用UTF16的编码方式把不在BMP范围内的字符编码成两个UTF16 code unit，但计算长度的时候，返回的是code unit的数量，而不是code point的数量！所以邮件列表上有人说，UCS2的Python用UTF16的编码处理了字符输入，又按照UCS2的方式在内部使用。UCS2和UTF16之间的混淆不清大概就是这个问题的根源。

平心而论，UTF16并不是一个糟糕的编码。它的优点是对于大多常用的字符（在BMP范围内的）更紧凑，无论是分割字符，计算字符，都和UTF32一样。但问题就在于不是BMP范围内的字符。要以code point为单位处理这些字符的UTF16编码需要更复杂和低效的算法，比如随机访问字符串中的某个字符从O(1)变成了O(N)。Java也是有这个问题的语言，它曾经是UCS2，但从1.5开始，增加了一套处理UTF16字符的API（String.codePointCount / String.codePointAt / String.codePointBefore / String.offsetByCodepoints）。所以在Java中，原来的代码会保持原来的UCS2处理方式，当你要使用超过BMP范围的字符时，可以使用新的API处理；这样在兼容和正确处理之间找一个妥协方案。但Python由于用了两种内部表示方案，问题就变得更复杂。程序员不仅要注意到code unit和code point的区别，还要注意到UCS4和UCS2中的code unit区别。

邮件列表中争吵到最后的结果大概是在文档中增加对这些区别的说明，同时增加一套新的API用于按照code point为单位处理（假如有人做的话），并不改变旧有的API的行为(isalpha之类的API可以改变，因为不影响兼容性）。跟现实世界javascript:void(0)一样，历史问题总是不能完美解决的。

最后推荐一本书，O'REILLY出版的[Fonts & Encoding](https://www.amazon.com/dp/0596102429)，前半部分关于unicode的讨论可以学到不少关于unicode的知识。
转载：http://jawahh.sjtubbs.org/2008/07/unicodepython.html
