## NetBIOS

NetBIOS (/ˈnɛtbaɪɒs/) is an acronym for Network Basic Input/Output System. It provides services related to the session layer of the OSI model allowing applications on separate computers to communicate over a local area network. As strictly an API, NetBIOS is not a networking protocol. Older operating systems[clarification needed] ran NetBIOS over IEEE 802.2 and IPX/SPX using the NetBIOS Frames (NBF) and NetBIOS over IPX/SPX (NBX) protocols, respectively. In modern networks, NetBIOS normally runs over TCP/IP via the NetBIOS over TCP/IP (NBT) protocol. This results in each computer in the network having both an IP address and a NetBIOS name corresponding to a (possibly different) host name.

NetBIOS is an OSI Session Layer 5 Protocol and a service that allows applications on computers to communicate with one another over a local area network (LAN). It is a non-routable Protocol and NetBIOS stands for Network Basic Input/Output System. NetBIOS was developed in 1983 by Sytek Inc. as an API for software communication over IBM PC Network LAN technology. On PC-Network, as an API alone, NetBIOS relied on proprietary Sytek networking protocols for communication over the wire.[citation needed] Despite supporting a maximum of 80 PCs in a LAN, NetBIOS became an industry standard.

In 1985, IBM went forward with the token ring network scheme and a NetBIOS emulator was produced to allow NetBIOS-aware applications from the PC-Network era to work over this new design. This emulator, named NetBIOS Extended User Interface (NetBEUI), expanded the base NetBIOS API with, among other things, the ability to deal with the greater node capacity of token ring. A new networking protocol, NBF(NetBIOS Frames), was simultaneously produced to allow NetBEUI (NetBIOS) to provide its services over token ring – specifically, at the IEEE 802.2 Logical Link Control layer.

In 1985, Microsoft created a NetBIOS implementation for its MS-Net networking technology. As in the case of IBM's token ring, the services of Microsoft's NetBIOS implementation were provided over the IEEE 802.2 Logical Link Control layer by the NBF protocol. Until Microsoft adopted Domain Name System (DNS) resolution of hostnames Microsoft operating systems used NetBIOS to resolve names in Windows client-server networks.

In 1987, a method of encapsulating NetBIOS in TCP and UDP packets, NetBIOS over TCP/IP (NBT), was published. It was described in RFC 1001 ("Protocol Standard for a NetBIOS Service on a TCP/UDP Transport: Concepts and Methods") and RFC 1002 ("Protocol Standard for a NetBIOS Service on a TCP/UDP Transport: Detailed Specifications"). The NBT protocol was developed in order to "allow an implementation of [NetBIOS applications] to be built on virtually any type of system where the TCP/IP protocol suite is available," and to "allow NetBIOS interoperation in the Internet."

### TL;DR，NetBIOS（排除group name）基本上可以认为等价于hostname（机器名或主机名）。

NetBIOS is an acronym for Network Basic Input/Output System. It provides services related to the session layer of the OSI model allowing applications on separate computers to communicate over a local area network. As strictly an API, NetBIOS is not a networking protocol. Older operating systems[clarification needed] ran NetBIOS over IEEE 802.2 and IPX/SPX using the NetBIOS Frames (NBF) and NetBIOS over IPX/SPX (NBX) protocols, respectively. In modern networks, NetBIOS normally runs over TCP/IP via the NetBIOS over TCP/IP (NBT) protocol. This results in each computer in the network having both an IP address and a NetBIOS name corresponding to a (possibly different) host name.

NETBIOS协议是由IBM公司开发，主要用于数十台计算机的小型局域网。该协议是一种在局域网上的程序可以使用的应用程序编程接口（API），为程序提供了请求低级服务的统一的命令集，作用是为了给局域网提供网络以及其他特殊功能。系统可以利用WINS服务、广播及Lmhost文件等多种模式将NetBIOS名-——特指基于NETBIOS协议获得计算机名称——解析为相应IP地址，实现信息通讯，所以在局域网内部使用NetBIOS协议可以方便地实现消息通信及资源的共享。因为它占用系统资源少、传输效率高，所以几乎所有的局域网都是在NetBIOS协议的基础上工作的。NetBIOS是Network Basic Input/Output System的简称，一般指用于局域网通信的一套API

## NetBEUI

`NetBEUI`(NetBIOS Enhanced User Interface) is an enhanced version of the NetBios protocol that is used by Microsoft Windows networking. It is a non-routable protocol, which means that computers that are not located on the same network segment or subnet can't communicate.

## NetBIOS name vs Internet host name

When NetBIOS is run in conjunction with Internet protocols (e.g., NBT), each computer may have multiple names: one or more NetBIOS name service names and one or more Internet host names.

### NetBIOS name

