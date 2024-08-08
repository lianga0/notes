## Cobalt Strike 与 Metasploit 的关系

Cobalt Strike 和 Metasploit 都是渗透测试中的重要工具，但它们并不是基于彼此开发的。早期版本的 Cobalt Strike 依赖于 Metasploit Framework，但现在 Cobalt Strike 已经不再使用 Metasploit Framework，而是作为一个独立的平台。

Cobalt Strike 和 Metasploit 各有所长。Cobalt Strike 更适合做稳控平台，而 Metasploit 则更擅长内网各类探测搜集与漏洞利用。尽管它们是两个独立的实体，但它们之间存在很多协同效应，可以灵活地联动，相互依托，从而提升渗透的效率。

例如，你可以使用 Metasploit Framework 的漏洞来传递 Cobalt Strike 的 Beacon。另外，Cobalt Strike 的 Beacon 负载自 2013 年以来就具有 SOCKS 代理转发功能，这使得许多工具可以通过 Beacon 进行隧道。这些都是 Cobalt Strike 和 Metasploit Framework 联动的例子。总的来说，虽然 Cobalt Strike 和 Metasploit 是两个独立的工具，但它们可以互相配合，提供更强大的渗透测试能力。


## Beacon与服务器通信延迟问题

受害机(肉鸡)运行Beacon后，会出现在“Session Table”中，右击选择interact，即可进行交互，由于受害机默认60秒进行一次回传，为了实验效果我们这里把时间设置成5秒或更短（例如，为了方便实验我们可以把时间设置为0），但实际中频率不宜过快，容易被发现。

```
beacon>sleep 0
```