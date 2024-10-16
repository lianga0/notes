## Linux 常用命令

### zip命令指定待压缩文件列表

```
zip 压缩后文件名 文件名1 文件名2 ...
zip -r 压缩后文件名 文件夹名1 文件夹名2 ... //-r 表示rescue 递归
```

从标准输入读取文件，`-@`放在压缩后文件名前后都可以

```
echo "文件名1
文件名2" | zip -@ test.zip
```

若zip命令不存在，可以使用`sudo apt install zip`命令安装


### file命令用来探测给定文件的类型。

file命令对文件的检查分为文件系统、魔法幻数检查和语言检查3个过程。

### hexdump命令查看文件十六进制编码

hexdump命令一般用来查看“二进制”文件的十六进制编码，但实际上它能查看任何文件，而不只限于二进制文件。

### tail显示文件中的尾部内容

tail命令默认在屏幕上显示指定文件的末尾10行。如果给定的文件不止一个，则在显示的每个文件前面加一个文件名标题。如果没有指定文件或者文件名为“-”，则读取标准输入。

tail常用参数 -f, --follow[={name|descriptor}] 显示文件最新追加的内容(output appended data as the file grows)

### stat查看文件或文件系统的属性

stat 可以查看文件或文件系统的创建、修改和最后访问时间、文件权限等

```
stat .bashrc
  File: .bashrc
  Size: 3771            Blocks: 8          IO Block: 4096   regular file
Device: 801h/2049d      Inode: 13762564    Links: 1
Access: (0644/-rw-r--r--)  Uid: ( 1000/      dr)   Gid: ( 1000/      dr)
Access: 2018-09-26 17:33:32.210153803 +0800
Modify: 2018-04-25 09:52:45.605824021 +0800
Change: 2018-04-25 09:52:45.605824021 +0800
 Birth: -
```

当然`ls`命令也可以查看这些信息，只是需要指定相应的参数即可。

```
ls -l --time=ctime .bashrc
-rw-r--r-- 1 dr dr 3771 4月  25 09:52 .bashrc
[root@web10 ~]# ls -l --time=atime .bashrc
-rw-r--r-- 1 dr dr 3771 9月  26 17:33 .bashrc
```

注意：ls参数里没有--mtime这个参数，因为我们默认通过ls -l查看到的时间就是mtime 。

### pidof 查看程序的进程ID

此命令将检查特定二进制文件的PID，即使另一个同名进程正在运行。例如，当运行两个 Nginx 实例，pidof 命令可用于确定每个特定 Nginx 实例的PID。

### iostat 查看磁盘读写速度

Ubuntu默认不提供此软件，需要使用命令`sudo apt install sysstat`安装。

iostat默认提供系统启动时间内平均速度，所以最初使用`iostat`查看磁盘速率，发现磁盘速度一直非常稳定（低，且不符合当时大量IO的真实速率）。

```
iostat -h
Linux 4.15.0-34-generic (user)  09/16/2018      _x86_64_        (24 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           0.1%    0.0%    0.0%    0.1%    0.0%   99.8%

Device             tps    kB_read/s    kB_wrtn/s    kB_read    kB_wrtn
loop0
                  0.00         0.0k         0.0k       1.1M       0.0k
loop1
                  0.03         0.0k         0.0k       9.8M       0.0k
loop2
                  0.00         0.0k         0.0k       5.0k       0.0k
sda
                 27.31         1.1M         2.1M     280.4G     533.1G
```

查看帮助文档，指定命令时可以指定时间间隔和期望显示的统计次数，格式为 `iostat  [ interval [ count ] ]`。例如：

```
iostat -hx 1 3 
Linux 4.15.0-34-generic (user)  09/16/2018      _x86_64_        (24 CPU)

avg-cpu:  %user   %nice %system %iowait  %steal   %idle
           0.6%    0.0%    0.8%    0.0%    0.0%   98.6%

Device            r/s     w/s     rkB/s     wkB/s   rrqm/s   wrqm/s  %rrqm  %wrqm r_await w_await aqu-sz rareq-sz wareq-sz  svctm  %util
loop0
                 0.00    0.00      0.0k      0.0k     0.00     0.00   0.0%   0.0%    0.00    0.00   0.00     0.0k     0.0k   0.00   0.0%
loop1
                 0.00    0.00      0.0k      0.0k     0.00     0.00   0.0%   0.0%    0.00    0.00   0.00     0.0k     0.0k   0.00   0.0%
loop2
                 0.00    0.00      0.0k      0.0k     0.00     0.00   0.0%   0.0%    0.00    0.00   0.00     0.0k     0.0k   0.00   0.0%
sda
                 0.00 1857.00      0.0k    463.5M     0.00     0.00   0.0%   0.0%    0.00   73.49 141.93     0.0k   255.6k   0.54 100.0%
```

Reference: [hexdump命令](http://man.linuxde.net/hexdump)

[Why doesn't my IOstat change its output at all?](https://unix.stackexchange.com/questions/191033/why-doesnt-my-iostat-change-its-output-at-all)
