# 铁威马RAID1单块硬盘数据读取

> 2021.11

手上有上一个铁威马NAS遗留下的两块RAID1的硬盘，想挂载到电脑上看看里面是不是还有啥数据。

搞了一圈，发现忘记怎么在电脑上配置单块RAID1的硬盘，从而读取硬盘中文件。

自己测试的Ubuntu系统为18.04LTS，之前已经装过`mdadm`软件。版本为`v4.1`。

硬盘接到电脑上后，通过`lsblk`查看硬盘设备信息，但是不能直接挂载。

```
$ lsblk
NAME                    MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
sdc                       8:32   0   3.7T  0 disk 
├─sdc1                    8:33   0   285M  0 part 
├─sdc2                    8:34   0   2.9G  0 part 
│ └─osprober-linux-sdc2 253:0    0   2.9G  1 dm   
├─sdc3                    8:35   0   1.9G  0 part 
│ └─osprober-linux-sdc3 253:1    0   1.9G  1 dm   
└─sdc4                    8:36   0   3.6T  0 part 
```

但是，发现`mdadm`会自动挂载几个虚拟设备，这里我看到的虚拟设备为

```
/dev/md125
/dev/md126
/dev/md127
```

尝试直接挂载虚拟设备，`mount`命令会报错。

```
$ mount /dev/md127 /home/ao/tmp/
mount: /home/ao/tmp: can't read superblock on /dev/md127.
```

使用如下命令把所有的虚拟设备删除掉，解除对raid硬盘的解析。

```
$ mdadm –stop /dev/md125
mdadm: stopped /dev/md125
```

然后再用下面命令重新配置虚拟设备

```
mdadm –assemble –run /dev/md0 /dev/sdb3
```

（这里md0是随便写的，只要不重名就行。）假如成功的话，可以看到如下信息

```
mdadm: /dev/md0 has been started with 1 drive (out of 2).
```

之后执行挂载命令

```
mount /dev/md0 /{empty_folder}
```

然后接着出错，错误信息如下：

```
mount: /home/ao/tmp: unknown filesystem type 'LVM2_member'.
```

此时，就比较简单了，安装`lvm2`

```
apt install lvm2
```

然后查看物理卷：`pvs`

```
$ pvs
  PV         VG  Fmt  Attr PSize PFree
  /dev/md0   vg0 lvm2 a--  3.63t    0 
```

查看卷组：`vgs`

```
$ vgs
  VG  #PV #LV #SN Attr   VSize VFree
  vg0   1   1   0 wz--n- 3.63t    0 
```

查看逻辑卷：`lvdisplay`

```
$ lvdisplay
  --- Logical volume ---
  LV Path                /dev/vg0/lv0
  LV Name                lv0
  VG Name                vg0
  LV UUID                77BSh2-7BCr-SLZv-IKsC-nBuw-t0rC-vGiPKn
  LV Write Access        read/write
  LV Creation host, time TNAS-00E789, 2020-04-10 13:10:05 +0800
  LV Status              available
  # open                 0
  LV Size                3.63 TiB
  Current LE             952537
  Segments               1
  Allocation             inherit
  Read ahead sectors     auto
  - currently set to     256
  Block device           253:2
```

如未激活，需要激活逻辑卷：`vgchange -ay /dev/vg0`

租后挂载逻辑卷即可

```
mount /dev/vg0/lv0 /home/tmp/
```

Reference:

[从 raid1 的单盘中取出文件](https://bellsprite.com/?p=839)

[mount: unknown filesystem type 'LVM2_*'解决方案](https://blog.csdn.net/dongshibo12/article/details/105838734/)
