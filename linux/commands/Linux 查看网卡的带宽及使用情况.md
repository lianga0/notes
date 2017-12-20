### Linux 查看网卡的带宽及使用情况

##### Linux中使用`ifconfig`查看机器网络端口配置信息

```
$ ifconfig
eth0      Link encap:Ethernet  HWaddr 5C:B9:01:9A:48:5D
          inet addr:10.10.11.12  Bcast:10.10.11.255  Mask:255.255.255.0
          inet6 addr: fe80::5eb9:1ff:fe9a:485d/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:18033924355 errors:0 dropped:857504 overruns:0 frame:0
          TX packets:52425526574 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:66937144646066 (60.8 TiB)  TX bytes:60037314294532 (54.6 TiB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:1192347276 errors:0 dropped:0 overruns:0 frame:0
          TX packets:1192347276 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0
          RX bytes:9188133537474 (8.3 TiB)  TX bytes:9188133537474 (8.3 TiB)
```

##### `ethtool`查看端口带宽，通过下面输出可以看到speed那一行，表示千兆网。

```
$ sudo ethtool eth0
Settings for eth0:
        Supported ports: [ TP ]
        Supported link modes:   10baseT/Half 10baseT/Full 
                                100baseT/Half 100baseT/Full 
                                1000baseT/Full 
        Supported pause frame use: No
        Supports auto-negotiation: Yes
        Advertised link modes:  10baseT/Half 10baseT/Full 
                                100baseT/Half 100baseT/Full 
                                1000baseT/Full 
        Advertised pause frame use: No
        Advertised auto-negotiation: Yes
        Speed: 1000Mb/s      /////////// 网卡流速上限
        Duplex: Full
        Port: Twisted Pair
        PHYAD: 0
        Transceiver: internal
        Auto-negotiation: on
        MDI-X: off (auto)
        Supports Wake-on: d
        Wake-on: d
        Current message level: 0x00000007 (7)
                               drv probe link
        Link detected: yes

```

##### `nload` 显示当前网络使用情况（displays the current network usage）

```
Device eth0 [10.206.131.20] (1/2):  
============================================
Incoming:       

                
                
                           Curr: 16.59 kBit/s
                           Avg: 10.83 kBit/s
                           Min: 2.34 kBit/s
                           Max: 19.86 kBit/s
                           Ttl: 1.48 GByte
Outgoing:       
                

                
                           Curr: 9.38 kBit/s
                           Avg: 9.21 kBit/s
                           Min: 5.20 kBit/s
                           Max: 9.85 kBit/s
                           Ttl: 216.75 MByte
```

##### `vnstat --live`显示当前网络使用情况

```
$ vnstat --live
Monitoring eth0...    (press CTRL-C to stop)

   rx:        9 kbit/s     7 p/s          tx:        1 kbit/s     0 p/s
```

##### `iftop` 可查看实时的端对端流量

display bandwidth usage on an interface by host. iftop must be run with sufficient permissions to monitor all network traffic on the  interface;

##### `ss` 连接查看工具，another utility to investigate sockets。

It allows showing information similar to netstat.  It can display more TCP and state informations than other tools.

From: [Linux 查看网络带宽是千兆还是万兆](http://blog.csdn.net/post_yuan/article/details/54378994)

[Linux 下大家喜欢用什么命令查看流量？](https://www.zhihu.com/question/19862245)