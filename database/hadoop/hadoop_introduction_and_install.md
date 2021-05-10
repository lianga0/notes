
# Hadoop 基础

## 安装模式简介

Hadoop粗略的可以分为三种部署模式：单机模式（Standalone Operation）、伪分布模式（Pseudo-Distributed Operation）、完全分布模式（Fully-Distributed Operation）

### 单机模式（Standalone Operation）

单机模式也叫本地模式，只适用于本地的开发调试，或快速安装体验hadoop，本地模式的安装比较简单，下载完hadoop安装包就可以直接运行。

>  Standalone mode is the default mode of operation of Hadoop and it runs on a single node ( a node is your machine). HDFS and YARN doesn't run on standalone mode.
> 
> Reference: [Setting up Hadoop -MapReduce, HDFS and YARN. Standalone and pseudo-distributed mode.](https://medium.com/@nidhinmahesh/getting-started-hadoop-mapreduce-hdfs-and-yarn-configuration-and-sample-program-febb1415f945)

本地模式不运行HDFS，采用本地文件系统来运行MapReduce程序。[官网样例命令](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html)解释如下：

```
$ bin/hadoop jar share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar grep input output 'dfs[a-z.]+'

bin/hadoop                                                    这是一个hadoop命令
jar                                                           这个命令在jar包内
share/hadoop/mapreduce/hadoop-mapreduce-examples-3.2.1.jar    jar包的具体位置
grep                                                          调用的函数名
input                                                         计算统计的文件来源自本地input文件夹
output                                                        计算结果输出到本地output文件夹
'dfs[a-z.]+'                                                  匹配的正则表达式
```

> Single Node (Local Mode or Standalone Mode)
> 
> Standalone mode is the default mode in which Hadoop run. Standalone mode is mainly used for > debugging where you don’t really use HDFS.
> 
> You can use input and output both as a local file system in standalone mode.
> 
> You also don’t need to do any custom configuration in the files- mapred-site.xml, core-site.xml, > hdfs-site.xml.
> 
> Standalone mode is usually the fastest Hadoop modes as it uses the local file system for all the > input and output.
> 
> Pseudo-distributed Mode
> 
> The pseudo-distributed mode is also known as a single-node cluster where both NameNode and > DataNode will reside on the same machine.
> 
> In pseudo-distributed mode, all the Hadoop daemons will be running on a single node. Such > configuration is mainly used while testing when we don’t need to think about the resources and > other users sharing the resource.
> 
> In this architecture, a separate JVM is spawned for every Hadoop components as they could > communicate across network sockets, effectively producing a fully functioning and optimized > mini-cluster on a single host.
> 
> So, in case of this mode, changes in configuration files will be required for all the three > files- mapred-site.xml, core-site.xml, hdfs-site.xml.
> 
> Reference: [Difference between single node & pseudo-distributed mode in Hadoop?](https://www.edureka.co/community/3444/difference-between-single-pseudo-distributed-mode-hadoop)

### 伪分布模式（Pseudo-Distributed Operation）

Hadoop can also be run on a single-node in a pseudo-distributed mode where each Hadoop daemon runs in a separate Java process.

Pseudo-Distributed mode stands between the standalone mode and fully distributed mode on a production level cluster. It is used to simulate the actual cluster. It gives you a fully-fledged test environment. HDFS is used for storage using some portion of your disk space and YARN needs to run to manage resources on this Hadoop installation.

### 完全分布模式（Fully-Distributed Operation）

Full Distributed runs on cluster of machines.

**Hadoop生成环境安装，推荐使用NameNode HA With QJM。**

> Using multiple NameNodes with a [distributed edit log](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HDFSHighAvailabilityWithQJM.html) (called Journal) in High Availability cluster is the recommended approach.

详细安装及架构信息可以参考Hadoop官方文档：

[HDFS Architecture](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HdfsDesign.html)

# Hadoop Fully-Distributed 配置

## 0. 配置SSH免密码登入 ssh trusted access configure

Setup `hadoop` user on each server, and enable SSH login through the same SSK key.

## 1. HADOOP_HOME

It is also traditional to configure HADOOP_HOME in the system-wide shell environment configuration. For example, a simple script inside /etc/profile.d:

```
HADOOP_HOME=/path/to/hadoop
export HADOOP_HOME
```

## 2. etc/hadoop/hadoop-env.sh

> The java implementation to use. By default, this environment
> variable is REQUIRED on ALL platforms except OS X!

```
export JAVA_HOME=/home/hadoop/jdk1.8.0_231
```

> Location of Hadoop.  By default, Hadoop will attempt to determine
> this location based upon its execution path.

```
export HADOOP_HOME=/home/hadoop/hadoop-3.2.1
```

## 3. Configuring the Hadoop Daemons


### etc/hadoop/core-site.xml

```
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://10.206.178.201:9000</value>
    </property>
    <property>
        <name>io.file.buffer.size</name>
        <value>131072</value>
    </property>
        <name>hadoop.tmp.dir</name>
        <value>file:/home/hadoop/tmp</value>
    </property>
    </property>
        <name>hadoop.http.staticuser.user</name>
        <value>hadoop</value>
    </property>
</configuration>
```


### etc/hadoop/hdfs-site.xml

for namenode

```
<configuration>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>/home/hadoop/hadoop-3.2.1/name_node_space</value>
    </property>
    <property>
        <name>dfs.blocksize</name>
        <value>268435456</value>
    </property>
    <property>
        <name>dfs.namenode.handler.count</name>
        <value>100</value>
    </property>
</configuration>
```


for datanode

```
<configuration>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>/home/hadoop/hadoop_data</value>
    </property>
    <property>
        <name>dfs.replication</name>
        <value>2</value>
    </property>
</configuration>

```

namenode and datanode can use the same `hdfs-site.xml` config file.

### Slaves File

etc/hadoop/workers

```
10.206.178.150
10.206.178.151
```

配置完上述配置后，可以使用`$HADOOP_HOME/sbin/start-dfs.sh`命令在NameNode上启动Hadoop dfs 服务。

使用`$HADOOP_HOME/sbin/stop-dfs.sh`命令在NameNode上停止Hadoop dfs 服务。


> Reference：Hadoop The Definitive Guide - Chapter 10: Setting Up a Hadoop Cluster 290页 Starting and Stopping the Daemons 章节：

>> Hadoop comes with scripts for running commands and starting and stopping daemons across the whole cluster. To use these scripts (which can be found in the sbin directory), you need to tell Hadoop which machines are in the cluster. There is a file for this purpose, called `slaves`, which contains a list of the machine hostnames or IP addresses, one per line. The slaves file lists the machines that the datanodes and node managers should run on. It resides in Hadoop’s configuration directory, although it may be placed elsewhere (and given another name) by changing the `HADOOP_SLAVES` setting in `hadoop-env.sh`. Also, this file does not need to be distributed to worker nodes, since they are used only by the control scripts running on the namenode or resource manager.

