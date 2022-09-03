# Spark运行时产生的临时目录的问题

> spark-3.2.0-bin-hadoop3.2

Spark的Job任务在运行过程中可能产生大量的临时文件，在Standalone模式这些文件默认存放于`/tmp/spark*`路径。

当Shuffle临时文件过多时，导致`/tmp`目录写满而出现如下错误 No Space Left on the device。

## 解决办法

### 第一种：

直接在bash中设置环境变量临时指定新的存储位置：

```
export SPARK_LOCAL_DIRS=/new/path/have/enough/space/tmp 
```

### 第二种：

修改配置文件`conf/spark-env.sh`,把临时文件引入到一个自定义的目录中去即可

```
export SPARK_LOCAL_DIRS=/home/utoken/datadir/spark/tmp 
```

### 第三种：

修改配置文件`conf/spark-defaults.conf`，增加如下一行（不推荐）：

```
spark.local.dir /diskb/sparktmp,/diskc/sparktmp,/diskd/sparktmp,/diske/sparktmp,/diskf/sparktmp,/diskg/sparktmp
```

如果`spark-env.sh`与`spark-defaults.conf`都配置，则`SPARK_LOCAL_DIRS`覆盖`spark.local.dir`的配置

> NOTE: In Spark 1.0 and later this will be overridden by SPARK_LOCAL_DIRS (Standalone, Mesos) or LOCAL_DIRS (YARN) environment variables set by the cluster manager.

Reference：https://blog.csdn.net/kwu_ganymede/article/details/49094881

[Spark Configuration](https://spark.apache.org/docs/2.3.0/configuration.html)
