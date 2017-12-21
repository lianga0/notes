### 适用于redis-py-cluster集群的Python client

目前redis官网推荐的 redis python client 为 `redis-py`。Ubuntu可以使用`sudo pip install redis`命令安装`redis-py`库，但是它目前并不支持 redis 集群的操作。

当Redis集群包含多个partition的时候，使用`redis-py`访问集群会出现如下异常。

```
Traceback (most recent call last):
  File "elasticache_t.py", line 9, in <module>
    redis_inst.set(i,i)
  File "/usr/local/lib/python2.7/dist-packages/redis/client.py", line 1055, in set
    return self.execute_command('SET', *pieces)
  File "/usr/local/lib/python2.7/dist-packages/redis/client.py", line 565, in execute_command
    return self.parse_response(connection, command_name, **options)
  File "/usr/local/lib/python2.7/dist-packages/redis/client.py", line 577, in parse_response
    response = connection.read_response()
  File "/usr/local/lib/python2.7/dist-packages/redis/connection.py", line 574, in read_response
    raise response
redis.exceptions.ResponseError: MOVED 14088 172.31.6.121:6379
```

##### redis-py-cluster

redis-py-cluster is a Cluster library for redis 3.0.0 built on top of redis-py lib. 

在Ubuntu中可以使用`pip install redis-py-cluster`命令安装redis-py-cluster库。redis-py-cluster库是基于`redis-py`的，支持连接池。

##### redis-py版本不匹配问题

安装完成后，运行如下样例代码，报错：`raise RedisClusterException("ERROR sending 'cluster slots' command to redis server: {0}".format(node))`。

```
from rediscluster import StrictRedisCluster

# Requires at least one node for cluster discovery. Multiple nodes is recommended.
startup_nodes = [{"host": "127.0.0.1", "port": "7000"}]

# Note: See note on Python 3 for decode_responses behaviour
rc = StrictRedisCluster(startup_nodes=startup_nodes, decode_responses=True)
```

百度发现，[网上有人碰到相同问题](http://blog.csdn.net/zt3032/article/details/77542797)。原因是，redis-py-cluster依赖redis-py，而系统同目前安装的redis-py版本较低。使用`sudo pip install -U redis`命令更新到最新版本的redis-py，运行就不再出现上述错误。

##### redis server屏蔽部分命令问题

但是在我的环境中又出现如下一个错误

```
ResponseError: unknown command 'CONFIG'
```

一翻搜索后，[redis-py-cluster一坑记录](http://mili-yini.blogspot.com/2017/01/redis-py-cluster.html)，发现原因是：redis server可以选择屏蔽一些命令的，需要设置参数`skip_full_coverage_check=True`来阻止redis-py-cluster运行`CONFIG`命令。

```
If your redis instance is configured to not have the `CONFIG ...` comannds enabled due to security reasons you need to pass this into the client object `skip_full_coverage_check=True`. Benefits is that the client class no longer requires the `CONFIG ...` commands to be enabled on the server. Downsides is that you can't use the option in your redis server and still use the same feature in this client.
```

##### redis-py-cluster连接池最大连接数设置问题

修完上述两个问题后，代码终于欢快的跑起来了。接下就是想调大并发数，测试下redis server的吞吐量，然后又碰到下面的错误信息。

```
rediscluster.exceptions.RedisClusterException: Too many Cluster redirections
```

找来找去没找到redis-py-cluster连接池或多线程相关的解释。最后一看代码，原来redis-py-cluster使用redis-py，也使用了线程池。构造函数有如下一系列参数，改为自己想要的值，程序终于顺畅的跑起来了。

```
    def __init__(self, host=None, port=None, startup_nodes=None, max_connections=32, max_connections_per_node=False, init_slot_cache=True,
                 readonly_mode=False, reinitialize_steps=None, skip_full_coverage_check=False, nodemanager_follow_cluster=False, **kwargs):
        """
        :startup_nodes:
            List of nodes that initial bootstrapping can be done from
        :host:
            Can be used to point to a startup node
        :port:
            Can be used to point to a startup node
        :max_connections:
            Maximum number of connections that should be kept open at one time
        :readonly_mode:
            enable READONLY mode. You can read possibly stale data from slave.
        :skip_full_coverage_check:
            Skips the check of cluster-require-full-coverage config, useful for clusters
            without the CONFIG command (like aws)
        :nodemanager_follow_cluster:
            The node manager will during initialization try the last set of nodes that
            it was operating on. This will allow the client to drift along side the cluster
            if the cluster nodes move around alot.
        :**kwargs:
            Extra arguments that will be sent into StrictRedis instance when created
            (See Official redis-py doc for supported kwargs
            [https://github.com/andymccurdy/redis-py/blob/master/redis/client.py])
            Some kwargs is not supported and will raise RedisClusterException
            - db (Redis do not support database SELECT in cluster mode)
        """
        ...........

```


Reference: 

[python之redis-cluster](http://blog.csdn.net/zt3032/article/details/77542797)

[redis-py-cluster一坑记录](http://mili-yini.blogspot.com/2017/01/redis-py-cluster.html)



