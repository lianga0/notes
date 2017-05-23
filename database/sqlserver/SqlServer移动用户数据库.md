### SqlServer移动用户数据库

> From: https://msdn.microsoft.com/zh-cn/library/ms345483.aspx

在 SQL Server 中，通过在 ALTER DATABASE 语句的 FILENAME 子句中指定新的文件位置，可以将用户数据库中的数据、日志和全文目录文件移动到新位置。 此方法适用于在同一 SQL Server 实例中移动数据库文件。 若要将数据库移动到另一个 SQL Server 实例或另一台服务器上，请使用[备份和还原](https://msdn.microsoft.com/zh-cn/library/ms187048.aspx)或[分离和附加操作](https://msdn.microsoft.com/zh-cn/library/ms187858.aspx)。

##### 注意事项

将数据库移动到另一个服务器实例上时，若要为用户和应用程序提供一致的体验，您可能需要为数据库重新创建部分或全部元数据。 有关详细信息，请参阅[当数据库在其他服务器实例上可用时管理元数据 (SQL Server)](https://msdn.microsoft.com/zh-cn/library/ms187580.aspx)。

SQL Server 数据库引擎的某些功能改变了数据库引擎在数据库文件中存储信息的方式。 这些功能仅限于特定 SQL Server版本。 不能将包含这些功能的数据库移到不支持这些功能的 SQL Server 版本。 使用 sys.dm_db_persisted_sku_features 动态管理视图可列出当前数据库中启用的所有特定于版本的功能。

**本主题中的过程需要数据库文件的逻辑名称。 若要获取该名称，请在 sys.master_files 目录视图中查询名称列。**

从 SQL Server 2008 R2 开始，全文目录已集成到数据库中，而不是存储在文件系统中。 现在移动数据库时将自动移动全文目录。

##### 计划的重定位过程

若要将移动数据或日志文件作为计划的重定位的一部分，请执行下列步骤：

1.运行以下语句。

```
ALTER DATABASE database_name SET OFFLINE;  
```

2.将文件移动到新位置。

3.对于已移动的每个文件，请运行以下语句。如果不知道逻辑文件名可以使用第5步语句查询

```
ALTER DATABASE database_name MODIFY FILE ( NAME = logical_name, FILENAME = 'new_path\os_file_name' ); 
```

4.运行以下语句。

```
ALTER DATABASE database_name SET ONLINE;  
```

5.通过运行以下查询来验证文件更改。

```
SELECT name, physical_name AS CurrentLocation, state_desc  
FROM sys.master_files  
WHERE database_id = DB_ID(N'<database_name>');  
```

##### 计划的磁盘维护的重定位

##### 故障恢复过程

如果由于硬件故障而必须移动文件，将文件重新定位到一个新位置。

请参照原始链接说明：https://msdn.microsoft.com/zh-cn/library/ms345483.aspx