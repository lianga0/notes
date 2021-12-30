# PostgreSQL14安装完成后用户的配置修改

> 2021.12.30

> [修改postgres的密码](http://www.360doc.com/content/13/0822/10/10384031_309039914.shtml)

Linux系统中PostgreSQL安装完成后，系统会创建一个数据库超级用户postgres，密码为空。

可以使用命令`sudo -i -u postgres`直接切换到该Linux用户，然后使用`psql`命令连接本地数据库。输出以下信息，说明安装成功：

```
$ psql
psql (14.1)
Type "help" for help.

postgres=#
```

## 修改PostgreSQL数据库的默认用户postgres的密码(注意不是linux系统帐号)

1. PostgreSQL登录(使用psql客户端登录)

```
sudo -u postgres psql        
```

其中，`sudo -u postgres` 是使用`postgres`用户登录的意思。PostgreSQL数据默认会创建一个`postgres`的数据库用户作为数据库的管理员，密码是随机的，这里修改为`postgres`

2. 修改PostgreSQL登录密码：

```
postgres=# ALTER USER postgres WITH PASSWORD 'postgres';
```

3. 退出PostgreSQL psql客户端

```
postgres=# \q
```

然后就可以使用`psql -h localhost -U postgres -W`命令登录了。

## 修改linux系统的postgres用户的密码

1. 删除PostgreSQL用户密码

```
# sudo passwd -d postgres
passwd: password expiry information changed.
```
passwd -d 是清空指定用户密码的意思

2. 设置PostgreSQL用户密码

PostgreSQL数据默认会创建一个linux用户`postgres`，通过上面的代码修改密码为`postgres`。

```
#sudo -u postgres passwd
```

现在，我们就可以在数据库服务器上用postgres帐号通过psql或者pgAdmin等等客户端操作数据库了。
