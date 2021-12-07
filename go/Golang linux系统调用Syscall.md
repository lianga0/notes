# Golang 系统调用Syscall

> 落城 2017-12-22 14:51:26

> https://blog.csdn.net/u011211976/article/details/78873252

最近在研究go语言，发现go语言系统调用源码只有调用函数的定义，没有指导文档，网上也没有相关文档的说明，自己稍微研究了一下，不对的地方欢迎指教

go源码中关于系统调用的定义如下：

```
func Syscall(trap, a1, a2, a3 uintptr) (r1, r2 uintptr, err Errno)
func Syscall6(trap, a1, a2, a3, a4, a5, a6 uintptr) (r1, r2 uintptr, err Errno)
func RawSyscall(trap, a1, a2, a3 uintptr) (r1, r2 uintptr, err Errno)
func RawSyscall6(trap, a1, a2, a3, a4, a5, a6 uintptr) (r1, r2 uintptr, err Errno)
```

其中`Syscall`和`RawSyscall`区别在于`Syscall`开始和结束，分别调用了 `runtime` 中的进入系统调用和退出系统调用的函数，说明`Syscall`函数受调度器控制，不会造成系统堵塞，而`RawSyscall`函数没有调用`runtime`，因此可能会造成堵塞，一般我们使用`Syscall`就可以了，`RawSyscall`最好用在不会堵塞的情况下。

```
func Syscall(trap, a1, a2, a3 uintptr) (r1, r2 uintptr, err Errno)
```

Syscall 的定义位于 `src/syscall/asm_linux_amd64.s`, 是用汇编写成的，封装了对linux底层的调用。接收4个参数，其中`trap`为中断信号，a1,a2,a3为底层调用函数对应的参数

## 举例说明：Go调用底层ioctl函数

`trap`中断类型传入`syscall.SYS_IOCTL`，`SYS_IOCTL`中断号表示调用linux底层ioctl函数
Syscall函数中剩下三个参数a1,a2,a3分别对应ioctl的三个参数。可以man命令查看linux ioctl函数参数，如下

```
int ioctl(int d, int request, ...);
```

第一个参数`d`指定一个由`open/socket`创建的文件描述符，即`socket`套接字
第二个参数`request`指定操作的类型，即对该文件描述符执行何种操作，设备相关的请求的代码
第三个参数为一块内存区域，通常依赖于`request`指定的操作类型

具体过程如下：

1. 通过socket创建套接字

2. 初始化struct ifconf与/或struct ifreq结构

3. 调用ioctl函数，执行相应类型的SIO操作

4. 获取返回至truct ifconf与/或struct ifreq结构中的相关信息

调用底层socket函数创建socket套接字，linux下用man命令查看socket函数用法

```
int socket(int domain, int type, int protocol);
```

其中domain为协议类型，type为套接字类型，protocol指定某个协议类型常值

domain的值有：

```
AF_INET IPv4协议
AF_INET6 Ipv6协议
AF_ROUTE 路由套接字
...
```

type的值有：

```
SOCK_STREAM 字节流套接字
SOCK_DGRAM 数据报套接字
SOCK_RAW 原始套接字
...
```

protocol的值有：

```
IPPROTO_IP IP传输协议
IPPROTO_TCP TCP传输协议
IPPROTO_UDP UDP传输协议
...
```

因此linux下调用socket生成套接字写法：

```
fd = socket(AF_INET, SOCK_DGRAM, IPPROTO_IP);
```

综上，转换成go语言中系统调用写法

```
fd, _, err := syscall.RawSyscall(syscall.SYS_SOCKET, syscall.AF_INET, syscall.SOCK_DGRAM, syscall.IPPROTO_IP)
```

此时即生成了的`socket`套接字`fd`

我们传给`int ioctl(int d, int request, …);`函数作为第一个参数，第二个参数`request`操作的类型我们传入`SIOCETHTOOL`，获取ethtool信息。

`SIOCETHTOOL` 在源码中宏定义为

```
#define SIOCETHTOOL     0x8946
```

第三个参数为`struct ifreq`结构内存地址

Struct ifreq结构如下：

```
Struct ifreq{
Char ifr_name[IFNAMSIZ];
Union{
    Struct  sockaddr  ifru_addr;
    Struct  sockaddr  ifru_dstaddr;
    Struct  sockaddr  ifru_broadaddr;
    Struct  sockaddr  ifru_netmask;
    Struct  sockaddr  ifru_hwaddr;
    Short  ifru_flags;
    Int     ifru_metric;
    Caddr_t ifru_data;
}ifr_ifru;
};
#define ifr_addr        ifr_ifru.ifru_addr
#define ifr_broadaddr   ifr_ifru.ifru_broadadd
#define ifr_hwaddr      ifr_ifru_hwaddr
```

综上，linux调用ioctl函数如下：

```
fd = socket(AF_INET, SOCK_DGRAM, IPPROTO_IP);
ioctl(fd, SIOCETHTOOL, &ifreq);
```

go语言：

```
fd, _, err := syscall.RawSyscall(syscall.SYS_SOCKET, syscall.AF_INET, syscall.SOCK_DGRAM, syscall.IPPROTO_IP)
if err != 0 {
        return syscall.Errno(err)
    }
, , ep := syscall.Syscall(syscall.SYS_IOCTL, uintptr(e.fd), SIOCETHTOOL, uintptr(unsafe.Pointer(&ifreq)))
if ep != 0 {
return syscall.Errno(ep)
}
```
