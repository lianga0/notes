# PowerShell

PowerShell（包括Windows PowerShell和PowerShell Core）是微软公司开发的任务自动化和配置管理架构（consisting of a command-line shell and the associated scripting language），最初仅仅是Windows组件，后于2016年8月18日开源并提供跨平台支持。

在PowerShell中，管理任务通常由cmdlets（发音为command-lets）执行，这是执行特定操作的专用.NET类。可以将cmdlet集合至脚本、可执行文件（一般是独立应用程序）中，或通过常规.NET类（或WMI / COM对象）实例化。

Windows PowerShell是以.NET Framework技术为基础，并且与现有的WSH保持回溯兼容，因此它的脚本程序不仅能访问.NET CLR，也能使用现有的COM技术。同时也包含了数种系统管理工具、简易且一致的语法，常见如登录数据库、WMI。


powershell是基于.Net框架的，powershell.exe只是命令行方式的一种实现，本质是对System.Management.Automation.dll的封装。

针对Windows applocker策略绕过，可以考虑以下方法：

1. 规则“漏洞”默认情况下会，会将Program Files和Windows路径设置为例外，通过寻找可写可执行路径，写入payload脚本即可。如果只是对于powershell.exe采用了路径限制，而不是哈希限制，那可以将其copy一份到别的路径，然后使用。

2. 使用C#下面是一个C#调用powershell的模板代码，将payload替换为实际执行代码最终编译为exe即可运行


[No Power No Shell --- 非PE攻击中的套路](https://zhuanlan.zhihu.com/p/30203859)

[Introduction to PowerShell](https://learn.microsoft.com/en-us/training/modules/introduction-to-powershell/)

