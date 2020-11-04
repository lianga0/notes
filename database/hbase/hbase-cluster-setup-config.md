HBASE Cluster Setup

> From: https://hbase.apache.org/book.html#_get_started_with_hbase

## Quick Start - Standalone HBase

### 1. Extract hbase bin files

### 2. You must set the `JAVA_HOME` environment variable before starting HBase.

You can edit the `conf/hbase-env.sh` file to set `JAVA_HOME` environment variable before starting HBase.

```
Example extract from hbase-env.sh where JAVA_HOME is set
# Set environment variables here.
# The java implementation to use.
export JAVA_HOME=/usr/jdk64/jdk1.8.0_112
```

### 3. Edit `conf/hbase-site.xml`, which is the main HBase configuration file.

At this time, you need to specify the directory on the local filesystem where HBase and ZooKeeper write data and acknowledge some risks.

Example 1. Example `conf/hbase-site.xml` for Standalone HBase

```
<configuration>
  <property>
          <name>hbase.rootdir</name>
          <value>hdfs://10.206.178.201:9000/drs2hbase</value>
  </property>
  <property>
          <name>hbase.zookeeper.property.dataDir</name>
          <value>/home/hadoop/hbase-2.2.1/data</value>
  </property>
  <property>
          <name>hbase.unsafe.stream.capability.enforce</name>
          <value>false</value>
          <description>
                  Controls whether HBase will check for stream capabilities (hflush/hsync).

                  Disable this if you intend to run on LocalFileSystem, denoted by a rootdir
                  with the 'file://' scheme, but be mindful of the NOTE below.

                  WARNING: Setting this to false blinds you to potential data loss and                                                                                    inconsistent system state in the event of process and/or node failures. If
                  HBase is complaining of an inability to use hsync or hflush it's most                                                                               likely not a false positive.
          </description>
  </property>
</configuration>
```

The `bin/start-hbase.sh` script is provided as a convenient way to start HBase.

 You can use the jps command to verify that you have one running process called HMaster. In standalone mode HBase runs all daemons within this single JVM, i.e. the HMaster, a single HRegionServer, and the ZooKeeper daemon. Go to http://localhost:16010 to view the HBase Web UI.

## Pseudo-Distributed Local Install

Pseudo-distributed mode means that HBase still runs completely on a single host, but each HBase daemon (HMaster, HRegionServer, and ZooKeeper) runs as a separate process: in standalone mode all daemons ran in one jvm process/instance.

Edit the `hbase-site.xml` configuration. First, add the following property which directs HBase to run in distributed mode, with one JVM instance per daemon.

```
<configuration>
  <property>
      <name>hbase.cluster.distributed</name>
      <value>true</value>
  </property>

  <property>
          <name>hbase.rootdir</name>
          <value>hdfs://10.206.178.201:9000/drs2hbase</value>
  </property>
  <property>
          <name>hbase.zookeeper.property.dataDir</name>
          <value>/home/hadoop/hbase-2.2.1/data</value>
  </property>
  <property>
          <name>hbase.unsafe.stream.capability.enforce</name>
          <value>false</value>
          <description>
                  Controls whether HBase will check for stream capabilities (hflush/hsync).

                  Disable this if you intend to run on LocalFileSystem, denoted by a rootdir
                  with the 'file://' scheme, but be mindful of the NOTE below.

                  WARNING: Setting this to false blinds you to potential data loss and                                                                                    inconsistent system state in the event of process and/or node failures. If
                  HBase is complaining of an inability to use hsync or hflush it's most                                                                               likely not a false positive.
          </description>
  </property>
</configuration>
```

### start HBase.

Use the `bin/start-hbase.sh` command to start HBase. If your system is configured correctly, the jps command should show the HMaster and HRegionServer processes running.


### Start and stop a backup HBase Master (HMaster) server.

The HMaster server controls the HBase cluster. You can start up to 9 backup HMaster servers, which makes 10 total HMasters, counting the primary. To start a backup HMaster, use the `local-master-backup.sh`.

### Start and stop additional RegionServers

The HRegionServer manages the data in its StoreFiles as directed by the HMaster. Generally, one HRegionServer runs per node in the cluster. Running multiple HRegionServers on the same system can be useful for testing in pseudo-distributed mode. The `local-regionservers.sh` command allows you to run multiple RegionServers.

## Advanced - Fully Distributed

In reality, you need a fully-distributed configuration to fully test HBase and to use it in real-world scenarios. In a distributed configuration, the cluster contains multiple nodes, each of which runs one or more HBase daemon. These include primary and backup Master instances, multiple ZooKeeper nodes, and multiple RegionServer nodes.

This advanced quickstart adds two more nodes to your cluster. The architecture will be as follows:

Table 1. Distributed Cluster Demo Architecture

|Node Name     | Master | ZooKeeper | RegionServer |
|--------------|--------|-----------|--------------|
|node-a(master)|yes     |yes        |no            |
|node-b(node-1)|backup  |yes        |yes           |
|node-c(node-2)|no      |yes        |yes           |

### 1. Enable Passwordless SSH Access

### 2. Prepare node-a

node-a will run your primary master and ZooKeeper processes, but no RegionServers. Stop the RegionServer from starting on node-a.

#### Edit `conf/regionservers` and remove the line which contains localhost. Add lines with the hostnames or IP addresses for node-b and node-c.

