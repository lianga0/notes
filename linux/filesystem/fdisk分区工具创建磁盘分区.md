# fdisk分区工具创建磁盘分区

随着时间推移，服务器上的磁盘往往容易出现容量不足的问题。增加新的硬盘和分区是一个不错的选择，接下来记录下使用fdisk命令增加linux分区的方法。

该文档中方法在`ubuntu 14.04 LTS`中测试通过，所有命令均已管理员身份运行。

### 在原有磁盘的剩余空间上增加新分区

##### 查看当前分区信息

```
fdisk -l
```

```
Disk /dev/sda: 27.9 GB, 27917287424 bytes
255 heads, 63 sectors/track, 3394 cylinders, total 54525952 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00058443

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048    39845887    19921920   83  Linux
/dev/sda2        39847934    41940991     1046529    5  Extended
/dev/sda5        39847936    41940991     1046528   82  Linux swap / Solaris

```
fdisk显示的总sectors数比分区/dev/sda5得结束位置大的多（此处扩大了虚拟机磁盘的总空间）。


##### 操作分区表 

```
fdisk /dev/sda
```

使用管理员身份运行`fdisk`后，进入`fdisk`操作界面，输入`m`显示帮助信息

```
Command (m for help): m
Command action
   a   toggle a bootable flag
   b   edit bsd disklabel
   c   toggle the dos compatibility flag
   d   delete a partition
   l   list known partition types
   m   print this menu
   n   add a new partition
   o   create a new empty DOS partition table
   p   print the partition table
   q   quit without saving changes
   s   create a new empty Sun disklabel
   t   change a partition's system id
   u   change display/entry units
   v   verify the partition table
   w   write table to disk and exit
   x   extra functionality (experts only)

```

输入`n`创建一个新分区

```
Command (m for help): n
Partition type:
   p   primary (1 primary, 1 extended, 2 free)
   l   logical (numbered from 5)
Select (default p):
```

因为已经存在一个扩展分区，所以此处选择创建一个主分区。
输入`p`创建一个新的主分区

```
Select (default p): p
Partition number (1-4, default 3):
```

当前已存在主分区`/dev/sda1`和`/dev/sda2`，所以Partition number选择`3`

```
Select (default p): p
Partition number (1-4, default 3): 3
First sector (39845888-54525951, default 39845888):
```

此处需要选择分区的起始扇区号，我们将新分区的开始扇区设置为`/dev/sda2`分区的结束扇区`41940992`。

```
Select (default p): p
Partition number (1-4, default 3): 3
First sector (39845888-54525951, default 39845888): 41940992
Last sector, +sectors or +size{K,M,G} (41940992-54525951, default 54525951):
```

此处新分区的结束扇区使用推荐值，即磁盘总扇区数-1

```
Select (default p): p
Partition number (1-4, default 3): 3
First sector (39845888-54525951, default 39845888): 41940992
Last sector, +sectors or +size{K,M,G} (41940992-54525951, default 54525951):
Using default value 54525951

Command (m for help):
```

输入`p`查看当前分区情况如下

```
Command (m for help): p

Disk /dev/sda: 27.9 GB, 27917287424 bytes
255 heads, 63 sectors/track, 3394 cylinders, total 54525952 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00058443

   Device Boot      Start         End      Blocks   Id  System
/dev/sda1   *        2048    39845887    19921920   83  Linux
/dev/sda2        39847934    41940991     1046529    5  Extended
/dev/sda3        41940992    54525951     6292480   83  Linux
/dev/sda5        39847936    41940991     1046528   82  Linux swap / Solaris
```

显示信息可以看出`/dev/sda3`已经设置好，输入`w`命令保存新建磁盘分区信息

```
Command (m for help): w
The partition table has been altered!

Calling ioctl() to re-read partition table.

WARNING: Re-reading the partition table failed with error 16: Device or resource busy.
The kernel still uses the old table. The new table will be used at
the next reboot or after you run partprobe(8) or kpartx(8)
Syncing disks.
```

** 因为当前磁盘`/dev/sda`是此虚拟机唯一的硬盘，所以我们调整分区前没有卸载分区。为了简单，此处我们直接重启虚拟机，使磁盘分区配置信息生效。 **

##### 格式化新建分区

```
mkfs -t ext4 /dev/sda3
```

```
mke2fs 1.42.9 (4-Feb-2014)
warning: 256 blocks unused.

Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
Stride=0 blocks, Stripe width=0 blocks
393984 inodes, 1572864 blocks
78643 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=1610612736
48 block groups
32768 blocks per group, 32768 fragments per group
8208 inodes per group
Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912, 819200, 884736

Allocating group tables: done
Writing inode tables: done
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done

```

##### 挂载格式化后的新分区

将新分区`/dev/sda3`挂载至目录 `/data`

```
mount /dev/sda3 /data
```

使用`df`命令查看挂载后系统文件分区的情况

