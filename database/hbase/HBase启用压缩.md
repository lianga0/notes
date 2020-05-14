## HBase启用压缩

> From: https://blog.csdn.net/young_0609/article/details/102860723

> GOD_WAR 2019-11-01 16:45:23

HBase 创建表时默认压缩为 NONE ，即没有压缩，除非指定。

目前 HBase 主要支持 4 种压缩方式：GZ（GZIP），SNAPPY，LZO，LZ4。

### 1. 压缩算法的比较

  <table>
   <thead>
    <tr>
     <th>算法</th> 
     <th>压缩比</th> 
     <th>压缩</th> 
     <th>解压</th> 
    </tr>
   </thead>
   <tbody>
    <tr>
     <td>GZIP</td> 
     <td>13.4%</td> 
     <td>21MB/s</td> 
     <td>118MB/s</td> 
    </tr>
    <tr>
     <td>LZO</td> 
     <td>20.5%</td> 
     <td>135MB/s</td> 
     <td>410MB/s</td> 
    </tr>
    <tr>
     <td>Snappy/Zippy</td> 
     <td>22.2%</td> 
     <td>172MB/s</td> 
     <td>409MB/s</td> 
    </tr>
   </tbody>
  </table>

总结：

- GZIP的压缩率最高，但它是CPU密集型的，对CPU的消耗较多，压缩和解压速度也慢；
- LZO的压缩率居中，比GZIP要低一些，但是压缩和解压速度明显要比GZIP快很多，其中解压速度快的更多；
- Zippy/Snappy的压缩率最低，而压缩和解压速度要稍微比LZO要快一些

所以，一般情况下，推荐使用Snappy和Zippy压缩算法。

### 2. hbase表启用压缩的步骤

这里分为两种情况：

一、在创建表时指定压缩算法；

二、在创建表后指定压缩算法或者修改压缩算法。

#### 2.1 创建表时指定压缩算法

```
create 'test', {NAME => 'info', VERSIONS => 1, COMPRESSION => 'snappy'}
# 表创建之后，使用describe命令查看表信息
describe 'test'
```

#### 2.2 创建表后指定或修改压缩算法

1) disable需要修改的表

```
disable 'test'
```

注意，如果表较大，disable需要一些时间，请耐心等待

2) 使用alter命令进行更改

```
alter 'test', NAME => 'info', COMPRESSION => 'snappy'
```

or 

```
alter 'test', NAME => 'column family name', COMPRESSION => 'GZ'
```

NAME即column family，列族。HBase修改压缩格式，需要一个列族一个列族的修改，注意大小写，不要弄错了。如果修改错了，将会创建一个新的列族，且压缩格式为snappy。当然，假如你还是不小心创建了一个新列族的话，可以通过以下方式删除：

```
alter 'test', {NAME=>'info', METHOD=>'delete'}
```

3) 重新enable表

```
enable 'test'
```

4) 对表进行major_compact操作，使压缩生效

```
major_compact 'test'
```

注意，如果表的数据较多，该操作需要（在后台运行）较长时间，所以尽量选择一个不忙的时间，避免对服务造成影响。

修改完成后，可使用describe命令查看表信息。
