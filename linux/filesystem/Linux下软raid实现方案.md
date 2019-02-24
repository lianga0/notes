## Linux下软raid实现方案

> 2019.02.21

Raid大家都知道是冗余磁盘的意思（Redundant Arrays of Independent Disks，RAID），可以按业务系统的需要提供高可用性和冗余性，目前市面上比较常见的是通过服务器的raid阵列卡来实现此功能。

通过硬件阵列卡实现raid具有可靠性高，性能好等特点，不过，如果没有支持RAID的硬件，也可以通过软件来实现RAID的需求。

软raid比较依赖操作系统，所以他的劣势也显而易见，需要占用系统资源（主要是CPU资源）。目前在Linux和windows下软raid都比较常见了，Linux是通过mdadm实现的，windows下则在win2003之后通过磁盘管理来实现。

### Ubuntu 18.04.02 使用 mdadm 创建软RAID

`mdadm` - manage MD(Multiple Devices)  devices aka *Linux Software RAID*. 

Linux Software RAID devices are implemented through the md device driver.

RAID devices are virtual devices created from two or more real block devices.  This allows multiple devices (typically disk drives or partitions thereof) to be combined into a single device to hold (for example) a single filesystem.  Some RAID levels include redundancy and so can survive some degree of device failure.

Ubuntu上使用mdadm创建软RAID操作并不复杂，下面以创建RAID0的软RAID进行举例。我们有两个未分区的硬盘，容量分别是2TB和4TB。

1. 查看当前系统上是否已经安装`mdadm`

<del>

```
mdadm -V
mdadm - v4.1-rc1 - 2018-03-22
```

如果输出如下，可以使用提示命令直接安装`mdadm`

```
mdadm

Command 'mdadm' not found, but can be installed with:

sudo apt install mdadm
```

</del>

> 注意：因为测试的Ubuntu18.04.02安装的NVIDIA驱动存在问题(且系统本身安装在主板支持的两个固态硬盘做的RAID分区中)，使用`sudo apt install mdadm`安装mdadm后，会导致Ubuntu启动失败。