The NetBIOS name is 16 ASCII characters, however Microsoft limits the host name to 15 characters and reserves the 16th character as a NetBIOS Suffix. This suffix describes the service or name record type such as host record, master browser record, or domain controller record or other services. **The host name (or short host name) is specified when Windows networking is installed/configured, the suffixes registered are determined by the individual services supplied by the host.** In order to connect to a computer running TCP/IP via its NetBIOS name, the name must be resolved to a network address. Today this is usually an IP address (the NetBIOS name to IP address resolution is often done by either broadcasts or a WINS Server – NetBIOS Name Server). **A computer's NetBIOS name is often the same as that computer's host name (see below), although truncated to 15 characters, but it may also be completely different.**

NetBIOS names are a sequence of alphanumeric characters. The following characters are explicitly not permitted:` \/:*?"<>|`. Since Windows 2000, NetBIOS names also had to comply with restrictions on DNS names: they cannot consist entirely of digits, and the hyphen ("-") or full-stop (".") characters may not appear as the first or last character. Since Windows 2000, Microsoft has advised against including any full-stop (".") characters in NetBIOS names, such that applications can use the presence of a full-stop to distinguish domain names from NetBIOS names.

The Windows LMHOSTS file provides a NetBIOS name resolution method that can be used for small networks that do not use a WINS server.

### Internet host name

A Windows machine's NetBIOS name is not to be confused with the computer's Internet host name. Generally a computer running Internet protocols (whether it is a Windows machine or not) has a host name (also sometimes called a machine name). Originally these names were stored in and provided by a hosts file but today most such names are part of the hierarchical Domain Name System (DNS). Generally the host name of a Windows computer is based on the NetBIOS name plus the Primary DNS Suffix, which are both set in the System Properties dialog box.

## Node types

The node type of a networked computer relates to the way it resolves NetBIOS names to IP addresses. There are four node types.

```
B-node: 0x01 Broadcast
P-node: 0x02 Peer (WINS only)
M-node: 0x04 Mixed (broadcast, then WINS)
H-node: 0x08 Hybrid (WINS, then broadcast)
```

The node type in use is displayed by opening a command line and typing `ipconfig /all` on windows. A Windows computer registry may also be configured in such a way as to display "unknown" for the node type.

```
ipconfig /all

Windows IP 配置

   主机名  . . . . . . . . . . . . . : nj-leo-z
   主 DNS 后缀 . . . . . . . . . . . : client.tw.trendnet.org
   节点类型  . . . . . . . . . . . . : 混合(H-node)
   IP 路由已启用 . . . . . . . . . . : 否
   WINS 代理已启用 . . . . . . . . . : 否
   DNS 后缀搜索列表  . . . . . . . . : client.tw.trendnet.org
                                       tw.trendnet.org
                                       trendnet.org
```

## Windows `Nbtstat` Command

**Nbtstat is designed to help troubleshoot NetBIOS name resolution problems.** When a network is functioning normally, NetBIOS over TCP/IP (NetBT) resolves NetBIOS names to IP addresses. It does this through several options for NetBIOS name resolution, including local cache lookup, WINS server query, broadcast, LMHOSTS lookup, Hosts lookup, and DNS server query.

```
nbtstat -h

显示协议统计和当前使用 NBI 的 TCP/IP 连接
(在 TCP/IP 上的 NetBIOS)。

NBTSTAT [ [-a RemoteName] [-A IP address] [-c] [-n]
        [-r] [-R] [-RR] [-s] [-S] [interval] ]

  -a   (适配器状态)    列出指定名称的远程机器的名称表
  -A   (适配器状态)    列出指定 IP 地址的远程机器的名称表。
  -c   (缓存)          列出远程[计算机]名称及其 IP 地址的 NBT 缓存
  -n   (名称)          列出本地 NetBIOS 名称。
  -r   (已解析)        列出通过广播和经由 WINS 解析的名称
  -R   (重新加载)      清除和重新加载远程缓存名称表
  -S   (会话)          列出具有目标 IP 地址的会话表
  -s   (会话)          列出将目标 IP 地址转换成计算机 NETBIOS 名称的会话表。
  -RR  (释放刷新)      将名称释放包发送到 WINS，然后启动刷新

  RemoteName   远程主机计算机名。
  IP address   用点分隔的十进制表示的 IP 地址。
  interval     重新显示选定的统计、每次显示之间暂停的间隔秒数。
               按 Ctrl+C 停止重新显示统计。
```

The options for the Nbtstat command are case sensitive. The Nbtstat switches are listed in the following table:

