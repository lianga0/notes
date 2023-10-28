# spark on yarn测试环境搭建

因为，我们之前已经搭建分布式的Hadoop测试环境，这里我们直接在Hadoop环境之上，搭建spark on yarn的测试环境。

为了节省磁盘空间，我们这里下载不包含Hadoop jar包的spark预编译二进制包[spark-3.3.2-bin-without-hadoop.tgz](https://spark.apache.org/downloads.html)。

下载完成后，解压运行最简单的[./bin/run-example SparkPi 10](https://spark.apache.org/docs/latest/#running-the-examples-and-shell)报缺失类错误，如下所示：

```
$ ./bin/run-example SparkPi 10
Error: A JNI error has occurred, please check your installation and try again
Exception in thread "main" java.lang.NoClassDefFoundError: org/apache/hadoop/fs/FSDataInputStream
        at java.lang.Class.getDeclaredMethods0(Native Method)
        at java.lang.Class.privateGetDeclaredMethods(Class.java:2701)
        at java.lang.Class.privateGetMethodRecursive(Class.java:3048)
        at java.lang.Class.getMethod0(Class.java:3018)
        at java.lang.Class.getMethod(Class.java:1784)
        at sun.launcher.LauncherHelper.validateMainClass(LauncherHelper.java:650)
        at sun.launcher.LauncherHelper.checkAndLoadMain(LauncherHelper.java:632)
Caused by: java.lang.ClassNotFoundException: org.apache.hadoop.fs.FSDataInputStream
        at java.net.URLClassLoader.findClass(URLClassLoader.java:387)
        at java.lang.ClassLoader.loadClass(ClassLoader.java:418)
        at sun.misc.Launcher$AppClassLoader.loadClass(Launcher.java:352)
        at java.lang.ClassLoader.loadClass(ClassLoader.java:351)
        ... 7 more
```

所以需要先按照官网[Using Spark's "Hadoop Free" Build](https://spark.apache.org/docs/latest/hadoop-provided.html)文档配置自己本地的Hadoop jar包。


考虑到Spark on Yarn仅需要一个正常的yarn集群即可提交Hadoop任务，不过我们可以配置一个单独的spark history server来查看结束的spark任务，详细信息可以参考官网文档[Monitoring and Instrumentation](https://spark.apache.org/docs/latest/monitoring.html#viewing-after-the-fact)

另外，我们也需要一个spark环境来提交编写的程序，所以也需要进行相关配置。

### 配置一个可以提交spark应用的docker环境，称之spark基础镜像

为配置spark client环境，我们需要分别修改`spark-env.sh`和`spark-defaults.conf`两个配置文件。

`spark-env.sh`添加如下配置项目

```
export JAVA_HOME=/opt/jdk-11.0.16
export HADOOP_CONF_DIR=/opt/hadoop-3.3.4/etc/hadoop
# With explicit path to 'hadoop' binary
export SPARK_DIST_CLASSPATH=$(/opt/hadoop-3.3.4/bin/hadoop classpath)
```


`spark-defaults.conf`添加如下配置项目
```
spark.history.fs.logDirectory hdfs://namenode:9000/sparklog/

```


### 构建spark基础镜像

使用如下命令构建基础spark镜像

```
cd spark-hadoop-base
docker build -t spark-hadoop -f .\Dockerfile.hadoop.spark .
```

### 创建spark client容器并挂载本地目录（方便spark-submit本地脚本）

运行spark并保持连接终端的话，暴漏4040端口可以直接从driver查看任务进度

```
docker run --network hadoop --ip 172.32.3.100 -p 222:22 -p 4040:4040 -v d:\\tmp:/host --name spark --hostname spark -it spark-hadoop bash
```
或仅创建容器，并不打开终端
```
docker run --network hadoop --ip 172.32.3.100 -p 222:22 -p 4040:4040 -v d:\\tmp:/host --detach=true --name spark --hostname spark spark-hadoop
```

容器启动后，在容器内运行如下命令，正常获取测试程序结果即说明配置环境完全正常

```
./bin/run-example SparkPi 10
2023-04-04 06:03:14,362 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
2023-04-04 06:03:14,561 INFO spark.SparkContext: Running Spark version 3.3.2
2023-04-04 06:03:14,584 INFO resource.ResourceUtils: ==============================================================
...
Pi is roughly 3.1442391442391444
...
```


### 配置单独的spark history server

这里我们需要分别修改`spark-env.sh`和`spark-defaults.conf`两个配置文件。

`spark-env.sh`添加如下配置项目

```
export JAVA_HOME=/opt/jdk-11.0.16
export HADOOP_CONF_DIR=/opt/hadoop-3.3.4/etc/hadoop
# With explicit path to 'hadoop' binary
export SPARK_DIST_CLASSPATH=$(/opt/hadoop-3.3.4/bin/hadoop classpath)
```


`spark-defaults.conf`添加如下配置项目
```
spark.history.fs.logDirectory hdfs://namenode:9000/sparklog/

```


### 构建spark history server镜像

使用如下命令构建spark history server镜像

```
cd spark-seperate-history-server
docker build -t spark-history -f .\Dockerfile.hadoop.spark.history .
```


### 运行spark history server，并暴漏18080端口

```
docker run --network hadoop --ip 172.32.3.50 -P -p 18080:18080 --name spark-history --hostname spark-history -d spark-history
```
