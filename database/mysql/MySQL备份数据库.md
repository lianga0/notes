# mysqldump备份成压缩包

> https://www.cnblogs.com/cxxjohnson/p/7496358.html

利用mysql自带的工具mysqldump备份，你可以备份单个表，有选择的备份多个表，也可以备份全库，他的速度要比直接用navicat转载成sql文件要快很多，一般我的做法是每日备份核心表，每周备份全库。

也可以直接应用mysqldump直接将mysql数据库中的表或者整个数据库备份成压缩格式的包。

备份命令：

```
mysqldump -h localhost -uroot -p密码 数据库名 备份表名 | gzip > 备份文件名.sql.gz
```

恢复备份命令：

```
gunzip < 备份文件名.sql.gz | mysql -h localhost -P端口 -uroot -p密码 数据库名
```

Reference：

[mysql备份之mysqldump](http://blog.csdn.net/zfszhangyuan/article/details/52459921)
