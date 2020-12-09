## 创建Amazon Redshift集群

> 2020.05.11

### 1. Amazon Redshift 设置先决条件

确定防火墙规则

在启动 Amazon Redshift 集群时，用户需要指定一个端口。同时您还需要在安全组中创建一个入站入口规则，以允许通过该端口访问您的集群。

如果您的客户端计算机位于防火墙后面，则您需要知道可用的开放端口。通过此开放端口，可以从 SQL 客户端工具连接到集群并运行查询。如果您不知道此类端口，则应与了解您网络防火墙规则的人员合作，以在您的防火墙中确定一个开放端口。

虽然 Amazon Redshift 默认使用端口 5439，但如果您的防火墙中未打开该端口，则无法建立连接。**创建了 Amazon Redshift 集群后，则不能再更改其端口号。因此，确保指定一个在启动过程中可在您的环境中工作的开放端口**。

这里我们选3389端口，因为公司防火墙不允许访问5439端口。

### 2. 创建 IAM 角色

对于任何访问其他 AWS 资源上的数据的操作，您的集群需要具有权限才能代表您访问该资源和该资源上的数据。例如，使用 COPY 命令从 Amazon S3 加载数据。

您可以在启动新集群时指定IAM角色，也可以为现有集群附加新角色。我们这里暂时用不到，所以可以先不创建IAM角色。

### 3. 创建示例 Amazon Redshift 集群

- Cluster identifier (集群标识符)：输入 drs-redshift-cluster。

- Database port (数据库端口)：输入 3389。

- Master user name (主用户名)：输入用户名值。

- Master user password (主用户密码)：输入密码的值。

#### CREATE DATABASE 创建新数据库

```
CREATE DATABASE database_name [ WITH ]
[ OWNER [=] db_owner ]
[ CONNECTION LIMIT { limit | UNLIMITED } ]
```

##### REATE DATABASE 限制

Amazon Redshift 针对数据库强制实施以下限制。

- 每个集群最多 60 个用户定义的数据库。

- 数据库名称最多为 127 个字节。

- 不能使用保留关键字。

#### PG_DATABASE_INFO 查看数据库名称列表

`PG_DATABASE_INFO` 是一个扩展 PostgreSQL 目录表 `PG_DATABASE` 的 Amazon Redshift 系统视图。PG_DATABASE_INFO 对所有用户可见。

##### 表列

除了`PG_DATABASE`中的列之外，`PG_DATABASE_INFO`还包含以下列。有关更多信息，请参阅 [PostgreSQL 8.0 文档](https://www.postgresql.org/docs/8.0/catalog-pg-database.html)。

|列名称 |数据类型 |描述 |
|------|---------|----|
|datid |oid |系统表在内部使用的对象标识符 (OID)|
|datconnlimit |text |可以对此数据库进行的最大并行连接数。值 -1 表示无限制。|

```
select * from PG_DATABASE_INFO;
```

| datid | datname | datdba | encoding | datistemplate | datallowconn | datlastsysoid | datvacuumxid | datfrozenxid | dattablespace | datconfig | datacl | datconnlimit |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 100391 | drs | 100 | 6 | false | true | 100388 | 707 | 707 | 1663 | NULL | NULL | UNLIMITED |
| 100387 | dev | 1 | 6 | false | true | 100388 | 0 | 0 | 1663 | NULL | NULL | UNLIMITED |
| 100388 | padb\_harvest | 1 | 6 | false | true | 100388 | 0 | 0 | 1663 | NULL | NULL | UNLIMITED |
| 1 | template1 | 1 | 6 | true | true | 100388 | 707 | 707 | 1663 | NULL | {rdsdb=CT/rdsdb} | NULL |
| 100389 | template0 | 1 | 6 | true | false | 100388 | 707 | 707 | 1663 | NULL | {rdsdb=CT/rdsdb} | UNLIMITED |

#### DROP DATABASE 删除数据库

```
DROP DATABASE database_name
```

`database_name`要删除的数据库的名称。您不能删除 dev、padb_harvest、template0 或 template1 数据库，并且不能删除当前数据库。



#### 查看表名称列表

例如，要查看 public schema 中所有表的列表，可以查询 PG_TABLE_DEF 系统目录表。

```
select distinct(tablename) from pg_table_def where schemaname = 'public'; 
```

#### 查看数据库用户

您可以查询`PG_USER`目录来查看所有数据库用户的列表，还可以查看用户 ID (USESYSID) 和用户权限。

```
select * from pg_user;
```

Amazon Redshift 在内部使用用户名称`rdsdb`执行日常管理和维护任务。您可以向 select 语句添加 `where usesysid > 1` 来筛选查询，使其只显示用户定义的用户名称。

#### 数据库Schema

要查看所有 Schemas 的列表，请查询 PG_NAMESPACE 系统目录表：

```
select * from pg_namespace;
```

要查看属于某 schema 的表列表，请查询 `PG_TABLE_DEF` 系统目录表。例如，以下查询会返回 PG_CATALOG schema 中的表列表。

```
select distinct(tablename) from pg_table_def
where schemaname = 'pg_catalog';
```

Reference：

[Amazon Redshift 入门指南](https://docs.aws.amazon.com/zh_cn/redshift/latest/gsg/rs-gsg-prereq.html)

[Amazon Redshift 数据库开发人员指南CREATE DATABASE](https://docs.aws.amazon.com/zh_cn/redshift/latest/dg/r_CREATE_DATABASE.html)

[Amazon Redshift数据库开发人员指南PG_DATABASE_INFO](https://docs.aws.amazon.com/zh_cn/redshift/latest/dg/r_PG_DATABASE_INFO.html)

[Amazon Redshift 数据库开发人员指南 Schemas](https://docs.aws.amazon.com/zh_cn/redshift/latest/dg/r_Schemas_and_tables.html)
