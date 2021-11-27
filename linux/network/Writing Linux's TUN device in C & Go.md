# Tun/Tap 编程接口入门

## tun/tap是什么？

tun与tap是操作系统内核中的虚拟网络设备。

tun是网络层的虚拟网络设备，可以收发第三层数据报文包，如IP封包，因此常用于一些点对点IP隧道，例如OpenVPN，IPSec等。

tap是链路层的虚拟网络设备，等同于一个以太网设备，它可以收发第二层数据报文包，如以太网数据帧。Tap最常见的用途就是做为虚拟机的网卡，因为它和普通的物理网卡更加相近，也经常用作普通机器的虚拟网卡。

### 如何操作tun/tap？

Linux tun/tap可以通过网络接口和字符设备两种方式进行操作。

当应用程序使用标准网络接口socket API操作tun/tap设备时，和操作一个真实网卡无异。

当应用程序使用字符设备操作tun/tap设备时，字符设备即充当了用户空间和内核空间的桥梁直接读写二层或三层的数据报文。在 Linux 内核 2.6.x 之后的版本中，tun/tap 对应的字符设备文件分别为：

```
tun：/dev/net/tun
tap：/dev/tap0
```

当应用程序打开字符设备时，系统会自动创建对应的虚拟设备接口，一般以tunX和tapX方式命名，虚拟设备接口创建成功后，可以为其配置IP、MAC地址、路由等。当一切配置完毕，应用程序通过此字符文件设备写入IP封包或以太网数据帧，tun/tap的驱动程序会将数据报文直接发送到内核空间，内核空间收到数据后再交给系统的网络协议栈进行处理，最后网络协议栈选择合适的物理网卡将其发出，到此发送流程完成。而物理网卡收到数据报文时会交给网络协议栈进行处理，网络协议栈匹配判断之后通过tun/tap的驱动程序将数据报文原封不动的写入到字符设备上，应用程序从字符设备上读取到IP封包或以太网数据帧，最后进行相应的处理，收取流程完成。

## linux提供操作tun/tap的命令

Linux 提供了一些命令行程序方便我们来创建持久化的tun/tap设备，我们把它当作普通网卡去使用。

```
# 创建 tap 
ip tuntap add dev tap0 mode tap 
# 创建 tun
ip tuntap add dev tun0 mode tun 

# 删除 tap
ip tuntap del dev tap0 mode tap
# 删除 tun
ip tuntap del dev tun0 mode tun 
```

tun/tap 设备创建成功后可以当作普通的网卡一样使用，因此我们也可以通过ip link命令来操作它。

```
# 例如使用ip link命令也可以删除tun/tap设备
ip link del tap0
ip link del tun0
```

## 读写TUN/TAP时内核的行为

tap/tun 是Linux内核 2.4.x 版本之后使用软件实现的虚拟网络设备，这类接口仅能工作在内核中。不同于普通的网络接口，没有物理硬件(因此也没有物理线路连接到这类接口)。可以将tun/tap接口认为是一个普通的网络接口，当内核决定发送数据时，会将数据发送到连接到该接口上的用户空间的应用(而不是"线路"上)。当一个程序附加到tun/tap接口上时，该程序将获得一个特定的文件描述符，从该描述符上可以获得接口上发送过来的数据。类似地，程序也可以往该描述符上发送数据(需要保证数据格式的正确性)，然后这些数据会输入给tun/tap接口，内核中的tun/tap接口就像从线路上接收到数据一样。

tap接口和tun接口的区别是，tap接口会会输出完整的以太帧，而tun接口会输出IP报文(不含以太头)。可以在创建接口时指定该接口是tun接口还是tap接口。

这类接口可能是临时的，意味着某些程序可以创建这类接口，并在使用后销毁。当程序结束，即使没有明确地删除接口，也会被系统回收。另一种方式是通过专有工具(如tunctl或openvpn --mktun)将接口持久化，这样其他程序就可以使用该接口，此时，使用该接口的程序必须使用与接口相同的类型(tun或tap)。

一旦创建了一个tun/tap接口，就可以像使用其他接口一样使用该接口，既可以给该接口分配IP，分析流量，创建防火墙规则，创建指向该接口的路由等。

## 创建接口

创建一个新接口的代码与连接到一个持久接口的代码基本是相同的，不同点是前者必须使用root权限执行(即使用· capability权限的用户)，而后者可以被任意用户执行。下面看下创建新接口的场景。

