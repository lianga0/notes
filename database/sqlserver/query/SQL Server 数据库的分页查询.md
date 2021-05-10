## SQL Server 数据库的分页查询

> 2017年9月16日

> http://zhiheng.me/149

SQL Server中进行分页查询并不像MySQL那样方便，前几天刚好有空整理了一下常见的分页写法，做一个简单的归纳。

### 1. 利用Top分页

TOP函数用来限制返回行数，如果使用两层TOP嵌套便可以实现分页。按照这个思路可以写出如下的查询语句:

```
SELECT TOP  (@pageSize) * FROM 
(
    SELECT TOP (@pageSize * @pageIndex) * FROM table WHERE 查询条件 ORDER BY 排序条件
)  AS tempTable
ORDER BY 排序条件
```
 
但是很明显，上面的写法是不对的，且不论性能如何，该方法永远返回一页内容，当翻页到最后一页甚至再试图往后翻页时，都是如此，Bug！所以，借助TOP函数来分页的常见做法是结合 NOT IN 来写的，如下：

```
SELECT TOP  (@pageSize) * FROM table WHERE 主键 NOT IN
(
    SELECT TOP ((@pageSize-1) * @pageIndex) 主键 FROM table WHERE 查询条件 ORDER BY 排序条件
)
ORDER BY 排序条件
```

该写法比较简单，通用性强，但也有个很明显的缺点，那就是当页数越靠后时，NOT IN中的数据会变得非常多从而影响性能。当然，当表中数据量不大时还是可以满足的。

结合 NOT IN 的写法之所以会产生性能上的缺陷是因为NOT IN 中的数据量可能会变得很大，那么，针对一些特殊情况是可以做个简单优化的，比如，当排序条件是像自增主键这样比较简单的情况时，我们可以做出如下改进：

```
SELECT TOP (@pageSize) * FROM table WHERE 查询条件 AND id >
(
    SELECT ISNULL(MAX(id),0) FROM 
    (
        SELECT TOP ((@pageSize-1) * @pageIndex) id FROM table WHERE 查询条件 ORDER BY id 
    ) AS tempTable
) 
ORDER BY id   
```

可以看出，这种改进是把 NOT IN 改为可比较值处理，所以性能上会有一定提升，但是适用面较窄，可用于排序条件单一且可比较的情况。

### 2. 利用ROW_NUMBER 分页

分页其实本质上是返回满足条件的结果集中连续的若干行，如果利用ROW_NUMBER函数将结果集编号，在指定返回行号在一个区间内的子集即可完成任务，于是，借助带有ROW_NUMBER的子查询来分页是一个很自热的思路：

```
SELECT * FROM 
(
    SELECT ROW_NUMBER() OVER (ORDER BY 排序条件) AS RowNum, * FROM table WHERE 查询条件
) AS tempTable
WHERE RowNum BETWEEN (@pageIndex-1)*@pageSize+1 AND @pageIndex*@pageSize
ORDER BY RowNum
```
 
上面的查询有个问题，那就是子查询会把所有满足条件的结果都查出并编号返回，对资源会造成很大的浪费，所以，我们可以借助TOP函数让子查询每次仅返回必要的结果来做个改进：

```
SELECT * FROM 
(
    SELECT TOP (@pageIndex * @pageSize) ROW_NUMBER() OVER (ORDER BY 排序条件) AS RowNum, * 
    FROM table WHERE 查询条件
) AS tempTable
WHERE RowNum > (@pageIndex-1)*@pageSize
ORDER BY RowNum
```

上面经过改进的语句基本可以满足绝大部分的查询了，但是，尽可能少的返回字段是我们写出高效SQL的一个原则，如果子查询返回太多字段的话，对性能的损耗也是非常大的。下面是一个仅让子查询返回必要字段后和原表链接查询的优化例子：

```
SELECT * FROM 
(
    SELECT TOP (@pageIndex * @pageSize) ROW_NUMBER() OVER (ORDER BY 排序条件) AS RowNum, 
                                        主键, 
                                        待排序字段 
    FROM table WHERE 查询条件
) AS tempTable
INNER JOIN table on table.主键=tempTable.主键
WHERE tempTable.RowNum > (@pageIndex-1)*@pageSize
ORDER BY RowNum
```

使用ROW_NUMBER函数来分页要比借助两层TOP的方式可靠高效，但这种写法的可读性较差，另外对于SQL Server 2005以前的版本也不适用。

### 3. 使用OFFSET FETCH子句分页

在SQL Server 2012 及以后的版本中终于出现了类似MySQL中LIMIT的写法了，那就是`OFFSET-FETCH`。

OFFSET子句用来声明跳过结果集中的若干行，FETCH子句用于声明从剩余的结果集中获取多少行。用法如下：

```
SELECT * FROM table ORDER BY 排序条件 
OFFSET  ( @pageSize * ( @pageIndex - 1 )) ROWS 
FETCH NEXT @pageSize ROWS ONLY
```
 
看以看到，这种方式非常简单，可读性好，而且经测试性能也可靠。但是对于OFFSET的使用还需要注意一些限制，下面四条摘录自MSDN：

Limitations in Using OFFSET-FETCH

- ORDER BY is mandatory to use OFFSET and FETCH clause.
- OFFSET clause is mandatory with FETCH. You can never use, ORDER BY … FETCH.
- TOP cannot be combined with OFFSET and FETCH in the same query expression.
- The OFFSET/FETCH rowcount expression can be any arithmetic, constant, or parameter expression that will return an integer value. The rowcount expression does not support scalar sub-queries.

## 小结

如今，大部分的SQL Server应该都是在使用较新的版本了，分页查询作为SQL Server数据库用户的一个痛点的历史也应该成为过去了，愉快的使用OFFSET FETCH来分页吧。

