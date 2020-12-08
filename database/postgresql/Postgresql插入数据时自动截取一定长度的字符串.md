## Postgresql插入数据时自动截取一定长度的字符串

使用mybatis的XML更新数据库时，当Java中String对象长度超出列varchar定义后，往往会出现如下错误：

```
### Error updating database.  Cause: org.postgresql.util.PSQLException: ERROR: value too long for type character varying(256)
### The error may exist in FeedbackErrorMapper.xml
### The error may involve mapper.userMapper.addFeedbackError-Inline
### The error occurred while setting parameters
### SQL: insert into ........
### Cause: org.postgresql.util.PSQLException: ERROR: value too long for type character varying(256)
org.apache.ibatis.exceptions.PersistenceException:
### Error updating database.  Cause: org.postgresql.util.PSQLException: ERROR: value too long for type character varying(256)
### The error may exist in FeedbackErrorMapper.xml
### The error may involve mapper.userMapper.addFeedbackError-Inline
### The error occurred while setting parameters
### SQL: insert into ........
### Cause: org.postgresql.util.PSQLException: ERROR: value too long for type character varying(256)
````

如果Java中一个一个字符串去判断，感觉会非常繁琐。可以直接使用PostgreSQL显示的字符串截断语法。对应的mybatis描述文件如下：

```
<insert id="addS3FileInfo" parameterType="com.trend.s3parser.model.S3FileInfo" useGeneratedKeys="true" keyProperty="id">
    insert into public.s3_file_info(path,
        created_date,
        last_modify_date,
        parse_start_time,
        parse_finish_time,
        parse_total_record,
        parse_success_record,
        parse_fail_record,
        parser_exit_status
    ) values
    (
        #{path,jdbcType=VARCHAR}::varchar(256),
        #{created_date,jdbcType=TIMESTAMP},
        #{last_modify_date,jdbcType=TIMESTAMP},
        #{parse_start_time,jdbcType=TIMESTAMP},
        #{parse_finish_time,jdbcType=TIMESTAMP},
        #{parse_total_record,jdbcType=INTEGER},
        #{parse_success_record,jdbcType=INTEGER},
        #{parse_fail_record,jdbcType=INTEGER},
        #{parser_exit_status,jdbcType=INTEGER}
    )
</insert>
```

Reference:

[PostgreSQL 13, 8.3. Character Types Chapter 8. Data Types](https://www.postgresql.org/docs/current/datatype-character.html)