首先，`/dev/net/tun`必须以读写方式打开，由于该设备被用作创建任何`tun/tap`虚拟接口的起点，因此也被称为**克隆设备**(clone device)。操作(`open()`)后会返回一个文件描述符，但此时还无法与接口通信。

下一步会使用一个特殊的`ioctl()`系统调用，该函数的入参为上一步得到的文件描述符，以及一个`TUNSETIFF`常数和一个指向描述虚拟接口的结构体指针(基本上为接口名称和操作模式--tun或tap)。作为一个可变的值，可以不指定虚拟接口名，此时内核将通过尝试分配“下一个”设备来选择一个名称(例如，如果已经存在tap2，则内核会分配tap3，以此类推)。这些操作必须通过`root`用户完成(或具有`CAP_NET_ADMIN` capability权限的用户)。

如果`ioctl()`执行成功，则说明已经成功创建虚拟接口，且可以使用文件描述符通信。

此时，会有两种情况：程序可以使用该接口(可能会在使用前分配IP)，并在程序执行完后结束并销毁该接口；另一种是通过两个特殊的`ioctl()`调用来将接口持久化，在程序运行结束后会保留该接口，这样其他程序就可以使用该接口(当使用`tunctl`或`openvpn --mktun`时会发生这种情况)。同时设置虚拟接口的所有者为一个非root的用户或组，这样当程序以非root用户运行时也可以使用该接口(程序也需要有合适的权限)。

可以在内核源码的`Documentation/networking/tuntap.rst`下找到基本的创建虚拟接口的示例代码，下面对该代码进行简单修改：

```
#include <linux /if.h>
#include <linux /if_tun.h>

int tun_alloc(char *dev, int flags) {

  struct ifreq ifr;
  int fd, err;
  char *clonedev = "/dev/net/tun";

  /* Arguments taken by the function:
   *
   * char *dev: the name of an interface (or '\0'). MUST have enough
   *   space to hold the interface name if '\0' is passed
   * int flags: interface flags (eg, IFF_TUN etc.)
   */

   /* open the clone device */
   if( (fd = open(clonedev, O_RDWR)) < 0 ) { /* 使用读写方式打开 */
     return fd;
   }

   /* preparation of the struct ifr, of type "struct ifreq" */
   memset(&ifr, 0, sizeof(ifr));

   ifr.ifr_flags = flags;   /* IFF_TUN or IFF_TAP, plus maybe IFF_NO_PI */

   if (*dev) {
     /* if a device name was specified, put it in the structure; otherwise,
      * the kernel will try to allocate the "next" device of the
      * specified type */
     strncpy(ifr.ifr_name, dev, IFNAMSIZ); /* 设置设备名称 */
   }

   /* try to create the device */
   if( (err = ioctl(fd, TUNSETIFF, (void *) &ifr)) < 0 ) {
     close(fd);
     return err;
   }

  /* if the operation was successful, write back the name of the
   * interface to the variable "dev", so the caller can know
   * it. Note that the caller MUST reserve space in *dev (see calling
   * code below) */
  strcpy(dev, ifr.ifr_name);

  /* this is the special file descriptor that the caller will use to talk
   * with the virtual interface */
  return fd;
}
```

其中，`tun_alloc()` 函数具有两个参数：

`char *dev`：包含接口的名称(例如，tap0，tun2等)。虽然可以使用任意名称，但建议最好使用能够代表该接口类型的名称。实际中通常会用到类似tunX或tapX这样的名称。如果*dev为'\0'，则内核会尝试使用第一个对应类型的可用的接口(如tap0，但如果已经存在该接口，则使用tap1，以此类推)。

`int flags`：包含接口的类型(tun或tap)。通常会使用`IFF_TUN`来指定一个TUN设备(报文不包括以太头)，或使用`IFF_TAP`来指定一个TAP设备(报文包含以太头)。

此外，还有一个`IFF_NO_PI`标志，可以与`IFF_TUN`或`IFF_TAP`执行`OR`配合使用。`IFF_NO_PI`会告诉内核不需要提供报文信息，即告诉内核仅需要提供"纯"IP报文，不需要其他字节。否则(不设置`IFF_NO_PI`)，会在报文开始处添加4个额外的字节(2字节的标识和2字节的协议)。`IFF_NO_PI`不需要再创建和连接之间进行匹配(即当创建时指定了该标志，可以在连接时不指定)，需要注意的是，当使用wireshark在该接口上抓取流量时，不会显示这4个字节。

