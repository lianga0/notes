### SMB/CIFS协议解析


#### SMB

SMB（Server Messages Block，信息服务块）是一种在局域网上共享文件和打印机的一种通信协议，它为局域网内的不同计算机之间提供文件及打印机等资源的共享服务。SMB协议是客户机/服务器型协议，客户机通过该协议可以访问服务器上的共享文件系统、打印机及其他资源。

SMB（Server Message Block）协议在NT/2000中用来作文件共享，在NT中，SMB运行于NBT（NetBIOS over TCP/IP）上，使用137，139（UDP），139（TCP）端口。 在2000中，SMB可以直接运行在tcp/ip上，而没有额外的NBT层，使用TCP 445端口。因此在2000上应该比NT稍微变化多一些。可以在“网络连接/属性/TCPIP协议/属性/高级/WINS中设置启用或者禁用 NBT（NetBIOS over TCP/IP）。 当2000使用网络共享的时候，就面临着选择139或者445端口了。下面的情况确定会话使用的端口：

1. 如果客户端启用了 NBT，那么连接的时候将同时访问139和445端口，如果从445端口得到回应，那么客户端将发送RST到139端口，终止这个端口的连接，接着就从 445端口进行SMB的会话了；如果没有从445端口而是从139得到回应，那么就从139端口进行会话；如果没有得到任何回应，那么SMB会话失败。

2. 如果客户端禁用了NBT，他就将只从445端口进行连接。当然如果服务器（开共享端）没有445端口进行SMB会话的话，那么就会访问失败了，所以禁用445端口后，对访问NT机器的共享会失败。

3. 如果服务器端启用NBT，那么就同时监听UDP 137、138端口和TCP139，445。如果禁用NBT，那么就只监听445端口了。 所以对于2000来说，共享问题就不仅仅是139端口，445端口同样能够完成。


#### SMB与Samba

Samba是在Linux和UNIX系统上实现SMB协议的一个免费软件，由服务器及客户端程序构成。通过设置“NetBIOS over TCP/IP”使得Samba不但能与局域网络主机分享资源，还能与全世界的电脑分享资源。


#### SMB与CIFS的联系

CIFS(Common Internet File System)协议，网络上部分文档写为SMB协议的另一种名称。MSND上其实是有关于SMB和CIFS之间关系的简介的。

The Server Message Block (SMB) Protocol is a network file sharing protocol, and as implemented in Microsoft Windows is known as Microsoft SMB Protocol. The set of message packets that defines a particular version of the protocol is called a dialect. The Common Internet File System (CIFS) Protocol is a dialect of SMB. Both SMB and CIFS are also available on VMS, several versions of Unix, and other operating systems.

在NetBIOS出现之后，Microsoft就使用NetBIOS实现了一个网络文件/打印服务系统，这个系统基于NetBIOS设定了一套文件共享协 议，Microsoft称之为SMB（Server Message Block）协议。这个协议被Microsoft用于它们Lan Manager和Windows NT服务器系统中，而Windows系统均包括这个协议的客户软件，因而这个协议在局域网系统中影响很大。

随着Internet的流行，Microsoft希望将这个协议扩展到Internet上去，成为Internet上计算机之间相互共享数据的一种标 准。因此它将原有的几乎没有多少技术文档的SMB协议进行整理，重新命名为CIFS（Common Internet File System），并打算将它与NetBIOS相脱离，试图使它成为Internet上的一个标准协议。

Reference：[SMB/CIFS协议解析（一）](https://blog.csdn.net/vevenlcf/article/details/43057435)

[Microsoft SMB Protocol and CIFS Protocol Overview](https://msdn.microsoft.com/en-us/library/windows/desktop/aa365233(v=vs.85).aspx)

[[MS-CIFS]: Common Internet File System (CIFS) Protocol](https://msdn.microsoft.com/en-us/library/ee442092.aspx)