> Even if you did want to run a RegionServer on node-a, you should refer to it by the hostname the other servers would use to communicate with it. In this case, that would be node-a.example.com. This enables you to distribute the configuration to each node of your cluster any hostname conflicts. Save the file.

#### Configure HBase to use node-b as a backup master.

Create a new file in `conf/` called `backup-masters`, and add a new line to it with the hostname for node-b. In this demonstration, the hostname is node-b.example.com.

#### Configure ZooKeeper

In reality, you should carefully consider your ZooKeeper configuration. You can find out more about configuring ZooKeeper in [zookeeper section](https://hbase.apache.org/book.html#zookeeper). This configuration will direct HBase to start and manage a ZooKeeper instance on each node of the cluster.

On node-a, edit conf/hbase-site.xml and add the following properties.

```
<property>
  <name>hbase.zookeeper.quorum</name>
  <value>node-a.example.com,node-b.example.com,node-c.example.com</value>
</property>
<property>
  <name>hbase.zookeeper.property.dataDir</name>
  <value>/home/hadoop/hbase-2.2.1/data</value>
</property>
```

Everywhere in your configuration that you have referred to node-a as localhost, change the reference to point to the hostname that the other nodes will use to refer to node-a. In these examples, the hostname is node-a.example.com.

### 3. Prepare node-b and node-c

node-b will run a backup master server and a ZooKeeper instance.

Each node of your cluster needs to have the same configuration information. Copy the contents of the `conf/` directory to the `conf/` directory on node-b and node-c.


### 4. Start and Test Your Cluster

#### Be sure HBase is not running on any node.

If you forgot to stop HBase from previous testing, you will have errors. Check to see whether HBase is running on any of your nodes by using the `jps` command. Look for the processes `HMaster`, `HRegionServer`, and `HQuorumPeer`. If they exist, kill them.

#### Start the cluster.

On node-a, issue the `start-hbase.sh` command. Your output will be similar to that below.

```
$ bin/start-hbase.sh
node-c.example.com: starting zookeeper, logging to /home/hbuser/hbase-0.98.3-hadoop2/bin/../logs/hbase-hbuser-zookeeper-node-c.example.com.out
node-a.example.com: starting zookeeper, logging to /home/hbuser/hbase-0.98.3-hadoop2/bin/../logs/hbase-hbuser-zookeeper-node-a.example.com.out
node-b.example.com: starting zookeeper, logging to /home/hbuser/hbase-0.98.3-hadoop2/bin/../logs/hbase-hbuser-zookeeper-node-b.example.com.out
starting master, logging to /home/hbuser/hbase-0.98.3-hadoop2/bin/../logs/hbase-hbuser-master-node-a.example.com.out
node-c.example.com: starting regionserver, logging to /home/hbuser/hbase-0.98.3-hadoop2/bin/../logs/hbase-hbuser-regionserver-node-c.example.com.out
node-b.example.com: starting regionserver, logging to /home/hbuser/hbase-0.98.3-hadoop2/bin/../logs/hbase-hbuser-regionserver-node-b.example.com.out
node-b.example.com: starting master, logging to /home/hbuser/hbase-0.98.3-hadoop2/bin/../logs/hbase-hbuser-master-nodeb.example.com.out
```

ZooKeeper starts first, followed by the master, then the RegionServers, and finally the backup masters.

### Verify that the processes are running.

On each node of the cluster, run the jps command and verify that the correct processes are running on each server. You may see additional Java processes running on your servers as well, if they are used for other purposes.

node-a jps Output

```
$ jps
20355 Jps
20071 HQuorumPeer
20137 HMaster
```

node-b jps Output

```
$ jps
15930 HRegionServer
16194 Jps
15838 HQuorumPeer
16010 HMaster
```

node-c jps Output

```
$ jps
13901 Jps
13639 HQuorumPeer
13737 HRegionServer
```

## Hbase thrift-server

Hbase是目前比较火的列存储数据库，由于Hbase是用Java写的，因此它原生地提供了Java接口，对非Java程序人员，怎么办呢？幸好它提供了thrift接口服务器，因此也可以采用其他语言来编写Hbase的客户端。

Apache Thrift 是 Facebook 实现的一种高效的、支持多种编程语言的远程服务调用的框架。Thrift是由Facebook开发的，并在2008年捐给了Apache基金会，成为了一个孵化器项目。

Thrift是一个软件框架，用来进行可扩展且跨语言的服务的开发。它结合了功能强大的软件堆栈和代码生成引擎

Thrift是一个驱动层接口，它提供了用于客户端使用多种语言实现的API。

### 1.启动thrift-server

要使用Hbase的thrift接口，必须将它的服务启动，启动Hbase的thrift-server进程如下：

```
$ cd hbase
$ ./bin/hbase-daemon.sh start thrift
# 执行jps命令检查：
$ jps
20651 ThriftServer
```

thrift默认端口是9090，启动成功后可以查看端口是否起来。

```
$ lsof -i:9090
COMMAND   PID   USER   FD   TYPE  DEVICE SIZE/OFF NODE NAME
java    20651 hadoop  443u  IPv6 1296675      0t0  TCP *:9090 (LISTEN)
```

### 

Reference: 

[Hbase thrift-server](https://www.jianshu.com/p/93e36d008313)

[HBase默认端口使用说明](http://www.fish2bird.com/?p=275)