到此为止，程序可以使用该接口进行通信，或将接口持久化(或将接口分配给特定的用户/组)。

还有两个`ioctl()`调用，通常是一起使用的。第一个调用用于设置(或移除)接口的持久化状态，第二个用于将接口分配给一个普通的(非root)用户。`tunctl`和`openvpn --mktun`这两个程序都实现了该特性。下面看下`tunctl`的代码：

```
...
  /* "delete" is set if the user wants to delete (ie, make nonpersistent)
     an existing interface; otherwise, the user is creating a new
     interface */
  if(delete) {
    /* remove persistent status */
    if(ioctl(tap_fd, TUNSETPERSIST, 0) < 0){
      perror("disabling TUNSETPERSIST");
      exit(1);
    }
    printf("Set '%s' nonpersistent\n", ifr.ifr_name);
  }
  else {
    /* emulate behaviour prior to TUNSETGROUP */
    if(owner == -1 && group == -1) {
      owner = geteuid(); /* 如果没有设置用户或组，则使用本uid */
    }

    if(owner != -1) {
      if(ioctl(tap_fd, TUNSETOWNER, owner) < 0){ /* 设置接口用户所属者 */
        perror("TUNSETOWNER");
        exit(1);
      }
    }
    if(group != -1) {
      if(ioctl(tap_fd, TUNSETGROUP, group) < 0){ /* 设置接口组所属者 */
        perror("TUNSETGROUP");
        exit(1);
      }
    }

    if(ioctl(tap_fd, TUNSETPERSIST, 1) < 0){ /* 设置接口持久化 */
      perror("enabling TUNSETPERSIST");
      exit(1);
    }

    if(brief)
      printf("%s\n", ifr.ifr_name);
    else {
      printf("Set '%s' persistent and owned by", ifr.ifr_name);
      if(owner != -1)
          printf(" uid %d", owner);
      if(group != -1)
          printf(" gid %d", group);
      printf("\n");
    }
  }
  ...
```

述的`ioctl()`调用必须以root执行。但如果该接口已经是一个属于特定用户的持久化接口，那么该用户就可以使用该接口。

如上所述，连接到一个已有的tun/tap接口的代码与创建一个tun/tap接口的代码相同，即，可以多次使用`tun_alloc()`。为了执行成功，需要注意如下三点：

- 接口必须已经存在，且所有者与连接该接口的用户相同

- 用户必须有`/dev/net/tun`的读写权限

- 必须提供创建接口时使用的相同的标志(即，如果接口使用`IFF_TUN`创建，则在连接时也必须使用该标志)

当用户指定一个已经存在的接口执行 `TUNSETIFF ioctl()` (且该用户是该接口的所有者)时会返回成功，但这种情况下不会创建新的接口，因此一个普通用户可以成功执行该操作。

因此这样也可以尝试解释当调用`ioctl(TUNSETIFF)` 会发生什么，以及内核如何区分请求分配一个新接口和请求连接到一个现有的接口。

- 如果没有现有的接口或没有指定接口名称，意味着用户需要请求申请一个新的接口，这样内核会使用给定的名称创建一个接口(如果没有给定接口名称，则会挑选下一个可用的名称)。仅能在root用户下执行。

- 如果指定了一个存在的接口名称，意味着用户期望连接到前面分配好的接口上。可以使用普通用户完成该操作。用户需要拥有克隆设备的合适(读写)权限，且为接口的所有者，且指定的模式(tun或tap)可以匹配创建时的模式。

可以在内核源码`drivers/net/tun.c`中查看上述代码的实现，实现函数为`tun_attach()`, `tun_net_init()`, `tun_set_iff()`, `tun_chr_ioctl()`，其中最后一个函数各种`ioctl()`，包括`TUNSETIFF`,` TUNSETPERSIST`, `TUNSETOWNER`, `TUNSETGROUP`等。

### 举例

使用tun/tap接口与使用其他接口并没有什么不同，在创建或连接到已有的接口时必须知道接口的类型，以及期望读取或写入的数据。下面创建一个持久化接口，并给该接口分配IP地址。

