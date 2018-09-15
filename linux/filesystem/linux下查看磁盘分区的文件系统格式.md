## linux下查看磁盘分区的文件系统格式

### df -T 只可以查看已经挂载的分区和文件系统类型。

```
df -T
Filesystem     Type     1K-blocks     Used Available Use% Mounted on
udev           devtmpfs   3996108        0   3996108   0% /dev
tmpfs          tmpfs       805276     1500    803776   1% /run
/dev/sda1      ext4     472449304 13495544 434931696   4% /
tmpfs          tmpfs      4026364        0   4026364   0% /dev/shm
tmpfs          tmpfs         5120        4      5116   1% /run/lock
tmpfs          tmpfs      4026364        0   4026364   0% /sys/fs/cgroup
```

### fdisk -l 可以显示出所有挂载和未挂载的分区，但不显示文件系统类型。

```
fdisk -l
Disk /dev/loop0: 86.9 MiB, 91099136 bytes, 177928 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes


Disk /dev/loop1: 87.9 MiB, 92164096 bytes, 180008 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes


Disk /dev/sda: 3.7 TiB, 3998614552576 bytes, 7809794048 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 63F93572-A264-41EF-85F5-6417A69930EC

Device          Start        End    Sectors  Size Type
/dev/sda1        2048       4095       2048    1M BIOS boot
/dev/sda2        4096 1048580095 1048576000  500G Linux filesystem
/dev/sda3  1048580096 1572868095  524288000  250G Linux filesystem
/dev/sda4  1572868096 7800571903 6227703808  2.9T Linux filesystem
```

### parted -l 可以查看未挂载的文件系统类型，以及哪些分区尚未格式化。

```
fdisk -l
Disk /dev/loop0: 86.9 MiB, 91099136 bytes, 177928 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes


Disk /dev/loop1: 87.9 MiB, 92164096 bytes, 180008 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes


Disk /dev/sda: 3.7 TiB, 3998614552576 bytes, 7809794048 sectors
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 63F93572-A264-41EF-85F5-6417A69930EC

Device          Start        End    Sectors  Size Type
/dev/sda1        2048       4095       2048    1M BIOS boot
/dev/sda2        4096 1048580095 1048576000  500G Linux filesystem
/dev/sda3  1048580096 1572868095  524288000  250G Linux filesystem
/dev/sda4  1572868096 7800571903 6227703808  2.9T Linux filesystem


root@user:/lib/systemd/system# parted -l
Model: DELL PERC H710 (scsi)
Disk /dev/sda: 3999GB
Sector size (logical/physical): 512B/512B
Partition Table: gpt
Disk Flags: 

Number  Start   End     Size    File system  Name  Flags
 1      1049kB  2097kB  1049kB                     bios_grub
 2      2097kB  537GB   537GB   ext4
 3      537GB   805GB   268GB   ext4
 4      805GB   3994GB  3189GB  ext4
```

### lsblk -f 也可以查看未挂载的文件系统类型。

lsblk - list block devices

```
lsblk
NAME   MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
loop0    7:0    0 86.9M  1 loop /snap/core/4917
loop1    7:1    0 87.9M  1 loop /snap/core/5328
sda      8:0    0  3.7T  0 disk 
├─sda1   8:1    0    1M  0 part 
├─sda2   8:2    0  500G  0 part /
├─sda3   8:3    0  250G  0 part /boot
└─sda4   8:4    0  2.9T  0 part /home
sr0     11:0    1 1024M  0 rom  
```

### file -s /dev/sda2 可以查看文件系统类型

```
/dev/sda2: Linux rev 1.0 ext4 filesystem data, UUID=edd21cce-b726-11e8-aea3-b82a72db2a12 (needs journal recovery) (extents) (64bit) (large files) (huge files)
```

From: [游必有方](https://www.cnblogs.com/youbiyoufang/p/7607174.html)