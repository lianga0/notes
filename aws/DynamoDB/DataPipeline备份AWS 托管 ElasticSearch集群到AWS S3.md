# 备份AWS 托管 ElasticSearch集群到AWS S3

## 1. 创建存储备份S3的bucket

## 2. 创建IAM policy并附加到IAM role

### 2.1 创建IAM策略

这里我们可以为策略起名为：`ElasticSerachSnapshotRolePolicyAllowS3Bucket`

策略设置内容设置为：

```
{
  "Version": "2012-10-17",
  "Statement": [{
      "Action": [
        "s3:ListBucket"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::s3-bucket-name"
      ]
    },
    {
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::s3-bucket-name/*"
      ]
    }
  ]
}
```


Reference： https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-snapshots.html

### 2.2 创建IAM角色，并附加上一步创建的role

在IAM页面选择`Create role`，这里可以先选“Another AWS account”，用自己账号的Account ID，后边再改信任实体。

这里我们可以为角色名设置为： `ElasticSerachSnapshotBackupToS3Role`

角色创建好后，选择刚创建好的角色，在Trust relationships标签中选择Edit trust relationship。输入下面策略：

```
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "",
    "Effect": "Allow",
    "Principal": {
      "Service": "es.amazonaws.com"
    },
    "Action": "sts:AssumeRole"
  }] 
}
```

## 3. 通过AWS提供的Python脚本，把上一步创建的角色`ElasticSerachSnapshotBackupToS3Role`配置到ElasticSearch集群中，并register a repository。

所以你需要一个拥有`es:ESHttpPut`和`iam:PassRole`的用户或服务器来执行上述操作。如果没有的话，可以参考[Creating index snapshots in Amazon OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/latest/developerguide/managedomains-snapshots.html)中的描述进行配置

将角色成功配置到ElasticSearch集群后，就可以进行后续操作了。

## 4. 手动创建一个快照

### 4.1 首先检查一下，是否有进行中的快照（快照执行过程中，不能创建新的快照）

```
curl -XGET 'domain-endpoint/_snapshot/_status'
```

#### 4.2 执行下面命令手动创建一个新的快照

```
curl -XPUT 'domain-endpoint/_snapshot/repository-name/snapshot-name'
```
