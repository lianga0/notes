## how to disable access time settings in linux

> 2015 Jul 29 at 11:05

Performance Best Practices for MongoDB implies that:

> Most file systems will maintain metadata for the last time a file was accessed. While this may be useful for some applications, in a database it means that the file system will issue a write every time the database accesses a page, which will negatively impact the performance and throughput of the system.

For mongoDB installation I need to disable access time on my Debian, how to do that?

### Answer

To disable the writing of access times, you need to mount the filesystem(s) in question with the `noatime` option.

To mount an already mounted filesystem with the `noatime` option, do the following:

```
mount /home -o remount,noatime
```

To make the change permanent, update your `/etc/fstab` and add `noatime` to the options field.

For example.

Before:

```
/dev/mapper/sys-home  /home  xfs  nodev,nosuid         0       2
```

After:

```
/dev/mapper/sys-home  /home  xfs  nodev,nosuid,noatime  0       2
```

On Ubuntu ext4 File system, it may like the following:

```
/dev/mapper/localhost-root / ext4 errors=remount-ro 0 1
```

After:

```
/dev/mapper/localhost-root / ext4 noatime,errors=remount-ro 0 1
```

From: https://unix.stackexchange.com/questions/219015/how-to-disable-access-time-settings-in-debian-linux