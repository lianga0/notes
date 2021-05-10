## SQL Server native client与sqlcmd单独安装

> 2021.01.06

### 背景

我有一台虚拟机，想要使用命令行实用工具连接sql server，但是又不想安装sql server怎么办。

### 方案

sql server有专门的访问客户端叫做sql server native client，然后还有一个命令行连接程序sqlcmd，其中sqlcmd依赖于sql server native client。这两者可以在[sqlcmd实用工具](https://docs.microsoft.com/zh-cn/sql/tools/sqlcmd-utility?view=sql-server-ver15)下载安装。

The sqlcmd utility lets you enter Transact-SQL statements, system procedures, and script files through a variety of available modes:

- At the command prompt.
- In Query Editor in SQLCMD mode.
- In a Windows script file.
- In an operating system (Cmd.exe) job step of a SQL Server Agent job.

The utility uses ODBC to execute Transact-SQL batches.

Reference：[Docs·SQL·工具·SQLCMD·sqlcmd 概述](https://docs.microsoft.com/zh-cn/sql/tools/sqlcmd-utility?view=sql-server-ver15)