<table>
   <colgroup>
      <col style="">
      <col style="">
      <col style="">
   </colgroup>
   <thead>
      <tr class="header">
         <th class="">
            <p>Switch</p>
         </th>
         <th>
            <p>Name</p>
         </th>
         <th>
            <p>Function</p>
         </th>
      </tr>
   </thead>
   <tbody>
      <tr class="odd">
         <td>
            <p>-a &lt; <em>name</em> &gt;</p>
         </td>
         <td>
            <p>adapter status</p>
         </td>
         <td>
            <p>Returns the NetBIOS name table and MAC address of the address card for the computer name specified.</p>
         </td>
      </tr>
      <tr class="even">
         <td>
            <p>-A &lt; <em>IP address</em> &gt;</p>
         </td>
         <td>
            <p>Adapter status</p>
         </td>
         <td>
            <p>Lists the same information as -a when given the target's IP address.</p>
         </td>
      </tr>
      <tr class="odd">
         <td>
            <p>-c</p>
         </td>
         <td>
            <p>cache</p>
         </td>
         <td>
            <p>Lists the contents of the NetBIOS name cache.</p>
         </td>
      </tr>
      <tr class="even">
         <td>
            <p>[ <em>Number</em> ]</p>
         </td>
         <td>
            <p>Interval</p>
         </td>
         <td>
            <p>Typing a numerical value tells Nbtstat to redisplay selected statistics each interval seconds, pausing between each display. Press Ctrl+C to stop redisplaying statistics.</p>
         </td>
      </tr>
      <tr class="odd">
         <td>
            <p>-n</p>
         </td>
         <td>
            <p>names</p>
         </td>
         <td>
            <p>Displays the names registered locally by NetBIOS applications such as the server and redirector.</p>
         </td>
      </tr>
      <tr class="even">
         <td>
            <p>-r</p>
         </td>
         <td>
            <p>resolved</p>
         </td>
         <td>
            <p>Displays a count of all names resolved by broadcast or WINS server.</p>
         </td>
      </tr>
      <tr class="odd">
         <td>
            <p>-R</p>
         </td>
         <td>
            <p>Reload</p>
         </td>
         <td>
            <p>Purges the name cache and reloads all #PRE entries from LMHOSTS.</p>
         </td>
      </tr>
      <tr class="even">
         <td>
            <p>-RR</p>
         </td>
         <td>
            <p>ReleaseRefresh</p>
         </td>
         <td>
            <p>Releases and reregisters all names with the name server.</p>
         </td>
      </tr>
      <tr class="odd">
         <td>
            <p>-s</p>
         </td>
         <td>
            <p>sessions</p>
         </td>
         <td>
            <p>Lists the NetBIOS sessions table converting destination IP addresses to computer NetBIOS names.</p>
         </td>
      </tr>
      <tr class="even">
         <td>
            <p>-S</p>
         </td>
         <td>
            <p>Sessions</p>
         </td>
         <td>
            <p>Lists the current NetBIOS sessions and their status, with the IP address.</p>
         </td>
      </tr>
      <tr class="odd">
         <td>
            <p>/?</p>
         </td>
         <td>
            <p>Help</p>
         </td>
         <td>
            <p>Displays this list.</p>
         </td>
      </tr>
   </tbody>
</table>

The following is a sample command in windows 10:

```
> nbtstat -a NJ-XXXXXX-XXXX0

VirtualBox Host-Only Network:
节点 IP 址址: [192.168.56.1] 范围 ID: []

    找不到主机。

Ethernet:
节点 IP 址址: [10.64.34.28] 范围 ID: []

           NetBIOS 远程计算机名称表

       名称               类型         状态
    ---------------------------------------------
    NJ-XXXXXX-XXXX0<20>  唯一          已注册
    NJ-XXXXXX-XXXX0<00>  唯一          已注册
    TREND          <00>  组           已注册
    TREND          <1E>  组           已注册

    MAC 地址 = F4-8E-38-7E-1D-2A


> nbtstat -A 10.64.34.60

VirtualBox Host-Only Network:
节点 IP 址址: [192.168.56.1] 范围 ID: []

    找不到主机。

Ethernet:
节点 IP 址址: [10.64.34.28] 范围 ID: []

           NetBIOS 远程计算机名称表

       名称               类型         状态
    ---------------------------------------------
    NJ-XXXXXX-XXXX0<20>  唯一          已注册
    NJ-XXXXXX-XXXX0<00>  唯一          已注册
    TREND          <00>  组           已注册
    TREND          <1E>  组           已注册

    MAC 地址 = F4-8E-38-7E-1D-2A


> nbtstat -c

VirtualBox Host-Only Network:
节点 IP 址址: [192.168.56.1] 范围 ID: []

    缓存中没有名称

Ethernet:
节点 IP 址址: [10.64.34.28] 范围 ID: []

                  NetBIOS 远程缓存名称表

        名称              类型       主机地址    寿命[秒]
    ------------------------------------------------------------
    NJ-XXXXXX-XXXX0<20>  唯一              10.64.34.60         571
    NJ-XXXXXX-XXXX0<00>  唯一              10.64.34.60         571


>nbtstat -r

    NetBIOS 名称解析和注册统计
    ----------------------------------------------------

    通过广播解析的     = 0
    通过名称服务器解析   = 4

    通过广播注册的   = 51
    通过名称服务器注册的 = 11
```

## Windows Internet Name Service

Windows Internet Name Service (WINS) is Microsoft's implementation of NetBIOS Name Service (NBNS), a name server and service for NetBIOS computer names. Effectively, WINS is to NetBIOS names what DNS is to domain names — a central mapping of host names to network addresses. Like the DNS, it is implemented in two parts, a server service (that manages the embedded Jet Database, server to server replication, service requests, and conflicts) and a TCP/IP client component which manages the client's registration and renewal of names, and takes care of queries.

