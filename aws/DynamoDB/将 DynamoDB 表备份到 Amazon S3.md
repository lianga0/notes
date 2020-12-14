## 如何将 DynamoDB 表备份到 Amazon S3？

https://aws.amazon.com/cn/premiumsupport/knowledge-center/back-up-dynamodb-s3/

简短描述

DynamoDB 提供两种内置备份方法：

按需：在您选择时创建备份。

时间点恢复：启用自动、连续备份。

这两种方法都使用 Amazon S3。但是，您无法访问用于这些备份的 S3 存储桶。要创建可以下载到本地或在另一个 AWS 服务中使用的备份，请使用 AWS Data Pipeline、Amazon EMR 或 AWS Glue。


## 如何使用 Data Pipeline 将 DynamoDB 表备份到另一个账户下的 S3 存储桶？

https://aws.amazon.com/cn/premiumsupport/knowledge-center/data-pipeline-account-access-dynamodb-s3/


我想使用 AWS Data Pipeline 将 Amazon DynamoDB 表备份到另一个 AWS 账户下的 Amazon Simple Storage Service (Amazon S3) 存储桶。

简短描述

1.    在源账户中，附加一条 AWS Identity and Access Management (IAM) 策略，授予 DataPipelineDefaultRole 和 DataPipelineDefaultResourceRole 角色 Amazon S3 权限。

2.    在目标账户中，创建一条存储桶策略，允许源账户中的 DataPipelineDefaultRole 和 DataPipelineDefaultResourceRole 角色访问 S3 存储桶。

3.    在源账户中，使用将 DynamoDB 表导出到 S3 Data Pipeline 模板创建管道。

4.    将 BucketOwnerFullControl 或 AuthenticatedRead 预装访问控制列表 (ACL) 添加到管道的 EmrActivity 对象的步骤字段中。

5.    激活管道以将 DynamoDB 表备份到目标账户下的 S3 存储桶。

6.    在目标账户中创建 DynamoDB 表。

7.    要将源表还原到目标表，请使用从 S3 导入 DynamoDB 备份数据 Data Pipeline 模板创建管道。
