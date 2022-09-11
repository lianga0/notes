# Memory Layout of C Programs

> Last Updated : 12 Oct, 2021

> https://www.geeksforgeeks.org/memory-layout-of-c-program/

A typical memory representation of a C program consists of the following sections.

1. Text segment  (i.e. instructions)
2. Initialized data segment 
3. Uninitialized data segment  (bss)
4. Heap 
5. Stack

一个典型的C程序存储分区包含以下几类：

1. Text段
2. 已初始化数据段
3. 未初始化数据段
4. 堆
5. 栈

<img src="imgs_memoryLayout/memoryLayoutC.jpg" alt="A typical memory layout of a running process
" />

A typical memory layout of a running process

## 1. Text Segment: 

A text segment, also known as a code segment or simply as text, is one of the sections of a program in an object file or in memory, which contains executable instructions.
As a memory region, a text segment may be placed below the heap or stack in order to prevent heaps and stack overflows from overwriting it. 
 

Usually, the text segment is sharable so that only a single copy needs to be in memory for frequently executed programs, such as text editors, the C compiler, the shells, and so on. Also, the text segment is often read-only, to prevent a program from accidentally modifying its instructions.

### 1. Text段

Text段通常也称为代码段，由可执行指令构成，是程序在目标文件或内存中的一部分，Text段通常放在栈或堆的下面，以防止堆栈溢出篡改其数据。

通常情况下，Text段是可共享的，对于需要频繁调用的程序，其在内存中只需要一份拷贝即可，如文本编辑器、C编译器、Shell等，因此text段通常设为只读以防止程序的突发性的修改。


## 2. Initialized Data Segment: 

Initialized data segment, usually called simply the Data Segment. A data segment is a portion of the virtual address space of a program, which contains the global variables and static variables that are initialized by the programmer.

Note that, the data segment is not read-only, since the values of the variables can be altered at run time.

This segment can be further classified into the initialized read-only area and the initialized read-write area.

For instance, the global string defined by `char s[] = “hello world”` in C and a C statement like `int debug=1` outside the main (i.e. global) would be stored in the initialized read-write area. And a global C statement like `const char* string = “hello world”` makes the string literal “hello world” to be stored in the initialized read-only area and the character pointer variable string in the initialized read-write area.

Ex: `static int i = 10` will be stored in the data segment and `global int i = 10` will also be stored in data segment


### 2. 已初始化数据段

已初始化数据段，通常简单称作数据段，数据段占据程序虚拟地址空间的一部分，内部包括全局变量、静态变量（程序负责初始化这些变量）。需注意的是，数据段不是只读的，在运行时变量值是可以变动的。

数据段还可以更细的分为初始化只读区以及初始化可读写区。

举例：全局字符串 char s[] = “hello world”，全局变量 int debug=1，静态变量 static int i = 10 存储在初始化可读写区；另一种情况下，const char* string = “hello world”，字符串“hello world”存储在初始化只读区，string指针则存在初始化可读写区。


## 3. Uninitialized Data Segment: 

Uninitialized data segment often called the **“bss”** segment, named after an ancient assembler operator that stood for **“block started by symbol.”** Data in this segment is initialized by the kernel to arithmetic `0` before the program starts executing

uninitialized data starts at the end of the data segment and contains all global variables and static variables that are initialized to zero or do not have explicit initialization in source code.

For instance, a variable declared `static int i;` would be contained in the BSS segment. 

For instance, a global variable declared `int j;` would be contained in the BSS segment.

### 3. 未初始化数据段

未初始化数据段，通常称作“bss”段，名字来源于古老的汇编操作符命名 “block started by symbol”，段内的数据在程序开始执行之前被内核初始化为0值，通常开始于已初始化数据段的末尾处。段内包含初始化为0的全局变量/静态变量以及源码中未显示进行初始化的变量。

举例：变量 static int i;  全局变量 int j;  包含在BBS段中。

## 4. Stack: 

The stack area traditionally adjoined the heap area and grew in the opposite direction; when the stack pointer met the heap pointer, free memory was exhausted. (With modern large address spaces and virtual memory techniques they may be placed almost anywhere, but they still typically grow in opposite directions.)

The stack area contains the program stack, a LIFO structure, typically located in the higher parts of memory. On the standard PC x86 computer architecture, it grows toward address zero; on some other architectures, it grows in the opposite direction. A “stack pointer” register tracks the top of the stack; it is adjusted each time a value is “pushed” onto the stack. The set of values pushed for one function call is termed a “stack frame”; A stack frame consists at minimum of a return address.

Stack, where automatic variables are stored, along with information that is saved each time a function is called. Each time a function is called, the address of where to return to and certain information about the caller’s environment, such as some of the machine registers, are saved on the stack. The newly called function then allocates room on the stack for its automatic and temporary variables. This is how recursive functions in C can work. Each time a recursive function calls itself, a new stack frame is used, so one set of variables doesn’t interfere with the variables from another instance of the function.

