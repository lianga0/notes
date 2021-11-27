# 透明代理

> 2021.08.13

因为疫情，在家办公需要测试Android应用中的购买功能，这就需要直接访问Google了。但又因为做的App是一个VPN应用，它排斥手机上的其他VPN，就只能选择在网关处做透明代理的方案。

因为之前研究过V2Ray的[透明代理(TPROXY)](https://toutyrater.github.io/app/tproxy.html)方案，心想可以临时用用。

可是谁知，好不容易找到一个机场，可是机场只能用`rc4-md5`加密方式，而悲催的是V2Ray不支持这种加密方式。运行即报如下错误：

```
/usr/local/bin/v2ray -config /usr/local/etc/v2ray/config.json
V2Ray 4.40.1 (V2Fly, a community-driven edition of V2Ray.) Custom (go1.16.5 linux/amd64)
A unified platform for anti-censorship.
2021/08/13 18:11:34 [Info] main/jsonem: Reading config: /usr/local/etc/v2ray/config.json
main: failed to read config files: [/usr/local/etc/v2ray/config.json] > infra/conf: unknown cipher method: rc4-md5
```

无奈只能使用`ShadowsocksR`客户端，考虑到`ShadowsocksR`支持从局域连接，那在网关处也不一定非要用`V2Ray`的方案。只要找到正确的转发流量方式，把流量转给`ShadowsocksR`客户端不就解决问题了。

幸运的是很快就找到[ipt2socks](https://github.com/zfl9/ipt2socks)这个工具。ipt2socks(libev)实用工具用于将 iptables(REDIRECT/TPROXY) 流量转换为 socks5(tcp/udp) 流量。

安装完成后，使用如下命令启动工具：

```
# -s 指定 socks5 服务器 ip
# -p 指定 socks5 服务器端口
# -R use redirect instead of tproxy for tcp
# -l listen port number, default: 60080

ipt2socks -R -s 127.0.0.1 -p 1080
```

然后参照[透明代理（REDIRECT）](https://toutyrater.github.io/app/transparent_proxy.html)章节中设定透明代理的 iptables 规则。

设定 TCP 透明代理的 iptables 规则，命令如下(#代表注释)：

```
iptables -t nat -N V2RAY # 新建一个名为 V2RAY 的链
iptables -t nat -A V2RAY -d 192.168.0.0/16 -j RETURN # 直连 192.168.0.0/16 
iptables -t nat -A V2RAY -p tcp -j RETURN -m mark --mark 0xff # 直连 SO_MARK 为 0xff 的流量(0xff 是 16 进制数，数值上等同与上面配置的 255)，此规则目的是避免代理本机(网关)流量出现回环问题
iptables -t nat -A V2RAY -p tcp -j REDIRECT --to-ports 60080 # 其余流量转发到 12345 端口（即 V2Ray）
iptables -t nat -A PREROUTING -p tcp -j V2RAY # 对局域网其他设备进行透明代理
iptables -t nat -A OUTPUT -p tcp -j V2RAY # 对本机进行透明代理
```

然后设定 UDP 流量透明代理的 iptables 规则，命令如下

```
ip rule add fwmark 1 table 100
ip route add local 0.0.0.0/0 dev lo table 100
iptables -t mangle -N V2RAY_MASK
iptables -t mangle -A V2RAY_MASK -d 192.168.0.0/16 -j RETURN
iptables -t mangle -A V2RAY_MASK -p udp -j TPROXY --on-port 12345 --tproxy-mark 1
iptables -t mangle -A PREROUTING -p udp -j V2RAY_MASK
使用电脑/手机尝试直接访问被墙网站，这时应该是可以访问的。
```

> 最开始尝试参考[透明代理(TPROXY)](https://toutyrater.github.io/app/tproxy.html)中iptables规则设置`TPROXY`，但不知道什么原因，设置并不怎么成功，以后有精力再研究下iptables的使用细节。

Reference：[希望shadowsocks支持rc4-md5加密 #2630](https://github.com/v2ray/v2ray-core/issues/2630)




<br />



因为上边设定电脑重启后就没了，全部命令记录如下以方便下次直接使用：

```
sysctl -w net.ipv4.ip_forward=1

ipt2socks -R -s 192.168.31.79 -p 1080



iptables -t nat -N V2RAY 
iptables -t nat -A V2RAY -d 192.168.0.0/16 -j RETURN
iptables -t nat -A V2RAY -p tcp -j RETURN -m mark --mark 0xff 
iptables -t nat -A V2RAY -p tcp -j REDIRECT --to-ports 60080 
iptables -t nat -A PREROUTING -p tcp -j V2RAY 
iptables -t nat -A OUTPUT -p tcp -j V2RAY


ip rule add fwmark 1 table 100
ip route add local 0.0.0.0/0 dev lo table 100
iptables -t mangle -N V2RAY_MASK
iptables -t mangle -A V2RAY_MASK -d 192.168.0.0/16 -j RETURN
iptables -t mangle -A V2RAY_MASK -p udp -j TPROXY --on-port 12345 --tproxy-mark 1
iptables -t mangle -A PREROUTING -p udp -j V2RAY_MASK
```