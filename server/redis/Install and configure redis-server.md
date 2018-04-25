### 配置安装Redis服务器

#### Building Redis
--------------

```
% make
```

After building Redis, it is a good idea to test it using:

```
% make test
```

Fixing build problems with dependencies or cached build options


#### Running Redis
-------------

To run Redis with the default configuration just type:

```
% cd src
% ./redis-server
```

If you want to provide your redis.conf, you have to run it using an additional
parameter (the path of the configuration file):

```
% cd src
% ./redis-server /path/to/redis.conf
```

It is possible to alter the Redis configuration by passing parameters directly
as options using the command line. Examples:

```
% ./redis-server --port 9999 --slaveof 127.0.0.1 6379
% ./redis-server /etc/redis/6379.conf --loglevel debug
```

All the options in redis.conf are also supported as options using the command
line, with exactly the same name.

当然，上面Run Redis的方法一般仅仅用于自己上手熟悉Redis的练习。正常Redis服务一般需要进行安装，以及Redis Server运行参数的配置。具体过程如下：

#### Installing Redis
-----------------

In order to install Redis binaries into `/usr/local/bin` just use:

```
% make install
```

You can use `make PREFIX=/some/other/directory install` if you wish to use a
different destination.

Make install will just install binaries in your system, but will not configure
init scripts and configuration files in the appropriate place. This is not
needed if you want just to play a bit with Redis, but if you are installing
it the proper way for a production system, we have a script doing this
for Ubuntu and Debian systems:

```
% cd utils
% ./install_server.sh
```

The script will ask you a few questions and will setup everything you need
to run Redis properly as a background daemon that will start again on
system reboots.

You'll be able to stop and start Redis using the script named
`/etc/init.d/redis_<portnumber>`, for instance `/etc/init.d/redis_6379`.

#### Redis安装文件详细

使用上述redis-4.0.9源代码包编译安装，在采用默认参数的情况下，Redis相关的可执行文件会被放置到`/usr/local/bin`目录中。其它主要文件默认分布如下：


```
/run/systemd/generator.late/redis_6379.service
/run/systemd/generator.late/graphical.target.wants/redis_6379.service
/run/systemd/generator.late/multi-user.target.wants/redis_6379.service
/usr/lib/libreoffice/share/gallery/www-graf/gredisk.gif
/usr/local/bin/redis-check-rdb
/usr/local/bin/redis-server
/usr/local/bin/redis-benchmark
/usr/local/bin/redis-check-aof
/usr/local/bin/redis-sentinel
/usr/local/bin/redis-cli
/etc/rc3.d/S02redis_6379
/etc/rc0.d/K01redis_6379
/etc/rc2.d/S02redis_6379
/etc/rc4.d/S02redis_6379
/etc/rc5.d/S02redis_6379
/etc/init.d/redis_6379
/etc/redis
/etc/redis/6379.conf
/etc/rc6.d/K01redis_6379
/etc/rc1.d/K01redis_6379
/home/dr/.rediscli_history
/home/dr/redis-4.0.9.tar.gz
/var/lib/redis
/var/lib/redis/6379
/var/lib/redis/6379/dump.rdb
/var/log/redis_6379.log
```

#### Ubuntu发行版包管理工具安装过程

Ubuntu等Linux发行版，均有自己的包管理工具。可以很方便的安装各种应用和系统软件工具。

包管理工具默认会将可执行文件安装于`/usr/bin`目录下，这和编译源代码默认安装路径`/usr/local/bin`存在一定的差别。

Ubuntu安装Redis服务的命令如下，但一般Linux发行版包管理工具安装的软件版本较官网版本更新较慢。

```
sudo apt-get install redis-server
```

比如，Redis官网已经发布了redis-4.0.9，而采用Ubuntu发行版包管理工具安装的Redis版本仅为redis-3.0.6。但通过Linux发行版安装比较方便，且包含的文件较多，同时会自动配置各种配置参数。下面列出Linux包管理器安装Redis时，默认安装文件路径信息：

