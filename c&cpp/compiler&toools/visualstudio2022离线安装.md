# Visual Studio 2022 离线安装

微软不再为Visual Studio 2022提供之气类似的ISO离线安装包，可以参考文档：[Create and maintain a network installation of Visual Studio](https://learn.microsoft.com/en-us/visualstudio/install/create-a-network-installation-of-visual-studio?view=vs-2022#use-a-configuration-file-to-initialize-the-contents-of-a-layout)
自己制作一个离线安装文件包

使用如下命令，可以下载Visual C++ Win32程序的开发资源包，压缩后拷贝到离线安装机器。

```
vs_enterprise.exe --layout D:\xxx\VSLayout --add Microsoft.VisualStudio.Workload.NativeDesktop --includeRecommended --lang en-US
```

使用如下命令可以完成离线安装

```
vs_setup.exe --noWeb
```

企业版安装完可以使用如下激活器进行激活测试[VS 2022专业版永久密钥](https://www.cnblogs.com/Jeffrey1172417122/p/18850936)

vs2022永久密钥：

Visual Studio 2022 Enterprise：VHF9H-NXBBB-638P6-6JHCY-88JWH

Visual Studio 2022 Professional：TD244-P4NB7-YQ6XK-Y8MMM-YWV2J

