## mysql CLI 查询数据并导出到文件

> 2018.10.29

### 方式1

在mysql命令行环境下执行： sql语句+INTO OUTFILE + 文件路径/文件名 + 编码方式（可选）。或者

```
select column1, column2 
into outfile "c:/data_out.txt" （输出的文件路径）
lines terminated by "\r\n" （每一行都换行）
from table_name; （注意最后使用分号）
```

如：

```
select * from user INTO OUTFILE '/var/lib/mysql/msg_data.csv';
```

注意事项：

1. 可能会报没有 select command denied（没有查询权限）  或者 Access denied for user（没有file权限） ，增加权限之后即可。

2. 不能存在同名文件，否则sql执行失败。

3. 生成文件格式也可以是.txt/.xls/.csv。

4. 生成的文件中可能会有中文乱码问题，可以在语句后面加CHARACTER SET gbk （utf8等）。如： `select * from user  INTO OUTFILE  '/var/lib/mysql/msg_data.csv'  CHARACTER SET gbk;``

5. 如果sql查询出来的数据包含有很大的数值型数据，则在excel中这些数值数据可能会出问题，因此，可以先导出为.txt/.csv文件格式，再复制黏贴到excel文件中（首先设置单元格格式为文本）

### 方式2

在登录某服务器后，采用 mysql 命令执行 ，不需要登录进mysql命令行环境下。

```
mysql  -u用户名 -p  -e"select * from a" 数据库名 > 1.txt   
```

如：

```
mysql  -u用户名 -p --default-character-set=gb2312  -e"select * from a" 数据库名 > 1.txt
```

若有中文乱码，添加设置编码方式 utf8 、gbk

From: [借鉴+总结！！ mysql 客户端命令行下 查询数据并生成文件导出](https://www.cnblogs.com/wuyun-blog/p/6943394.html)

[从mysql中导出一列数据到txt](https://blog.csdn.net/u012654154/article/details/73036789)