## NetBIOS Service codes in the NetBIOS suffix

> Wayne Maples POSTED ON MARCH 17, 2004

NetBIOS resources are referenced by name. Lower-level address information is not
available to NetBIOS applications. An application registers one or more names
that it wishes to use. **The NetBIOS name space is flat and uses sixteen
alphanumeric characters. Only 15 characters are available as the last letter is
reserved for service type**:

<table>
   <tbody>
      <tr>
         <td bgcolor="cyan">Name</td>
         <td bgcolor="cyan">Number(h)</td>
         <td bgcolor="cyan">Type</td>
         <td bgcolor="cyan">Usage</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">00<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">Workstation Service </td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">01<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">Messenger Service</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;\\--__MSBROWSE__&gt;<br></td>
         <td bgcolor="#ff9966">01<br></td>
         <td bgcolor="#66ff99">G<br></td>
         <td bgcolor="yellow">Master Browser</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">03<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">Messenger Service</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">06<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">RAS Server Service</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">1F<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">NetDDE Service</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">20<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">File Server Service</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">21<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">RAS Client Service</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">22<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">Microsoft Exchange Interchange(MSMail Connector)</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">23<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">Microsoft Exchange Store</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">24<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">Microsoft Exchange Directory</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">30<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">Modem Sharing Server Service</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">31<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">Modem Sharing Client Service</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">43<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">SMS Clients Remote Control</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">44<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">SMS Administrators Remote Control Tool</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">45<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">SMS Clients Remote Chat</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">46<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">SMS Clients Remote Transfer</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">4C<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">DEC Pathworks TCPIP service on Windows NT</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">42<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">mccaffee anti-virus</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">52<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">DEC Pathworks TCPIP service on Windows NT</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">87<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">Microsoft Exchange MTA</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">6A<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">Microsoft Exchange IMC</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">BE<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">Network Monitor Agent</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">BF<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">Network Monitor Application</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;username&gt;<br></td>
         <td bgcolor="#ff9966">03<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">Messenger Service</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;domain&gt;<br></td>
         <td bgcolor="#ff9966">00<br></td>
         <td bgcolor="#66ff99">G<br></td>
         <td bgcolor="yellow">Domain Name</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;domain&gt;<br></td>
         <td bgcolor="#ff9966">1B<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">Domain Master Browser</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;domain&gt;<br></td>
         <td bgcolor="#ff9966">1C<br></td>
         <td bgcolor="#66ff99">G<br></td>
         <td bgcolor="yellow">Domain Controllers</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;domain&gt;<br></td>
         <td bgcolor="#ff9966">1D<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">Master Browser</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;domain&gt;<br></td>
         <td bgcolor="#ff9966">1E<br></td>
         <td bgcolor="#66ff99">G<br></td>
         <td bgcolor="yellow">Browser Service Elections</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;INet~Services&gt;<br></td>
         <td bgcolor="#ff9966">1C<br></td>
         <td bgcolor="#66ff99">G<br></td>
         <td bgcolor="yellow">IIS</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;IS~computer name&gt;<br></td>
         <td bgcolor="#ff9966">00<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">IIS</td>
      </tr>
      <tr>
         <td bgcolor="yellow">&lt;computername&gt;<br></td>
         <td bgcolor="#ff9966">[2B]<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">Lotus Notes Server Service</td>
      </tr>
      <tr>
         <td bgcolor="yellow">IRISMULTICAST<br></td>
         <td bgcolor="#ff9966">[2F]<br></td>
         <td bgcolor="#66ff99">G<br></td>
         <td bgcolor="yellow">Lotus Notes</td>
      </tr>
      <tr>
         <td bgcolor="yellow">IRISNAMESERVER<br></td>
         <td bgcolor="#ff9966">[33]<br></td>
         <td bgcolor="#66ff99">G<br></td>
         <td bgcolor="yellow">Lotus Notes</td>
      </tr>
      <tr>
         <td bgcolor="yellow">Forte_$ND800ZA<br></td>
         <td bgcolor="#ff9966">[20]<br></td>
         <td bgcolor="#6699ff">U<br></td>
         <td bgcolor="yellow">DCA IrmaLan Gateway Server Service </td>
      </tr>
   </tbody>
</table>

### The NetBIOS name types describes the functionality:

U : unique - the name may have only one IP address assigned to it. On a network device multiple occurrences of a single name may appear to be registered. The suffix may be the only unique character in the name.

Unique (U): The name may have only one IP address assigned to it. On a network device, multiple occurences of a single name may appear to be registered, but the suffix will be unique, making the entire name unique.

G : group - a normal group; the single name may exist with many IP addresses. WINS responds to a name query on a group name with the limited broadcast address (255.255.255.255). Because routers block the transmission of these addresses, the Internet Group was designed to service
communications between subnets.

