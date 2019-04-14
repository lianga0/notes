## Linux top 命令

> 2019.04.14

在Linux下使用top命令时，默认显示如下：

```
top - 01:56:13 up 32 min,  2 users,  load average: 1.35, 3.79, 2.79
Tasks: 253 total,   2 running, 176 sleeping,   0 stopped,   0 zombie
%Cpu(s):  3.5 us,  1.2 sy, 25.0 ni, 70.0 id,  0.1 wa,  0.0 hi,  0.2 si,  0.0 st
KiB Mem :  3049504 total,  1465528 free,   617168 used,   966808 buff/cache
KiB Swap:  2097148 total,  2097148 free,        0 used.  2258920 avail Mem

   PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND
  3207 root      39  19   11656   4308   1740 R  99.7  0.1   0:10.01 bc
   794 root      39  19 1455068  29804  12632 S  17.9  1.0   8:38.41 snapd
   326 root      20   0       0      0      0 S   1.7  0.0   0:31.53 jbd2/sda1-8
  3208 dr        20   0   51352   4104   3288 R   0.7  0.1   0:00.09 top
   792 root      20   0  565796  16844  13716 S   0.3  0.6   0:00.74 NetworkManager

```

其中，Tasks一栏中各个字段的含义如下（来源于top的man文档中2. SUMMARY Display小结）：

#### TASK and CPU States

This portion consists of a minimum of two lines.  In an SMP environment, additional lines can reflect individual CPU state percentages.

Line 1 shows total tasks or threads, depending on the state of the Threads-mode toggle.  That total is further classified as:

```
running; sleeping; stopped; zombie
```

Line 2 shows CPU state percentages based on the interval since the last refresh.

As a default, percentages for these individual categories are displayed.  Where two labels are shown below, those for more recent kernel versions are shown first.

```
   us, user    : time running un-niced user processes
   sy, system  : time running kernel processes
   ni, nice    : time running niced user processes
   id, idle    : time spent in the kernel idle handler
   wa, IO-wait : time waiting for I/O completion
   hi : time spent servicing hardware interrupts
   si : time spent servicing software interrupts
   st : time stolen from this vm by the hypervisor
```

翻译一下：

```
us：用户态使用的cpu时间比
sy：系统态使用的cpu时间比
ni：nice加权的进程使用的cpu时间比
id：空闲的cpu时间比
wa：cpu等待磁盘写入完成时间
hi：硬中断消耗时间
si：软中断消耗时间
st：虚拟机偷取时间
```

其中，ni是nice的意思，nice是什么呢，每个linux进程都有个优先级，优先级高的进程有优先执行的权利，这个叫做pri。进程除了优先级外，还允许用户设置一个优先级的修正值。即比如你原先的优先级是20，然后修正值为-2，那么你最后的进程优先级为18。这个修正值就叫做进程的nice值。nice值越小，进程的优先级就越高。

Ubuntu中用户可以通过 `sudo nice -n adjustment_value [COMMAND [ARG]...]` 命令来调整运行指定COMMAND进程的nice值，调整后这个COMMAND所对应的进程所占用的CPU会算在ni中。

对于已经存在的进程，可以使用 `sudo renice -n priority_value -p process IDs`命令进行调整，调整后这个进程所占用的CPU会算在ni中。

Reference: 

[你不一定懂的cpu显示信息](https://www.cnblogs.com/yjf512/p/3383915.html)


[What is the difference between the NI and PR values in the top(1) command's output? I know NI is the nice value, which ranges from -19 to 20, but what is the significance of PR value?](https://www.quora.com/What-is-the-difference-between-the-NI-and-PR-values-in-the-top-1-commands-output-I-know-NI-is-the-nice-value-which-ranges-from-19-to-20-but-what-is-the-significance-of-PR-value)

[In Linux “top” command what are us, sy, ni, id, wa, hi, si and st (for CPU usage)?](https://unix.stackexchange.com/questions/18918/in-linux-top-command-what-are-us-sy-ni-id-wa-hi-si-and-st-for-cpu-usage)