```
# openvpn --mktun --dev tun2 #当然也可以使用 ip tuntap add tun3 mode tun创建tun接口
Fri Mar 26 10:29:29 2010 TUN/TAP device tun2 opened
Fri Mar 26 10:29:29 2010 Persist state set to: ON
# ip link set tun2 up
# ip addr add 10.0.0.1/24 dev tun2
```

下面启动一个网络分析器来查看流量：

```
# tshark -i tun2 #使用 tcpdump -i tun2 即可
Running as user "root" and group "root". This could be dangerous.
Capturing on tun2


# On another console
# ping 10.0.0.1
PING 10.0.0.1 (10.0.0.1) 56(84) bytes of data.
64 bytes from 10.0.0.1: icmp_seq=1 ttl=64 time=0.115 ms
64 bytes from 10.0.0.1: icmp_seq=2 ttl=64 time=0.105 ms
```

**执行ping操作后发现tshark并没有任何打印信息，即没有任何流量经过该接口。这种现象是符合预期的，因为当ping该接口的IP地址时，操作系统会认为报文不需要在"线路"上进行传输，由内核负责回应ping请求(当ping其他接口的IP地址时的现象也是一样的)。tshark抓包是在网络协议栈外进行的，ping本地IP地址时的报文会在协议层面处理，因此无法抓到报文。**

上面已经创建了接口，但没有程序连接这些接口，下面编写一个简单的程序来在接口上读取内核发送的数据。

## 简单的C程序

下面的程序会连接到一个tun接口，并读取内核发送到该接口的数据。如果该接口已经被持久化，那么就可以使用一个普通用户(可以读写克隆设备`/dev/net/tun`，并且为接口的所有者)来运行这个程序。下面程序只是个框架，展示了如何从设备获取数据，并对这些数据进行简单的处理。下面程序使用了上面定义的`tun_alloc()`函数，完整代码如下:

```
#include <net/if.h>
#include <linux/if_tun.h>
#include <fcntl.h>
#include <sys/ioctl.h>

int tun_alloc(char *dev, int flags) {
    struct ifreq ifr;
    int fd, err;
    char *clonedev = "/dev/net/tun";

    /* Arguments taken by the function:
     *
     * char *dev: the name of an interface (or '\0'). MUST have enough
     *   space to hold the interface name if '\0' is passed
     * int flags: interface flags (eg, IFF_TUN etc.)
     */
    
     /* open the clone device */
    if( (fd = open(clonedev, O_RDWR)) < 0 ) {
        return fd;
    }
    
    /* preparation of the struct ifr, of type "struct ifreq" */
    memset(&ifr, 0, sizeof(ifr));
    
    ifr.ifr_flags = flags;   /* IFF_TUN or IFF_TAP, plus maybe IFF_NO_PI */
    
    if (*dev) {
        /* if a device name was specified, put it in the structure; otherwise,
         * the kernel will try to allocate the "next" device of the
         * specified type */
        strncpy(ifr.ifr_name, dev, IFNAMSIZ);
    }
    
    /* try to create the device */
    if( (err = ioctl(fd, TUNSETIFF, (void *) &ifr)) < 0 ) {
        close(fd);
        return err;
    }
    
    /* if the operation was successful, write back the name of the
     * interface to the variable "dev", so the caller can know
     * it. Note that the caller MUST reserve space in *dev (see calling
     * code below) */
    strcpy(dev, ifr.ifr_name);
    
    /* this is the special file descriptor that the caller will use to talk
     * with the virtual interface */
    return fd;
}

int main(){
    int tun_fd,nread;
    unsigned char buffer[2000];
    char tun_name[IFNAMSIZ];
    
    /* Connect to the device */
    strcpy(tun_name, "tun77");
    tun_fd = tun_alloc(tun_name, IFF_TUN | IFF_NO_PI);  /* tun interface */
    
    if(tun_fd < 0){
        perror("Allocating interface");
        exit(1);
    }

    /* Now read data coming from the kernel */
    while(1) {
        /* Note that "buffer" should be at least the MTU size of the interface, eg 1500 bytes */
        nread = read(tun_fd,buffer,sizeof(buffer));
        if(nread < 0) {
            perror("Reading from interface");
            close(tun_fd);
            exit(1);
        }
	   
        /* Do whatever with the data */
        printf("Read %d bytes from device %s\n", nread, tun_name);
    }
}
```

