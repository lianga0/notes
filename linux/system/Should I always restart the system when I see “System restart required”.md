## Should I always restart the system when I see “System restart required”?

> asked 2013.02.19 at 17:21

有时SSH远程登录到Linux系统中会出现如下提示，要求重启系统。

```
Welcome to Ubuntu 16.04.2 LTS (GNU/Linux 4.4.0-1061-aws x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud

*** System restart required ***
Last login: Sat Jul 21 07:43:41 2018 from 203.90.248.163
ubuntu@ip-172-30-0-168:~$
```

Q: 这必须要重启么？

Yes, you should. For most cases, a restart is required when an update to the Linux kernel has been installed. These updates are usually security updates, and then only come into effect after a reboot. Updates to normal applications such as Firefox come into effect after you restart the program. Firefox should prompt you to do this automatically, but other programs may not, so it's something to bear in mind.

**You may view the list of packages that require a restart with:**

```
more /var/run/reboot-required.pkgs
```

Based on the list, you can decide whether it is worth restarting.

Example of output:

```
ubuntu@ip-172-30-0-168:/var/run$ cat /var/run/reboot-required.pkgs
libssl1.0.0
linux-image-4.4.0-1062-aws
linux-base
```

(The answer was tested on Ubuntu 14.04 LTS x64 and Ubuntu 16.04 LTS x64)

From: [Should I always restart the system when I see “System restart required”?](https://askubuntu.com/questions/258297/should-i-always-restart-the-system-when-i-see-system-restart-required)