# Linux端口转发的几种常用方法

> https://cloud.tencent.com/developer/article/1688152

## ncat 端口转发

netcat（简称nc）被誉为网络安全界的”瑞士军刀“，一个简单而有用的工具，这里介绍一种使用netcat实现端口转发的方法。

1. 安装ncat

```
yum install nmap-ncat -y
```

2. 监听本机 9876 端口，将数据转发到 192.168.172.131的 80 端口

```
ncat --sh-exec "ncat 192.168.172.131 80" -l 9876  --keep-open
```

## socat 端口转发

socat是一个多功能的网络工具，使用socat进行端口转发。

1. socat安装

```
yum install -y socat
```

2. 在本地监听12345端口，并将请求转发至192.168.172.131的22端口。

```
socat TCP4-LISTEN:12345,reuseaddr,fork TCP4:192.168.172.131:22
```
