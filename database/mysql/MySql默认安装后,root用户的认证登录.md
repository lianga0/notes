## MySql默认安装后，root用户的认证登录

> 2019.02.20

升级至Ubuntu18.04.2后，全新安装`mysql-server-5.7`发现安装过程中居然不再提示设置用户名和密码。

安装完成后，切换至Ubuntu的root用户，可以直接用`mysql -uroot`命令连接到MySQL服务。其它管理员组用户使用`sudo mysql -uroot`命令也可以登录MySQL服务。

不过，以前习惯从其他机器上，通过`MySQL Workbanch`连接MySQL的方法就没办法工作了。Google发现如下解决方案：

1. 设置root用户使用`mysql_native_password`认证插件，而不是`auth_socket`。
2. 创建一个新的MySQL用户，并授予相应的访问权限。推荐使用第二种方法。
3. 为当前Ubuntu系统用户创建对应的MySQL用户，并使用`auth_socket`方式认证。

#### MySQL用户认证plugin 

Some systems like Ubuntu, mysql is using by default the [UNIX auth_socket plugin](https://dev.mysql.com/doc/refman/8.0/en/pluggable-authentication.html#pluggable-authentication-available-plugins).

> The server-side `auth_socket` authentication plugin authenticates clients that connect from the local host through the Unix socket file. The plugin uses the `SO_PEERCRED` socket option to obtain information about the user running the client program. Thus, the plugin can be used only on systems that support the `SO_PEERCRED` option, such as Linux.

Basically means that: `db_users` using it, will be "auth" by the *system user credentias*. You can see if your *root user* is set up like this by doing the following:

```
$ sudo mysql -u root # I had to use "sudo" since is new installation

mysql> USE mysql;
mysql> SELECT user, plugin, authentication_string FROM user;
+------------------+-----------------------+-------------------------------------------+
| user             | plugin                | authentication_string                     |
+------------------+-----------------------+-------------------------------------------+
| root             | auth_socket           |                                           |
| mysql.session    | mysql_native_password | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
| mysql.sys        | mysql_native_password | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
| debian-sys-maint | mysql_native_password | *96F673A30D26A9FA1DF69AD59711F8ABE1756532 |
+------------------+-----------------------+-------------------------------------------+
```

As you can see in the query, the root user is using the `auth_socket` plugin.

#### Option 1:

修改root用户的认证方式，可以通过如下SQL将root用户的认证方式改为`mysql_native_password`。

```
$ sudo mysql -u root  # I had to use "sudo" since is new installation

mysql> USE mysql;
mysql> UPDATE user SET plugin='mysql_native_password' WHERE User='root';
mysql> FLUSH PRIVILEGES;
mysql> exit;

$ sudo service mysql restart
```

修改后，可以通过`mysql -uroot -p`命令直接连接MySQL服务器，此时root用户的密码为空。通过下面命令查看`mysql`数据库中的`user`表可以看到修改已经生效，并且`authentication_string`字段的值为空。

```
select user, plugin, authentication_string from user;
+------------------+-----------------------+-------------------------------------------+
| user             | plugin                | authentication_string                     |
+------------------+-----------------------+-------------------------------------------+
| root             | mysql_native_password |                                           |
| mysql.session    | mysql_native_password | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
| mysql.sys        | mysql_native_password | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
| debian-sys-maint | mysql_native_password | *96F673A30D26A9FA1DF69AD59711F8ABE1756532 |
+------------------+-----------------------+-------------------------------------------+
4 rows in set (0.00 sec)
```

然后可以通过`mysqladmin -uroot -p password 新密码`命令修改为新的想设置的登录密码。修改后查看`mysql`数据库中的`user`表，可以看到新密码已经写入数据库。

```
select user, plugin, authentication_string from user;
+------------------+-----------------------+-------------------------------------------+
| user             | plugin                | authentication_string                     |
+------------------+-----------------------+-------------------------------------------+
| root             | mysql_native_password | *7EE4271DC428151A9073B548FF9F7B73ACD8CBCC |
| mysql.session    | mysql_native_password | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
| mysql.sys        | mysql_native_password | *THISISNOTAVALIDPASSWORDTHATCANBEUSEDHERE |
| debian-sys-maint | mysql_native_password | *96F673A30D26A9FA1DF69AD59711F8ABE1756532 |
+------------------+-----------------------+-------------------------------------------+
4 rows in set (0.00 sec)
```

#### Option 2: 

```
CREATE USER 'user'@'172.30.0.%' IDENTIFIED BY 'password';
GRANT all ON *.* TO 'user'@'172.30.0.%' IDENTIFIED BY 'password';
FLUSH PRIVILEGES; 
```

#### Option 3: (replace YOUR_SYSTEM_USER with the username you have)

```
$ sudo mysql -u root # I had to use "sudo" since is new installation

mysql> USE mysql;
mysql> CREATE USER 'YOUR_SYSTEM_USER'@'localhost' IDENTIFIED BY '';
mysql> GRANT ALL PRIVILEGES ON *.* TO 'YOUR_SYSTEM_USER'@'localhost';
mysql> UPDATE user SET plugin='auth_socket' WHERE User='YOUR_SYSTEM_USER';
mysql> FLUSH PRIVILEGES;
mysql> exit;

$ service mysql restart
```

Remember that if you use option #3 you'll have to connect to mysql as your system username (mysql -u YOUR_SYSTEM_USER)

> Note: On some systems (e.g., Debian stretch) 'auth_socket' plugin is called 'unix_socket', so the corresponding SQL command should be: UPDATE user SET plugin='unix_socket' WHERE User='YOUR_SYSTEM_USER';



Reference：

[ERROR 1698 (28000): Access denied for user 'root'@'localhost'](https://stackoverflow.com/questions/39281594/error-1698-28000-access-denied-for-user-rootlocalhost)

[Pluggable Authentication](https://dev.mysql.com/doc/refman/8.0/en/pluggable-authentication.html#pluggable-authentication-available-plugins)

[6.5.1.9 Socket Peer-Credential Pluggable Authentication](https://dev.mysql.com/doc/refman/8.0/en/socket-pluggable-authentication.html)

[mysql修改用户密码的方法及命令](https://www.cnblogs.com/mmx8861/p/9062363.html)


## mysql修改用户密码的方法及命令

> 查文档时看到*mx8088*的总结，正好直接贴在这下面了。

> From: https://www.cnblogs.com/mmx8861/p/9062363.html

### 方法1： 用SET PASSWORD命令 

首先登录MySQL。 

格式：mysql> set password for 用户名@localhost = password('新密码'); 

例子：mysql> set password for root@localhost = password('123'); 

### 方法2：用mysqladmin 

格式：mysqladmin -u用户名 -p旧密码 password 新密码 

例子：mysqladmin -uroot -p123456 password 123 

### 方法3：用UPDATE直接编辑user表 

首先登录MySQL。 

```
mysql> use mysql; 
mysql> update user set password=password('123') where user='root' and host='localhost'; 
mysql> flush privileges; 
```

### 方法4：在忘记root密码的时候，可以这样 

以windows为例： 

1. 关闭正在运行的MySQL服务。 
2. 打开DOS窗口，转到mysql\bin目录。 
3. 输入mysqld --skip-grant-tables 回车。--skip-grant-tables 的意思是启动MySQL服务的时候跳过权限表认证。 
4. 再开一个DOS窗口（因为刚才那个DOS窗口已经不能动了），转到mysql\bin目录。 
5. 输入mysql回车，如果成功，将出现MySQL提示符 >。 
6. 连接权限数据库： use mysql; 。 
6. 改密码：update user set password=password("123") where user="root";（别忘了最后加分号） 。 
7. 刷新权限（必须步骤）：flush privileges;　。 
8. 退出 quit。 
9. 注销系统，再进入，使用用户名root和刚才设置的新密码123登录。

《完》