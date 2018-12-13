## Linux下动态库so文件的一些认识

> 匡子语

通常情况下，对函数库的链接是放在编译时期（compile time）完成的。所有相关的对象文件（object file）与牵涉到的函数库（library）被链接合成一个可执行文件（executable file）。程序在运行时，与函数库再无瓜葛，因为所有需要的函数已拷贝到自己门下。所以这些函数库被成为静态库（static libaray），通常文件名为“libxxx.a”的形式。

其实，我们也可以把对一些库函数的链接载入推迟到程序运行的时期（runtime）。这就是如雷贯耳的动态链接库（dynamic link library）技术。

### 动态链接库的特点与优势

首先让我们来看一下，把库函数推迟到程序运行时期载入的好处：

1. 可以实现进程之间的资源共享。

某个程序的在运行中要调用某个动态链接库函数的时候，操作系统首先会查看所有正在运行的程序，看在内存里是否已有此库函数的拷 贝了。如果有，则让其共享那一个拷贝；只有没有才链接载入。这样的模式虽然会带来一些“动态链接”额外的开销，却大大的节省了系统的内存资源。C的标准库 就是动态链接库，也就是说系统中所有运行的程序共享着同一个C标准库的代码段。

2. 将一些程序升级变得简单。用户只需要升级动态链接库，而无需重新编译链接其他原有的代码就可以完成整个程序的升级。Windows 就是一个很好的例子。

3. 甚至可以真正坐到链接载入完全由程序员在程序代码中控制。

程序员在编写程序的时候，可以明确的指明什么时候或者什么情况下，链接载入哪个动态链接库函数。你可以有一个相当大的软件，但每次运行的时候，由于 不同的操作需求，只有一小部分程序被载入内存。所有的函数本着“有需求才调入”的原则，于是大大节省了系统资源。比如现在的软件通常都能打开若干种不同类 型的文件，这些读写操作通常都用动态链接库来实现。在一次运行当中，一般只有一种类型的文件将会被打开。所以直到程序知道文件的类型以后再载入相应的读写

### .so文件是什么

Linux下的`.so`文件是基于Linux下的动态链接，其功能和作用类似与windows下.dll文件。so其实就是shared object的意思。`.so`文件也是ELF(Executable and Linkable Format,可执行连接格式)格式文件，类似于DLL。可以节约资源，加快速度，简化代码升级。

### ELF文件格式分析

ELF全称Executable and Linkable Format,可执行连接格式，ELF格式的文件用于存储Linux程序。ELF文件（目标文件）格式主要三种：

- 可重定向文件：文件保存着代码和适当的数据，用来和其他的目标文件一起来创建一个可执行文件或者是一个共享目标文件。（目标文件或者静态库文件，即linux通常后缀为.a和.o的文件）

- 可执行文件：文件保存着一个用来执行的程序。（例如bash，gcc等）
共享目标文件：共享库。文件保存着代码和合适的数据，用来被下连接编辑器和动态链接器链接。（linux下后缀为.so的文件。）

- 目标文件既要参与程序链接又要参与程序执行：

一般的 ELF 文件包括三个索引表：ELF header，Program header table，Section header table。

- ELF header：在文件的开始，保存了路线图，描述了该文件的组织情况。

- Program header table：告诉系统如何创建进程映像。用来构造进程映像的目标文件必须具有程序头部表，可重定位文件不需要这个表。

- Section header table：包含了描述文件节区的信息，每个节区在表中都有一项，每一项给出诸如节区名称、节区大小这类信息。用于链接的目标文件必须包含节区头部表，其他目标文件可以有，也可以没有这个表。

进入终端输入`cd /usr/include`进入include文件夹后查看`elf.h`文件，查看ELF的文件头包含整个文件的控制结构。使用`readelf –a executable_file_name`命令，可以查看ELF文件的ELF Header头信息。

### 怎么生成以及使用一个so动态库文件? 

先写一个C文件：s.c 

```
#include <stdio.h>  
int count;  
void out_msg(const char *m)  
{//2秒钟输出1次信息，并计数  
     for(;;) {printf("%s %d\n", m, ++count); sleep(2);}  
}
```

编译：得到输出文件libs.o 

```
gcc -fPIC -g -c s.c -o libs.o 
```

----------------------------------------------------------------------

`-fPIC`:  -fPIC作用于编译阶段，告诉编译器产生与位置无关代码(Position-Independent Code)，则产生的代码中，没有绝对地址，全部使用相对地址，故而代码可以被加载器加载到内存的任意 位置，都可以正确的执行。这正是共享库所要求的，共享库被加载时，在内存的位置不是固定的。

`-g`:  令 gcc 生成调试信息,该选项可以利用操作系统的“原生格式（native format）”生成调试信息。GDB 可以直接利用这个信息，其它调试器也可以使用这个调试信息

`-c`:  仅执行编译操作，不进行连接操作。
`-o`:  指定生成的输出文件名称 


----------------------------------------------------------------------
链接：得到输出文件libs.so 

```
gcc -g -shared -Wl,-soname,libs.so -o libs.so libs.o -lc 
```

-----------------------------------------------------------------------

上述语句中 libs.o是输入文件

