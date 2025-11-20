# cobaltstrike使用WinHTTP库配置生成的beacon可以上线，但在相同配置环境下，使用WinINet库配置生成的beacon却无法上线，都有哪些可能的原因？

> 经过验证，为Windows系统配置错误HTTP代理问题，导致WinINet库配置生成beacon无法上线，移除代理后，两种类型beacon均可上线

## 代理配置问题

- WinINet使用IE代理设置，如果目标环境有特定代理配置可能阻断连接

- WinHTTP默认不使用IE代理设置，除非显式配置

## 认证问题

- WinINet可能尝试进行Windows/NTLM认证，在某些环境下触发安全警报

- 认证弹窗可能阻碍后台连接

## SSL/TLS处理差异

- WinINet和WinHTTP对证书验证、TLS版本支持有差异
- WinINet可能对自签名证书更严格

## 系统环境限制

- 某些企业环境可能限制WinINet库的网络访问

- EDR/防火墙可能针对WinINet有特殊规则
## 防病毒/EDR检测

- 某些安全产品可能对WinINet库的特定使用模式有更严格监控

微软官方推荐优先使用WinINet，除了一些例外情况，WinINet 是 WinHTTP 的超集。 在两者之间进行选择时，应使用 WinINet ，除非你打算在需要模拟和会话隔离的服务或类似服务的进程中运行。

Reference： [WinINet vs. WinHTTP](https://learn.microsoft.com/zh-cn/windows/win32/wininet/wininet-vs-winhttp?redirectedfrom=MSDN)