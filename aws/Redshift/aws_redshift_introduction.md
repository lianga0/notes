## Redshitf集群的限制及特性

1. Amazon Redshift 默认使用端口 5439，创建了 Amazon Redshift 集群后，则不能再更改其端口号。通过此开放端口，可以从 SQL 客户端工具连接到集群并运行查询。

2. Amazon Redshift 中调整集群大小

- **弹性调整大小** – 使用弹性调整大小来更改节点的数量。如果更改节点数，则查询将暂时暂停，如果可能，连接保持打开状态。在调整大小操作期间，集群是只读的。通常情况下，弹性调整大小需要 10 – 15 分钟。我们建议尽可能使用弹性调整大小。

- **经典调整大小** – 使用经典调整大小以更改节点类型和/或节点数量。当您将大小调整为无法通过弹性调整大小实现的配置时，请选择此选项。一个示例是进/出单节点集群。在调整大小操作期间，集群是只读的。通常情况下，经典调整大小需要 2 小时 – 2 天，具体取决于您的数据大小。

- **快照、还原以及调整大小** – 要使集群在经典调整大小期间可用，可以先创建现有集群的副本，然后调整新集群的大小。

3. 重命名集群

如果您希望集群使用其他名称，则可以对其进行重命名。由于连接到集群的终端节点包含集群名称（也称集群标识符），因此重命名集群之后，终端节点也会改为使用新名称。


## Data redistribution

When you load data into a table, Amazon Redshift distributes the table's rows to the compute nodes and slices according to the distribution style that you chose when you created the table. Data distribution has two primary goals:

- To distribute the workload uniformly among the nodes in the cluster. Uneven distribution, or data distribution skew, forces some nodes to do more work than others, which impairs query performance.

- To minimize data movement during query execution. If the rows that participate in joins or aggregates are already collocated on the nodes with their joining rows in other tables, the optimizer does not need to redistribute as much data during query execution.

The distribution strategy that you choose for your database has important consequences for query performance, storage requirements, data loading, and maintenance. By choosing the best distribution style for each table, you can balance your data distribution and significantly improve overall system performance.

Reference： https://docs.aws.amazon.com/redshift/latest/dg/t_Distributing_data.html


## Choosing Sort Keys

When you create a table, you can define one or more of its columns as sort keys. When data is initially loaded into the empty table, the rows are stored on disk in sorted order. Information about sort key columns is passed to the query planner, and the planner uses this information to construct plans that exploit the way that the data is sorted.

To define a sort type, use either the INTERLEAVED or COMPOUND keyword with your CREATE TABLE or CREATE TABLE AS statement. The default is COMPOUND. An INTERLEAVED sort key can use a **maximum of eight columns**.


## 价格

dc2.large	2	15 GiB	0.16TB SSD	0.6 GB/秒	每小时 0.25 USD
dc2.large	2	15 GiB	0.16TB SSD	0.6 GB/秒	每小时 0.33 USD   0.33*24*30 = 237.6/month


FP2.0纯文本log最高可以达到1:8的压缩比（GZ），但Redshift压缩率远远到不了这个程度。

## Others


[Amazon Redshift 的新用户阅读顺序](https://docs.aws.amazon.com/zh_cn/redshift/latest/dg/c-first-time-user.html)


1. [Amazon Redshift 管理概览](https://docs.aws.amazon.com/zh_cn/redshift/latest/mgmt/overview.html)

简要介绍 Amazon Redshift。



2. [Amazon Redshift 入门](https://docs.aws.amazon.com/zh_cn/redshift/latest/gsg/getting-started.html)

   包含一个示例，引导您完成创建 Amazon Redshift 数据仓库集群、创建数据库表、上传数据和测试查询的过程。
   

3. [Amazon Redshift Cluster Management Guide](https://docs.aws.amazon.com/zh_cn/redshift/latest/mgmt/welcome.html)


Reference:

[在生产中结合使用 Amazon Redshift Spectrum、Amazon Athena 和 AWS Glue 与 Node.js](https://aws.amazon.com/cn/blogs/china/big-data-using-amazon-redshift-spectrum-amazon-athena-and-aws-glue-with-node-js-in-production/)


[How is AWS Redshift Spectrum different than AWS Athena?](https://blog.openbridge.com/how-is-aws-redshift-spectrum-different-than-aws-athena-9baa2566034b)

