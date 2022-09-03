
##  查看数据库大小

```
select pg_size_pretty(pg_database_size('test'));
```


## 查看单个表的大小

```
select pg_size_pretty(pg_relation_size('table_name'));
```

or

```
select n.nspname ||'.'|| c.relname as table_name, pg_table_size(n.nspname ||'.'|| c.relname) as table_size from pg_catalog.pg_namespace n, pg_catalog.pg_class c where c.relnamespace=n.oid and n.nspname != 'pg_toast' and c.relkind='r' and c.relpersistence = 'u' order by table_size desc;
```


## 查看服务器配置参数设置

```
SHOW ALL;
```

or

```
psql -c 'SHOW ALL;'
```


## 将timestamp转为date进行查询聚合

```
COPY (select CAST(to_timestamp(cast(data->'first_submission_date' as int4))  as date ) as date, count(1) as number from psjson group by date) TO '/tmp/date-range.csv' (format csv, delimiter ',');
COPY (select CAST(to_timestamp(cast(data->'last_submission_date' as int4))  as date ) as date, count(1) as number from psjson group by date) TO '/tmp/last-submission-date-range.csv' (format csv, delimiter ',');
COPY (select cast(data->'times_submitted' as int4) times, count(1) as number from psjson group by times) TO '/tmp/count-range.csv' (format csv, delimiter ',');

select to_timestamp(cast(data->'first_submission_date' as int4)) as date from psjson
where to_timestamp(cast(data->'first_submission_date' as int4)) > CAST( '2020-10-10 00:00:00' AS TIMESTAMP) limit 100;

select to_timestamp(cast(data->'first_submission_date' as int4)) as date from psjson
where data->>'first_submission_date' > CAST(extract(epoch from CAST( '2021-11-30 00:00:00' AS TIMESTAMP)) as text ) limit 100;

select CAST(to_timestamp(cast(data->'first_submission_date' as int4))  as date ) as date, count(1) as number from psjson group by date;
```


## 使用psql导入JSON文件

```
psql -h localhost test -U postgres -c "COPY test (data) FROM PROGRAM 'sed \"s#\\\\\\\\#\\\\\\\\\\\\\\\\#g\" /tmp/pattern_source_ten_million.json';"
```
