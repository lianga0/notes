# DbgView在Window10虚拟机中捕捉内核DbgPrint日志崩溃问题

在Windows10中，使用DbgView捕捉内核DbgPrint日志时，部分内核日志会导致DbgView直接崩溃退出，捕捉用户态日志一切正常。

问题原因：Dbgv.sys 驱动与系统/虚拟机冲突 。

解决方法：

关闭“Capture Kernel”选项（仅查看用户态日志）。以管理员身份运行 DbgView 。

重命名 Dbgv.sys（位于 C:\Windows\System32\drivers\）后重启 DbgView 。

如仍崩溃：改用 WinDbg 或 WPA (Windows Performance Analyzer) 捕获内核日志

参考：
[实战经验：记录一次蓝屏崩溃诊断经历](https://www.topomel.com/archives/514.html)