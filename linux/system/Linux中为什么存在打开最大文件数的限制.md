### Linux中为什么存在最大打开文件数的限制

Linux系统中`/proc/sys/fs/file-max `文件指定了可以分配的文件句柄的最大数目。

```
[root@localhost home]# cat /proc/sys/fs/file-max 
100966
```

这表明这台Linux系统最多允许同时打开(即包含所有用户打开文件数的总和)100966个文件，是Linux系统级的硬限制，所有用户级的打开文件数限制都不应超过这个数值。通常这个系统级的硬限制是Linux系统在启动时根据系统硬件资源状况计算出来的最佳参数。如果没有特殊需要，不应该修改此限制，除非想为用户级打开文件数限制设置超过此限制的值。这个参数的默认值是跟内存大小有关系的，增加物理内存以后重启机器，这个值会增大。大约1G内存10万个句柄的线性关系。

`ulimit -n`命令可显示每个进程所允许打开的最大文件数，该限制对root用户不生效。

##### 那么操作系统为什么要设置一个最大可打开的文件数限制呢？简单的说是因为计算机内存有限。操作系统需要为每一个打开的文件分配一定的内存来完成必要的管理工作，然而内存是有限的资源（特别对于嵌入式系统而言）。另外，出于安全性考虑，操作系统存在最大可打开文件数限制，可防止出现某一进程意外耗尽系统资源的情况。


如果用户程序得到的错误消息声明，类似于”too many open files”，这是由于打开文件数已经达到了最大值，从而他们不能打开更多文件，此时可能需要增加该值。作为root用户，可以根据实际需求修改最大打开文件数限制。

#### 查看系统已经打开的文件句柄数

`lsof | wc -l` 获得的系统打开文件总数往往偏大，因为它可能包含一些重复的文件（比如，fork的进程会共享打开的文件句柄）。使用下面命令，从Linux内核的视图中获取系统当前打开的文件总数更为精准。

```
cat /proc/sys/fs/file-nr
```

例如：服务器在65536最大打开文件数的限制下打开40096个文件，而`lsof`命令简单统计获得的数字明显超出许多

```
# cat /proc/sys/fs/file-max
65536
# cat /proc/sys/fs/file-nr 
40096   0       65536
# lsof | wc -l
521504
```

#### 如何查看某一程序打开的文件数：`lsof -p pid`

```
[root@localhost ~]# lsof -p 1812|wc -l
163
[root@localhost ~]# lsof -p 1827|wc -l
150
```
#### 查看某一程序最大可打开文件数：`cat /proc/pid/limits`

```
[root@alille-654-1-41-1 bin]# ps -ef|grep -i "ProxyServer"
root     12091 12083 99 10:25 pts/0    05:32:45  proxyserver
[root@alille-654-1-41-1 bin]# cat /proc/12091/limits 
Max open files            65535                65535                files
```

Reference：

[Why is number of open files limited in Linux?](https://unix.stackexchange.com/questions/36841/why-is-number-of-open-files-limited-in-linux)

[Linux 打开文件数1024限制的原理以及解决办法](http://ityunwei2017.blog.51cto.com/7662323/1558092)
