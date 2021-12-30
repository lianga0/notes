## Install PostgreSQL for Ubuntu

From: https://www.postgresql.org/download/linux/ubuntu/

PostgreSQL is available in all Ubuntu versions by default. However, Ubuntu "snapshots" a specific version of PostgreSQL that is then supported throughout the lifetime of that Ubuntu version.
Other versions of PostgreSQL are available through the PostgreSQL apt repository.

### PostgreSQL Apt Repository

<p>
If the version included in your version of Ubuntu is not the one you want,
you can use the <a href="https://apt.postgresql.org" target="_blank" rel="noopener">PostgreSQL Apt Repository</a>. This repository will integrate
with your normal systems and patch management, and provide automatic
updates for all supported versions of PostgreSQL throughout the support
<a href="/support/versioning/">lifetime</a> of PostgreSQL.
</p>
<p>
The PostgreSQL Apt Repository supports the current LTS versions of Ubuntu:
</p><ul>
  <li>20.04</li>
  <li>18.04</li>
  <li>16.04</li>
</ul>
on the following architectures:
<ul>
  <li>amd64</li>
  <li>arm64 (18.04 and newer)</li>
  <li>i386 (18.04 and older)</li>
  <li>ppc64el</li>
</ul>

<p>
While not fully supported, the packages often work on other non-LTS versions as well,
by using the closest LTS version available.
</p>
<p>
To use the apt repository, follow these steps:
</p>

```
# Create the file repository configuration:
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Import the repository signing key:
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Update the package lists:
sudo apt-get update

# Install the latest version of PostgreSQL.
# If you want a specific version, use 'postgresql-12' or similar instead of 'postgresql':
sudo apt-get -y install postgresql
```

<p>
For more information about the apt repository, including answers to frequent
questions, please see the <a href="https://wiki.postgresql.org/wiki/Apt" target="_blank" rel="noopener">PostgreSQL Apt Repository</a> page on
<a href="https://wiki.postgresql.org/wiki/Apt" target="_blank" rel="noopener">the wiki</a>.
</p>

<h2>Included in distribution</h2>

<p>
Ubuntu includes PostgreSQL by default. To install PostgreSQL on
Ubuntu, use the <em>apt-get</em> (or other apt-driving) command:
</p>

<code>
apt-get install postgresql-12
</code>

<p>
The repository contains many different packages including third party
addons. The most common and important packages are (substitute the
version number as required):
</p>

<table class="table table-striped">
  <tbody>
    <tr>
     <th scope="row">postgresql-client-12</th>
     <td>client libraries and client binaries</td>
    </tr>
    <tr>
     <th scope="row">postgresql-12</th>
     <td>core database server</td>
    </tr>
    <tr>
     <th scope="row">postgresql-contrib-9.x</th>
     <td>additional supplied modules (part of the postgresql-xx package in version 10 and later)</td>
    </tr>
    <tr>
     <th scope="row">libpq-dev</th>
     <td>libraries and headers for C language frontend development</td>
    </tr>
    <tr>
     <th scope="row">postgresql-server-dev-12</th>
     <td>libraries and headers for C language backend development</td>
    </tr>
    <tr>
     <th scope="row">pgadmin4</th>
     <td>pgAdmin 4 graphical administration utility</td>
    </tr>
  </tbody>
</table>



## 启用开机自启动

```
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

## 修改用户密码

切换用户

```
su - postgres
```

登录数据库

```
psql -U postgres
```

设置postgres用户密码

```   
ALTER USER postgres WITH PASSWORD 'yourpassword'
```

## 数据库和表的常见操作

```
退出数据库
\q  

列出数据库
\l

切换数据库
\c database_name

列出表
\dt
```

## 设置远程访问

```
vim /etc/postgresql/11/main/postgresql.conf
```

修改`#listen_addresses = 'localhost'` 为 `listen_addresses='*'`。

此项表示绑定本机的网卡，*是代表每个网卡都接受请求

️pg_hba.conf需要着重调试，添加新行`host    all             all             0.0.0.0/0              md5`。

```
vim /etc/postgresql/11/main/pg_hba.conf
```

修改如下内容，信任本地连接，远程连接需要认证

```
# "local" is for Unix domain socket connections only
local   all             postgres                                peer

# TYPE  DATABASE        USER            ADDRESS                 METHOD
# "local" is for Unix domain socket connections only
local   all             all                                     peer

# IPv4 local connections:
host    all         all                 127.0.0.1/32           md5
host    all             all             0.0.0.0/0              md5

# IPv6 local connections:
host    all             all             ::1/128                 md5

# Allow replication connections from localhost, by a user with the
# replication privilege.
#local   replication     all                                     peer
#host    replication     all             127.0.0.1/32            md5
#host    replication     all             ::1/128                 md5
#host     all            all             0.0.0.0/0               md5
```

## 重启服务

```
sudo systemctl restart postgresql
```

## 备份

```
/opt/PostgreSQL/9.5/bin/pg_dump -h 164.82.233.54 -U postgres databasename > databasename.bak
```

## 恢复 

```
/opt/PostgreSQL/9.5/bin/psql -h localhost -U postgres -d databasename < databasename.bak
```

## 完全删除已安装的Postgres

```
sudo apt-get remove postgresql
sudo apt-get --purge remove postgresql

sudo rm -rf /var/lib/postgresql/
sudo rm -rf /var/log/postgresql/
sudo rm -rf /etc/postgresql/
```

## 用以下命令查看还有哪些包

```
dpkg -l | grep postgres
sudo apt-get --purge remove package_name
```