Group (G): A normal group; the single name may exist with many IP addresses.

M : multihomed - the name is unique, but due to multiple network interfaces on the same computer this configuration is necessary to permit the registration. The maximum number of addresses is 25.

Multihomed (M): The name is unique, but due to multiple network interfaces on the same computer, this configuration is necessary to permit the registration. Maximum number of addresses is 25.

I : Internet group - a special configuration of the group name used to manage Windows NT Domain names.

Internet Group (I): This is a special configuration of the group name used to manage WinNT domain names.

D : domain name - new in Windows NT 4.0.

## List of names registered with WINS Service

### Summary

Names registered by the WINS server can be divided into three groups:

- Computer Name
- Domain Name
- Other/Special Names

Each WINS Client actually registers its name with the WINS Server three or four times.

> NOTE: The MS-DOS clients that ship with Windows NT version 3.5 (LAN Manager version 2.2c client for MS-DOS and Microsoft Network Client version 3.0) provide support for WINS resolution, but not registration.

Several special NetBIOS names are also registered to maintain and retrieve browse lists. Names listed here are indicated by "Name(xx)" name followed by the hex value (xx) and padded with spaces to the 16th byte.

### Registered Computer Names:

```\\<computer_name>[00h]```

This name is registered for the WINS Client Workstation name.


```\\<computer_name>[03h]```

This name is registered for the Messenger Service on the WINS.


### Client:

```\\<computer_name>[BFh]```

Network monitoring utility (group name, registered when running netmon) This name is registered for the Network Monitoring Agent service and will only appear if the service is started on the system. If the computer name is not a full 15 characters, the name will be padded with plus (+) symbols.


```\\<computer_name>[BEh]```

Network monitoring agent (unique name, registered when remote agent is started)


```\\<computer_name>[1Fh]```

This name is registered for the Network Dynamic Data Exchange (NetDDE) services and will only appear if the NetDDE services are started on the system. By default, under Windows NT version 3.5, the NetDDE services are not automatically started.


```\\<computer_name>[20h]```

This name is registered for the Server Service on the WINS Client.


```\\<computer_name>[21h]```

RAS client.


```\\<computer_name>[06h]```

RAS server service.



### Registered Domain Names:

```\\<domain_name>[00h]```

This instance of the domain name is registered by the Workstation so that it can receive browser broadcasts from LAN Manager-based systems. This is the name to which server announcements are broadcast in Microsoft LAN Manager so that other Microsoft LAN Manager computers can track the servers on the network. Windows computers do not make these broadcasts unless the LMAnnounce option has been enabled by configuring the Server service in the Control Panel/Networks application.


```\\<domain_name>[1Bh]```

This instance of the domain name is registered by the Windows NT Server system that is running as the Domain Master Browser and is used to allow remote browsing of domains. When a WINS Server is queried for this name, a WINS Server returns the IP address of the system that registered this name.


```\\<domain_name>[1Ch]```

This name is registered for use by the domain controllers within the domain and can contain up to 25 IP addresses. One IP address will be that of the Primary Domain Controller (PDC) and the other 24 will be the IP addresses of Backup Domain Controllers (BDCs). The [1Ch] domain name is used by the BDCs to locate the PDC and is used when pass- through authentication is needed to validate a logon request.


```\\<domain_name>[1Dh]```

This instance of the domain name is registered only by the Master Browser, of which there can only be one for the domain. This name is used by the Backup Browsers to communicate with the Master Browser in order to retrieve the list of available servers from the Master Browser.



```\\<domain_name>[1Eh]```

This name is registered by all Browser servers and Potential Browser servers in a domain or workgroup. It is used for announcement requests which are sent by Master Browsers to fill up its browse lists, and for election request packets to force an election.


### Other/Special Names:

In addition to computer names and domain names, the following names also appear in the WINS database.

```\\--__MSBROWSE__[01h]```

This name is registered by the Master Browser and is used to broadcast and receive domain announcements on the local subnet. It is through this name that Master Browsers for different domains learn the names of different domains and the names of the Master Browsers on those domains. When a WINS Server receives a name query for this name, the WINS Server will always return the subnet broadcast address for the requesting client's local subnet.


```\\<username>[03h]```

When viewing the WINS database, the usernames for the currently logged on users will also be registered in the WINS database. The username is registered by the Server component so that the user can receive any 'net send' commands sent to their username.


## NMAP scripts sample

