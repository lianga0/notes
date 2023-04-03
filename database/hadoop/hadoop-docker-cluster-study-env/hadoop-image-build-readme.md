# zip资源用途

`hadoop-docker-build-deploy-all-res.zip` 解压后，可以直接使用目录下`bat`或`sh`脚本完成Hadoop image的构建和部署，可以获得一个完全分布式的docker测试环境。

> 注意：需要自己下载替换zip文件中的`jdk-11.0.16_linux-x64_bin.tar.gz`和`hadoop-3.3.4.tar.gz`空文件。

`hadoop-config-separately.zip`包含早期不同组件最小配置的测试Hadoop集群配置文件，无构建脚本，且Hadoop服务需要自己进入容器内分别逐个进行启动。



# Hadoop网页默认URL


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


Windows中可以使用Firefox容器来查看上述页面，启动命令如下：

```
docker run --network hadoop --ip 172.32.3.200 -d --name=firefox -p 5800:5800 -v d:\\tmp\firefox:/config:rw --shm-size=512m --hostname firefox wellsen/firefox

```


# 关于Hadoop不同服务组件依赖配置项多少的问题

其实配置文件不用过分纠结，虽然有些配置项目仅对特定服务生效，但仍然可以合并一个大的配置文件，Hadoop组件允许无用的配置项存在。

例如，namenode自然不需要`datanode`的`dfs.datanode.data.dir`配置项，但是配置文件中存在该冗余项也不会出错。

总的来说，多总比少好，比如jobhistory服务不配置`fs.defaultFS`也可以启动，但你并不能看到历史任务，因为jobhistory没有可用信息来找到hdfs上汇聚的日志。


## 删除所有容器命令

```
docker rm $(docker ps -a -q)
```


## 移除所有悬空的镜像命令

```
docker image prune -f
```
