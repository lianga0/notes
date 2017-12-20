### How to force a SQL Server database to go Offline immediately

How do I force my Database to go Offline immediately, without regard to what or who is already using it?

I tried:

```
ALTER DATABASE [database-name] SET OFFLINE;
```

But it's still hanging after 5 min.

###### Answer one (by TarkaDaal):

MSDN says to use master when operating DB's state. If you USE MY_DATABASE, then ALTER DATABASE MY_DATABASE SET OFFLINE will fail, because you're using it! Yes, I just got stung by that...

##### Go offline

You need to use `WITH ROLLBACK IMMEDIATE` to boot other connections out with no regards to what or who is is already using it. Or use `WITH NO_WAIT` to not hang and not kill existing connections.

```
USE master
GO
ALTER DATABASE [YourDatabaseName]
SET OFFLINE WITH ROLLBACK IMMEDIATE
GO
```


##### Go online

```
USE master
GO
ALTER DATABASE [YourDatabaseName]
SET ONLINE
GO
```

From: [How to force a SQL Server 2008 database to go Offline](https://stackoverflow.com/questions/3005662/how-to-force-a-sql-server-2008-database-to-go-offline)