```
<script output="NetBIOS name: TOMMYPC, NetBIOS user: <unknown>, NetBIOS MAC: 84:4b:f5:1c:13:b4 (Hon Hai Precision Ind. Co.) Names:TOMMYPC<00> Flags: <unique><active>WORKGROUP<00> Flags: <group><active>TOMMYPC<20> Flags: <unique><active>WORKGROUP<1e> Flags: <group><active>WORKGROUP<1d> Flags: <unique><active>\x01\x02__MSBROWSE__\x02<01> Flags: <group><active>" id="nbstat">
    <table key="names">
        <table>
            <elem key="name">TOMMYPC</elem>
            <elem key="flags">1024</elem>
            <elem key="suffix">0</elem>
        </table>
        <table>
            <elem key="name">WORKGROUP</elem>
            <elem key="flags">33792</elem>
            <elem key="suffix">0</elem>
        </table>
        <table>
            <elem key="name">TOMMYPC</elem>
            <elem key="flags">1024</elem>
            <elem key="suffix">32</elem>
        </table>
        <table>
            <elem key="name">WORKGROUP</elem>
            <elem key="flags">33792</elem>
            <elem key="suffix">30</elem>
        </table>
        <table>
            <elem key="name">WORKGROUP</elem>
            <elem key="flags">1024</elem>
            <elem key="suffix">29</elem>
        </table>
        <table>
            <elem key="name">\x01\x02__MSBROWSE__\x02</elem>
            <elem key="flags">33792</elem>
            <elem key="suffix">1</elem>
        </table>
    </table>
    <elem key="server_name">TOMMYPC</elem>
    <table key="statistics">
        <elem>84 4b f5 1c 13 b4 00 00 00 00 00 00 00 00 00 00 00</elem>
        <elem>00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00</elem>
        <elem>00 00 00 00 00 00 00 00 00 00 00 00 00 00</elem>
    </table>
    <table key="mac">
        <elem key="address">84:4b:f5:1c:13:b4</elem>
        <elem key="manuf">Hon Hai Precision Ind. Co.</elem>
    </table>
    <elem key="user"><unknown></elem>
</script>
```

### what is `server_name`

In NMAP script, the `server_name` key is the entry in its NBSTAT table with a 0x20 suffix. Blow is the Lua Scripts

```
--- Sends out a UDP probe on port 137 to get the server's name (that is, the
--  entry in its NBSTAT table with a 0x20 suffix).
--@param host The IP or hostname of the server.
--@param names [optional] The names to use, from <code>do_nbstat</code>.
--@return (status, result) If status is true, the result is the NetBIOS name.
--        otherwise, result is an error message.
function get_server_name(host, names)

  local status
  local i

  if names == nil then
    status, names = do_nbstat(host)

    if(status == false) then
      return false, names
    end
  end

  for i = 1, #names, 1 do
    if names[i]['suffix'] == 0x20 then
      return true, names[i]['name']
    end

    if #names[i]['name'] > 0 then
      return true, names[i]['name']
    end
  end

  return false, "Couldn't find NetBIOS server name"
end
```
### what is `user`

The `user` key's value is use name. User name is the entry in its NBSTAT table with a 0x03 suffix, that isn't the same as the server's name. 
If the username can't be determined, which is frequently the case, nil is returned (XML will show `<unknown>`).


# How NetBIOS name resolution really works

## NetBIOS alone should not give you many headaches. Unfortunately, when NetBIOS problems occur they can be difficult to detect. Understanding how NetBIOS works is the key.

> By Robert L Bogue | March 11, 2003, 12:00 AM PST

One of the important steps in trying to resolve IP problems is determining if name resolution is working. It seems simple enough: If you can connect to a computer by IP address and not by NetBIOS name, the problem is with name resolution. That is great, but what happens if NetBIOS name resolution is not functioning? To help you overcome this obstacle, I will explore the components of NetBIOS resolution and help isolate the cause of name resolution problems.

### Which name are we talking about?

The first issue is determining the kind of name. In the Windows client world, there are two basic types of names. The first kind is a name for IP addresses. Host name resolution uses a host’s file and DNS for resolution. The second kind of name is the NetBIOS name, which is used for Windows (SMB) type sharing and messaging. These are the names that are used when you are mapping a drive or connecting to a printer. These names are resolved either by using an LMHosts file on the local machine or WINS server, or by broadcasting a request.

Just to muddy the waters, Microsoft allows IP host names to be used as a substitute for NetBIOS names. Although the net effect is making it easier to resolve names, the substitution strategy makes troubleshooting problems more difficult. You not only have to troubleshoot all of the NetBIOS name resolution options, but you must also troubleshoot the IP host name resolution. The best way to determine what is broken in NetBIOS name resolution, however, starts with understanding how NetBIOS name resolution works.

### How NetBIOS names work

NetBIOS names are located through a series of steps that begins with checking the local cache. You then check an LMHosts file and, lastly, progress into a broadcast message that looks for the name (that is, unless the default actions have been changed). Before you begin, you need to understand the four kinds of resolution that NetBIOS does natively.

**First resolution:** The first resolution mechanism is not really a resolution mechanism at all. It is an internal cache that is in each Windows machine. This cache is populated by previous name resolution attempts and by a special option in the LMHosts file (described next). The idea behind the cache is that, if the software needed to resolve the name once, it is quite likely that it will soon need to do so again. If you need to resolve the name again, the name is cached in order to improve responsiveness and limit network traffic. In order to reduce the possibility that the cache will become invalid because too much time has passed since the name was resolved, the cache has a limited lifetime, typically 10 minutes. However, entries put into cache by the LMHosts file option never expire. It is also important to have a limited lifetime for the cache to minimize the amount of memory used for caching. Although in today’s world of 512-MB desktop computers this may seem odd, it was a real concern when the NetBIOS naming strategy was developed and we were still dealing with conventional (640K) memory.

