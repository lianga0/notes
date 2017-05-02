### Ubuntu 16.04添加到init.d的服务不显示echo信息

自己添加脚本到/etc/init.d里面，在之前的Ubuntu 14.04系统中，启动、关闭、重启服务都会显示相应的 echo 消息，比如，Nginx服务启动成功提示消息。

但是这一次不管怎样都没有了相关信息的显示，不过如果在其目录里面按照Shell脚本的方式运行，echo 则可以正常显示……

虽说消息不显示并不妨碍功能正常使用，但总觉得服务启动后明确给出启动结果还是很有必要的，并且也很想知道问题究竟出在哪里。

**解决方案1：可以使用`systemd`的命令显示服务启动信息：**

```
systemctl status xxxxxx.service
# xxxxxx 为/etc/init.d服务启动脚本的名字
```

**解决方案2：直接执行初始化脚本文件：**

```
/etc/init.d/nginx restart
```

**从v2ex发现一个人的回答如下：**

从Ubuntu 15.04开始，管理系统启动和系统服务启动的默认工具已经从`upstart`切换到`systemd`。

> The larger change that comes with Ubuntu 15.04 is the switch from `upstart` to `systemd` as the default for managing boot and system service startup.

在 `systemd` 里面，`/etc/init.d` 里面的文件已经再不是主要的服务启动方式，而是 `systemd` 的 service unit ，旧版的 init.d 文件通过 unit 配置文件里面类似下面这样的方式启动 

```
[Service] 
ExecStart=/etc/init.d/xxx start 
ExecStop=/etc/init.d/xxx stop 
```

脚本启动过程不是根据当前 shell 子进程启动的， stdin/out/err 都会被 `systemd` 接管，所以你看不到 echo 了。

**askubuntu.com上面的另一个回答如下：**

**You're running the same command … but actually you're not.**

You are using Ubuntu version 15.10, a systemd operating system. Your system service management is no longer performed by upstart. It is performed by systemd.

The `service` command may be the same … but the Debian/Ubuntu `service` command is a shell script that tries to auto-detect whether `upstart` or `systemd` is the running system service manager, and run the actual native service management commands for upstart and systemd. It executes two pretty much entirely different code paths for upstart and for systemd.

upstart's native service management commands are `initctl start`, `initctl stop`, `initctl status` and so forth. Those print messages as they go.

systemd's native service management commands are `systemctl start`, `systemctl stop`, `systemctl status` and so forth. Those print no output as they operate.

Further reading

https://unix.stackexchange.com/a/233840/5132
https://askubuntu.com/a/621209/43344
https://askubuntu.com/a/613814/43344

最后一篇博客介绍了Ubuntu 15.04和之前版本的差异，以及原因：
##### Why No Output From Ubuntu 16.04 service start/stop Command?

Service nginx reload/restart Gives No Output Unlike 14.01. Is not it? This Article Explains Why No Output From Ubuntu 16.04 service start/stop Command. We should not be expecting such output. Earlier Ubuntu versions didn’t behave this way because Ubuntu was an upstart system for a decade. In Ubuntu 15.04 and later version, systemd is only fully supported. So, that change from upstart to systemd made few changes. Commands actually changed and usually kind of linked with service commands with scripts.

###### Not Understood! Why No Output From Ubuntu 16.04 service start/stop Command?

Ubuntu 16.04 uses systemd. Ubuntu 14.04 or earlier used upstart. upstart is an event-based replacement for the /sbin/init daemon which handled starting of tasks and services during boot, stopping them during shutdown and supervising them while the system is running. systemd is actually used by all other major GNU/Linux distro. Debian/Ubuntu service command is a shell script that tries to detect whether upstart or systemd is the running system service manager, and run the actual native service management commands for upstart and systemd. It executes two pretty much entirely different code paths for upstart and for systemd. upstart‘s native service management commands are initctl start, initctl stop, initctl status etc. They printed the informative messages. systemd‘s native service management commands are systemctl start, systemctl stop, systemctl status and so forth. Most of the commands print no output as they operate. Hence the silent output output is expected. Here is more on Systemd : `https://wiki.ubuntu.com/SystemdForUpstartUsers`

###### Now Understood. Is There Some Way to Get Output From Ubuntu 16.04 service start/stop Command?

You can print messages with this kind of command :

```
/etc/init.d/nginx restart
```

For example :

```
root@abhishekghosh:~# /etc/init.d/nginx restart
[ ok ] Restarting nginx (via systemctl): nginx.service.
```


From: 
[添加到 init.d 的服务不显示 echo 信息，请问问题出在哪里？](https://www.v2ex.com/t/316494)

[Why No Output From Ubuntu 16.04 service start/stop Command?](https://thecustomizewindows.com/2016/11/no-output-ubuntu-16-04-service-startstop-command/)

Reference: 
[Rationale for switching from upstart to systemd?](https://askubuntu.com/questions/613366/rationale-for-switching-from-upstart-to-systemd/613814#613814)

[SystemdForUpstartUsers](https://wiki.ubuntu.com/SystemdForUpstartUsers)

[How do I get service command to print output in 15.10?](https://askubuntu.com/questions/713825/how-do-i-get-service-command-to-print-output-in-15-10)

[No output from service start/stop/restart command](https://askubuntu.com/questions/792940/no-output-from-service-start-stop-restart-command)



