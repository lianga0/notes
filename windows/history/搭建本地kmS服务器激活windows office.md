# 搭建本地kmS服务器激活windows office

> https://segmentfault.com/a/1190000019997976

发布于 2019-08-07

## 准备

1. windows 或 linux 主机或需拟机一台  （假如ip 192.168.1.1）

2. 在主机安装 python 环境

3. git clone https://github.com/SystemRage/py-kms.git

## 运行kms服务器

1. 在准备中的服务器上进入clone下来仓库<a href="imgs/py-kms-master.zip">py-kmy</a>目录

2. 确认准备的kms服务器ip和需要激活的机器是否在一个网段或者通过ip能够互通（假如ip 192.168.1.2）

3. 执行`python3 pykms_Server.py`启动kms server(python没有加入环境变量的需要补全python的执行路径 默认IPADDRESS为“0.0.0.0”（所有接口），默认PORT为“1688”。)

4. 在client 执行`telnet 192.168.1.1 1688`看是否能连通（此非必需）

5. 在 微软查找对应的kms密钥 https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-R2-and-2012/jj612867(v=ws.11)

## 激活

1. 管理员在 192.168.1.2 打开cmd 

2. slmgr /upk  卸载原密钥 

3. slmgr /ipk 密钥  （安装上面第五步查到的对应密钥）

4. slmgr /skms 192.168.1.1:1688 （连接上面启动的kms server）

5. slmgr /ato （激活）

6. slmgr /xpr (显示激活时间 为180天以后到期，到期时 运行一下kms server 然后执行  激活里面的4，5，6 部份又可以继续180天)    

《完》

# Appendix A: KMS Client Setup Keys

> https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-R2-and-2012/jj612867(v=ws.11)

Applies To: Windows 10, Windows 8.1, Windows Server 2012 R2

Computers that are running volume licensing editions of Windows 10, Windows 8.1, Windows Server 2012 R2, Windows 8, Windows Server 2012, Windows 7, Windows Server 2008 R2, Windows Vista, and Windows Server 2008 are, by default, KMS clients with no additional configuration needed.

## Windows 10

|Operating system edition  |  KMS Client Setup Key |
|--------------------------|-----------------------|
|Windows 10 Professional   |W269N-WFGWX-YVC9B-4J6C9-T83GX|
|Windows 10 Professional N |MH37W-N47XK-V7XM9-C7227-GCQG9|
|Windows 10 Enterprise     |NPPR9-FWDCX-D2C8J-H872K-2YT43|
|Windows 10 Enterprise N   |DPH2V-TTNVB-4X9Q3-TJR4H-KHJW4|
|Windows 10 Education      |NW6C2-QMPVW-D7KKK-3GKT6-VCFB2|
|Windows 10 Education N    |2WH4N-8QGBV-H22JP-CT43Q-MDWWJ|
|Windows 10 Enterprise 2015 LTSB|WNMTR-4C88C-JK8YV-HQ7T2-76DF9|
|Windows 10 Enterprise 2015 LTSB N|2F77B-TNFGY-69QQF-B8YKP-D69TJ|
|Windows 10 Enterprise 2016 LTSB|DCPHK-NFMTC-H88MJ-PFHPY-QJ4BJ|
|Windows 10 Enterprise 2016 LTSB N|QFFDN-GRT3P-VKWWX-X7T3R-8B639|