`-shared`:  

　　Produce a shared object which can then be linked with other objects to form an executable. Not all systems support this option. For predictable results, you must also specify the same set of options used for compilation (-fpic, -fPIC, or model suboptions) when you specify this linker option.

`-Wl`: 注意第二个字母是小写的L，不是I　

　　Pass option as an option to the linker. If option contains commas, it is split into multiple options at the commas. You can use this syntax to pass an argument to the option. For example, -Wl,-Map,output.map passes -Map output.map to the linker. When using the GNU linker, you can also get the same effect with -Wl,-Map=output.map.

`-soname`:

　　soname的关键功能是它提供了兼容性的标准：

　　当要升级系统中的一个库时，并且新库的soname和老库的soname一样，用旧库链接生成的程序使用新库依然能正常运行。这个特性使得在Linux下，升级使得共享库的程序和定位错误变得十分容易。

　　在Linux中，应用程序通过使用soname，来指定所希望库的版本，库作者可以通过保留或改变soname来声明，哪些版本是兼容的，这使得程序员摆脱了共享库版本冲突问题的困扰。

`-lc`:

　　-l 是直接加上某库的名称,如-lc是libc库 -L 是库的路径,搜索的时候优先在-L目录下搜索

------------------------------------------------------------------------

一个头文件:s.h 

```
#ifndef _MY_SO_HEADER_  
#define _MY_SO_HEADER_  
void out_msg(const char *m);  
#endif 
```

再来一个C文件来引用这个库中的函数:ts.c 

```
 #include <stdio.h>  
 #include "s.h"  
 int main(int argc, char** argv)  
 {  
  　　printf("TS Main\n");  
  　　out_msg("TS ");  
  　　sleep(5);  //这句话可以注释掉，在第4节的时候打开就可以。  
 　　 printf("TS Quit\n");  
 }  
```

编译链接这个文件：得到输出文件ts 

```
gcc -g ts.c -o ts -L. -ls 
```

执行./ts,嗯：成功了。。。还差点 
得到了ts:error while loading shared libraries: libs.so: cannot open shared object file: No such file or directory 
系统不能找到我们自己定义的libs.so，那么告诉他，修改变量`LD_LIBRARY_PATH`，为了方便，写个脚本:ts.script

```
export LD_LIBRARY_PATH=${pwd}:${LD_LIBRARY_PATH} 
./ts
```

执行：`./ts.script & `

屏幕上就开始不停有信息输出了，当然TS Quit你是看不到的，前面是个死循环，后面会用到这句 

----------------------

& 放在启动参数后面表示设置此进程为后台进程。默认情况下，进程是前台进程，这时就把Shell给占据了，我们无法进行其他操作，对于那些没有交互的进程，很多时候，我们希望将其在后台启动，可以在启动参数的时候加一个'&'实现这个目的。

----------------------

### 地址空间，以及线程安全：

如果这样：

`./ts.script &`开始执行后，稍微等待一下然后再`./ts.script&`，这个时候屏幕信息会怎么样呢？全局变量count会怎么变化？

会是两个进程交叉输出信息，并且各自的count互不干扰，虽然他们引用了同一个so文件。 

也就是说只有代码是否线程安全一说，没有代码是否是进程安全这一说法。

### 库的初始化，解析

windows下的动态库加载，卸载都会有初始化函数以及卸载函数来完成库的初始化以及资源回收，linux当然也可以实现。 

ELF文件本身执行时就会执行一个`_init()`函数以及`_fini()`函数来完成这个，我们只要把自己的函数能让系统在这个时候执行，就可以了。 

修改我们前面的s.c文件： 

 
```
#include <stdio.h>  
 void my_init(void) __attribute__((constructor)); //告诉gcc把这个函数扔到init section  
 void my_fini(void) __attribute__((destructor));  //告诉gcc把这个函数扔到fini section  
 void out_msg(const char *m)  
 {  
  printf(" Ok!\n");   
 }  
 int i; //仍然是个计数器  
 void my_init(void)  
 {  
  printf("Init ... ... %d\n", ++i);  
 }  
 void my_fini(void)  
 {  
  printf("Fini ... ... %d\n", ++i);  
 }  
```

重新制作 libs.so，ts本是不用重新编译了，代码维护升级方便很多。 

然后执行: `./ts.script & `，可以看到屏幕输出：(不完整信息，只是顺序一样) 

```
Init 
Main 
OK 
Quit 
Fini
```

可以看到我们自己定义的初始化函数以及解析函数都被执行了，而且是在最前面以及最后面。 
如果s.c中的`sleep(5)`没有注释掉，那么有机会： 

`./ts.script&`连续执行两次，那么初始化函数和解析函数也会执行两次，虽然系统只加载了一次libs.so。 
如果sleep时候kill 掉后台进程，那么解析函数不会被执行。 

[【linux】linux下动态库so文件的一些认识](https://www.cnblogs.com/dplearning/p/5770650.html)

[linux第三次实践：ELF文件格式分析](https://www.cnblogs.com/cdcode/p/5551649.html)

[关于linux下的.a文件与 .so 文件](https://www.cnblogs.com/luntai/p/5291354.html)