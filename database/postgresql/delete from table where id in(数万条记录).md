## delete from table where id in(数万条记录)

> 从未完美过 2018-06-26 17:28:54

> from: https://blog.csdn.net/weixin_42056745/article/details/80818336

刚从数据库中 delete from table where id in(1，2，3，4) 没问题，速度很快

但是一旦加上子查询 如delete from table where id in(select id from table2)  就非常慢，有时候跑了一整天都没动静，

最后搜索查询了下  in子查询这个样的语句在mysql5.6之前一直是禁止使用的 效率极差 改成表连接的方式

采用如下方式：

```
delete a from table1 a inner join table2 b on a.id=b.id
```

速度就快了很多。

不过PostgreSQL并不支持这种语法，可以使用下面的语句实现类似的效果。具体细节可以参照[Delete using left outer join in Postgres](https://stackoverflow.com/questions/21662726/delete-using-left-outer-join-in-postgres)

```
DELETE FROM tv_episodes
USING tv_episodes AS ed
LEFT OUTER JOIN data AS nd ON
   ed.file_name = nd.file_name AND 
   ed.path = nd.path
WHERE
   tv_episodes.id = ed.id AND
   ed.cd_name = 'MediaLibraryDrive' AND nd.cd_name IS NULL;
```

## Delete using left outer join in Postgres

I am switching a database from MySQL to Postgres SQL. A select query that worked in MySQL works in Postgres but a similar delete query does not.

I have two tables of data which list where certain back-up files are located. Existing data (ed) and new data (nd). This syntax will pick out existing data which might state where a file is located in the existing data table, matching it against equal filename and path, but no information as to where it is located in the new data:

```
SELECT ed.id, ed.file_name, ed.cd_name, ed.path, nd.cd_name
FROM tv_episodes AS ed
LEFT OUTER JOIN data AS nd ON
ed.file_name = nd.file_name AND 
ed.path = nd.path
WHERE ed.cd_name = 'MediaLibraryDrive' AND nd.cd_name IS NULL;
```

I wish to run a delete query using this syntax:

```
DELETE ed
FROM tv_episodes AS ed
LEFT OUTER JOIN data AS nd ON
ed.file_name = nd.file_name AND 
ed.path = nd.path
WHERE ed.cd_name = 'MediaLibraryDrive' AND nd.cd_name IS NULL;
```

I have tried DELETE ed and DELETE ed.* both of which render syntax error at or near "ed". Similar errors if I try without the alias of ed. If I attempt

```
DELETE FROM tv_episodes AS ed
LEFT  JOIN data AS nd.....
```

Postgres sends back syntax error at or near "LEFT".

I'm stumped and can't find much on delete queries using joins specific to psql.


### Answers

As others have noted, you can't LEFT JOIN directly in a DELETE statement. You can, however, self join on a primary key to the target table with a USING statement, then left join against that self-joined table.

```
DELETE FROM tv_episodes
USING tv_episodes AS ed
LEFT OUTER JOIN data AS nd ON
   ed.file_name = nd.file_name AND 
   ed.path = nd.path
WHERE
   tv_episodes.id = ed.id AND
   ed.cd_name = 'MediaLibraryDrive' AND nd.cd_name IS NULL;
```

Note the self join on tv_episodes.id in the WHERE clause. This avoids the sub-query route provided above.


From: https://stackoverflow.com/questions/21662726/delete-using-left-outer-join-in-postgres
