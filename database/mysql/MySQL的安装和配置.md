### MySQL的安装和配置

##### 1. 安装Ubuntu 16.04 LTS

##### 2. 安装Ubuntu提供的MySQL 5.7版本

```
	sudo apt-get install mysql-server-core-5.7
	sudo apt-get install mysql-server-5.7
```

##### 3. 设置MySQL服务启动时绑定的IP，从而允许其它IP访问MySQL服务

根据MySQL版本的不同，bind-address配置文件的位置也会存在差别。
一般位于`/etc/mysql/my.cnf`或`/etc/mysql/mysql.conf.d/mysqld.cnf`文件中。

```
# Instead of skip-networking the default is now to listen only on
# localhost which is more compatible and is not less secure.
bind-address            = ::
# 或者 bind-address     = 本机IP
# reference: https://dev.mysql.com/doc/refman/5.7/en/server-options.html#option_mysqld_bind-address
```

##### 5. 添加用户访问MySQL的权限

MySQL支持指定用户可登录IP和授予的具体访问权限。
这里为简单方便，直接配置为允许同一局域网的其它主机使用root用户访问数据库服务。

```
CREATE USER 'root'@'172.30.0.%' IDENTIFIED BY 'password';
GRANT USAGE ON *.* TO 'root'@'172.30.0.%' IDENTIFIED BY 'password';
```

##### 6. 检查Ubuntu防火墙设置

Ubuntu默认使用`ufw (Uncomplicated Firewall)`作为防火墙配置工具，且ufw处于禁用状态。如果您想不使用终端来设置防火墙，也可安装 `gufw`。

如果防火墙已经启动需要添加规则，允许其他主机通过防火墙访问MySQL服务。

为方便起见，`ufw`中添加允许同一局域网内任意主机访问访问MySQL服务器任意服务规则。

```
sudo ufw allow from 172.30.0.0/24
```

删除添加规则使用命令

```
sudo ufw delete allow 172.30.0.0/24
```

使用`sudo ufw status`命令查看防火墙状态，结果如下：

```
Status: active

To                         Action      From
--                         ------      ----
Anywhere                   ALLOW       172.30.0.0/24
```

可以使用`sudo ufw enable`和`sudo ufw disable`启用或关闭防火墙服务。

Reference:
[Assigning Account Passwords](https://dev.mysql.com/doc/refman/5.6/en/assigning-passwords.html)

[Server Command Options](https://dev.mysql.com/doc/refman/5.7/en/server-options.html#option_mysqld_bind-address)

[防火墙](https://help.ubuntu.com/lts/serverguide/firewall.html)

[启用和阻止防火墙访问](https://help.ubuntu.com/16.04/ubuntu-help/net-firewall-on-off.html)

[UFW防火墙简单设置](http://wiki.ubuntu.org.cn/UFW%E9%98%B2%E7%81%AB%E5%A2%99%E7%AE%80%E5%8D%95%E8%AE%BE%E7%BD%AE)