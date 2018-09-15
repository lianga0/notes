## Mongodb 使用numactl 启动

From: http://blog.51cto.com/linuxg/1921697

### NUMA介绍

在介绍numactl之前，需要先说说NUMA是什么，这样才能更好的理解numactl。

NUMA（Non Uniform Memory Access Architecture）字面直译为"非一致性内存访问",对于Linux内核来说最早出现在2.6.7版本上。这种特性对于当下大内存+多CPU为潮流的X86平台来说确实会有不少的性能提升，但相反的，如果配置不当的话，也是一个很大的坑。

非统一内存访问（NUMA）是一种用于多处理器的电脑记忆体设计，内存访问时间取决于处理器的内存位置。 在NUMA下，处理器访问它自己的本地存储器的速度比非本地存储器（存储器的地方到另一个处理器之间共享的处理器或存储器）快一些。NUMA架构在逻辑上遵循对称多处理（SMP）架构。 

NUMA通过提供分离的存储器给各个处理器，避免当多个处理器访问同一个存储器产生的性能损失来试图解决这个问题。对于涉及到分散的数据的应用（在服务器和类似于服务器的应用中很常见），NUMA可以通过一个共享的存储器提高性能至n倍,而n大约是处理器（或者分离的存储器）的个数。

#### [更详细的讲NUMA 概念](https://docs.microsoft.com/zh-cn/previous-versions/sql/sql-server-2008/ms178144%28v%3dsql.100%29)

硬件已经趋向使用多条系统总线，每条系统总线为一小组处理器提供服务。每组处理器都有自己的内存，并可能有自己的 I/O 通道。但是，每个 CPU 都可以通过一致的方式访问与其他组关联的内存。每个组称为一个“NUMA 节点”。NUMA 节点中的 CPU 数量取决于硬件供应商。访问本地内存比访问与其他 NUMA 节点关联的内存快。这就是“非一致性内存访问体系结构”名称的由来。

在 NUMA 硬件上，有些内存区域与其他区域位于不同的物理总线上。由于 NUMA 同时使用本地内存和外部内存，因此，访问某些内存区域的时间会比访问其他内存区域的要长。“本地内存”和“外部内存”通常用于引用当前正在运行的线程。本地内存是指与当前正在运行线程的 CPU 位于同一节点上的内存。任何不属于当前正在运行的线程所在的节点的内存均为外部内存。外部内存也称为“远程内存”。访问外部内存的开销与访问本地内存的开销比率称为 NUMA 比率。如果 NUMA 比率为 1，则它是对称多处理 (SMP)。比率越高，访问其他节点内存的开销就越大。不支持 NUMA 的 Windows 应用程序（包括 SQL Server 2000 SP3 及更低版本）有时在 NUMA 硬件上的执行效果非常差。

NUMA 的主要优点是伸缩性。NUMA 体系结构在设计上已超越了 SMP 体系结构在伸缩性上的限制。通过 SMP，所有的内存访问都传递到相同的共享内存总线。这种方式非常适用于 CPU 数量相对较少的情况，但不适用于具有几十个甚至几百个 CPU 的情况，因为这些 CPU 会相互竞争对共享内存总线的访问。NUMA 通过限制任何一条内存总线上的 CPU 数量并依靠高速互连来连接各个节点，从而缓解了这些瓶颈状况。

### numactl介绍

numactl - Control NUMA policy for processes or shared memory

翻译：控制进程或共享内存的NUMA策略

Linux提供了一个手工调优的命令numactl（默认不安装），首先你可以通过它查看系统的numa状态

```
numactl --hardware 
available: 2 nodes (0-1)
node 0 cpus: 0 2 4 6 8 10 12 14 16 18 20 22
node 0 size: 64376 MB
node 0 free: 63556 MB
node 1 cpus: 1 3 5 7 9 11 13 15 17 19 21 23
node 1 size: 64506 MB
node 1 free: 63835 MB
node distances:
node   0   1 
  0:  10  20 
  1:  20  10 
```

此系统共有2个node，各领取12个CPU和64G内存。

### 使用numactl启动mongodb

When running MongoDB on Linux, you should disable zone reclaim in the sysctl settings using one of the following commands:

```
echo 0 | sudo tee /proc/sys/vm/zone_reclaim_mode
```

```
sudo sysctl -w vm.zone_reclaim_mode=0
```

Then, you should use numactl to start your mongod instances

```
numactl --interleave=all <path> <options>
```

To fully disable NUMA behavior, you must perform both operations. For more information, see the Documentation for [/proc/sys/vm/](https://www.kernel.org/doc/Documentation/sysctl/vm.txt)

即分配所有的node供其使用，这也是官方推荐的用法。

### zone_reclaim_mode详解

zone_reclaim_mode模式是在2.6版本后期开始加入内核的一种模式，可以用来管理当一个内存区域(zone)内部的内存耗尽时，是从其内部进行内存回收还是可以从其他zone进行回收的选项，我们可以通过/proc/sys/vm/zone_reclaim_mode文件对这个参数进行调整。

在申请内存时(内核的get_page_from_freelist()方法中)，内核在当前zone内没有足够内存可用的情况下，会根据zone_reclaim_mode的设置来决策是从下一个zone找空闲内存还是在zone内部进行回收。这个值为0时表示可以从下一个zone找可用内存，非0表示在本地回收。这个文件可以设置的值及其含义如下：

- echo 0 > /proc/sys/vm/zone_reclaim_mode：意味着关闭zone_reclaim模式，可以从其他zone或NUMA节点回收内存。
- echo 1 > /proc/sys/vm/zone_reclaim_mode：表示打开zone_reclaim模式，这样内存回收只会发生在本地节点内。
- echo 2 > /proc/sys/vm/zone_reclaim_mode：在本地回收内存时，可以将cache中的脏数据写回硬盘，以回收内存。
- echo 4 > /proc/sys/vm/zone_reclaim_mode：可以用swap方式回收内存。

不同的参数配置会在NUMA环境中对其他内存节点的内存使用产生不同的影响，大家可以根据自己的情况进行设置以优化你的应用。默认情况下，zone_reclaim模式是关闭的。这在很多应用场景下可以提高效率，比如文件服务器，或者依赖内存中cache比较多的应用场景。这样的场景对内存cache速度的依赖要高于进程进程本身对内存速度的依赖，所以我们宁可让内存从其他zone申请使用，也不愿意清本地cache。

如果确定应用场景是内存需求大于缓存，而且尽量要避免内存访问跨越NUMA节点造成的性能下降的话，则可以打开zone_reclaim模式。此时页分配器会优先回收容易回收的可回收内存（主要是当前不用的page cache页），然后再回收其他内存。

打开本地回收模式的写回可能会引发其他内存节点上的大量的脏数据写回处理。如果一个内存zone已经满了，那么脏数据的写回也会导致进程处理速度收到影响，产生处理瓶颈。这会降低某个内存节点相关的进程的性能，因为进程不再能够使用其他节点上的内存。但是会增加节点之间的隔离性，其他节点的相关进程运行将不会因为另一个节点上的内存回收导致性能下降。

From: [
zone_reclaim_mode详解](https://blog.csdn.net/AXW2013/article/details/79659055)

