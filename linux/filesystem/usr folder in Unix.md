### `usr` folder in Unix?

> 2018.04.01

#### 1. `usr` history

`usr` are holdover from Unix. Memory and disk space was in short supply. Hacking out a few vowels and other abbreviations gave real savings. A few disk blocks or a few bytes could mean the difference in being able to run a program or not. 

In the original Unix implementations, `/usr` was where the home directories of the users were placed (that is to say, /usr/someone was then the directory now known as /home/someone). In current Unices, `/usr` is where user-land programs and data (as opposed to 'system land' programs and data) are. The name hasn't changed, but it's meaning has narrowed and lengthened from "everything user related" to "user usable programs and data". As such, some people may now refer to this directory as meaning `User System Resources` and not `user` as was originally intended.

Some people on stackexchange also says the same thing. At the time `/usr` was coined, its meaning was user and home directories were located there. `unix/universal system resource` is actually a backronym.


很多linux初学者都会误认为`/usr`为user的缩写，最早`/usr`产生时，这么讲可能是正确的。但是，目前Unix中`usr`是`Unix Software Resource` 或 `unix/universal system resource` 或 `User System Resources` 的缩写， 也就是"Unix操作系统软件资源"所放置的目录，而不是用户的数据！


#### 2. what's in `usr`

`/usr` usually contains the largest share of data on a system. Hence, this is one of the most important directories in the system as it contains all the user binaries, their documentation, libraries, header files, etc.... X Window System and its supporting libraries can be found here. User programs like telnet, ftp, etc.... are also placed here. 

> `/usr` is shareable, read-only data. That means that `/usr` should be shareable between various FHS-compliant hosts and must not be written to. Any information that is host-specific or varies with time is stored elsewhere.

> Large software packages must not use a direct subdirectory under the `/usr` hierarchy.


`/usr/bin/`    

> 绝大部分的用户可使用指令都放在这里！请注意到他与`/bin`的不同之处。(是否与开机过程有关)。

`/usr/include/`    

> c/c++等程序语言的头部(header)与包含档(include)放置处，当我们以tarball方式 (\*.tar.gz 的方式安装软件)安装某些数据时，会使用到里面的许多头部文件。


`/usr/lib/`    

> 包含各应用软件的函式库、目标文件(object file)，以及不被一般使用者惯用的执行档或脚本(script)。 某些软件会提供一些特殊的指令来进行服务器的设定，这些指令也不会经常被系统管理员操作， 那就会被摆放到这个目录下啦。要注意的是，如果你使用的是X86_64的Linux系统， 那可能会有/usr/lib64/目录产生！

`/usr/local/`    

> 系统管理员在本机自行安装自己下载的软件(非distribution默认提供者)，建议安装到此目录， 这样会比较便于管理。举例来说，你的distribution提供的软件较旧，你想安装较新的软件但又不想移除旧版， 此时你可以将新版软件安装于`/usr/local/`目录下，这样就可与原先的旧版软件区别开来。 你可以到`/usr/local`下看看，该目录下也是具有bin, etc, include, lib…的次目录。

`/usr/sbin/`    

> 非系统正常运作所需要的系统指令。最常见的就是某些网络服务器软件的服务指令(daemon)！

`/usr/share/`    

> 放置共享文件的地方，在这个目录下放置的数据几乎是不分硬件架构均可读取的数据， 因为几乎都是文本文件！在此目录下常见的还有这些次目录：

`/usr/share/man`

> 联机帮助文件

`/usr/share/doc`

> 软件杂项的文件说明

`/usr/share/zoneinfo`

> 与时区有关的时区文件

`/usr/src/`

>一般源码软件建议放置到这里，src有source的意思。

Reference:

[Why do /usr and /tmp directories for Linux miss vowels in their spellings?](https://unix.stackexchange.com/questions/8677/why-do-usr-and-tmp-directories-for-linux-miss-vowels-in-their-spellings)

[Linux Filesystem Hierarchy: Chapter 1. Linux Filesystem Hierarchy](http://www.tldp.org/LDP/Linux-Filesystem-Hierarchy/html/usr.html)

[2.8 Linux下/usr目录和/var目录的含义和内容](https://coderschool.cn/641.html)