```
/run/redis
/run/redis/redis-server.pid
/var/cache/apt/archives/redis-server_2%3a3.0.6-1_amd64.deb
/var/cache/apt/archives/redis-tools_2%3a3.0.6-1_amd64.deb
/var/log/redis
/var/log/redis/redis-server.log
/var/lib/systemd/deb-systemd-helper-enabled/redis-server.service.dsh-also
/var/lib/systemd/deb-systemd-helper-enabled/redis.service
/var/lib/systemd/deb-systemd-helper-enabled/multi-user.target.wants/redis-server.service
/var/lib/redis
/var/lib/dpkg/info/redis-tools.md5sums
/var/lib/dpkg/info/redis-server.list
/var/lib/dpkg/info/redis-server.postinst
/var/lib/dpkg/info/redis-server.conffiles
/var/lib/dpkg/info/redis-server.prerm
/var/lib/dpkg/info/redis-server.md5sums
/var/lib/dpkg/info/redis-server.postrm
/var/lib/dpkg/info/redis-tools.list
/usr/share/bash-completion/completions/bash_completion.d/redis-cli
/usr/share/man/man1/redis-server.1.gz
/usr/share/man/man1/redis-cli.1.gz
/usr/share/man/man1/redis-benchmark.1.gz
/usr/share/doc/redis-server
/usr/share/doc/redis-server/changelog.Debian.gz
/usr/share/doc/redis-server/copyright
/usr/share/doc/redis-tools
/usr/share/doc/redis-tools/changelog.Debian.gz
/usr/share/doc/redis-tools/examples
/usr/share/doc/redis-tools/examples/redis-trib.rb
/usr/share/doc/redis-tools/examples/lru
/usr/share/doc/redis-tools/examples/lru/test-lru.rb
/usr/share/doc/redis-tools/examples/lru/README
/usr/share/doc/redis-tools/copyright
/usr/bin/redis-server
/usr/bin/redis-benchmark
/usr/bin/redis-cli
/usr/bin/redis-check-aof
/usr/bin/redis-check-dump
/usr/lib/tmpfiles.d/redis-server.conf
/tmp/systemd-private-9523075e9cd94559a74007de70ae30f9-redis-server.service-1GxclW
/tmp/systemd-private-9523075e9cd94559a74007de70ae30f9-redis-server.service-1GxclW/tmp
/etc/rc4.d/S03redis-server
/etc/rc2.d/S03redis-server
/etc/rc3.d/S03redis-server
/etc/init.d/redis-server
/etc/systemd/system/redis.service
/etc/systemd/system/multi-user.target.wants/redis-server.service
/etc/redis
/etc/redis/redis.conf
/etc/redis/redis-server.pre-up.d
/etc/redis/redis-server.pre-up.d/00_example
/etc/redis/redis-server.pre-down.d
/etc/redis/redis-server.pre-down.d/00_example
/etc/redis/redis-server.post-up.d
/etc/redis/redis-server.post-up.d/00_example
/etc/redis/redis-server.post-down.d
/etc/redis/redis-server.post-down.d/00_example
/etc/rc6.d/K01redis-server
/etc/rc0.d/K01redis-server
/etc/rc1.d/K01redis-server
/etc/rc5.d/S03redis-server
/etc/logrotate.d/redis-server
/etc/default/redis-server
/sys/fs/cgroup/devices/system.slice/redis-server.service
/sys/fs/cgroup/devices/system.slice/redis-server.service/tasks
/sys/fs/cgroup/devices/system.slice/redis-server.service/cgroup.procs
/sys/fs/cgroup/devices/system.slice/redis-server.service/devices.allow
/sys/fs/cgroup/devices/system.slice/redis-server.service/cgroup.clone_children
/sys/fs/cgroup/devices/system.slice/redis-server.service/notify_on_release
/sys/fs/cgroup/devices/system.slice/redis-server.service/devices.deny
/sys/fs/cgroup/devices/system.slice/redis-server.service/devices.list
/sys/fs/cgroup/systemd/system.slice/redis-server.service
/sys/fs/cgroup/systemd/system.slice/redis-server.service/tasks
/sys/fs/cgroup/systemd/system.slice/redis-server.service/cgroup.procs
/sys/fs/cgroup/systemd/system.slice/redis-server.service/cgroup.clone_children
/sys/fs/cgroup/systemd/system.slice/redis-server.service/notify_on_release
/lib/systemd/system/redis-server.service
```


《完》
