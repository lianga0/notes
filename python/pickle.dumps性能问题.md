## pickle.dumps性能问题

MongoDB中存在一张8千多万记录的collection，且记录平均尺寸达26998字节。

我们希望遍历每条记录，做些统计运算，使用python2.7脚本进行测试。

在Windows平台（MongoDB所在机器）上，使用如下脚本进行读操作，平均每秒可以处理3111个记录。

```
for cc in collection.find():
    process_total_count += 1
    ...
```

而添加`pickle.dumps()`代码后，在windows上读(并处理)的速率直接掉到653个/s。

```
for cc in collection.find():
    content = pickle.dumps(cc)
    process_total_count += 1
    ...
```

Linux平台上也存在上述差异。将测试脚本放到Linux服务器上，此服务器与MongoDB服务器间是千兆网络直接互连。没有`pickle.dumps()`时每秒可以读1687个记录，而加上上述代码后，降为830个/s。虽然没有windos平台下降比例多，但下降也非常显著。

查询Python序列化性能文章，其中，比较了eval, cPickle, json方式三种对相应字符串反序列化的效率。

```
import json
import cPickle
a = range(10000)
s1 = str(a)
s2 = cPickle.dumps(a)
s3 = json.dumps(a)
%timeit -n 100 x = eval(s1)
%timeit -n 100 x = cPickle.loads(s2)
%timeit -n 100 x = json.loads(s3)
100 loops, best of 3: 16.8 ms per loop
100 loops, best of 3: 2.02 ms per loop
100 loops, best of 3: 798 µs per loop
```

### 可见json比cPickle快近3倍，比eval快20多倍。

将pickle模块替换json后，序列化性能有所提高，在windows平台上可以跑到1152个记录每秒。代码如下：

```
    for cc in collection.find():
        process_total_count += 1
        content = json.dumps(cc, cls=CJsonEncoder.CJsonEncoder)
```

### 另外，mongodump会同时dump几张表，来提高备份速度

测试过程中发现，使用mongodump仅dump一张表时，网络发送带宽为300Mbits。再额外指定一张表dump时，网络发送速率能够到达500Mbits。

可见，遍历mongoDB时，多开几个连接，并行处理会大大加快处理速度（因为通常情况下，一个进程（线程）读并处理数据，不容易把Mongo Server的处理能力全部利用起来）。

### 直接获取raw BSON，不使用Python解码文档，可以达到更高的数据加载速度

```
    for cc in collection.find_raw_batches():
        # type(cc) is str in python2.7
        import bson
        docs = bson.decode_all(cc)
        # type(docs) is list in python2.7
```

测试中通过网络读取，性能比上述各种方法都要更好（至少一倍提升，不包括bson.decode_all代码）

Reference： [【Python】Python性能优化的20条建议](https://blog.csdn.net/ztf312/article/details/78906311)
