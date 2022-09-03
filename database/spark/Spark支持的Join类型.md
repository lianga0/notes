# Spark支持的Join类型

> https://github.com/apache/spark/blob/master/sql/catalyst/src/main/scala/org/apache/spark/sql/catalyst/plans/joinTypes.scala

Spark支持的Join类型如下：

- `inner`,
- `outer`, `full`, `fullouter`, `full_outer`
- `leftouter`, `left`, `left_outer`
- `rightouter`, `right`, `right_outer`
- `leftsemi`, `left_semi`, `semi`
- `leftanti`, `left_anti`, `anti`
- `cross`

Spark支持SEMI JOIN（半连接），并支持LEFT SEMI JOIN和LEFT ANTI JOIN两种语法。

## LEFT SEMI JOIN

当`JOIN`条件成立时，返回左表中的数据。如果`mytable1`中某行的`id`在`mytable2`的所有`id`中出现过，则此行保留在结果集中。 示例如下：

```
SELECT * from mytable1 a LEFT SEMI JOIN mytable2 b on a.id=b.id;
```

只会返回`mytable1`中的数据，只要`mytable1`的`id`在`mytable2`的`id`中出现。


## LEFT ANTI JOIN

<img src="spark_join_img/left anti join.png" alt="left anti join">

当`JOIN`条件不成立时，返回左表中的数据。如果`mytable1`中某行的`id`在`mytable2`的所有`id`中没有出现过，则此行保留在结果集中。示例如下：

```
SELECT * from mytable1 a LEFT ANTI JOIN mytable2 b on a.id=b.id;
```

只会返回`mytable1`中的数据，只要`mytable1`的`id`在`mytable2`的`id`没有出现。


### `in subquery`与`left semi join`用法类似。

```
select * from mytable1 where id in (select id from mytable2);
--等效于以下语句。
select * from mytable1 a left semi join mytable2 b on a.id = b.id;
```

### `not in subquery`与`left anti join`用法类似，但并不完全相同。示例如下。

```
select * from mytable1 where id not in (select id from mytable2);
--如果mytable2中的所有id都不为NULL，则等效于以下语句。
select * from mytable1 a left anti join mytable2 b on a.id = b.id;
```

如果`mytable2`中有任意一列为`NULL`，则`not in`表达式会为`NULL`，导致`where`条件不成立，无数据返回，这点与`left anti join`不同。
