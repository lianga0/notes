## 透明代理(TPROXY)

> From: https://toutyrater.github.io/app/tproxy.html

原来出过一篇透明代理的教程，但过了许久，V2Ray 也已经迭代了好多个版本。原来的教程依旧可以正常使用，但随着 V2Ray 的更新，V2Ray 推出了新的透明代理方式—— TPROXY，原来的叫 REDIRECT。最近测试了一下 TPROXY ，效果还不错，主观感觉比 REDIRECT 好。并且在本文的透明代理中，DNS 服务将由 V2Ray 提供。不过这种方式需要 iptables 的 TPROXY 模块支持，有一些阉割版的系统会精简掉 TPROXY 模块，这种系统是不适用于本文的。

普通家庭大多数是光纤入户接光猫调制解调，一个路由器的 WAN 口接光猫的 LAN 口，要上网的设备（如 PC 、电视盒子、手机）接路由器 LAN 口。本文的透明代理需要一台 Linux 主机接路由器 LAN 口，作为局域网中的网关，为其他接入局域网中的设备提供翻墙功能。这样的方式与我原来的透明代理教程是一样的，都是搭建在一个 Linux 主机上。这样可以透明代理的设备，有的人叫“透明网关”，也有的叫“旁路由”。我觉得这种不是很严肃的场合，叫什么都行，只要不妨碍理解。

很多设备都可以做透明网关，路由器、开发板、个人电脑、虚拟机和 Android 设备等。路由器可能比较特殊点，因为它本身就可以充当网关。上面可能说得太抽象，我就举些实际的，比如说树莓派、香橙派、用 PC 装的 Linux 虚拟机、淘宝的工控机（如 j1900）、NAS、电视盒子（如翻车迅）、你刚配的牙膏厂或农厂的电脑，这些都没问题。至于到底用什么？这得看需求，我觉得网络 200M 以下搞个高性能的类树莓派的 SBC 就够了，200M 以上就得考虑 X86 主机了（如今甚火的软路由）。当然，到底怎么选择还是得看自己。

本文假设你已经有一个设备（就以树莓派举例），将用来作网关（或说旁路由），并且已经安装好 Linux。关于系统，我更推荐 Debian 或 Debian 衍生版。为方面起见，本文均以 root 权限账户执行命令。并且有一台 PC 以便于操作。

### 1.1. 设置网关

用网线将树莓派接入路由器 LAN 口，假设分给树莓派的 IP 是 192.168.1.22。

树莓派开启 IP 转发（需要开启 IP 转发才能作为网关）。命令为 echo net.ipv4.ip_forward=1 >> /etc/sysctl.conf && sysctl -p。执行后将出现 net.ipv4.ip_forward=1 的提示。

手动配置 PC 的网络，将默认网关指向树莓派的地址即 192.168.1.22。此时 PC 应当能正常上网（由于还没设置代理，“正常”是指可以上国内的网站）。

1.2. 树莓派安装配置 V2Ray

安装 V2Ray。可以使用 V2Ray 提供的 go.sh 脚本安装，由于 GFW 会恶化对 GitHub 的访问，直接运行脚本几乎无法安装，建议先下载 V2Ray 的压缩包，然后用安装脚本通过 --local 参数进行安装。

配置 V2Ray。按照前文教程将 V2Ray 配置成客户端形式。然后执行 curl -so /dev/null -w "%{http_code}" google.com -x socks5://127.0.0.1:1080 确认 V2Ray 已经可以翻墙(命令中 socks5 指 inbound 协议为 socks，1080 指该 inbound 端口是 1080)。如果执行这个命令出现了 301 或 200 这类数字的话代表可以翻墙，如果长时间没反应或者是 000 的话说明不可以翻墙。

### 1.3. 配置透明代理

#### 1.3.1. 为 V2Ray 配置透明代理的入站和 DNS 分流

以下是 V2Ray 透明代理的配置示例