在一个终端中执行如下命令，创建一个与程序中使用的名称相同的`tun`接口`tun77`，并执行`ping`操作：

```
# openvpn --mktun --dev tun77 --user waldner
Fri Mar 26 10:48:12 2010 TUN/TAP device tun77 opened
Fri Mar 26 10:48:12 2010 Persist state set to: ON
# ip link set tun77 up
# ip addr add 10.0.0.1/24 dev tun77
# ping 10.0.0.2
```

在另一个终端中启用编译好的程序，可以得到如下结果。84字节中，20个字节为IP首部，8字节为ICMP首部，其余56字节为ICMP的echo负载。

```
# ./tunclient
Read 84 bytes from device tun77
Read 84 bytes from device tun77
Read 84 bytes from device tun77
Read 84 bytes from device tun77
...
```

此时看下路由信息，由于连接了程序，tun77对应的路由是linkup的

```
# ip route
default via 172.20.98.253 dev eth0
10.0.0.0/24 dev tun77 proto kernel scope link src 10.0.0.1
```

可以使用上述程序将多种类型的流量发送到创建的tun接口，并校验从接口上读取的数据的大小。每次read()操作都会返回一个完整的报文。类似地，如果需要往该接口写入数据，则需要写入完整的IP报文。

那么如何使用这些数据呢?例如可以模拟读取的目标流量行为，为了方便解释，以上面的ping为例。可以解析报文，并从IP首部，ICMP首部和负载中抽取信息，用于构造一个包含ICMP响应的IP报文，并发送出去(即，写入`tun/tap`设备对应的描述符)，这样发送ping的源头将会接收到该响应。当然，上述程序的使用场景并没有限制为ping，因此可以实现各种网络协议。通常需要解析接收到的报文，并作出相应动作。如果使用tap，为了正确构建响应帧，需要在代码中实现ARP。

类似地，也可以将自己的代码连接到接口上，并尝试网络编程以及实现以太网和TCP/IP栈。可以通过查看 `drivers/net/tun.c`中的函数 `tun_get_user()` 和 `tun_put_user()`来了解tun驱动在内核侧做的事情。

# 下面是go语言实现的一个版本

```
package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"syscall"
	"unsafe"
)

func main() {
	var fdInt int
	var err error
	// O_NONBLOCK表示使用nonblocking mode，当网卡上没有可读数据时，read函数会立即返回"resource temporarily unavailable"错误。
	// 去掉该参数可以使用blocking mode，read函数从文件中读取到数据时才返回
	//fdInt, err = syscall.Open("/dev/net/tun", os.O_RDWR|syscall.O_NONBLOCK, 0)
	fdInt, err = syscall.Open("/dev/net/tun", os.O_RDWR, 0)
	if err != nil {
		return
	}
	fmt.Println("fdInt: " + strconv.Itoa(fdInt) + "$")

	ifr := make([]byte, 18)
	copy(ifr, []byte("tun0"))
	ifr[16] = 0x01
	ifr[17] = 0x10
	// 创建虚拟接口，成功后可以使用文件描述符通信
	_, _, errno := syscall.Syscall(syscall.SYS_IOCTL, uintptr(fdInt), syscall.TUNSETIFF, uintptr(unsafe.Pointer(&ifr[0])))
	if errno != 0 {
		fmt.Println("error syscall.Ioctl(): " + errno.Error())
	}
	sargs := "tun0 192.168.8.1 pointopoint 192.168.8.2 up"
	args := strings.Split(sargs, " ")
	cmd := exec.Command("ifconfig", args...)
	log.Printf("[DEBG] command: %v", cmd.String())
	if err := cmd.Run(); err != nil {
		fmt.Println("Err: %v" + err.Error())
	}
	for {
		buf := make([]byte, 2048)
		read, err := syscall.Read(fdInt, buf)
		if err != nil {
			fmt.Println("error os.Read(): " + err.Error())
		}
		fmt.Println(buf)
		for i := 0; i < 4; i++ {
			buf[i+12], buf[i+16] = buf[i+16], buf[i+12]
		}
		buf[20] = 0
		buf[22] = 0
		buf[23] = 0
		var checksum uint16
		for i := 20; i < read; i += 2 {
			checksum += uint16(buf[i])<<8 + uint16(buf[i+1])
		}
		checksum = ^(checksum + 4)
		buf[22] = byte(checksum >> 8)
		buf[23] = byte(checksum & ((1 << 8) - 1))

		_, err = syscall.Write(fdInt, buf)
		if err != nil {
			fmt.Println("error os.Write(): " + err.Error())
		}
	}
}
```

