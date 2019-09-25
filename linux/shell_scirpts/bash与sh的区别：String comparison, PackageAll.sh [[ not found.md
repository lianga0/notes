## bash与sh的区别：String comparison, PackageAll.sh: [[: not found

> 2018.08.16

由于要支持个新的业务，server中某个之前使用Zip打包的特定资源，必须使用tar打包（因为新平台没有解压Zip包的工具）。所以，我决定修改CI的脚本，将这个包额外使用tar打包一份，脚本如下：

```
        if [[ $nmap_folder == *nmap-7.12* ]] ; then
            tar -cf ${nmap_folder}_hk.zip $nmap
            cp -f ${nmap_folder}_hk.zip $DrServerDst/config/client/
            rm -f ${nmap_folder}_hk.zip
        fi
```

自己在Ubuntu上测试可以正常工作，但是到Build机器上之后，build失败，查找错误信息，发现如下细节：

```
[[: not found
```

Google后发现： Linux中shell有多种具体实现软件。 \[\[ 是`bash`的内部命令（buildin），而在dash中却不是。 

```
[[ is a bashism, ie built into Bash and not available for other shells. 
If you want your script to be portable, use [. 
Comparisons will also need a different syntax: change == to =.
```

碰巧脚本中没有指定使用哪个shell，所出现测试能工作，到Build机器上就不能通过的情况。也就是说写shell脚本时，需要考虑到具体的执行环境。下面是Ubuntu16.04 LTS上的差异

```
$ ls -al /bin/bash
-rwxr-xr-x 1 root root 1037528 5月  16  2017 /bin/bash

$ ls -al /bin/sh
lrwxrwxrwx 1 root root 4 4月  25 09:46 /bin/sh -> dash

$ /bin/bash --version
GNU bash, version 4.3.48(1)-release (x86_64-pc-linux-gnu)
Copyright (C) 2013 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>

This is free software; you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

$ /bin/sh --version
/bin/sh: 0: Illegal option --
```

解决方案，在脚本开头指定bash的路径`#!/bin/bash` or `#!/bin/sh`。

### shell基本知识：

用户在命令行输入命令后，一般情况下Shell会fork并exec该命令，但是Shell的内建命令例外，执行内建命令相当于调用Shell进程中的一个函数，并不创建新的进程。

比如:cd、alias、umask、exit等命令即是内建命令，凡是用which命令查不到程序文件所在位置的命令都是内建命令，内建命令没有单独的man手册，要在man手册中查看内建命令，应该`man bash-builtins`，进而查找内建命令用法；内建命令虽然不创建新的进程，但也会有Exit Status，通常也用0表示成功非零表示失败，虽然内建命令不创建新的进程，但执行结束后也会有一个状态码，也可以用特殊变量$?读出。

Reference: [String comparison in bash. \[\[: not found](https://stackoverflow.com/questions/12230690/string-comparison-in-bash-not-found/12230723)

[什么是Bash Shell的内建(build in)命令](https://blog.csdn.net/wxqian25/article/details/20634437)