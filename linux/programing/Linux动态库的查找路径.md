### Linux动态库的查找路径

> 黑翼天使23

前两天写了一个动态库，然后试图编译到程序里面去运行，结果发现编译的时候通过gcc的-L参数来指定路径仅仅能让编译通过，运行时还是会出问题的。

比如下面这个例子：

main.c是主程序，sum.c中间含有一个函数add，用来执行加法，代码如下：

```
// main.c
#include <stdio.h>
int add(int a, int b);
int main(int argc,char *argv[])
{
    printf("sum = %d\n", add(3,5));
    return 0;
}
```

```
// sum.c
int add(int a, int b)
{
    return a + b;
}
```

出错结果如下所示：

```
$ ls
main.c  sum.c
$ gcc -o libsum.so -shared -fPIC sum.c
$ ls
libsum.so  main.c  sum.c
$ gcc -o bin main.c -L . -lsum
$ ls
bin  libsum.so  main.c  sum.c
$ ./bin 
./bin: error while loading shared libraries: libsum.so: cannot open shared object file: No such file or directory
```

我在编译的时候通过-L指定了查找动态库的位置，结果运行的时候还是找不到我自己写的那个libsum.so这个动态库，后来去查了一下，才明白其中原委。

程序在链接动态库的时候分为2步，编译时链接和运行时链接。

#### 1. 编译时链接

这个过程是由ld程序来执行的，所以编译时找不到动态库的位置的话，经常就会看到这种错误：

```
/usr/bin/ld: cannot find -lsum
collect2: error: ld returned 1 exit status
```

这个过程严格意义上来说并不能说是链接，因为在这里ld程序并没有真正的把库里面的函数的执行代码写到可执行文件里面，只是把一些符号还有其他的必要信息写道了可执行文件里面，供可执行文件运行时查找。

总的来说，ld在这一步里面就是做了两个事情：

1. 查找动态库中是否含有我们需要的符号（函数和全局变量），如果都能找到，则链接允许通过，生成了可执行文件。

2. 在可执行文件中写入了符号和其他必要的信息（例如符号的地址），供可执行文件运行时查找。

#### 2. 运行时链接

这个过程是由ld-linux.so程序来执行，这个才是真正的链接。它所做的工作就是将动态库的代码映射到进程（可执行文件运行起来就是进程啦...）的虚拟地址空间中，供进程来调用。

关于链接，加载，运行的更多信息可以参看[C编译器、链接器、加载器详解](http://www.cnblogs.com/oubo/archive/2011/12/06/2394631.html)。

OK，明白了上面两个链接之后，我们再来看这两个链接查找动态库的目录位置，如下：

#### 运行时，ld-linux.so查找共享库的顺序

（1）ld-linux.so.6在可执行的目标文件中被指定的路径，可用`readelf`命令查看。`gcc`编译时使用Linker Options中的-Wl,option的选项`-Wl,-rpath`进行指定，例如`gcc -o bin main.c -L . -lsum -Wl,-rpath=.`。

（2）ld-linux.so.6缺省在`/usr/lib`和`/lib`中搜索；当glibc安装到/usr/local下时，它查找`/usr/local/lib`

（3）LD_LIBRARY_PATH环境变量中所设定的路径 

（4）/etc/ld.so.conf（或/usr/local/etc/ld.so.conf）中所指定的路径，由ldconfig生成二进制的ld.so.cache中

另一篇文章[Linux下so动态库查看与运行时搜索路径的设置](https://blog.csdn.net/renwotao2009/article/details/51398739)中介绍的共享库的查找顺序如下：

（1）LD_RUN_PATH设置的路径

（2）链接器使用-rpath或-R选项设置的路径

（3）LD_LIBRARY_PATH设置的路径

（4）/etc/ld.so.conf配置的路径

（5）/usr/lib/和 /lib/

其中LD_RUN_PATH和链接器使用-rpath或-R选项都是设置可执行文件中的Library rpath。

#### 编译时，ld-linux.so查找共享库的顺序

（1）ld-linux.so.6由gcc的spec文件中所设定

（2）gcc --print-search-dirs所打印出的路径，主要是libgcc_s.so等库。可以通过GCC_EXEC_PREFIX来设定

（3）LIBRARY_PATH环境变量中所设定的路径，或编译的命令行中指定的-L /usr/local/lib

（4）binutils中的ld所设定的缺省搜索路径顺序，编译binutils时指定。（可以通过`ld --verbose | grep SEARCH`来查看）

（5）二进制程序的搜索路径顺序为PATH环境变量中所设定。一般/usr/local/bin高于/usr/bin

（6）编译时的头文件的搜索路径顺序，与library的查找顺序类似。一般/usr/local/include高于/usr/include


> 大家注意编译时查找的路径可以通过gcc -L参数或者LIBRARY_PATH来指定，但是运行时的查找路径却不包含gcc -L和LIBRARY_PATH环境变量指定的路径，所以这样就会出现我们刚开始所说的那个问题，编译时通过-L指定了动态库的搜索路径，编译也通过了，但是运行时却会报错，这是因为运行时查找动态库的路径还没指定，所以我们自己写的动态库就找不到了，而要解决这个问题，通过设置环境变量LD_LIBRARY_PATH或者修改`/etc/ld.so.conf`（记得修改完了运行`ldconfig`来生成ld.so.cache）就可以了。

### ldd命令

linux 下可以使用ldd查看可执行文件所需要的动态链接库（*.so）。 

例如，上述例子中编译的bin文件需要的动态链接库如下：

```
ldd bin 
        linux-vdso.so.1 (0x00007fffdf3c3000)
        libsum.so => ./libsum.so (0x00007f612b49c000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f612b0ab000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f612b8a0000)
```

如果我们自定义的库显示如下，那么说明ldd命令没有找到对应的共享库文件和其具体位置。

```
libsum.so => not found
```

一般可能是以下两种情况引起的，我们根据之前介绍，修改配置信息或安装相应的共享库。

1）共享库没有安装在该系统中；

2）共享库所在的位置不在系统配置的搜索路径中。


FROM:

[Linux动态库的查找路径](https://www.cnblogs.com/bwangel23/p/4695342.html)

[Linux动态库(.so)搜索路径设置方法](https://blog.csdn.net/chenycbbc0101/article/details/54893027)

[C编译器、链接器、加载器详解](http://www.cnblogs.com/oubo/archive/2011/12/06/2394631.html)

[Linux下so动态库查看与运行时搜索路径的设置](https://blog.csdn.net/renwotao2009/article/details/51398739)

[gcc/ld: what is to -Wl,-rpath in dynamic linking what -l is to -L in static linking?](https://stackoverflow.com/questions/33373851/gcc-ld-what-is-to-wl-rpath-in-dynamic-linking-what-l-is-to-l-in-static-link)