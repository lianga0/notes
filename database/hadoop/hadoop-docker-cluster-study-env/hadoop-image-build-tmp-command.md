# 这里的配置项仅包含每个服务可以启动的最基本的最小配置

容器启动后，需要手动启动不同的Hadoop服务组件

构建镜像是依赖的Hadoop文件名和Java文件名如下，需要自己手动下载并放到当前目录下。

```
hadoop-3.3.4.tar.gz
jdk-11.0.16_linux-x64_bin.tar.gz
```

## 创建虚拟机网络

```
docker network create --driver=bridge --subnet=172.32.3.0/16  --ip-range=172.32.3.0/24 --gateway=172.32.3.254 hadoop
```


## 构建镜像

```
docker build -t namenode . -f Dockerfile.namenode
docker build -t secondarynamenode . -f Dockerfile.secondarynamenode
docker build -t datanode . -f Dockerfile.datanode
docker build -t resourcemanager . -f Dockerfile.resourcemanager
docker build -t nodemanager . -f Dockerfile.nodemanager
docker build -t jobhistory . -f Dockerfile.jobhistory
```


## 1. 启动namenode节点
```
docker run  --network hadoop --ip 172.32.3.10 --name namenode --hostname namenode -it namenode bash
```
##### docker run --name namenode --hostname namenode -it namenode bash

##### 在容器中启动namenode服务
```
cd /opt/hadoop-3.3.4/ && bin/hdfs --daemon start namenode
```

## 2. 启动secondarynamenode节点
```
docker run  --network hadoop --ip 172.32.3.21 --name secondarynamenode --hostname secondarynamenode -it secondarynamenode bash
```
##### 在容器中启动secondarynamenode服务
cd /opt/hadoop-3.3.4/ && bin/hdfs --daemon start secondarynamenode



## 3. 启动datanode节点
```
docker run  --network hadoop --ip 172.32.3.11 --name datanode1 --hostname datanode1 -it datanode bash
docker run  --network hadoop --ip 172.32.3.12 --name datanode2 --hostname datanode2 -it datanode bash
docker run  --network hadoop --ip 172.32.3.13 --name datanode3 --hostname datanode3 -it datanode bash
```
##### docker run --name datanode1 --hostname datanode1 -it datanode bash

##### 在容器中启动datanode服务
```
cd /opt/hadoop-3.3.4/ && bin/hdfs --daemon start datanode
```



## 4. 启动resourcemanager节点
```
docker run  --network hadoop --ip 172.32.3.15 --name resourcemanager --hostname resourcemanager -it resourcemanager bash
```

#####docker run --name resourcemanager --hostname resourcemanager -it resourcemanager bash

##### 在容器中启动resourcemanager服务
```
cd /opt/hadoop-3.3.4/ && bin/yarn --daemon start resourcemanager
```



## 5. 启动nodemanager节点
```
docker run  --network hadoop --ip 172.32.3.16 --name nodemanager1 --hostname nodemanager1 -it nodemanager bash
```
##### docker run --name nodemanager1 --hostname nodemanager1 -it nodemanager bash

##### 在容器中启动nodemanager服务
```
cd /opt/hadoop-3.3.4/ && bin/yarn --daemon start nodemanager
```



## 6. 启动jobhistory节点
```
docker run  --network hadoop --ip 172.32.3.20 --name jobhistory --hostname jobhistory -it jobhistory bash
```
##### 在容器中启动jobhistory服务
```
cd /opt/hadoop-3.3.4/ && bin/mapred --daemon start historyserver
```



# 关于Hadoop不同服务组件依赖配置项多少的问题

其实配置文件不用过分纠结，虽然有些配置项目仅对特定服务生效，但仍然可以合并一个大的配置文件，Hadoop组件允许无用的配置项存在。

例如，namenode自然不需要`datanode`的`dfs.datanode.data.dir`配置项，但是配置文件中存在该冗余项也不会出错。

总的来说，多总比少好，比如jobhistory服务不配置`fs.defaultFS`也可以启动，但你并不能看到历史任务，因为jobhistory没有可用信息来找到hdfs上汇聚的日志。



## 查看namenode节点状态网页

http://namenode:9870/dfshealth.html#tab-overview
## 查看secondarynamenode节点状态网页
http://secondarynamenode:9868/status.html
## 查看datanode节点状态网页
http://datanode1:9864/datanode.html
## 查看resourcemanager节点状态网页
http://resourcemanager:8088/cluster
## 查看nodemanager节点状态网页
http://nodemanager1:8042/node
## 查看yarn jobhistory节点状态网页
http://jobhistory:19888/jobhistory
