## MongoDB 4.0在Ubuntu18.04上的默认安装路径

### 启动服务

MongoDB 4.0使用官方源安装后，可以使用`sudo systemctl start mongod.service`命令启动mongo服务。

### 查看服务状态

上述`systemctl start mongod`命令执行后，一般不会有输出信息，可以使用命令`systemctl status mongod.service`查看服务状态，信息如下：

```
● mongod.service - MongoDB Database Server
   Loaded: loaded (/lib/systemd/system/mongod.service; disabled; vendor preset: enabled)
   Active: active (running) since Fri 2018-09-14 06:17:20 UTC; 1 day 2h ago
     Docs: https://docs.mongodb.org/manual
 Main PID: 4964 (mongod)
   CGroup: /system.slice/mongod.service
           └─4964 /usr/bin/mongod --config /etc/mongod.conf

Sep 14 06:17:20 user systemd[1]: Started MongoDB Database Server.
Sep 14 06:17:20 user numactl[4964]: 2018-09-14T06:17:20.598+0000 I CONTROL  [main] Automatically disabling TLS 1.0, to force-enable TLS 1.0 specify --sslDisabledProtocols
```

从服务状态可以看出，MongoDB在Ubuntu18.04中服务启动脚本为systemd脚本。该脚本路径为位于`/lib/systemd/syste/mongod.service`。MongoDB启动时默认的配置文件为`/etc/mongod.conf`。

MongoDB安装的文件则遵循一般linux软件安装路径，可执行文件默认位于`/usr/bin/`。
默认配置文件中日志文件位于`/var/log/mongodb/`。

### 修改默认配置

我们可以修改相应的配置文件，来完成定制化。

比如修改数据库默认存储路径`/var/lib/mongodb`至我们自定义路径。

假如我们手动编辑systemd的启动脚本时，记得使用命令更新`systemctl daemon-reload`更新。

### 开机自启动

如果需要MongoDB开机自启动，那么使用命令`systemctl enable mongodb.service`设置。

Reference： [Centos7 设置Mongodb开机启动-自定义服务](https://www.jianshu.com/p/61582f4beff2)

[Install MongoDB Community Edition on Ubuntu](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/)