```
{
  "inbounds": [
    {
      "tag":"transparent",
      "port": 12345,
      "protocol": "dokodemo-door",
      "settings": {
        "network": "tcp,udp",
        "followRedirect": true
      },
      "sniffing": {
        "enabled": true,
        "destOverride": [
          "http",
          "tls"
        ]
      },
      "streamSettings": {
        "sockopt": {
          "tproxy": "tproxy" 
        }
      }
    },
    {
      "port": 1080, 
      "protocol": "socks", 
      "sniffing": {
        "enabled": true,
        "destOverride": ["http", "tls"]
      },
      "settings": {
        "auth": "noauth"
      }
    }
  ],
  "outbounds": [
    {
      "tag": "proxy",
      "protocol": "vmess",
      "settings": {
        "vnext": [{
            "address": "server_ip_address",
            "port": 10086,
            "users": [
              {
                "id": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
              }]
        }]
      },
      "streamSettings": {
        "sockopt": {
          "mark": 255
        }
      },
      "mux": {
        "enabled": true
      }
    },
    {
      "tag": "direct",
      "protocol": "freedom",
      "settings": {
        "domainStrategy": "UseIP"
      },
      "streamSettings": {
        "sockopt": {
          "mark": 255
        }
      }      
    },
    {
      "tag": "block",
      "protocol": "blackhole",
      "settings": {
        "response": {
          "type": "http"
        }
      }
    },
    {
      "tag": "dns-out",
      "protocol": "dns",
      "streamSettings": {
        "sockopt": {
          "mark": 255
        }
      }  
    }
  ],
  "dns": {
    "servers": [
      "8.8.8.8", 
      "1.1.1.1", 
      "114.114.114.114", 
      {
        "address": "223.5.5.5", 
        "port": 53,
        "domains": [
          "geosite:cn",
          "ntp.org"
        ]
      }
    ]
  },
  "routing": {
    "domainStrategy": "IPOnDemand",
    "rules": [
      { 
        "type": "field",
        "inboundTag": [
          "transparent"
        ],
        "port": 53,
        "network": "udp",
        "outboundTag": "dns-out" 
      },    
      { 
        "type": "field",
        "inboundTag": [
          "transparent"
        ],
        "port": 123,
        "network": "udp",
        "outboundTag": "direct" 
      },    
      {
        "type": "field", 
        "ip": [ 
          "223.5.5.5",
          "114.114.114.114"
        ],
        "outboundTag": "direct"
      },
      {
        "type": "field",
        "ip": [ 
          "8.8.8.8",
          "1.1.1.1"
        ],
        "outboundTag": "proxy" 
      },
      { 
        "type": "field", 
        "domain": [
          "geosite:category-ads-all"
        ],
        "outboundTag": "block"
      },
      { 
        "type": "field",
        "protocol":["bittorrent"], 
        "outboundTag": "direct"
      },
      { 
        "type": "field", 
        "ip": [
          "geoip:private",
          "geoip:cn"
        ],
        "outboundTag": "direct"
      },
      { 
        "type": "field", 
        "domain": [
          "geosite:cn"
        ],
        "outboundTag": "direct"
      }
    ]
  }
}
```

以上是 V2Ray 透明代理的参考配置，关于配置有一些注意点及说明:

- dokodemo-door 是用来接收透明代理的入站协议，followRedirect 项须为 true 以及 sockopt.tproxy 项须为 tproxy，建议开启 sniffing，否则路由无法匹配域名；

- 本节添加了 DNS 配置，用来对国内外域名进行 DNS 分流，需要 DNS 配置、DNS 入站、DNS 出站和路由四者配合，在本例中 DNS 入站直接使用透明代理入站，可参考 DNS 及其应用；

- 在 DNS 配置中，依次配置了 Google、Cloudflare、114 和阿里的 DNS，由于在阿里的 DNS 中指定了 domain，所以匹配的域名会用阿里的 DNS 查询，其他的先查询 Google 的 DNS，如果查不到的话再依次查 Cloudflare 及 114 的。所以达到了国内外域名 DNS 分流，以及 DNS 备用。要注意把 NTP 服务器和你自己 VPS 域名也加入到直连的 DNS ，否则会导致 V2Ray 无法与 VPS 正常连接；

