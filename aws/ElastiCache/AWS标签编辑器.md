### 标签编辑器

标签是一些充当元数据的词和短语，用于标识和组织 AWS 资源。标签限制随资源而有所不同，但大多数最多可以有 50 个标签。每个标签都包含一个键和一个值。

您可以在创建资源时向资源添加标签，也可以在每个资源的控制台中一次向一个资源添加、更改或删除这些标签。要一次向多个资源添加标签，需要使用标签编辑器。借助标签编辑器，可以搜索要标记的资源，然后为搜索结果中的资源添加、删除或编辑标签。

##### 在AWS Web Console中启动标签编辑器

1. 登录 AWS 管理控制台。

2. 在导航栏中，选择 Resource Groups，然后选择 Tag Editor。

标签并非适用于所有资源。要查看某个资源是否支持标记，请参阅该资源的服务的文档。

You can use the AWS CLI to add, modify, or remove cost allocation tags. The following shows how to list,add,delete tags in ElastiCache.

Cost allocation tags are applied to ElastiCache resources which are specified in CLI and API operations as an ARN. The resource-type will be a "cluster" or a "snapshot".

### 使用AWS CLI操作elasticache的标签

##### elasticache实例的ARN结构

```
Sample ARN: arn:aws:elasticache:<region>:<customer-id>:<resource-type>:<resource-name>
```

Memcached: Tags are applied to clusters.

>> Sample arn: arn:aws:elasticache:us-west-2:1234567890:cluster:mymemcached


Redis: Tags are applied to individual nodes. Because of this, nodes in Redis clusters with replication can have different tags.

> Redis (cluster mode disabled) no replication:

>> Sample arn: arn:aws:elasticache:us-west-2:1234567890:cluster:myredis

> Redis (cluster mode disabled) with replication:

>> Sample arn: arn:aws:elasticache:us-west-2:1234567890:cluster:myredis-001

> Redis (cluster mode enabled):

>> Sample arn: arn:aws:elasticache:us-west-2:1234567890:cluster:myredis-0001-001

Backups (Redis): Tags are applied to the backup.

>> Sample arn: arn:aws:elasticache:us-west-2:1234567890:snapshot:myredisbackup

##### 查看elasticache实例的所有tag

```
aws elasticache list-tags-for-resource --resource-name arn:aws:elasticache:us-west-1:944809154377:cluster:drs-test-redis-0001-001
```

输出信息如下：

```
{
    "TagList": [
        {
            "Value": "drs-test-liangao",
            "Key": "project"
        }
    ]
}
```

##### Adding Tags Using the AWS CLI

```
aws elasticache add-tags-to-resource \
 --resource-name arn:aws:elasticache:us-west-2:0123456789:cluster:memcluster \
 --tags Key=Service,Value=elasticache \
        Key=Region,Value=us-west-2 
```

##### Removing Tags Using the AWS CLI

```
aws elasticache remove-tags-from-resource \
 --resource-name arn:aws:elasticache:us-west-2:0123456789:cluster:myCluster \
 --tag-keys PM Service 
```

#####Modifying Tags Using the AWS CLI

You can use the AWS CLI to modify the tags on an ElastiCache resource.

To modify the value of a tag:

> Use add-tags-to-resource to either add a new tag and value or to change the value associated with an existing tag.

> Use remove-tags-from-resource to remove specified tags from the resource.


Reference：[使用标签编辑器](http://docs.aws.amazon.com/zh_cn/awsconsolehelpdocs/latest/gsg/tag-editor.html)

[Using Cost Allocation Tags (AWS Billing and Cost Management)](http://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/cost-alloc-tags.html#allocation-what)

[Managing Your Cost Allocation Tags Using the AWS CLI (Amazon ElastiCache)](http://docs.aws.amazon.com/AmazonElastiCache/latest/UserGuide/Tagging.Managing.CLI.html)

[Monitoring Costs with Cost Allocation Tags (Amazon ElastiCache)](http://docs.aws.amazon.com/AmazonElastiCache/latest/UserGuide/Tagging.html)
