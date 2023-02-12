# spark history server 搭建

> 2023.02.12

> https://spark.apache.org/docs/latest/monitoring.html#viewing-after-the-fact


每一个Spark应用都是一个SparkContext实例，每个SparkContext默认会启用一个Web页面，默认端口号4040，用于显示Spark应用运行的一些状态信息。

你可以使用浏览器访问此web页面，页面默认URL为`http://<driver-node>:4040`，如果driver节点上有多个SparkContext在运行，那么他们绑定的端口号依次递增，即4040（4041，4042等等）。

注意，driver节点上SparkContext实例启用的Web页面仅在Spark应用运行期间可以访问。如果想在Spark应用运行结束后，仍然可以查看此页面的内容，则需要在Spark应用运行前将`spark.eventLog.enabled`配置项值设置为`true`。这个配置项控制Spark将应用运行时显示在Web UI中的事件信息存在持久化的存储上（以供Spark history server读取显示使用）。

> Every SparkContext launches a Web UI, by default on port 4040, that displays useful information about the application. This includes:

- A list of scheduler stages and tasks
- A summary of RDD sizes and memory usage
- Environmental information.
I- nformation about the running executors

> You can access this interface by simply opening `http://<driver-node>:4040` in a web browser. If multiple SparkContexts are running on the same host, they will bind to successive ports beginning with 4040 (4041, 4042, etc).

> Note that this information is only available for the duration of the application by default. To view the web UI after the fact, set spark.eventLog.enabled to true before starting the application. This configures Spark to log Spark events that encode the information displayed in the UI to persisted storage.

## 事后查看（Viewing After the Fact）

Spark应用存储的运行事件日志，可以使用Spark history server来重新解析显示Saprk应用运行状态的Web页面。可以使用下面命令启动Spark history server服务，需要配置要显示Spark应用事件日志所在路径，配置项名称为`spark.history.fs.logDirectory`，该配置项的值可以是Linux本地文件系统路径，也可以是Hadoop文件系统路径。Spark history server服务启动后，默认Web页面访问URL为`http://<server-url>:18080`。

Spark应用提交时使用如下两个配置项指定启用日志，并将日志存储在指定位置。

```
spark.eventLog.enabled true
spark.eventLog.dir file:///tmp/spark-events
```

一般来说，当仅有一个spark history server时，spark应用存储事件日志的路径应当和spark history server配置的日志读取路径一致。即Spark应用的配置项`spark.eventLog.dir`的值应当与Spark history server配置项`spark.history.fs.logDirectory`的值相同。不然spark history server是找不到spark应用存储的事件日志信息，自然也无法解析显示。

> 注意：上述三个配置项目均位于Spark的`spark-defaults.conf`配置文件内。

It is still possible to construct the UI of an application through Spark’s history server, provided that the application’s event logs exist. You can start the history server by executing:

```
./sbin/start-history-server.sh
```

This creates a web interface at `http://<server-url>:18080` by default, listing incomplete and completed applications and attempts.

When using the file-system provider class (see spark.history.provider below), the base logging directory must be supplied in the `spark.history.fs.logDirectory` configuration option, and should contain sub-directories that each represents an application’s event logs.

The spark jobs themselves must be configured to log events, and to log them to the same shared, writable directory. For example, if the server was configured with a log directory of `hdfs://namenode/shared/spark-logs`, then the client-side options would be:

```
spark.eventLog.enabled true
spark.eventLog.dir hdfs://namenode/shared/spark-logs
```

## 本地单线程运行Spark应用配置举例

Spark应用配置项

```
spark.eventLog.enabled true
spark.eventLog.dir file:///tmp/spark-events
spark.eventLog.compress true
```

Saprk history server配置项

```
spark.history.fs.logDirectory file:///tmp/spark-events
```


## 集群模式Spark应用配置举例

Spark应用配置项

```
spark.eventLog.enabled true
spark.eventLog.dir hdfs://namenode/shared/spark-logs
spark.eventLog.compress true
```

Saprk history server配置项

```
spark.history.fs.logDirectory hdfs://namenode/shared/spark-logs
```

注意：需要确保Hadoop集群中存在`/shared/spark-logs`目录，并且Spark拥有正确的访问权限。


## Spark on yarn应用配置举例

Spark应用配置项

```
spark.eventLog.enabled true
spark.eventLog.dir hdfs://namenode/shared/spark-logs
spark.eventLog.compress true
spark.yarn.historyServer.address spark-history-server:18080
```

Saprk history server配置项

```
spark.history.fs.logDirectory hdfs://namenode/shared/spark-logs
```

注意：需要确保Hadoop集群中存在`/shared/spark-logs`目录，并且Spark拥有正确的访问权限。


其中多出来的`spark.yarn.historyServer.address`允许用户从Yara的Application页面中的`Tracking URL:`直接跳转到Spark History Server的Web页面。更详细信息请参考文档[Running Spark on YARN](https://spark.apache.org/docs/latest/running-on-yarn.html)。


更多可以参考文档 [Monitoring and Instrumentation
](https://spark.apache.org/docs/latest/monitoring.html#viewing-after-the-fact)和[Enabling the Spark History service
](https://www.ibm.com/docs/en/pasc/1.1.1?topic=ego-enabling-spark-history-service)