## 隧道

此外，还可以使用`tun/tap`接口来实现隧道功能。此时不需要重新实现TCP/IP，只需要编写一个程序，在运行相同程序的主机之间进行原始数据的传递即可(通过反射方式)。假设上面的程序中，除了连接到了`tun/tap`接口，还与一个远端主机建立了网络连接(该远端主机以服务器模式运行了一个类型的程序)。(实际上两个程序都是相同的，谁是客户端，谁是服务端取决于命令行参数)。一旦运行了两个程序，就可以在两个方向上传递数据。网络连接使用了TCP，但也可以使用给其他协议(如UDP，甚至ICMP)。可以在`simpletun`下载完整的代码。

下面是程序的主要循环，主要的工作是在tun/tap接口和网络隧道之间传数据。下面简化了debug语句：

```
...
  /* net_fd is the network file descriptor (to the peer), tap_fd is the
     descriptor connected to the tun/tap interface */

  /* use select() to handle two descriptors at once */
  maxfd = (tap_fd > net_fd)?tap_fd:net_fd;

  while(1) {
    int ret;
    fd_set rd_set;

    FD_ZERO(&rd_set);
    FD_SET(tap_fd, &rd_set); FD_SET(net_fd, &rd_set);

    ret = select(maxfd + 1, &rd_set, NULL, NULL, NULL);

    if (ret < 0 && errno == EINTR) {
      continue;
    }

    if (ret < 0) {
      perror("select()");
      exit(1);
    }

    if(FD_ISSET(tap_fd, &rd_set)) {
      /* data from tun/tap: just read it and write it to the network */

      nread = cread(tap_fd, buffer, BUFSIZE);

      /* write length + packet */
      plength = htons(nread);
      nwrite = cwrite(net_fd, (char *)&plength, sizeof(plength));
      nwrite = cwrite(net_fd, buffer, nread);
    }

    if(FD_ISSET(net_fd, &rd_set)) {
      /* data from the network: read it, and write it to the tun/tap interface.
       * We need to read the length first, and then the packet */

      /* Read length */
      nread = read_n(net_fd, (char *)&plength, sizeof(plength));

      /* read packet */
      nread = read_n(net_fd, buffer, ntohs(plength));

      /* now buffer[] contains a full packet or frame, write it into the tun/tap interface */
      nwrite = cwrite(tap_fd, buffer, nread);
    }
  }

...
```

上述代码的主要逻辑为：

- 程序使用`select()`多路复用来同时操作两个描述符，当任何一个描述符接收到数据后，就会发送到另一个描述符中

- 由于程序使用了TCP，接收者会会看到一条数据流，比较难以分辨报文边界。因此当向网络写入一个报文或一个帧时，会在实际数据包的前面加上它的长度(2个字节)。

- 当数据来自于tap_fd 描述符时，会一次性读取一个完整的报文或帧，这样就可以将读取的数据直接写入网络，并在报文前面加上长度。由于长度字段为一个short int类型的值，大于1个字节，且使用了二进制格式，因此可以使用`ntohs()/htons()`来兼容不同机器的字节序。

- 当数据来自于网络时，使用前面提到的技巧，可以通过报文前面的两个字节了解到后面要读取字节流中的报文的长度。当读取报文后，会将其写入tun/tap接口描述符，后续会被内核接收。

使用上述代码可以创建一个隧道。首先在隧道两端的主机上配置必要的tun/tap接口，并分配IP地址。在本例中使用了两个tun接口：本机的tun11接口，IP为192.168.0.1/24；远端主机的tun3接口，IP为192.168.0.2/24。simpletun默认会使用TCP端口55555进行连接。远端主机以服务器模式运行simpletun程序，本机以客户端模式运行(远端服务器为10.86.43.52)。

