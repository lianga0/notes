### 扩大Virtual Box VDI格式虚拟硬盘大小

由于在Virtual Box中创建虚拟机的硬盘时指定的磁盘空间上限较低，随着虚拟机的使用磁盘出现空间不足的现象。

添加一块新的虚拟磁盘是一个不错的选择，但这里介绍另一种方案：扩大已有虚拟硬盘的总空间。

在Virtual Box界面中并未发现扩大虚拟磁盘空间的配置项目，Google后发现可以使用Virtual Box安装目录下的VBoxManage.exe工具来完成虚拟磁盘的扩容工作。

进入Virtual Box的安装目录，（如C:\Program Files\Oracle\VirtualBox），打开CMD命令行窗口即可执行VBoxManage命令。

##### 查找你虚拟机的硬盘，获取想修改的虚拟硬盘的UUID。
执行如下命令

```
VBoxManage list hdds
```

可以看到如下示例：

```
UUID:           8f0cb9a5-0c31-462a-ba8b-c025da88dc6f
Parent UUID:    base
State:          locked write
Type:           normal (base)
Location:       D:\application\VirtualBox\ubuntu16.04.vdi
Storage format: VDI
Capacity:       22600 MBytes
Encryption:     disabled

UUID:           9ec3c12d-f2fb-437d-8549-2684eda22e3f
Parent UUID:    base
State:          created
Type:           normal (base)
Location:       C:\Users\liang\VirtualBox VMs\Win7_32\Win7_32.vdi
Storage format: VDI
Capacity:       25600 MBytes
Encryption:     disabled
```

此处可以获得想要修改的ubuntu16.04.vdi虚拟硬盘的UUID

##### 扩大VDI硬盘大小的命令

```
VBoxManage modifyhd 虚拟硬盘的UUID --resize 40960
```

如下示例现实修改成功：

```
C:\Program Files\Oracle\VirtualBox>VBoxManage modifyhd 8f0cb9a5-0c31-462a-ba8b-c025da88dc6f --resize 122600
0%...10%...20%...30%...40%...50%...60%...70%...80%...90%...100%
```

--resize参数后的值单位为MB，这里仅测试扩容情形，未测试指定比原始值小的情况。

##### 启动虚拟机，修改虚拟机文件系统分区

由于第二步中仅仅修改了虚拟磁盘的总大小，新增的磁盘空间属于尚未分配的虚拟机的空闲空间。所以Linux系统可以使用`fdisk`和`mkfs`调整虚拟机文件系统，以使用新增磁盘空间。

这里不详细介绍文件系统分区调整的方法了，可以参考[fdisk分区工具创建磁盘分区](#)。

Reference:

1. [调整扩大VMDK格式VirtualBox磁盘空间](http://www.cnblogs.com/platero/p/4105808.html)

2. [调整扩大VMDK格式VirtualBox磁盘空间](http://www.cnblogs.com/wayfarer/archive/2011/11/15/2249556.html)

<完>