# CDH的介绍

> 2022.02.10

hadoop是一个开源项目，所以很多公司在这个基础进行商业化，Cloudera对hadoop做了相应的改变。

Cloudera最早的定位在于 Bringing Big Data to the Enterprise with Hadoop

Cloudera为了让Hadoop的配置标准化，可以帮助企业安装，配置，运行hadoop以达到大规模企业数据的处理和分析。

Cloudera's Distribution, including Apache Hadoop（CDH）：

是Hadoop众多分支中的一种，由Cloudera维护，基于稳定版本的Apache Hadoop构建

CDH是Cloudera的100％开放源代码平台发行版，包括Apache Hadoop，是专门为满足企业需求而构建的。

CDH可立即提供企业使用所需的一切。通过将Hadoop与十几个其他关键的开源项目集成在一起，Cloudera创建了功能先进的系统，可以帮助您执行端到端的大数据工作流程。


## 为什么需要CDH？

大致提出一个问题，假如公司要求给500台机器，进行安装hadoop集群。

只给你一天时间，完成以上工作。

或者如果对于以上集群进行hadoop版本升级，你会选择什么升级方案，最少要花费多长时间？

你在过程中会大大考虑新版本的Hadoop，与Hive、Hbase、Flume、Kafka、Spark等等兼容？

集群的版本限制很重要。

CDH 6 Download Information:
https://docs.cloudera.com/documentation/enterprise/6/release-notes/topics/rg_cdh_6_download.html


## [最后CDH已经过时了](https://www.cloudera.com/legal/policies/support-lifecycle-policy.html)

熟悉大数据业界的小伙伴们都知道，Cloudera 在跟HortonWorks 合并后，便推出了新一代大数据平台 CDP，并正在逐步停止原有的大数据平台 CDH 和 HDP。

For eligible customers, Limited Support for CDH versions 6.2 and 6.3 and HDP version 3.1 will be provided during the six-month period (i)starting on January 1, 2022, and ending on June 30, 2022, for HDP products and (ii) beginning on April 1, 2022, and ending on September 30, 2022, for CDH products See the terms associated with this Limited Support offering.

比如可以参考[从CDH升级到CDP私有云之路](https://www.jianshu.com/p/b9ec402c8a31)研究如何无缝升级，以继续使用本地得环境。

Reference: [CDH是什么？](https://blog.csdn.net/qq_41946557/article/details/103011675)

[Support lifecycle policy](https://www.cloudera.com/legal/policies/support-lifecycle-policy.html)

[从CDH升级到CDP私有云之路](https://www.jianshu.com/p/b9ec402c8a31)
