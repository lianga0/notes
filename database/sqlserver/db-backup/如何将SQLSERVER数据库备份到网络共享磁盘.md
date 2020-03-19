## 如何将SQLSERVER数据库备份到网络共享磁盘

> 2020.03.01
> From: https://blog.51cto.com/pizibaidu/1845684

背景： 今天备份一个SQLServer库，本机空间不足；我就想着要备份到共享磁盘上。记录一下备忘。

### 1. 启用xp_cmdshell

```
EXEC sp_configure 'show advanced options', 1;
RECONFIGURE;EXEC sp_configure 'xp_cmdshell', 1;
RECONFIGURE;
```

### 2. 创建网络盘符映射

```
Exec master..Xp_cmdshell 'net use Z: "\\10.206.132.127\DR_Important_data\DiamondRingDBBackup\server124.2020.02.23" /USER:usernamestring passwordstring'
```

### 3.备份数据库


```
backup database test to disk='\\10.206.132.127\DR_Important_data\DiamondRingDBBackup\server124.2020.02.23\test.bak' with init  --未验证命令
```

也可以直接在界面上操作，备份界面可以直接看到新挂载的共享目录Z盘。

Reference：

https://dba.stackexchange.com/questions/27576/how-to-map-another-server-through-sql-server-management-studio

https://social.msdn.microsoft.com/Forums/sqlserver/en-US/004b386d-1cb5-4e16-9c1c-cbed96c02fa8/to-access-a-shared-folder-providing-user-name-and-password?forum=transactsql
