## ps (Process Status) - report a snapshot of the current processes.

`ps`显示进程选中部分信息。如果你希望重复地更新显示选中信息，那么你可以使用`top`命令。

`ps` displays information about a selection of the active processes.  If you want a repetitive update of the selection and the displayed information, use `top` instead.

`ps`命令是最基本同时也是非常强大的进程查看命令。使用该命令可以确定有哪些进程正在运行和运行的状态、进程是否结束、进程有没有僵死、哪些进程占用了过多的资源等等。总之大部分信息都是可以通过执行该命令得到的。

当前版本的`ps`支持如下三种格式的参数：不同格式参数可以混用，但可能会出现冲突现象。

This version of `ps` accepts several kinds of options:

1. UNIX options, which may be grouped and must be preceded by a dash.
2. BSD options, which may be grouped and must not be used with a dash.
3. GNU long options, which are preceded by two dashes.

Options of different types may be freely mixed, but conflicts can appear.

There are some synonymous options, which are functionally identical, due to the many standards and `ps` implementations that this `ps` is compatible with.

linux上进程有5种状态: 

```
1. 运行(正在运行或在运行队列中等待) 
2. 中断(休眠中, 受阻, 在等待某个条件的形成或接受到信号) 
3. 不可中断(收到信号不唤醒和不可运行, 进程必须等待直到有中断发生) 
4. 僵死(进程已终止, 但进程描述符存在, 直到父进程调用wait4()系统调用后释放) 
5. 停止(进程收到SIGSTOP, SIGSTP, SIGTIN, SIGTOU信号后停止运行)
```
 
ps工具标识进程的5种状态码: 

```
D 不可中断 uninterruptible sleep (usually IO) 
R 运行 runnable (on run queue) 
S 中断 sleeping 
T 停止 traced or stopped 
Z 僵死 a defunct (”zombie”) process
```

### PROCESS STATE CODES

Here are the different values that the s, stat and state output specifiers (header "STAT" or "S") will display to describe the state of a process:

```
D    uninterruptible sleep (usually IO)
R    running or runnable (on run queue)
S    interruptible sleep (waiting for an event to complete)
T    stopped by job control signal
t    stopped by debugger during the tracing
W    paging (not valid since the 2.6.xx kernel)
X    dead (should never be seen)
Z    defunct ("zombie") process, terminated but not reaped by its parent
```

For BSD formats and when the stat keyword is used, additional characters may be displayed:

```
<    high-priority (not nice to other users)
N    low-priority (nice to other users)
L    has pages locked into memory (for real-time and custom IO)
s    is a session leader
l    is multi-threaded (using CLONE_THREAD, like NPTL pthreads do)
+    is in the foreground process group
```

