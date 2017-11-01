### Linux的top命令中load average多少才算正常

首先，我们要搞清楚ubuntu top命令中load average的含义是什么？

top命令并不是自己计算load average，而是仅仅是从`/proc/loadavg`文件中读取这些信息。在Linux系统中，它表示操作系统中可执行队列或等待磁盘I/O队列的平均长度（**部分Unix系统中仅代表可执行队列的长度**）而并不是简单的表示CPU的使用率。**Linux load averages track not just runnable tasks, but also tasks in the uninterruptible sleep state. Linux load averages are "system load averages" that show the running thread (task) demand on the system as an average number of running plus waiting threads.**

First, `top` does not calculate load average itself. It just reads load average from the /proc/loadavg file (strace shows that top opens /proc/loadavg and then reads from it periodically). man proc says this for `/proc/loadavg`:

```
/proc/loadavg
    The first three fields in this file are load average figures giving the number of jobs in the run queue (state R) or waiting for disk I/O (state D) averaged over 1, 5, and 15  minutes. They are the same as the load average numbers given by uptime(1) and other programs. The fourth field consists of two numbers separated by a slash (/).  The first of these is the number of currently runnable kernel scheduling entities (processes, threads).  The value after the slash is the number of kernel scheduling  entities that currently exist on the system.  The fifth field is the PID of the process that was most recently created on the system.
```

So load average shows the number of jobs in the run queue. And you are shown the first three values from `/proc/loadavg` by the `top`. If you run `cat /proc/loadavg` you will see all values in the file.

`load average` figures giving the number of jobs in the **run queue (state R)** or **waiting for disk I/O (state D)** averaged over 1, 5, and 15  minutes.
So `load average` does not simply mean "% of CPU capacity" on linux system.


严禁的讲：服务器的负载类型不同，正常的标准也不一样。load 值仅供参考，选用其他系统负载相关信息、以及完善的应用级别Profiling和监控比较靠谱。

通常有说法认为（单核）0.7以上就该检讨哪里出了问题，到了1.0就应该立即找到问题所在并且解决，不然肯定会被半夜叫起来加班。也有人讲：见过一堆做VPN，L2TP的，机器没事就跑个100+的load，vpn用户还没半点卡的感觉，这类应用负载值只供参考就好，因为瓶颈一般会出现在带宽上。

所以这个不是用简单的数字可以衡量的，如果有人根据简单一个数字就告诉你“高了”或者“没问题”，这都是没真正理解这事的。事实上load average是否合适，跟你的应用，尤其是高负载的类型有关。需要具体问题具体分析。 

唯一应该注意的是，当load average超过cpu核数的时候，你就应该部署各种监控工具，获取更多数据了。 

有一些应用类型是单次访问负载大，但频度低（比如数据分析之类的服务），这种load average甚至能长期维持在10几都没问题。但如果是单次访问负载小，频度极高的应用（比如普通网站？），那么有可能接近cpu核数的load average都会让系统在某一点彻底崩溃。 

比load average更有衡量效果的是看ps的结果中的STATE，有没有即将可能卡住的进程。通常vmstat会提供更多信息。load average只能做为一个简单的参照值，不能用来得出最终结论。

关于load average常见的误解：

##### 误解 一：系统 Load 高一定是性能有问题。

真相：系统 Load 高也或许是因为在进行 CPU 密集型的计算(比如编译)

##### 误解 二：系统 Load 高一定是 CPU 能力问题或数量不够。

真相：Load 高只是代表需要运行的队列累积过多了。但队列中的任务实际可能是耗 CPU的，也可能是耗 I/O 乃至其它因素的。

##### 误解 三：系统长期 Load 高，首选增加 CPU。

真相：Load 只是表象，不是实质。增加 CPU 个别时候会临时看到系统 Load 下降，但治标不治本。



Reference: https://www.v2ex.com/t/43287

http://dbanotes.net/arch/unix_linux_load.html

https://stackoverflow.com/questions/21617500/understanding-load-average-vs-cpu-usage

[Linux Load Averages: Solving the Mystery](http://www.brendangregg.com/blog/2017-08-08/linux-load-averages.html)
