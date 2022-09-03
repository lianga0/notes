# Spark单机测试环境的安装

> https://spark.apache.org/docs/latest/quick-start.html

Spark测试环境搭建非常简单，仅需配置Java和下载Spark编译好的二进制包即可。

Spark支持如下几种集群模式：

- Standalone: a simple cluster manager included with Spark that makes it easy to set up a cluster.
- Apache Mesos: a general cluster manager that can also run Hadoop MapReduce and service applications. (Deprecated)
- Hadoop YARN: the resource manager in Hadoop 2.
- Kubernetes: an open-source system for automating deployment, scaling, and management of containerized applications.

> Spark uses the Hadoop core library to talk to HDFS and other Hadoop-supported storage systems. Because the protocols have changed in different versions of Hadoop, you must build Spark against the same version that your cluster runs.

由于本地测试版本不需要使用Hadoop，所以下任意版本的Spark包都行。

> Spark runs on both Windows and UNIX-like systems (e.g. Linux, Mac OS), and it should run on any platform that runs a supported version of Java. This should include JVMs on x86_64 and ARM64. It’s easy to run locally on one machine — all you need is to have java installed on your system `PATH`, or the `JAVA_HOME` environment variable pointing to a Java installation.

具体Java版本的需求可以参考链接（https://spark.apache.org/docs/latest/index.html），这里用Java8最新的小版本即可。

配置好Java环境后，解压下载好的Spark包，运行`bin/pyspark`即可获得一个交互式的pyspark shell。

也可以运行命令`bin/spark-submit test.py`运行写好的测试Python脚本。

## Interactive Analysis with the Spark Shell

PySpark也可以直接用pip命令安装`pip install pyspark`，安装后同样需要配置Java环境。否则会提示如下信息：

```
ubuntu@ubuntu:~$ pyspark
JAVA_HOME is not set
```