### windows10安装linux子系统

> 2018.04.01

微软在2016年3月的开发者大会上位windows10系统带来了Bash on Ubuntu on Windows （也即linux子系统），通过 Windows Subsystem for Linux（WSL）这一 Windows 10 的最新特性实现的，使用此功能，你可以在 Windows 中原生运行 Linux 的大多数命令行程序。

##### 1. 打开windows10开发人员模式

步骤为：设置-->更新和安全-->针对开发人员，点击开发人员模式打开即可。


##### 2. 在控制面板中添加linux子系统

安装步骤为：控制面板-->程序-->启用或关闭windows功能，勾选“适用于windows的linux的子系统”

##### 3. 重启电脑


##### 4. 命令行运行 `lxrun /install /y`开始安装


安装速度取决于网络情况，下载的文件在`%localappdata%\lxss`目录下`lxss.tar.gz`，解压后大概500M,`rootfs` 目录即为子系统根目录。

##### 5. 命令行运行`bash`进入Ubuntu

默认使用的 root 帐号登录，通过指令 passwd 设置密码。

注：本文脚本均在root帐号下操作，因此建议使用root帐号

毕竟爱折腾，难免会把子系统环境(lxss目录)玩坏掉，因此干正事前最好先备份下以便快速还原。注意，不要直接右键复制或者打包，可能会导致文件权限丢失的。

```
xcopy %localappdata%\lxss %localappdata%\lxss.bak /E
```

当然，如果你比较任性也可以不执行上一步的备份操作，通过命令行运行`lxrun /uninstall /full`轻松卸载子系统，重复上面的步骤即可重装，不过要注意下载速度时好时坏哦。

Reference: [Windows10内置Linux子系统初体验](https://www.jianshu.com/p/bc38ed12da1d)

[About the Windows Subsystem for Linux](https://aka.ms/wsldocsv)
