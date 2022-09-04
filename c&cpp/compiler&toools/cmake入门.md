#cmake快速入门

# 从“Hello, world!”开始

> https://blog.csdn.net/kai_zone/article/details/82656964

第一步，我们给这个项目起个名字——就叫HELLO吧。因此，第一部为项目代码建立目录hello，与此项目有关的所有代码和文档都位于此目录下。

第二步，在hello目录下建立一个main.c文件，其代码如下：

```
#include<stdio.h>
int main(void)
{
    printf("Hello,World\n");
    return 0;
}
```
第三步，在hello目录下建立一个新的文件CMakeLists.txt，它就是 cmake所处理的“代码“。在CMakeLists.txt文件中输入下面的代码(#后面的内容为代码行注释)：

```
#cmake最低版本需求，不加入此行会受到警告信息
CMAKE_MINIMUM_REQUIRED(VERSION 2.6)
PROJECT(HELLO) #项目名称
#把当前目录(.)下所有源代码文件和头文件加入变量SRC_LIST
AUX_SOURCE_DIRECTORY(. SRC_LIST)
#生成应用程序 hello
ADD_EXECUTABLE(hello ${SRC_LIST})
```

至此，整个hello项目就已经构建完毕，可以进行编译了。

第四步，编译项目。

为了使用外部编译方式编译项目，需要先在目录hello下新建一个目录build(也可以是其他任何目录名)。现在，项目整体的目录结构为：

```
hello/
|– CMakeLists.txt
|– build /
|– main.c
```

在linux命令行下，首先进入目录build，然后运行命令(注：后面的“..”不可缺少)：

该命令使cmake检测编译环境，并生成相应的makefile。接着，运行命令make进行编译。编译后，生成的所有中间文件和可执行文件会在build目录下。 下面是我在ubuntu上的运行过程：

```
$ ls hello/
build  CMakeLists.txt  main.c
$ cd hello/build/
$ ls
$ cmake ..
– The C compiler identification is GNU
– The CXX compiler identification is GNU
– Check for working C compiler: /usr/bin/gcc
– Check for working C compiler: /usr/bin/gcc — works
– Detecting C compiler ABI info
– Detecting C compiler ABI info - done
– Check for working CXX compiler: /usr/bin/c++
– Check for working CXX compiler: /usr/bin/c++ — works
– Detecting CXX compiler ABI info
– Detecting CXX compiler ABI info - done
– Configuring done
– Generating done
– Build files have been written to: /home/kermit/Project/cmake/hello/build
$ make
Scanning dependencies of target hello
[100%] Building C object CMakeFiles/hello.dir/main.c.o
Linking C executable hello
$ ls
CMakeCache.txt CMakeFiles cmake_install.cmake hello Makefile
$ ./hello
Hello,World
```

上面，我们提到了一个名词，叫**外部编译方式**。其实，`cmake`还可以直接在当前目录进行编译，无须建立build目录。但是，这种做法会将所有生成的中间文件和源代码混在一起，而且cmake生成的makefile无法跟踪所有的中间文件，即无法使用`make distclean`命令将所有的中间文件删除。因此，我们推荐建立build目录进行编译，所有的中间文件都会生成在build目录下，需要删除时直接清空该目录即可。这就是所谓的外部编译方式。


# 处理多源文件目录的方法

CMake处理源代码分布在不同目录中的情况也十分简单。现假设我们的源代码分布情况如下:

```
project
├── CMakeLists.txt
├── main.c
└── src
    ├── CMakeLists.txt
    ├── test1.c
    └── test1.h
```

其中 src 目录下的文件要编译成一个链接库。

第一步，项目主目录中的 CMakeLists.txt，文件内容如下:

```
PROJECT(main)
CMAKE_MINIMUM_REQUIRED(VERSION 2.6) 
ADD_SUBDIRECTORY( src )
AUX_SOURCE_DIRECTORY(. DIR_SRCS)
# INCLUDE_DIRECTORIES(./src)
ADD_EXECUTABLE(main ${DIR_SRCS}  )
# TARGET_INCLUDE_DIRECTORIES(main PRIVATE ./src)
TARGET_LINK_LIBRARIES( main Test )
```

该文件中 `ADD_SUBDIRECTORY` 命令指明本项目包含一个子目录 src 。
命令 `TARGET_LINK_LIBRARIES` 指明可执行文件 main 需要连接一个名为Test的链接库 。

第二步，子目录中的 CmakeLists.txt，文件内容如下:

```
AUX_SOURCE_DIRECTORY(. DIR_TEST1_SRCS)
ADD_LIBRARY ( Test ${DIR_TEST1_SRCS})
```

在该文件中使用命令 `ADD_LIBRARY` 将 src 目录中的源文件编译为共享库。

第三步，执行 `cmake`

至此我们完成了项目中所有 `CMakeLists.txt` 文件的编写， 进入目录 project 中依次执行命令 `cmake .` 和 `make`即可。

在执行 `cmake` 的过程中,首先解析目录 project 中的 CMakeLists.txt ,当程序执行命令 `ADD_SUBDIRECTORY( src )` 时进入目录 src 对其中的 CMakeLists.txt 进行解析。

# 在工程中查找并使用其他程序库的方法

在开发软件的时候我们会用到一些函数库，这些函数库在不同的系统中安装的位置可能不同，编译的时候需要首先找到这些软件包的头文件以及链接库所在的目录以便生成编译选项。例如一个需要使用博克利数据库项目,需要头文件`db_cxx.h` 和链接库 `libdb_cxx.so` ,现在该项目中有一个源代码文件 `main.cpp` ，放在项目的根目录中。

第一步，程序库说明文件

在项目的根目录中创建目录 `cmake/modules/` ，在 `cmake/modules/` 下创建文件 `Findlibdb_cxx.cmake` ，内容如下：

```
01 MESSAGE(STATUS "Using bundled Findlibdb.cmake...")
02
03 FIND_PATH(
04   LIBDB_CXX_INCLUDE_DIR
05   db_cxx.h 
06   /usr/include/ 
07   /usr/local/include/ 
08   )
09 
10 FIND_LIBRARY(
11   LIBDB_CXX_LIBRARIES NAMES  db_cxx
12   PATHS /usr/lib/ /usr/local/lib/
13   )
```

文件 `Findlibdb_cxx.cmake` 的命名要符合规范: `FindlibNAME.cmake` ,其中`NAME` 是函数库的名称。`Findlibdb_cxx.cmake` 的语法与 `CMakeLists.txt` 相同。这里使用了三个命令： `MESSAGE` ， `FIND_PATH` 和 `FIND_LIBRARY`。

- 命令 `MESSAGE` 会将参数的内容输出到终端。

- 命令 `FIND_PATH` 指明头文件查找的路径，原型如下：

    `find_path(<VAR> name1 [path1 path2 ...])` 该命令在参数 `path*` 指示的目录中查找文件 `name1` 并将查找到的路径保存在变量 `VAR`中。文件第`3－8`行的意思是在 `/usr/include/` 和 `/usr/local/include/` 中查找文件`db_cxx.h` ,并将`db_cxx.h` 所在的路径保存在 `LIBDB_CXX_INCLUDE_DIR`中。

- 命令 `FIND_LIBRARY` 同 `FIND_PATH` 类似,用于查找链接库并将结果保存在变量中。文件第`10－13`行的意思是在目录 `/usr/lib/` 和 `/usr/local/lib/` 中寻找名称为 `db_cxx` 的链接库,并将结果保存在 `LIBDB_CXX_LIBRARIES`。

第二步, 项目的根目录中的 CmakeList.txt

```
01 PROJECT(main)
 
02 CMAKE_MINIMUM_REQUIRED(VERSION 2.6)
 
03 SET(CMAKE_SOURCE_DIR .)
 
04 SET(CMAKE_MODULE_PATH ${CMAKE_ROOT}/Modules ${CMAKE_SOURCE_DIR}/cmake/modules)
 
05 AUX_SOURCE_DIRECTORY(. DIR_SRCS)
 
06 ADD_EXECUTABLE(main ${DIR_SRCS})
 
0708 FIND_PACKAGE( libdb_cxx REQUIRED)
 
09 MARK_AS_ADVANCED(
 
10 LIBDB_CXX_INCLUDE_DIR
 
11 LIBDB_CXX_LIBRARIES
 
12 )
 
13 IF (LIBDB_CXX_INCLUDE_DIR AND LIBDB_CXX_LIBRARIES)
 
14 MESSAGE(STATUS "Found libdb libraries")
 
15 INCLUDE_DIRECTORIES(${LIBDB_CXX_INCLUDE_DIR})
 
16 MESSAGE( ${LIBDB_CXX_LIBRARIES} )
 
17 TARGET_LINK_LIBRARIES(main ${LIBDB_CXX_LIBRARIES}18 )
 
19 ENDIF (LIBDB_CXX_INCLUDE_DIR AND LIBDB_CXX_LIBRARIES)
```

在该文件中第4行表示到目录 `./cmake/modules` 中查找 `Findlibdb_cxx.cmake`，`8-19` 行表示查找链接库和头文件的过程。
第8行使用命令 `FIND_PACKAGE` 进行查找,这条命令执行后 `CMake` 会到变量 `CMAKE_MODULE_PATH` 指示的目录中查找文件 `Findlibdb_cxx.cmake` 并执行。
第13-19行是条件判断语句,表示如果 `LIBDB_CXX_INCLUDE_DIR` 和 `LIBDB_CXX_LIBRARIES` 都已经被赋值,则设置编译时到 `LIBDB_CXX_INCLUDE_DIR` 寻找头文件并且设置可执行文件 `main` 需要与链接库 `LIBDB_CXX_LIBRARIES` 进行连接。

第三步，执行 cmake

完成 `Findlibdb_cxx.cmake` 和 `CMakeList.txt`的编写后在项目的根目录依次执行`cmake .` 和 `make`可以进行编译，生成可执行程序`main`



# cmake命令 `aux_source_directory(dir var)`

> https://zhuanlan.zhihu.com/p/153990002

假设当前源代码目录下有如下文件：

```
$ ls
CMakeLists.txt
main.c
test1.c
test1.h
test2.c
test2.h
```

当同一目录下面，有多个源文件的时候，这个时候你一直手动往下面第三条命令里面添加源文件，那工作效率多低啊：

```
cmake_minimum_required(VERSION 2.8)

project(main)

add_executable(main main.c test1.c)
```

于是乎为了解决这种低效率的操作， cmake 提供了`aux_source_directory(dir var)`命令。接下来我们在CMakeLists.txt这样操作：

```
cmake_minimum_required(VERSION 2.8)

project(main)

aux_source_directory(. SRC_LIST)

add_executable(main ${SRC_LIST})
```

其中`aux_source_directory(. SRC_LIST)`表示是把当当前目录下的所有源文件都添加到源列表变量里面去，最后用`add_executable(main ${SRC_LIST})`把所有有用的源文件加工成目标文件`main`。不过这方法也有他的缺点，就是把当前目录下的源文件都添加到变量`SRC_LIST`，如果我们不需要一些没有用的文件（比如只要拿到所需的源文件就行），可以进行这样操作：

```
cmake_minimum_required(VERSION 2.8)

project(main)

set(SRC_LIST
        ./main.c
        ./test1.c
        ./test2.c
         )

add_executable(main ${SRC_LIST})
```

上面的例子中，我们会发现同一目录下源文件比较乱，所以在`cmake`里面可以采用把相同类型以及相关的源文件放到同一个目录，比如说，现在我在test目录下创建test1和test2两个目录文件，并同时把test1.c、test1.h、test2.c、test2.h分别放到这两个目录下去：

```
tree
├── CMakeLists.txt
├── main.c
├── test1
│   ├── test1.c
│   └── test1.h
└── test2
    ├── test2.c
    └── test2.h
```

然后这个时候要修改CMakeLists.txt里面的规则属性了：

```
cmake_minimum_required(VERSION 2.8)

project(main)

include_directories(test1 test2)
aux_source_directory(test1 SRC_LIST)
aux_source_directory(test2 SRC_LIST1)

add_executable(main main.c  ${SRC_LIST} ${SRC_LIST1})
```

然后编译输出，也是能够通过的。这里出现了一个新的命令：`include_directories`。该命令是用来向工程添加多个指定头文件的搜索路径，路径之间用空格分隔。

其实在实际开发工程中，一般会把源文件放到`src`目录下，把头文件放入到`include`文件下，生成的对象文件放入到`build`目录下，最终输出的`elf`文件会放到`bin`目录下，这样让人看起来一目了然。



# Cmake 进一步详细学习资料

[CMake Examples](https://github.com/ttroy50/cmake-examples)

[cmake-examples-Chinese](https://github.com/SFUMECJF/cmake-examples-Chinese)

[cmake快速入门](https://blog.csdn.net/kai_zone/article/details/82656964)
