## ECU(EC2 Compute Unit)

ECU的全称是EC2 Compute Unit的缩写，也就是EC2计算单元的意思。

[one ECU provides the equivalent CPU capacity of a 1.0-1.2 GHz 2007 Opteron or 2007 Xeon processor](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts_micro_instances.html)

由于EC2本身的历史很长，各个时期采购的机器配置也不一样，

AWS为了让不同时期的机器也有一个比较统一的计算能力标准，提出了这么一个概念。

1个ECU大概相当于 2007年的1GHz Xeon处理器的性能。

这样，比较新的单个CPU超线程的ECU值就高于老CPU的ECU值。

### vCPU

在2014年4月，AWS提出了vCPU的概念来替换ECU。

简单来理解，一个vCPU指的是一个CPU超线程。

这个vCPU更容易被已经熟悉了vmWare中的vCPU概念的用户所接受。

https://aws.amazon.com/cn/ec2/instance-types/ 里的实例规格信息也已不见了ECU的踪影。


From: [EC2的vCPU与ECU的区别](https://blog.csdn.net/aws0to1/article/details/48055637)