## mongoDB常用命令和数据库迁移

### 常用指令 
/----------------------------------------------------------------------------------------------/
查看mongodb支持的所有指令，直接输入help
查看当前数据库支持哪些方法：db.help()
查看当前数据库下的某一张表支持哪些方法：db.表名.help()
/----------------------------------------------------------------------------------------------/

①查看数据库的状态 （比如：当前数据库的名字，有多少表，多少条数据，总大小等）
db.stats()

②查看当前数据库某一张表的状态
db.posts.stats();

③查看当前处于哪个数据库 （扩展：也可以用db.stats()间接得到）
db

④查看当前数据库下有哪些表
show collections

⑤查看表的大小
db.表名.dataSize()

⑥删除表
db.表名.drop()

⑦删除当前的数据库
db.dropDatabase()

### 数据库的迁移 

两种方法：(1)先备份在还原；(2)远程克隆拷贝。这里仅记录先备份再还原的方法，此方法限制较少，能跨数据库版本进行操作。远程克隆拷贝db.cloneDatabase和db.copyDatabase方法均以不推荐使用。

#### 利用mongodump备份(所有)数据库：

mongodump -h IP --port 端口 -u 用户名 -p 密码 -d 数据库 -o 文件存在路径
- 如果没有用户谁，可以去掉-u和-p
- 如果导出本机的数据库，可以去掉-h。
- 如果是默认端口，可以去掉--port。
- 如果想导出所有数据库，可以去掉-d。

如，远程备份10.206.132.100这台服务器上的数据库到当前主机的工作路径下。数据库认证用户名和密码属于admin数据库。

```
mongodump -h 10.206.132.100 -u root -p password --authenticationDatabase=admin --authenticationMechanism=SCRAM-SHA-1 -d databaseName -o ./
```

仅备份指定collection

```
mongodump -h 10.206.132.100 -u root -p password --authenticationDatabase=admin --authenticationMechanism=SCRAM-SHA-1 -d databaseName -c collectionName -o ./
```

#### 利用mongorestore还原(所有)数据库

```
mongorestore -d mobile_staging_logs mobile_staging_logs
```

如果加--drop意思是，先删除所有的记录，然后恢复。

```
mongorestore --drop -d mobile_staging_logs mobile_staging_logs
```

参数--collection <collection>, -c <collection>指定恢复的集合名

```
mongorestore -d mobile_staging_logs  -c <collection> mobile_staging_logs/<collection>.bson
```

From: [mongoDB常用命令和数据库迁移（亲测）](https://blog.csdn.net/Qiuoooooo/article/details/56489341)