### 4. 栈

栈与堆是相互毗邻的，并且生长方向相反；当栈指针触及到堆指针位置，意味着栈空间已经被耗尽（如今地址空间越来越大，及虚拟内存技术发展，栈与堆可能放置在内存的任何地方，但生长方向依然还是相向的）。

栈区域包含一个LIFO结构的程序栈，其通常放置在内存的高地址处，在x86架构中，栈朝地址0方向生长，在其它架构也可能朝着相反的方向生长。栈指针寄存器跟踪栈顶位置，每当有数值被压入栈中，栈顶指针会被调整，在一个函数的调用过程中，压入的一系列数值被称作“栈帧”，栈帧至少包含一个返回地址。

栈存储着自动变量以及每次函数调用时保存的信息，每当函数被调用时，返回地址以及调用者的上下文环境例如一些机器寄存器都存储在栈中，新的被调用函数此时会在栈上重新分配自动/临时变量，这就是递归函数的工作原理。每当函数递归调用自己时，都会使用新的栈帧，因此当前函数实体内的栈帧内的变量不会影响另外一个函数实体内的变量。

## 5. Heap: 

Heap is the segment where dynamic memory allocation usually takes place.

The heap area begins at the end of the BSS segment and grows to larger addresses from there. The Heap area is managed by malloc, realloc, and free, which may use the brk and sbrk system calls to adjust its size (note that the use of `brk/sbrk` and a single “heap area” is not required to fulfill the contract of `malloc/realloc/free`; they may also be implemented using `mmap` to reserve potentially non-contiguous regions of virtual memory into the process’ virtual address space). The Heap area is shared by all shared libraries and dynamically loaded modules in a process.

### 5. 堆

堆通常用作动态内存分配，堆空间起始于BSS段的末尾，并向高地址处生长，堆空间通常由malloc, realloc 及 free管理，这些接口可能再使用`brk/sbrk`系统调用来调整大小，在一个进程中，堆空间被进程内所有的共享库及动态加载模块所共享。

## Examples.

The `size(1)` command reports the sizes (in bytes) of the text, data, and bss segments. ( for more details please refer man page of `size(1)` )

注：size命令以字节为单位统计可执行程序的text, data, 及bss段（更多详情参考man page of size(1)）

1. Check the following simple C program 

```
#include <stdio.h>
 
int main(void)
{
    return 0;
}
```

```
[narendra@CentOS]$ gcc memory-layout.c -o memory-layout
[narendra@CentOS]$ size memory-layout
text       data        bss        dec        hex    filename
960        248          8       1216        4c0    memory-layout
```

2. Let us add one global variable in the program, now check the size of bss (highlighted in red color).

```
#include <stdio.h>
 
int global; /* Uninitialized variable stored in bss*/
 
int main(void)
{
    return 0;
}
```

编译后观察变化，bss区域增加了4字节


```
[narendra@CentOS]$ gcc memory-layout.c -o memory-layout
[narendra@CentOS]$ size memory-layout
text       data        bss        dec        hex    filename
 960        248         12       1220        4c4    memory-layout
```


3. Let us add one static variable which is also stored in bss.


```
#include <stdio.h>
 
int global; /* Uninitialized variable stored in bss*/
 
int main(void)
{
    static int i; /* Uninitialized static variable stored in bss */
    return 0;
}
```

编译后再看变化，bss区域增加了4字节


```
[narendra@CentOS]$ gcc memory-layout.c -o memory-layout
[narendra@CentOS]$ size memory-layout
text       data        bss        dec        hex    filename
 960        248         16       1224        4c8    memory-layout
```

4. Let us initialize the static variable which will then be stored in the Data Segment (DS)


```
#include <stdio.h>
 
int global; /* Uninitialized variable stored in bss*/
 
int main(void)
{
    static int i = 100; /* Initialized static variable stored in DS*/
    return 0;
}
```

此时变量存储到了data段，data增加了4字节，bss减少了4字节

```
[narendra@CentOS]$ gcc memory-layout.c -o memory-layout
[narendra@CentOS]$ size memory-layout
text       data        bss        dec        hex    filename
960         252         12       1224        4c8    memory-layout
```

5. Let us initialize the global variable which will then be stored in the Data Segment (DS)

```
#include <stdio.h>
 
int global = 10; /* initialized global variable stored in DS*/
 
int main(void)
{
    static int i = 100; /* Initialized static variable stored in DS*/
    return 0;
}
```

此时静态变量也存储到了data段，data增加了4字节，bss减少了4字节


```
[narendra@CentOS]$ gcc memory-layout.c -o memory-layout
[narendra@CentOS]$ size memory-layout
text       data        bss        dec        hex    filename
960         256          8       1224        4c8    memory-layout
```

