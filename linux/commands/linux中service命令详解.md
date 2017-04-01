##linux service命令常见使用方法

`service`命令，顾名思义，就是用于管理Linux操作系统中服务的命令。然而也不是所有的Linux发行版中都带有这个命令。`service`命令一般位于`/usr/sbin`目录或`/sbin`目录下。`/usr/bin/`等目录可能存在相应的链接文件。

用`file`命令查看`service`命令会发现它是一个脚本命令。查看文件内容和`service`命令的帮助文档，可知此命令的作用是去`/etc/init`目录寻找upstart jobs和`/etc/init.d`目录寻找System V初始化脚本，进行开启和关闭等操作。`service`命令脚本如下：

```
#!/bin/sh

###########################################################################
# /usr/bin/service
#
# A convenient wrapper for the /etc/init.d init scripts.
#
...
```

service命令格式如下：

```
service SCRIPT COMMAND [OPTIONS]
```

`service` runs a System V init script or upstart job in as predictable an environment as possible, removing most environment  variables  and  with  the  current  working directory set to /.

The `SCRIPT` parameter specifies a System V init script, located in `/etc/init.d/SCRIPT`, or the name of an upstart job in `/etc/init`. 

同名的upstart job优先于同名的System V初始化脚本执行。

The existence of an upstart job of the same name as a script in `/etc/init.d` will cause the upstart job to take precedence over the `init.d` script.

The supported values of `COMMAND` depend on the invoked script.   

service passes `COMMAND` and `OPTIONS` to the init script unmodified. 

For upstart jobs, start, stop, status, are passed through to their upstart  equivalents. 

All scripts should support at least the start and stop commands.  

As a special case, if `COMMAND` is --full-restart, the script is run twice,  first with the stop command, then with the start command. This option has no effect on upstart jobs.

service `--status-all` runs all init scripts, in alphabetical order, with the  status command. This option only calls status for sysvinit jobs, upstart jobs can be queried in a similar manner with initctl list'.

查看`/etc/init/`文件夹中许多文件是和`/etc/init.d/`文件夹中重复的，一位外国大神对这两个文件夹的区别描述如下：

> /etc/init.d contains scripts used by the System V init tools (SysVinit). This is the traditional service management package for Linux, containing the init program (the first process that is run when the kernel has finished initializing¹) as well as some infrastructure to start and stop services and configure them. Specifically, files in /etc/init.d are shell scripts that respond to start, stop, restart, and (when supported) reload commands to manage a particular service. These scripts can be invoked directly or (most commonly) via some other trigger (typically the presence of a symbolic link in /etc/rc?.d/).

> /etc/init contains configuration files used by Upstart. Upstart is a young service management package championed by Ubuntu. Files in /etc/init are configuration files telling Upstart how and when to start, stop, reload the configuration, or query the status of a service. As of lucid, Ubuntu is transitioning from SysVinit to Upstart, which explains why many services come with SysVinit scripts even though Upstart configuration files are preferred. In fact, the SysVinit scripts are processed by a compatibility layer in Upstart.

简而言之，`/etc/init.d/`就是旧时代liunx的用法，`/etc/init/`是现在Ubuntu的提倡并一步步转型的用法。为了平缓过渡，便让`service`命令可以同时寻找到两个文件夹。

`service`这个命令一开始就是用在SysVinit上的，为了支持Upstart才额外增加了启动`/etc/init/`文件夹。

那么如何使用Upstart启动服务呢。最后查看Upstart的文档，当我要重启mysql时。我只需要输入如下命令：

```
sudo restart mysql
```

而且Upstart的启动配置文件确实简单很多。其实这两个文件夹的区别也就是服务启动方式的区别，目前有三种启动方式。(例如我启动mysql服务)

1.只从`/etc/init.d/`文件夹启动：
```
/etc/init.d/mysql start
```

2.只从`/etc/init/`文件夹启动(Ubuntu提倡)：
```
sudo start mysql
```

3.从两个文件夹中启动：
```
service start mysql
```

Reference:
[Linux系统下/etc/init/和/etc/init.d/的区别](http://liaolushen.github.io/2015/09/11/Linux%E7%B3%BB%E7%BB%9F%E4%B8%8B-etc-init-%E5%92%8C-etc-init-d-%E7%9A%84%E5%8C%BA%E5%88%AB/)