```
df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        19G  5.6G   13G  32% /
none            4.0K     0  4.0K   0% /sys/fs/cgroup
udev            484M  4.0K  484M   1% /dev
tmpfs            99M  1.1M   98M   2% /run
none            5.0M     0  5.0M   0% /run/lock
none            494M     0  494M   0% /run/shm
none            100M     0  100M   0% /run/user
/dev/sda3       5.8G   12M  5.5G   1% /data
```

这个挂载只是临时的，重启服务器之后又需要重新挂载，通过修改/etc/fstab文件使挂载永久有效

##### 永久挂载

修改`/etc/fstab`文件，在文件最后添加以下一行记录

```
/dev/sda3        /data       ext4    defaults 0 0
```

## 硬盘持久化命名法挂载

> 2020.12.22

> reference: https://wiki.archlinux.org/index.php/Persistent_block_device_naming_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

如果你的机器上有不止一个 SATA, SCSI 或 IDE 磁盘控制器，那么它们所对应的设备节点将会依随机次序添加。这样就可能导致每次引导时设备的名字如 /dev/sda 与 /dev/sdb 互换了，最终导致系统不可引导、kernel panic、或者设备不可见。持久化命名法可以解决这些问题。

在Azure的Ubuntu虚拟机上就碰到这样的情况，因为Azure虚拟机会有一个OS硬盘和临时硬盘，重启系统时，自己添加的数据盘的设备名字存在和临时硬盘互换的情况。这时，在`/etc/fstab`文件中使用by-uuid的方法挂载数据盘就不会出现问题了。

### 持久化命名的方法

有四种持久化命名方案：by-label、by-uuid、by-id 和 by-path。对于那些使用GUID 分区表(GPT)的磁盘，还有额外的两种方案，by-partlabel 和 by-partuuid。你也可以使用 Udev 静态设备名方案。

下面讲解各种命名方案及其用法。

`lsblk -f`命令用于以图示方式查看第一种方案：

```
$ lsblk -f
NAME   FSTYPE LABEL  UUID                                 MOUNTPOINT
sda                                                       
├─sda1 vfat          CBB6-24F2                            /boot
├─sda2 ext4   SYSTEM 0a3407de-014b-458b-b5c1-848e92a327a3 /
├─sda3 ext4   DATA   b411dc99-f0a0-4c87-9e05-184977be8539 /home
└─sda4 swap          f9fe0b69-a280-415d-a03a-a32752370dee [SWAP]
```

GPT 分区表的系统应改用`blkid`命令，这个命令更方便脚本使用但可读性低。

```
$ blkid
/dev/sda1: UUID="CBB6-24F2" TYPE="vfat" PARTLABEL="EFI SYSTEM PARTITION" PARTUUID="d0d0d110-0a71-4ed6-936a-304969ea36af" 
/dev/sda2: LABEL="SYSTEM" UUID="0a3407de-014b-458b-b5c1-848e92a327a3" TYPE="ext4" PARTLABEL="GNU/LINUX" PARTUUID="98a81274-10f7-40db-872a-03df048df366" 
/dev/sda3: LABEL="DATA" UUID="b411dc99-f0a0-4c87-9e05-184977be8539" TYPE="ext4" PARTLABEL="HOME" PARTUUID="7280201c-fc5d-40f2-a9b2-466611d3d49e" 
/dev/sda4: UUID="f9fe0b69-a280-415d-a03a-a32752370dee" TYPE="swap" PARTLABEL="SWAP" PARTUUID="039b6c1c-7553-4455-9537-1befbc9fbc5b"
```

#### by-uuid

UUID is a mechanism to give each filesystem a unique identifier. These identifiers are generated by filesystem utilities (e.g. mkfs.*) when the partition gets formatted and are designed so that collisions are unlikely. All GNU/Linux filesystems (including swap and LUKS headers of raw encrypted devices) support UUID. FAT and NTFS filesystems (fat and windows labels above) do not support UUID, but are still listed in `/dev/disk/by-uuid` with a shorter UID (unique identifier):

```
$ ls -l /dev/disk/by-uuid/
total 0
lrwxrwxrwx 1 root root 10 May 27 23:31 0a3407de-014b-458b-b5c1-848e92a327a3 -> ../../sda2
lrwxrwxrwx 1 root root 10 May 27 23:31 b411dc99-f0a0-4c87-9e05-184977be8539 -> ../../sda3
lrwxrwxrwx 1 root root 10 May 27 23:31 CBB6-24F2 -> ../../sda1
lrwxrwxrwx 1 root root 10 May 27 23:31 f9fe0b69-a280-415d-a03a-a32752370dee -> ../../sda4
```

The advantage of using the UUID method is that it is much less likely that name collisions occur than with labels. Further, it is generated automatically on creation of the filesystem. It will, for example, stay unique even if the device is plugged into another system (which may perhaps have a device with the same label).

The disadvantage is that UUIDs make long code lines hard to read and break formatting in many configuration files (e.g. fstab or crypttab). Also every time a partition is resized or reformatted a new UUID is generated and configs have to get adjusted (manually).

<完>