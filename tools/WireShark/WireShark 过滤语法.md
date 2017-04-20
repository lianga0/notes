### WireShark 过滤语法

##### 0. WireShark逻辑操作符

```
lt 小于
le 小于等于
eq 等于
gt 大于
ge 大于等于
ne 不等
```

##### 1. 过滤IP。

指定源IP或者目的IP查找

例子:查找指定IP所有数据包
```
ip.src eq 192.168.1.107 or ip.dst eq 192.168.1.107
```

或者
```
ip.addr eq 192.168.1.107
```

##### 2. 过滤端口。

指定UPD或TCP协议端口的数据包

例子：查找指定端口数据包
```
tcp.port eq 80 // 不管端口是来源的还是目标的都显示
tcp.port == 80
tcp.port eq 2722
tcp.port eq 80 or udp.port eq 80
tcp.dstport == 80 // 只显tcp协议的目标端口80
tcp.srcport == 80 // 只显tcp协议的来源端口80

udp.port eq 15000
```

例子：过滤指定端口范围
```
tcp.port >= 1 and tcp.port <= 80
```

##### 3. 过滤协议

例子: 仅显示指定协议数据包
```
tcp
udp
arp
icmp
http
smtp
ftp
dns
msnms
ip
oicq
bootp
等等
```

排除指定协议
```
!arp 或者 not arp  //排除arp协议的数据包
```

##### 4. 过滤MAC

按MAC地址过滤
```
eth.dst == A0:00:00:04:C5:84 // 过滤目标mac
eth.src eq A0:00:00:04:C5:84 // 过滤来源mac
eth.dst==A0:00:00:04:C5:84
eth.dst==A0-00-00-04-C5-84
eth.addr eq A0:00:00:04:C5:84 // 过滤来源MAC和目标MAC都等于A0:00:00:04:C5:84的
```

##### 5. 包长度过滤

```
udp.length == 26 这个长度是指udp本身固定长度8加上udp下面那块数据包之和
tcp.len >= 7 指的是ip数据包(tcp下面那块数据),不包括tcp本身
ip.len == 94 除了以太网头固定长度14,其它都算是ip.len,即从ip本身到最后
frame.len == 119 整个数据包长度,从eth开始到最后
```

##### 6. http模式过滤

过滤HTTP协议指定条件包
```
http.request.method == "GET"
http.request.method == "POST"
http.request.uri == "/img/logo-edu.gif"
http contains "GET"
http contains "HTTP/1."

// GET包
http.request.method == "GET" && http contains "Host: "
http.request.method == "GET" && http contains "User-Agent: "
// POST包
http.request.method == "POST" && http contains "Host: "
http.request.method == "POST" && http contains "User-Agent: "
// 响应包
http contains "HTTP/1.1 200 OK" && http contains "Content-Type: "
http contains "HTTP/1.0 200 OK" && http contains "Content-Type: "
```

##### 7. TCP参数过滤

```
tcp.flags 显示包含TCP标志的封包。
tcp.flags.syn == 0x02   显示包含TCP SYN标志的封包。
tcp.window_size == 0 && tcp.flags.reset != 1
```

##### 8. 过滤内容

获取数据包指定位置范围的值
```
tcp[20]表示从20开始，取1个字符
tcp[20:]表示从20开始，取1个字符以上
tcp[20:8]表示从20开始，取8个字符
tcp[offset,n]

udp[8:3]==81:60:03 // 偏移8个bytes,再取3个数，是否与==后面的数据相等
udp[8:1]==32 如果我猜的没有错的话，应该是udp[offset:截取个数]=nValue
eth.addr[0:3]==00:06:5B
```

例子：判断upd下面那块数据包前三个字节是否等于0x20 0x21 0x22
```
udp[8:3]==20:21:22  //udp数据包头部固定长度为8
```

判断tcp那块数据包前三个是否等于0x20 0x21 0x22

```
tcp[8:3]==20:21:22
```

tcp一般情况下，长度为20,但也有不是20的时候。如果想得到最准确的，应该先知道tcp长度。

matches(匹配)和contains(包含某字符串)语法
```
ip.src==192.168.1.107 and udp[8:5] matches "\\x02\\x12\\x21\\x00\\x22"
ip.src==192.168.1.107 and udp contains 02:12:21:00:22
ip.src==192.168.1.107 and tcp contains "GET"
udp contains 7c:7c:7d:7d //匹配payload中含有0x7c7c7d7d的UDP数据包
```

wireshark支持正则表达式，更详细的说明[wireshark过滤表达式实例介绍](http://www.csna.cn/viewthread.php?tid=14614)

Reference：[WireShark 过滤语法](http://blog.csdn.net/grmsu/article/details/6642639)