# char 与 unsigned char的本质区别

> [char 与 unsigned char的本质区别](https://www.cnblogs.com/qytan36/archive/2010/09/27/1836569.html)

在C中，默认的基础数据类型均为`signed`，现在我们以`char`为例，说明`(signed) char`与`unsigned char`之间的区别 

首先在内存中，`char`与`unsigned char`没有什么不同，都是一个字节，唯一的区别是，`char`的最高位为符号位，因此`char`能表示-128~127, `unsigned char`没有符号位，因此能表示0~255，这个好理解，8个bit，最多256种情况，因此无论如何都能表示256个数字。

在实际使用过程种有什么区别呢？

主要是符号位，但是在普通的赋值，读写文件和网络字节流都没什么区别，反正就是一个字节，不管最高位是什么，最终的读取结果都一样，只是你怎么理解最高位而已，在屏幕上面的显示可能不一样。

但是我们却发现在表示`byte`时，都用`unsigned char`，这是为什么呢？

首先我们通常意义上理解，`byte`没有什么符号位之说，更重要的是如果将`byte`的值赋给`int`，`long`等数据类型时，系统会做一些额外的工作。

如果是`char`，那么系统认为最高位是符号位，而`int`可能是16或者32位，那么会对最高位进行扩展（注意，赋给`unsigned int`也会扩展）

而如果是`unsigned char`，那么不会扩展。

这就是二者的最大区别。

同理可以推导到其它的类型，比如`short`， `unsigned short`。等等

具体可以通过下面的小例子看看其区别


```
include <stdio.h>

void f(unsigned char v)
{
    char c = v;
    unsigned char uc = v;
    unsigned int a = c, b = uc;
    int i = c, j = uc;
    printf("----------------\n");
    printf("%%c: %c, %c\n", c, uc);
    printf("%%X: %X, %X\n", c, uc);
    printf("%%u: %u, %u\n", a, b);
    printf("%%d: %d, %d\n", i, j);
}

int main(int argc, char *argv[])
{
    f(0x80);
    f(0x7F); 
    return 0;
}
```

输出结果：

```
----------------
%c: ?, ?
%X: FFFFFF80, 80
%u: 4294967168, 128
%d: -128, 128
----------------
%c: , 
%X: 7F, 7F
%u: 127, 127
%d: 127, 127
```

由此可见，最高位若为0时，二者没有区别，若为0时，则有区别了。