- DNS 配置只是说明哪些域名查哪个 DNS，至于哪个 DNS 走代理哪个 DNS 直连要在 routing 里设置规则；

- routing 也要设置 123 端口的 UDP 流量直连，不然的话要是时间误差超出允许范围(90s)，要使用 NTP 校准时间就要先连上代理，但是连代理又要确保时间准确，结果就是既连不上代理，也无法自动校准时间；

- freedom 的出站设置 domainStrategy 为 UseIP，以避免直连时因为使用本机的 DNS 出现一些奇怪问题；

- 注意要在所有的 outbound 加一个 255 的 mark,这个 mark 与下文 iptables 命令中 iptables -t mangle -A V2RAY_MASK -j RETURN -m mark --mark 0xff 配合，以直连 V2Ray 发出的流量（blackhole 可以不配置 mark）。

#### 1.3.2. 配置透明代理规则

执行下面的命令开启透明代理。由于使用了 TPROXY 方式的透明代理，所以 TCP 流量也是使用 mangle 表。以下命令中，以 # 开头的为注释。

```
ip rule add fwmark 1 table 100
ip route add local 0.0.0.0/0 dev lo table 100


iptables -t mangle -N V2RAY
iptables -t mangle -A V2RAY -d 127.0.0.1/32 -j RETURN
iptables -t mangle -A V2RAY -d 224.0.0.0/4 -j RETURN
iptables -t mangle -A V2RAY -d 255.255.255.255/32 -j RETURN
iptables -t mangle -A V2RAY -d 192.168.0.0/16 -p tcp -j RETURN 
iptables -t mangle -A V2RAY -d 192.168.0.0/16 -p udp ! --dport 53 -j RETURN 
iptables -t mangle -A V2RAY -p udp -j TPROXY --on-port 12345 --tproxy-mark 1 
iptables -t mangle -A V2RAY -p tcp -j TPROXY --on-port 12345 --tproxy-mark 1 
iptables -t mangle -A PREROUTING -j V2RAY 
```
#### 1.4. 开机自动运行透明代理规则

由于策略路由以及iptables 有重启会失效的特性，所以当测试配置没有问题之后，需要再弄个服务在开机时自动配置策略路由和 iptables，否则每次开机的时候就要手动来一遍了。

由于 iptables 命令有点多，所以先将 iptables 规则保存到 /etc/iptables/rules.v4 中。

```
mkdir -p /etc/iptables && iptables-save > /etc/iptables/rules.v4
```

在 /etc/systemd/system/ 目录下创建一个名为 tproxyrule.service 的文件，然后添加以下内容并保存。

```
[Unit]
Description=Tproxy rule
After=network.target
Wants=network.target

[Service]

Type=oneshot
#注意分号前后要有空格
ExecStart=/sbin/ip rule add fwmark 1 table 100 ; /sbin/ip route add local 0.0.0.0/0 dev lo table 100 ; /sbin/iptables-restore /etc/iptables/rules.v4

[Install]
WantedBy=multi-user.target
```

执行下面的命令使 tproxyrule.service 可以开机自动运行。

```
systemctl enable tproxyrule
```

#### 1.5.2. 设定网关为静态 IP

最好给网关设成静态IP，以免需要重启的时 IP 发生变化。如何设置请自行探究。 提示一下，如果你用 nmcli 命令设置静态 IP，最好先另外添加一个 connection 进行配置，配置好之后在切换到新添加的这个 connection 来。因为如果在原有的 connection 上直接修改成静态 IP 可能会导致无法透明代理。

#### 1.5.3. 设定 DHCP

在路由器上设定 DHCP，将网关地址指向网关设备，在本文的举例中即为树莓派的IP 192.168.1.22； DNS 随意，因为已经配置了劫持 53 端口的 UDP，当然填常规的 DNS 也更是没有问题的
