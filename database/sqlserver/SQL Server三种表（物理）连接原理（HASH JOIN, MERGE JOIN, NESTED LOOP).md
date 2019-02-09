## SQL Server三种表（物理）连接原理（HASH JOIN, MERGE JOIN, NESTED LOOP)

> 2019.02.09

在SQL Server数据库中，查询优化器在处理表连接时，通常会使用一下三种连接方式：

- 嵌套循环连接（Nested Loop Join）
- 合并连接 （Merge Join）
- Hash连接 （Hash Join）

充分理解这三种表连接工作原理，可以使我们在优化SQL Server连接方面的代码有据可依，为开展优化工作提供一定的思路。接下来我们来认识下这三种连接。

### 1. 嵌套循环连接（Nested Loop Join）

该连接方式通常在小数据量并且语句比较简单的场景中使用，循环嵌套连接是最基本的连接，正如其名所示那样，需要进行循环嵌套，嵌套循环是三种方式中唯一支持不等式连接的方式，这种连接方式的过程可以简单的用下图展示:

<img src="imgs/1.Nested Loop Join step1.png" alt="图1.循环嵌套连接的第一步">

<img src="imgs/1.Nested Loop Join step1.png" alt="图2.循环嵌套连接的第二步">

由上面两个图不难看出，循环嵌套连接查找内部循环表的次数等于外部循环的行数，当外部循环没有更多的行时，循环嵌套结束。另外，还可以看出，这种连接方式需要内部循环的表有序（也就是有索引），并且外部循环表的行数要小于内部循环的行数，否则查询分析器就更倾向于Hash Join(会在本文后面讲到)。

当外部表较小，而内部表较大并且连接字段上有索引的情况下，循环嵌套非常高效。并且嵌套循环是三种方式中唯一支持不等式连接的方式。

### 2. 合并连接(Merge Join)

在SQL Server数据库中，如果查询优化器，发现要连接的两张对象表，在连接列上都已经排序并包含索引，那么优化器将会极大可能选择“合并”连接策略。条件是：两个表都是排序的，并且表连接条件中至少有一个等号连接，查询分析器会去选择合并连接。

Merge Join的过程我们可以简单用下面图进行描述:


<img src="imgs/3.Merge Join step1.png" alt="Merge Join第一步">

<img src="imgs/4.Merge Join step2.png" alt="更小值的输入集合向下进1">

因此，通常来说Merge Join如果输入两端有序，则Merge Join效率会非常高，但是如果需要使用显式Sort来保证有序实现Merge Join的话，那么Hash Join将会是效率更高的选择。但是也有一种例外，那就是查询中存在order by,group by,distinct等可能导致查询分析器不得不进行显式排序，那么对于查询分析器来说，反正都已经进行显式Sort了,何不一石二鸟的直接利用 Sort后的结果进行成本更小的MERGE JOIN？在这种情况下，Merge Join将会是更好的选择。

> 有关表排序的问题，如果连接语句中使用Sort关键字来排序数据表，那么SQL Server的优化器会比较倾向于Hash Join。在合并连接中，并不排斥order by, group by, distinct等关键字，在使用这些语句时，查询优化器也有极大的可能选择合并连接。

当我们使用一些查询限定条件，比如不等式（>,<,>=等）限定条件范围，那么合并连接的效率会有更好。

### 3. 哈希匹配(Hash Join)

哈希匹配连接相对前面两种方式更加复杂一些，但是哈希匹配对于大量数据，并且无序的情况下性能均好于Merge Join和Loop Join。对于连接列没有排序的情况下(也就是没有索引)，查询分析器会倾向于使用Hash Join。

哈希匹配分为两个阶段,分别为生成和探测阶段，首先是生成阶段，第一阶段生成阶段具体的过程可以如下图所示。

<img src="imgs/5.Hash Join step1.png" alt="哈希匹配的第一阶段">

上图中，将输入源中的每一个条目经过散列函数的计算都放到不同的Hash Bucket中，其中Hash Function的选择和Hash Bucket的数量都是黑盒，微软并没有公布具体的算法，但我相信已经是非常好的算法了。另外在Hash Bucket之内的条目是无序的。通常来讲，查询优化器都会使用连接两端中比较小的那个输入集来作为第一阶段的输入源。

接下来是探测阶段，对于另一个输入集合，同样针对每一行进行散列函数，确定其所应在的Hash Bucket,在针对这行和对应Hash Bucket中的每一行进行匹配，如果匹配则返回对应的行。

通过了解哈希匹配的原理不难看出，哈希匹配涉及到散列函数，所以对CPU的消耗会非常高，此外，在Hash Bucket中的行是无序的，所以输出结果也是无序的。

上面的情况都是内存可以容纳下生成阶段所需的内存，如果内存吃紧，则还会涉及到Grace哈希匹配和递归哈希匹配，这就可能会用到TempDB从而吃掉大量的IO。这里就不细说了,有兴趣的同学可以参考微软帮助文档。

### 总结
下面我们通过一个表格简单总结这几种连接方式的消耗和使用场景:

<table style="border-collapse: collapse; padding: 0px; width: 1017px; border: 1px solid #bbbbbb; color: #000000; font-size: 13px; line-height: 17px; text-align: start;"> 
 <tbody> 
  <tr> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;">&nbsp;</td> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">嵌套循环连接</p> </td> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">合并连接</p> </td> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">哈希连接</p> </td> 
  </tr> 
  <tr> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">适用场景</p> </td> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">外层循环小，内存循环条件列有序</p> </td> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">输入两端都有序</p> </td> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">数据量大，且没有索引</p> </td> 
  </tr> 
  <tr> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">CPU</p> </td> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">低</p> </td> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">低（如果没有显式排序）</p> </td> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">高</p> </td> 
  </tr> 
  <tr> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">内存</p> </td> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">低</p> </td> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">低（如果没有显式排序）</p> </td> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">高</p> </td> 
  </tr> 
  <tr> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">IO</p> </td> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">可能高可能低</p> </td> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">低</p> </td> 
   <td style="border: 1px solid #bbbbbb; margin: 10px; padding: 10px 8px; color: #2a2a2a; vertical-align: top;"> <p style="margin-top: 0px; margin-bottom: 0px; line-height: 18px;">可能高可能低</p> </td> 
  </tr> 
 </tbody> 
</table>

理解SQL Server这几种物理连接方式对于性能调优来说必不可少，很多时候当筛选条件多表连接多时，查询分析器就可能不是那么智能了，因此理解这几种连接方式对于定位问题变得尤为重要。此外，我们也可以通过从业务角度减少查询范围来减少低下性能连接的可能性。

From: 

[浅谈SQL Server中的三种物理连接操作(HASH JOIN MERGE JOIN NESTED LOOP)](https://www.cnblogs.com/niceofday/p/5231271.html)

[SQL Server三种表连接原理](https://www.cnblogs.com/wanghao4023030/p/3429837.html)