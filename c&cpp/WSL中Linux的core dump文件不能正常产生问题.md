# WSL中Linux的core dump文件不能正常产生

> 2021.12.28

在linux下开发时，如果程序突然崩溃了，也没有任何日志。这时可以查看core文件。从core文件中分析原因，通过gdb看出程序挂在哪里，分析前后的变量，找出问题的原因。

## Core Dump

当程序运行的过程中异常终止或崩溃，操作系统会将程序当时的内存状态记录下来，保存在一个文件中，这种行为就叫做Core Dump（中文有的翻译成“核心转储”)。我们可以认为 core dump 是“内存快照”，但实际上，除了内存信息之外，还有些关键的程序运行状态也会同时 dump 下来，例如寄存器信息（包括程序指针、栈指针等）、内存管理信息、其他处理器和操作系统状态和信息。core dump 对于编程人员诊断和调试程序是非常有帮助的，因为对于有些程序错误是很难重现的，例如指针异常，而 core dump 文件可以再现程序出错时的情景。

## 系统是否可以产生core dump文件的相关配置

在一些Linux版本下，默认是不产生core文件的。

首先可以查看一下系统core文件的大小限制：

```
ulimit -c
```

如果输出0，那么说明系统禁止生成core dump文件。
下面命令可以临时修改配置允许产生core dump文件，系统重启后配置就丢失了。

```
ulimit -c unlimited
```

### 需要此设置一直生效需要做如下设置

```
vim /etc/profile       #然后进入编辑模式，在profile文件中加入
ulimit -c unlimited
```

保存退出，重启服务器或者`source /etc/profile`不重启服务器，使用source使文件马上生效。

### 指定生成文件的路径和名字

默认情况下，core dump生成的文件名为core，而且就在程序当前目录下。新的core会覆盖已存在的core, 通过修改/proc/sys/kernel/core_uses_pid文件，可以控制core文件保存位置和文件格式。

```
vim /etc/sysctl.conf                 # 进入编辑模式，加入下面两行

kernel.core_pattern=/tmp/core_dump_%t_%e_%p
kernel.core_uses_pid=0
```

使用`sysctl -p /etc/sysctl.conf`命令让修改马上生效。

core_pattern的命名参数如下：

```
%c 转储文件的大小上限
%e 所dump的文件名
%g 所dump的进程的实际组ID
%h 主机名
%p 所dump的进程PID
%s 导致本次coredump的信号
%t 转储时刻(由1970年1月1日起计的秒数)
%u 所dump进程的实际用户ID
```

配置完成后使用命令`kill -s SIGSEGV $$`, 测试是否正确在配置路径下产生core dump文件。

# Windows WSL中的Ubuntu `ulimit -c unlimited`配置不生效问题

在使用WSL中运行的Ubuntu20.04LTS调试程序时，发现即使配置`ulimit -c unlimited`后，依然不会在运行程序的目录下产生core dump文件。

经过一圈查找，发现这是WSL实现的BUG，在WSL 2中运行的Ubuntu20.04LTS使用相同的配置项即可产生core dump文件。

> reference: [Core dump file is unavailable #1262](https://github.com/microsoft/WSL/issues/1262)

> > Under the fast ring feature WSL2 (Ubuntu 18.04.3 LTS), the core dump file appeared.

> > However, it appeared as an empty file in the working folder. Fortunately, the post on stackoverflow comes to rescue.

> > (see Empty [core dump file after Segmentation fault](https://stackoverflow.com/questions/13403824/empty-core-dump-file-after-segmentation-fault#comment18496435_13411054))

> > Use `sysctl` to set `/proc/sys/kernel/core_pattern=/tmp/core`

> > `sudo sysctl -w kernel.core_pattern=/tmp/core`

> > Now, the command `gdb` with core dump file works as expected.

> > `gdb ./testCoreDump /tmp/core`

> > I think it is the best workaround I can find now.



[Linux下core dump](https://www.cnblogs.com/s-lisheng/p/11278193.html)

[Linux 生成 core dump的方法及设置](https://www.cnblogs.com/flyinggod/p/13415862.html)

[Empty core dump file after Segmentation fault](https://stackoverflow.com/questions/13403824/empty-core-dump-file-after-segmentation-fault#comment18496435_13411054)