**Second resolution:** The second resolution method is where the LMHosts file is consulted to see if there are any NetBIOS names that match the NetBIOS name being queried. In its simplest form, the LMHosts file contains an IP address and a host name. In addition to the IP address and NetBIOS name, you have two more options. The first option is #PRE, which causes the entry to be cached into memory. This has little effect in today’s environment. The second option, #DOM (domain), is used to associate the computer with a NetBIOS domain name. This can be helpful if you are trying to find a domain controller to log into. The LMHosts file is located in %SYSTEMROOT%\SYSTEM32\DRIVERS\ETC. Typically, %SYSTEMROOT% is the C:\WINNT directory.

**Third resolution:** The third resolution mechanism used by the local computer to resolve the NetBIOS name involves consulting one or more naming servers. In most cases, the naming server contacted is a Windows Internet Naming Server (WINS). Technically, you could create a NetBIOS naming server that is not a WINS server, but it is rarely done. The NetBIOS naming server standard is an open standard controlled by RFC 1001 and RFC 1002. Each computer contacts the WINS server upon startup and provides the computer’s IP address, as well as its name. It stores this information into a database that may be replicated with other WINS servers. The WINS server also verifies that the name is not already in use. The database maintained by the WINS server is queried each time a client computer asks it to resolve a NetBIOS name. The WINS server can either resolve a name or not. There is no delegation of authority with a WINS server. Multiple WINS servers can be listed in the client configuration for consultation. In this case, the last WINS server to respond will be consulted. It is assumed to be a copy of all of the other WINS servers listed in the client configuration. The client will cycle through the list of its WINS servers until it locates one that is responsive.

**Fourth resolution:** The fourth and final resolution method is to broadcast for the NetBIOS name. The computer broadcasts a special packet that is received and processed by all machines on the network. The packet then requests that the computer identify itself. This is effective within a local network but is ineffective across routers, which do not forward broadcast packets. This means that the broadcast NetBIOS name resolution method does not work across routers. It can only be used for computers within the same IP subnet. Another problem with broadcast resolution is that it takes time from every computer. Finally, broadcast resolution requires that the packet be transmitted to every computer on a subnet. This can effectively eliminate the usefulness of a switch, which is designed to prevent computers from seeing traffic that is not destined for them. Since a broadcast is by definition destined for every computer on the subnet, it must be broadcast to every computer. As the amount of broadcast traffic increases, the switches tend to behave more like hubs—passing on every packet to every connected computer. The tendency to broadcast is one of the reasons that NetBIOS is not well liked in networking circles.

While the preceding is the default order, the order itself can be controlled via a node type attribute. The node type controls the order of resolution for the computer and the types of resolution consulted. The node type can never prevent the local cache from being consulted first, nor can it prevent the LMHosts file from being consulted. It only controls the behavior of the resolving computer with regard to when it will broadcast and when it will use a WINS server.

The node type can be set to only three modes. The first mode, B-mode, only uses the cache, LMHosts and broadcast. It will not try to use the WINS server. The second mode, P-mode, never broadcasts. It only uses the cache, LMHosts file, and WINS server. The final mode, H mode, or hybrid mode, behaves as described above by checking the LMHosts file and the WINS server, and then broadcasting. Hybrid mode is the default mode for all Windows workstations that have not had another node type provided via configuration or via DHCP.

### Types of NetBIOS names

Although we typically think just of computer names, there are many different kinds of NetBIOS names that you may need to resolve. Obviously, computer names need to be resolved to locate shared folders and printers. However, the names of logged-in users may also need to be resolved. The NetBIOS system allows you to send messages to users in addition to being able to attach to shared drives and printers; this requires that the system be able to resolve user names into IP addresses as well.

In addition, Windows domain names must be resolved. When a user attempts to log into a domain, the computer must contact a domain controller for the domain to verify the user account. The domain name is registered in a special way by all of the domain controllers within a domain so that the client will know which machines it can contact to validate username and password.

The way that these multiple name types are resolved is by recording a value in the 16th position of a registration. NetBIOS names have a fixed 16-byte format; however, Microsoft reserves the last byte for name type identification. This allows for registration of multiple types of names without redefining the standard to include a separate type field. This is important for a standard that was developed a long time ago and that had a substantial amount of deployed code.

### Resolving across the network

One of the most frequent problems that organizations have is managing NetBIOS name resolution across networks. Name resolution problems on local networks are often not visible because NetBIOS can resolve names via broadcast. Of course, broadcasting is not an option in networks attached to each other via routers. In local networks, even if other name resolution options fail, they may be masked by broadcast name resolution.

Of course, you can use LMHosts to handle cross-network name resolution; however, the administrative burden of doing this is prohibitive. This means that cross-network name resolution requests are almost always handled by WINS, which is tricky on its own.

