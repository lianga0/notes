# PostgreSQL unlogged表

> 2019-11-02 18:44

> https://www.cnblogs.com/ilifeilong/p/11783565.html

PostgreSQL有一种介于正常表和临时表之间的类型表，称之为unlogged表，在该表新建的索引也属于unlogged，该表在写入数据时候并不将数据写入到持久的write-ahead log文件中，在数据库异常关机或者异常崩溃后该表的数据会被truncate掉，但是在写入性能上会比正常表快几倍。

## 分别测试正常表和unlogged表数据插入速度区别

```
uber_geocoder=# \dt+

                                      List of relations
          Schema          |          Name          | Type  |  Owner   |  Size  | Description 
--------------------------+------------------------+-------+----------+--------+-------------
 uber_geocoder_tw_15q3_v2 | compiling_info         | table | postgres | 16 kB  | 
 uber_geocoder_tw_15q3_v2 | data_process_reports   | table | postgres | 16 kB  | 
 uber_geocoder_tw_15q3_v2 | info                   | table | postgres | 16 kB  | 
 uber_geocoder_tw_15q3_v2 | twn_addr_compact       | table | postgres | 774 MB | 
(4 rows)

uber_geocoder=# \timing 
Timing is on.

uber_geocoder=# create table twn_addr_compact_loggod as select * from twn_addr_compact ;

SELECT 258902
Time: 977250.581 ms
```

可以看到在新建正常表并插770M的数据的情况下耗时近16分钟

新建一张unlogged表并插入770M数据进行测试

```
uber_geocoder=# create unlogged table twn_addr_compact_unloggod as select * from twn_addr_compact ;

SELECT 258902
Time: 300683.321 ms
```

可以看到在同等条件下unlogged表的插入速度为5分钟，性能提高了三倍。

感兴趣的可以将postgres进程kill掉，然后再启动数据库，就会发现我们刚才创建的unlogged表数据丢失。

## 如何查看当前数据库中所有的unlogged表

```
SELECT relname, relowner FROM pg_class WHERE relpersistence='u';
```

或者

```
uber_geocoder=# select n.nspname as schema_name,c.relname as table_name from pg_catalog.pg_namespace n, pg_catalog.pg_class c where c.relnamespace=n.oid and n.nspname != 'pg_toast' and c.relkind='r' and c.relpersistence = 'u';

       schema_name        |        table_name         
--------------------------+---------------------------
 edbstore                 | emp
 uber_geocoder_tw_15q3_v2 | twn_addr_compact_unloggod
(2 rows)
```

## 如果需要批量将unlogged表修改为正常的表，则执行如下

Postgres 9.5 添加了`ALTER TABLE ... SET LOGGED`语法允许将unlogged表修改为正常的表。

```
uber_geocoder=# select 'ALTER TABLE'||' '||concat(n.nspname,'.' ,c.relname)||' '||'SET LOGGED ;' AS convert_logged_sql from pg_catalog.pg_namespace n, pg_catalog.pg_class c where c.relnamespace=n.oid and n.nspname != 'pg_toast' and c.relkind='r' and c.relpersistence = 'u';

                             convert_logged_sql                              
-----------------------------------------------------------------------------
 ALTER TABLE edbstore.emp SET LOGGED ;
 ALTER TABLE uber_geocoder_tw_15q3_v2.twn_addr_compact_unloggod SET LOGGED ;
```

Reference: 

[How to speed up insertion performance in PostgreSQL](https://stackoverflow.com/questions/12206600/how-to-speed-up-insertion-performance-in-postgresql)

[Write Ahead Log](https://www.postgresql.org/docs/9.1/runtime-config-wal.html#GUC-SYNCHRONOUS-COMMIT)
