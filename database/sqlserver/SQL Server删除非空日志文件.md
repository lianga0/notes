### SQL Server删除非空的第二个日志文件

当使用SSMS删除SQL Server的日志文件时，如果日志文件非空，那么SQL Server将会提示以下错误：

```
Msg 5042 - The file cannot be removed because it is not empty and dbcc shrinkfile emptyfile
```

有时候使用SSMS将选中的目标日志文件清空，但并不总是有效。Google后发现可以使用SQL语句清空日志文件后，可再用SQL语句直接删除日志文件。

> From: http://www.sqlserver-dba.com/2013/02/msg-5042-the-file-cannot-be-removed-because-it-is-not-empty-and-dbcc-shrinkfile-emptyfile.html

> Author: Jack Vamvas

To remove a secondary sql transaction log file is accomplished by the ALTER DATABASE REMOVE FILE command .   You may have needed to add a second transaction log file to deal with a very large transaction . Now the transaction is finished , you’re looking to delete the secondary transaction log file.

```
USE [mydatabase]
GO
ALTER DATABASE [mydatabase]  REMOVE FILE [mydatabase_Log_2]
GO
```

But under certain circumstances this error message may appear

```
Msg 5042, Level 16, State 1, Line 1
```

The file 'mydatabase_Log_2' cannot be removed because it is not empty.

To fix this error use the DBCC SHRINKFILE with the EMPTYFILE argument command

```
dbcc ShrinkFile (mydatabase_Log_2, EmptyFile)
```

The EMPTYFILE argument moves data from the chosen file to another file in the same filegroup. Once completed, rerun the ALTER DATABASE  command

<完>