If you are having problems resolving host names remotely, but not locally, you may need to review the details of how WINS works. Fortunately, Peter Parsons has full details on WINS and how to troubleshoot it in the article "Troubleshoot WINS on your Windows 2000 server." Before going that route, however, we need to test to see what the actual problem is.

### Testing NetBIOS name resolution

The tool to use for testing NetBIOS name resolution is NBTStat, which is short for NetBIOS over TCP/IP Status. This comes from the fact that originally NetBIOS used the NetBEUI protocol for transport. Today, most environments are only running NetBIOS naming across TCP/IP. This is frequently abbreviated NBT.

The first thing to do with NBTStat is to input `NBTStat –a <hostname>`, where `<hostname>` is the name that you are trying to resolve. NBTStat will display how that name was resolved on each network connection on your computer. This is helpful in several ways. First, the name resolution occurs without any other actions, so it is clear whether the name is resolving or not. Other techniques for determining whether name resolution is working may be testing more than just name resolution. Second, if the problem that you are trying to troubleshoot is one where the wrong address appears to have been received, it is possible to determine which adapter will lead to the wrong answer.

After running the NBTStat command, you may receive one of three results. First, the answer is correct and everything is working—at least for the moment. Second, the answer is incorrect. In other words, the wrong IP address is returned. Third, the answer is that there was no answer. The name did not resolve at all.

If the server returned the correct IP address for the name, then whatever problem that leads you to research the NetBIOS naming services is either broken or the problem you are troubleshooting is intermittent. If you get the wrong answer, you need to investigate the LMHosts file on the local machine in the %SYSTEMROOT%\SYSTEM32\DRIVERS\ETC directory, the WINS server’s registration database, and finally, the settings of the computers on the network.

If there is no answer, you must determine how you expected the name to be resolved. If either LMHosts file should have contained the answer or the WINS server should have contained the appropriate record, then you must review those sources. If, however, you anticipated that the answer would come from the other computer being on the network and responding to the broadcast for the name request, then either the computer is not responding to the broadcast name requests or it is never receiving it. The most likely cause of it not responding to a broadcast name request is because it is not on the same subnet as the computer making the request.

When resolving names with NBTStat, remember you can always try to resolve a name for a given IP address. This strategy can be helpful if you are unsure of the address and are trying to verify that the address returned is correct. The syntax of the command is `NBTStat –A <ip address>` where `<ip address>` is the IP address to test. The results will be the names registered to that IP address. If you resolve a name, then try to resolve the IP address without getting the same name, you know that your LMHosts file or WINS server contains a bad record for the NetBIOS name you have specified.

### All about cache

As we discussed above, in order to reduce the amount of name resolution traffic, each machine keeps a cache of the names that it has resolved previously. This cache is consulted before any other name resolution mechanism. This works well in most cases, but in cases where you have corrected an IP address that was wrong, it could be a problem. However, clearing the cache is easy. Just type “NBTStat –R.” This will clear the cache. If you want to confirm that the cache was cleared, you can type “NBTStat –c” to display the cache. By manually clearing the resolver cache, you can test your fixes.

### NetBIOS to DNS

Microsoft muddied the water when it allowed IP host names to be used to resolve NetBIOS names. Although the option has been removed from Windows 2000 and above, it is still a possible consideration when debugging clients. When enabled, the option causes the system to attempt to resolve NetBIOS names via DNS resolution. Therefore, in cases where you are getting incorrect IP addresses back from NetBIOS after having checked both the LMHosts file and WINS servers, you will have to troubleshoot IP host name resolution. For more information on NetBIOS and Windows 2000 see "Speed up Windows 2000 by eliminating NetBIOS."

### Browsing problems

Name resolution and browsing the network would seem to be closely related. If you can resolve all of the names on a network, then you should be able to browse the network. While this appears on the surface to be true, it is not. The mechanism for browsing is unrelated to the name resolution process.


Reference: [NetBIOS](https://en.wikipedia.org/wiki/NetBIOS)

[NetBIOS Service codes in the NetBIOS suffix](http://techgenix.com/netbiosservicecodesinthenetbiossuffix/)

[Registration of NetBIOS Names](https://www.petri.com/registration_of_netbios_names)

[RFC1001 - Protocol Standard for a NetBIOS service on a TCP/UDP transport](https://tools.ietf.org/html/rfc1001)

[List of names registered with WINS Service](https://support.microsoft.com/en-us/help/119495/list-of-names-registered-with-wins-service)

[Windows Internet Name Service](https://en.wikipedia.org/wiki/Windows_Internet_Name_Service)

[Nbtstat](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-2000-server/cc940106(v%3dtechnet.10))

[How NetBIOS name resolution really works](https://www.techrepublic.com/article/how-netbios-name-resolution-really-works/)

[Chapter 12 - Windows Internet Name Service Overview](https://docs.microsoft.com/en-us/previous-versions//bb727015(v=technet.10))