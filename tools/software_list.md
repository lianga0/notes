## 不常用软件记录
|软件名称 |功能简介            |
|---------|--------------------|
|USB宝盒   |U盘SD卡修复软件     |
|快剪辑    |简单的视频剪辑软件  |
|oCam     |简单的屏幕录制软件  |
|FFmpeg   |视频处理最常用的开源软件|
|StarUML  |超好用的UML画图工具|
|WirelessMon  |无线网络监控软件|



### [Squid](http://www.squid-cache.org/) fully-featured HTTP proxy

Squid is a fully-featured HTTP/1.0 proxy which is almost (but not quite - we're getting there!) a fully-featured HTTP/1.1 proxy. 
Squid offers a rich access control, authorization and logging environment to develop web proxy and content serving applications. 
Squid offers a rich set of traffic optimization options, most of which are enabled by default for simpler installation and high performance.


### [youtube-dl](https://github.com/ytdl-org/youtube-dl) download videos from youtube.com or other video platforms

youtube-dl is a command-line program to download videos from YouTube.com and a few more sites. It requires the Python interpreter, version 2.6, 2.7, or 3.2+, and it is not platform specific. It should work on your Unix box, on Windows or on macOS. It is released to the public domain, which means you can modify it, redistribute it or use it however you like.

```
youtube-dl [OPTIONS] URL [URL...]
```

列出所有可下载的文件信息：

```
youtube-dl -F https://www.youtube.com/watch?v=AZP9CU-RPpw
[youtube] AZP9CU-RPpw: Downloading webpage
[info] Available formats for AZP9CU-RPpw:
format code  extension  resolution note
249          webm       audio only tiny   58k , opus @ 50k (48000Hz), 8.67MiB
250          webm       audio only tiny   72k , opus @ 70k (48000Hz), 10.96MiB
251          webm       audio only tiny  130k , opus @160k (48000Hz), 19.73MiB
248          webm       1920x1080  1080p 4418k , vp9, 30fps, video only, 290.07MiB
271          webm       2560x1440  1440p 9128k , vp9, 30fps, video only, 769.65MiB
313          webm       3840x2160  2160p 17898k , vp9, 30fps, video only, 1.92GiB
```

下载指定大小的视频文件

```
youtube-dl -f 251 https://www.youtube.com/watch?v=AZP9CU-RPpw
```

### [JumpServer](https://github.com/jumpserver/jumpserver)多云环境下更好用的堡垒机

JumpServer 是全球首款开源的堡垒机，使用 GPLv3 开源协议，是符合 4A 规范的运维安全审计系统。

JumpServer 使用 Python 开发，遵循 Web 2.0 规范，配备了业界领先的 Web Terminal 方案，交互界面美观、用户体验好。

JumpServer 采纳分布式架构，支持多机房跨区域部署，支持横向扩展，无资产数量及并发限制。


### [drawio-desktop](https://www.diagrams.net/) 免费开源的流程图软件

drawio-desktop is a diagrams.net desktop app based on Electron. draw.io is the old name for diagrams.net, we just don't want the hassle of changing all the binary's names.

draw.io Desktop is designed to be completely isolated from the Internet, apart from the update process. This checks github.com at startup for a newer version and downloads it from an AWS S3 bucket owned by Github. All JavaScript files are self-contained, the Content Security Policy forbids running remotely loaded JavaScript.

No diagram data is ever sent externally, nor do we send any analytics about app usage externally. This means certain functionality for which we do not have a JavaScript implementation do not work in the Desktop build, namely .vsd and Gliffy import.


### [StarUML](http://staruml.io/) 超好用的UML画图工具推荐

A sophisticated software modeler for agile and concise modeling

StarUML是一个复杂的软件建模工具，旨在支持敏捷和简洁的建模。


### [WirelessMon](https://www.passmark.com/products/wirelessmonitor/) Wireless 802.11 WiFi monitoring software

Monitor wireless adapters and WiFi access points

允许使用者监控无线适配器和聚集的状态，显示周边无线接入点或基站实时信息的工具，列出计算机与基站间的信号强度，实时的监测无线网络的传输速度，以便让我们了解网络的下载速度或其稳定性。


### [YApi](https://hellosean1025.github.io/yapi/)

旨在为开发、产品、测试人员提供更优雅的接口管理服务。可以帮助开发者轻松创建、发布、维护 API

- 可视化接口管理
- Mock Server
- 自动化测试

Github: https://github.com/ymfe/yapi

### [eoLinker](https://www.eolinker.com/)

EOLINKER  API Studio 5 开箱即用的API研发管理方案，0代码实现API自动化测试

API接口在设计时往往需要编写大量的文档，而且编写完成后往往需要根据实际情况，经常改动文档，文档编写维护工作量相对较大，有点头疼。

由于我们项目还经常会因为交付周期的原因，需要接入一个第三方的库，而第三方的库通常都存在文档老旧，文档不够全面等等或多或少的问题。那这个问题相比于没有文档，对程序员来说更加难以棘手。因为会造成：我们需要的接口不在文档上，文档上的接口不存在库里，又或者是少了一行关键的代码。  

然后我在网上找解决办法，找到了eoLinker，作为苦逼的开发，在此分享我一些使用过程中的心得，希望都能脱（ji）离（xu）苦（kai）海（fa）。

作者：叮叮叮当
链接：https://juejin.im/post/5ac31a2a6fb9a028d043a06d
来源：掘金