```
[remote]# openvpn --mktun --dev tun3 --user waldner
Fri Mar 26 11:11:41 2010 TUN/TAP device tun3 opened
Fri Mar 26 11:11:41 2010 Persist state set to: ON
[remote]# ip link set tun3 up
[remote]# ip addr add 192.168.0.2/24 dev tun3

[remote]$ ./simpletun -i tun3 -s
# server blocks waiting for the client to connect

[local]# openvpn --mktun --dev tun11 --user waldner
Fri Mar 26 11:17:37 2010 TUN/TAP device tun11 opened
Fri Mar 26 11:17:37 2010 Persist state set to: ON
[local]# ip link set tun11 up
[local]# ip addr add 192.168.0.1/24 dev tun11

[local]$ ./simpletun -i tun11 -c 10.86.43.52
# nothing happens, but the peers are now connected

[local]$ ping 192.168.0.2
PING 192.168.0.2 (192.168.0.2) 56(84) bytes of data.
64 bytes from 192.168.0.2: icmp_seq=1 ttl=241 time=42.5 ms
64 bytes from 192.168.0.2: icmp_seq=2 ttl=241 time=41.3 ms
64 bytes from 192.168.0.2: icmp_seq=3 ttl=241 time=41.4 ms
64 bytes from 192.168.0.2: icmp_seq=4 ttl=241 time=41.0 ms

--- 192.168.0.2 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 2999ms
rtt min/avg/max/mdev = 41.047/41.599/42.588/0.621 ms

# let's try something more exciting now
[local]$ ssh waldner@192.168.0.2
waldner@192.168.0.2's password:
Linux remote 2.6.22-14-xen #1 SMP Fri Feb 29 16:20:01 GMT 2008 x86_64

Welcome to remote!

[remote]$ 

```

上面例子中tun3和tun11之间的流量实际最终还是走的默认路由，通过eth0出去。

不要在k8s环境或容器环境中运行上述程序，可能会由于iptables导致连接失败

```
# route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.86.42.1      0.0.0.0         UG    100    0        0 eth0
10.86.42.0      0.0.0.0         255.255.254.0   U     100    0        0 eth0
169.254.169.254 10.86.43.39     255.255.255.255 UGH   100    0        0 eth0
192.168.0.0     0.0.0.0         255.255.255.0   U     0      0        0 tun11
```

当上述隧道up之后，就可以看到`simpletun`两端的TCP连接。"真实的"数据(即，上层应用传输的数据，ping或ssh)不会在线路上传输。如果在运行`simpletun`的主机上启用了IP转发，并在其他主机上创建了必要的路由，那么就可以通过隧道连接到远端网络。

当使用的虚拟接口类型为tap时，可以透明地桥接两个地理位置遥远的以太网LAN，这样设备会认为它们位于相同的二层网络。为了到这种效果，需要将本地LAN接口和虚拟tap接口一起桥接到网关(即，运行simpletun的主机或使用tap接口的另外一个隧道软件)上。这样，从LAN接收到的帧也会发送到tap接口上(因为使用了桥接)，隧道应用会读取数据并发送到远端。另一个网桥将确保将接收到的帧转发到远程LAN。另外一端也会发生相同的情况。由于在两个LAN之间使用了以太帧，因此可以将两个局域网有效地连接在一起。意味着可以在伦敦有10台机器，而在柏林有50台机器，且可以使用192.168.1.0/24 子网创建一个60台计算机的以太网络(或使用其他子网地址)。

## 拓展

`simpletun` 是一个非常简单的程序，可以通过多种方式进行扩展。首先，可以增加新的连接方式，例如，可以实现使用UDP的连接。再者，目前的数据是以明文方式传输的，但当数据位于程序的buffer中时，可以在传输前进行变更，例如进行加密。

虽然`simpletun`是一个简单的程序，但很多热门的程序也是通过这种方式使用`tun/tap`网络的，如 OpenVPN, vtun或Openssh的 VPN 特性。

最后要说明的是，在TCP之上运行隧道并没有任何意义，上述使用场景被称为"tcp之上的tcp"，更多参见[Why tcp over tcp is a bad idea](http://sites.inka.de/~W1011/devel/tcp-tcp.html)。OpenVPN等应用程序默认使用UDP正是出于这个原因，使用TCP会导致性能降低。

参考

Reference：

[Linux tun:tap 详解](https://zhuanlan.zhihu.com/p/293658778)

[Tun/Tap接口指导](https://www.cnblogs.com/charlieroro/p/13497340.html)

[The IFF_ prefix stands for "interface flags.=>from Linux Device Drivers, 2nd Edition"](https://www.xml.com/ldd/chapter/book/ch14.html#t3)