后边发现使用*A guide to mdadm*上推荐的[源代码](https://mirrors.edge.kernel.org/pub/linux/utils/raid/mdadm/)编译安装后，不会导致Ubuntu启动失败。这里我安装的版本如下：

```
mdadm -V
mdadm - v4.1 - 2018-10-01
```

2. 查看待分配硬盘的信息

使用命令`lsblk`查看系统中所有可用的硬盘信息，从而确定创建软RAID需要使用的硬盘分配的路径信息。

```
lsblk -o NAME,SIZE,FSTYPE,TYPE,MOUNTPOINT
```

我们待会创建建软RAID使用的两块硬盘信息如下：

```
NAME                         SIZE FSTYPE            TYPE   MOUNTPOINT
sdc                          1.8T linux_raid_member disk   
sdd                          3.7T linux_raid_member disk   

```

3. 创建磁盘阵列

<del>

使用`mdadm --create`来创建*RAID 0*的磁盘阵列，我们需要额外指定磁盘阵列的设备名称（这里我们使用`/dev/md0`），RAID类型和使用实际设备的数量。样例命令如下：

```
sudo mdadm --create --verbose /dev/md0 --level=0 --raid-devices=2 /dev/sdc /dev/sdd
```

</del>

可以通过查看`/proc/mdstat`文件，来确认RAID是否创建成功。如下，表示创建成功：

```
cat /proc/mdstat
Personalities : [raid0] 
md0 : active raid0 sdd[1] sdc[0]
      5860268544 blocks super 1.2 512k chunks
      
unused devices: <none>
```

可以看到，设备`/dev/md0`创建成功，并配置为在RAID 0模式下使用硬盘`/dev/sda`和`/dev/sdb`。

> 注意：这里是按照文档中解释的设置步骤创建的，虽然可以创建成功，并且后续操作也没问题。但是Ubuntu重启后，会导致这里配置的好RAID丢失。 使用`sudo mdadm -A /dev/md0 /dev/sdc /dev/sdd`命令也无法恢复。

在重新启动前使用`mdadm`命令查看RAID磁盘的信息显示如下：

```
sudo mdadm -E /dev/sdc
/dev/sdc:
          Magic : a92b4efc
        Version : 1.2
    Feature Map : 0x0
     Array UUID : dc1ab7de:01ced64b:ae4e8f84:890d2bd9
           Name : dr-xxx:0  (local to host dr-xxx)
  Creation Time : Sun Feb 24 13:57:14 2019
     Raid Level : raid0
   Raid Devices : 2

 Avail Dev Size : 3906764976 (1862.89 GiB 2000.26 GB)
    Data Offset : 264192 sectors
   Super Offset : 8 sectors
   Unused Space : before=264112 sectors, after=0 sectors
          State : clean
    Device UUID : fb4a083d:b37762a3:42e89e23:4ec59381

    Update Time : Sun Feb 24 13:57:14 2019
  Bad Block Log : 512 entries available at offset 8 sectors
       Checksum : 146e0e8 - correct
         Events : 0

     Chunk Size : 512K

   Device Role : Active device 0
   Array State : AA ('A' == active, '.' == missing, 'R' == replacing)
```

重启动后，使用相同的命令查看RAID磁盘的信息显示如下：

```
sudo mdadm -E /dev/sdc
/dev/sdc:
   MBR Magic : aa55
Partition[0] :   4294967294 sectors at            1 (type ee)
```

可以看到，superblock的确丢失了。经过Google搜索，发现一篇文章[New mdadm RAID vanish after reboot](https://superuser.com/questions/801826/new-mdadm-raid-vanish-after-reboot/803182)与自己情况类似，里面有个回答提到，先在硬盘上创建分区，然后再在分区上创建软RAID，可以解决这个问题。下面是部分回答的片段：

> Your RAID device is not being discovered and assembled automatically at boot.

> To provide for that, change the types of member partitions to `0xfd` (Linux RAID autodetect) — for MBR-style partition tables or to `00FD` (same) for GPT. You can use `fdisk` or `gdisk`, respectively, to do that.

> `mdadm` runs at boot (off the initramfs), scans available partitions, reads metadata blocks from all of them having type `0xfd` and assembles and starts all the RAID devices it is able to. This does not require a copy of an up-to-date `mdadm.conf` in the initramfs image.

>> Thanks for you answer.

>> I already tried to update initranfd, but without success.

>> With your second tip, I fix the problem:

>> create partion on each disk using :

这里我们分别是`fdisk`命令在`/dev/sdc`和`/dev/sdd`两个磁盘上创建两个分区。创建命令执行过程如下：

```
sudo fdisk /dev/sdc

Welcome to fdisk (util-linux 2.31.1).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

The old ext4 signature will be removed by a write command.

Device does not contain a recognized partition table.
Created a new DOS disklabel with disk identifier 0x752fdb0f.

Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (1-4, default 1): 
First sector (2048-3907029167, default 2048): 
Last sector, +sectors or +size{K,M,G,T,P} (2048-3907029167, default 3907029167): 

Created a new partition 1 of type 'Linux' and of size 1.8 TiB.

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
```

创建好分区后，使用如下命令创建*RAID 0*的磁盘阵列：

```
sudo mdadm --create --verbose /dev/md0 --level=0 --raid-devices=2 /dev/sdc1 /dev/sdd1
```


4. 创建并挂载文件系统

格式化创建好的虚拟RAID盘，命令如下：

```
sudo mkfs.ext4 -F /dev/md0
```

在现有文件系统中，创建挂载点

```
sudo mkdir -p /storage
```

最后，使用如下命令，挂载格式化好的RAID虚拟设备

```
sudo mount /dev/md0 /storage
```

挂载完成后，可以使用如下命令，查看挂载是否成功

```
df -h -x devtmpfs -x tmpfs

Filesystem                          Size  Used Avail Use% Mounted on
/dev/md0                            5.5T  4.3T  963G  82% /storage
```


5. 保存RAID阵列配置，从而保证重启后仍然有效

为了保证重启后，RAID能够正确挂载，我们需要修改`/etc/mdadm/mdadm.conf`配置文件。可以使用下面命令，自动扫描活跃的虚拟磁盘阵列设备，并写入配置文件。

```
sudo mdadm --detail --scan | sudo tee -a /etc/mdadm/mdadm.conf

ARRAY /dev/md0 metadata=1.2 name=dr-xxx:0 UUID=da169289:04021437:089c7662:e7d704d2
```

然后，你可以更新initramfs(initial RAM file system)，从而保证你的虚拟磁盘阵列设备能够在早期的启动过程中可用。

> Afterwards, you can update the initramfs, or initial RAM file system, so that the array will be available during the early boot process:

```
sudo update-initramfs -u
```

最后，修改文件系统挂载配置文件`/etc/fstab`，使系统启动后，自动将虚拟磁盘设备的文件系统挂载到制定路径上。命令如下：

```
echo '/dev/md0 /storage ext4 defaults,nofail,discard 0 0' | sudo tee -a /etc/fstab
```

经过上述配置后，你的虚拟磁盘阵列就配置好了。并且每次系统启动后，都会自动挂载。

### Resetting Existing RAID Devices

This section can be referenced to learn how to quickly reset your component storage devices prior to testing a new RAID level. Skip this section for now if you have not yet set up any arrays.

> Warning: This process will completely destroy the array and any data written to it. Make sure that you are operating on the correct array and that you have copied off any data you need to retain prior to destroying the array.

Find the active arrays in the `/proc/mdstat` file by typing:

```
cat /proc/mdstat
```

output

```
Personalities : [raid0] [linear] [multipath] [raid1] [raid6] [raid5] [raid4] [raid10] 
md0 : active raid0 sdc[1] sdd[0]
      209584128 blocks super 1.2 512k chunks

            unused devices: <none>
```

Unmount the array from the filesystem:

```
sudo umount /dev/md0
```

Then, stop and remove the array by typing:

```
sudo mdadm --stop /dev/md0
```

Find the devices that were used to build the array with the following command:

> Warning: Keep in mind that the `/dev/sd*` names can change any time you reboot! Check them every time to make sure you are operating on the correct devices.

```
lsblk -o NAME,SIZE,FSTYPE,TYPE,MOUNTPOINT
```

After discovering the devices used to create an array, zero their superblock to remove the RAID metadata and reset them to normal:

```
sudo mdadm --zero-superblock /dev/sdc
sudo mdadm --zero-superblock /dev/sdd
```

You should remove any of the persistent references to the array. Edit the `/etc/fstab` file and comment out or remove the reference to your array:

```
sudo nano /etc/fstab

                         /etc/fstab
. . .
# /dev/md0 /mnt/md0 ext4 defaults,nofail,discard 0 0
```

Also, comment out or remove the array definition from the `/etc/mdadm/mdadm.conf` file:

```
sudo nano /etc/mdadm/mdadm.conf

                          /etc/mdadm/mdadm.conf
. . .
# ARRAY /dev/md0 metadata=1.2 name=dr-xxx:0 UUID=da169289:04021437:089c7662:e7d704d2
```

Finally, update the `initramfs` again so that the early boot process does not try to bring an unavailable array online.

```
sudo update-initramfs -u
```


At this point, you should be ready to reuse the storage devices individually, or as components of a different array.

#### Creating Other RAID Level Array

#### Creating a RAID 1 Array

#### Creating a RAID 5 Array

#### Creating a RAID 6 Array

#### Creating a Complex RAID 10 Array

Please referece [How To Create RAID Arrays with mdadm on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-create-raid-arrays-with-mdadm-on-ubuntu-18-04)

## A guide to mdadm

> From: https://raid.wiki.kernel.org/index.php/A_guide_to_mdadm

### Overview

mdadm has replaced all the previous tools for managing raid arrays. It manages nearly all the user space side of raid. There are a few things that need to be done by writing to the `/proc` filesystem, but not much.

### Getting mdadm

This is a pretty standard part of any distro, so you should use your standard distro software management tool. If, however, you are having any problems it does help to be running the absolute latest version, which can be downloaded with

```
git clone git://git.kernel.org/pub/scm/utils/mdadm/mdadm.git
```

or from

```
https://kernel.org/pub/linux/utils/raid/mdadm/
```

In the absence of any other preferences, it belongs in the `/usr/local/src` directory. As a linux-specific program there is none of this autoconf stuff - just follow the instructions as per the INSTALL file.

Do not use Neil Brown's version unless he tells you to do so - he is no longer the maintainer and it is not kept up-to-date.

### Modes

mdadm has seven modes. You will normally only use a few of them. They are as follows:-

#### Assemble

This is probably the mode that is used most, but you won't be using it much - it happens in the background. Every time the system is booted, this needs to run. It scans the drives, looking for superblocks, and rebuilds all the arrays for you. This is why you need an initramfs when booting off a raid array - because mdadm is a user-space program, if root is on an array then we have a catch-22 - we can't boot until we have root, and we can't have root until we've booted and can run mdadm.

#### Create

This is the first of the two modes you will use a lot. As the name implies, it creates arrays, and writes the superblocks for arrays that have them. It also fires off initialisation - making sure that the disks of a mirror are identical, or that on a parity array the parities are correct. This is why raids 5&6 are created in degraded mode - if they weren't then any check of the raid would spew errors for areas that hadn't been written to.

#### Grow

A bit of a misnomer, this mode takes care of all operations that change the size of an array, such as changing the raid level, changing the number of active devices, etc.

#### Manage

This is the default mode, and is used primarily to add and remove devices. It can be confusing, as several options (such as --add) are also used in grow mode, most typically when adding a device at the same time as changing the number of devices.

#### Follow or Monitor

#### Build

This is a relic of when superblocks didn't exist. It is used to (re)create an array, and should not be used unless you know exactly what you are doing. Because there are no superblocks, or indeed, any array metadata, the system just has to assume you got everything right because it has no way of checking up on you.

[TODO: Can you use this mode to create a temporary mirror, for the purpose of backing up your live data? No. Trying to build a RAID 1 with a device that is mounted, mdadm says "Device or resource busy", even with --force. If --force worked the backup would still be at risk of being inconsistent as some older writes to the device may not have finished and new writes may occur. The (degraded) RAID 1 must be built and placed between device and filesystem before going live, i.e. mounting the filesystem. After hot-adding the backup disk, the sync must be allowed to finish. Then, one of the disks can be failed and removed. The backup will be a device snapshot and as such still has a small risk of being inconsistent. This risk is a lot smaller than for a simple "dd" copy that would contain data from different points in time. Whether the risk is as low as with LVM snapshots depends on the exact RAID implementation, i.e. whether the data left behind will be a true point-in-time snapshot.]

#### Misc

This contains all the bits that don't really fit anywhere else.

### Array internals and how it affects mdadm

More information, please reference the origin link page.

Reference:

[Linux下软raid实现方案](http://blog.chinaunix.net/uid-26252206-id-5785379.html)

[How To Create RAID Arrays with mdadm on Ubuntu 18.04](https://www.digitalocean.com/community/tutorials/how-to-create-raid-arrays-with-mdadm-on-ubuntu-18-04)

[A guide to mdadm](https://raid.wiki.kernel.org/index.php/A_guide_to_mdadm)

[New mdadm RAID vanish after reboot](https://superuser.com/questions/801826/new-mdadm-raid-vanish-after-reboot/803182)

[Linux raid disappears after reboot](https://unix.stackexchange.com/questions/411286/linux-raid-disappears-after-reboot)

Not work for me [Software Raid not available after reboot](https://superuser.com/questions/1162114/software-raid-not-available-after-reboot)