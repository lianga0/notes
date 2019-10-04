## Mysql删除以“#sql-”开头的临时(Orphan Intermediate)表

> 2017年05月23日
> https://blog.csdn.net/shaochenshuo/article/details/72637466

现象：在重建表（optimize table table_name_x）释放空间失败后，发现Mysql服务器的磁盘空间快满了。

数据库执行如下命令失败：

```
mysql> OPTIMIZE TABLE 表名; 
```

在重建的过程中，因为空间不足，导致任务失败，之后发现空间少了10G。于是查看是哪个目录占用了这10G，最后发现在数据目录里发现
很多类似`#sql-*.ibd`临时文件和同文件名的`#sql-*.frm`。既然知道是临时表了，那就删除吧，但是不敢直接通过rm删除了，因为在ibdata里保存字典信息和Undo信
息，数据库重启后会报错的。

后来想想，也可以不使用`OPTIMIZE TABLE`命令，而是采用创建一个新表，然后再重命名的办法。这样应该可以降低命令执行过程中对临时磁盘空间的需求量。

```
mysql>CREATE  TABLE IF NOT EXISTS new_table_xxx LIKE exit_table_xxx;
mysql>RENAME TABLE exit_table_xxx TO old_table_xxx;
mysql>RENAME TABLE new_table_xxx TO exit_table_xxx;
```

### 删除的方法

在alter table的过程中，如果Mysql突然crash了，就会在数据目录里存在一些中间表，这些中间表是以“#sql-”开头的临时表，在你的数据目录里会看到
`#sql-*.ibd`和相应的`#sql-*.frm` ，如果`#sql-*.ibd`和`#sql-*.frm`两个文件都存在数据目录里的话，可以直接drop table，类似：

```
mysql> drop table `#mysql50##sql-928_76f7`;
```

前缀`#mysql50#`是让Mysql忽略文件名的安全编码，这个前缀是在Mysql5.1引入的。

如果在数据目录里只有`#sql-*.ibd`，而没有`#sql-*.frm`的话，就需要特殊处理。详细步骤如下：

> If there is no .frm file, you can recreate it. The .frm file must have the same table schema as the orphan intermediate table (it must have the same columns and indexes) and must be placed in the database directory of the orphan intermediate table.

1. 在另一数据schema里创建一个和欲删除表一样的表结构（包括相同的列和索引），这就要求你需要知道.ibd文件对应原始表的结构了。

```
mysql> create database test;
mysql> create table test.tmp like talbe_xxx;  //只复制表的结构和索引，不复制数据
```

2. 把新创建的临时表的.frm文件复制到欲删除的数据目录里，并修改和`#sql-*.ibd`一样的文件名

```
shell> cp test/tmp.frm  destination_db_folder/#sql-928_76f7.frm
```

3. 确认`#sql-*.ibd`和`#sql-*.frm`两个文件都存，然后在mysql中直接drop，如下：

```
mysql> drop table `#mysql50##sql-928_76f7`;
```

### 怎么根据上面提到的#开头的临时文件名来定位到原来的表名呢？

1. 如果语句还在执行中，我们在 show processlist; 中能看到ddl 操作了哪张表

2. 如果是数据库 crash 后重启，我们可以尝试通过下面方法来找到原表

```
SELECT * FROM INFORMATION_SCHEMA.INNODB_SYS_TABLES order by N_COLS,SPACE;
|      677 | newsitetest/rs_order_goods#P#p12                        |    1 |     52 |   663 | Antelope    | Compact    |             0 |
|      709 | newsitetest/#sql-ib665-867311400                        |    1 |     52 |   695 | Antelope    | Compact    |             0 |
```

N_COLS 表示表的列，我们看#开头的表的列数量同哪张表一致，然后就碰运气吧。

### 查看MySQL表占用空间大小

```
mysql> use information_schema; 
mysql> select concat(round(sum(data_length/1024/1024),2),'MB') as data_length_MB,  
     concat(round(sum(index_length/1024/1024),2),'MB') as index_length_MB  
     from tables where
     table_schema='database_name_xxx'  
     and table_name = 'table_name_yyy';  
```

Reference:

[14.21.3 Troubleshooting InnoDB Data Dictionary Operations](https://dev.mysql.com/doc/refman/5.6/en/innodb-troubleshooting-datadict.html)

[MySQL查看表占用空间大小(转)](https://www.cnblogs.com/qq78292959/archive/2012/12/26/2833698.html)