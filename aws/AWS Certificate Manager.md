AWS Certificate Manager

> 2019.07.23

要在 AWS 中启用与您的网站或应用程序的 HTTPS 连接，您需要 SSL/TLS 服务器证书。AWS提供两种方式来管理用户上传的证书：
1. AWS Certificate Manager (ACM) 服务
2. 直接使用 IAM 作为证书管理器

ACM 是预配置、管理和部署您的服务器证书的首选工具。利用 ACM，您可以请求证书或将现有 ACM 或外部证书部署到 AWS 资源。

AWS推荐优先使用 ACM进行证书的管理。

> https://aws.amazon.com/cn/premiumsupport/knowledge-center/import-ssl-certificate-to-iam/

> 最佳做法是将 SSL 证书上传到 AWS Certificate Manager (ACM)。

> 如果您使用的是 ACM 或关联的 AWS 资源当前不支持的证书算法和密钥大小，则您还可以使用 AWS 命令行界面 (AWS CLI) 将 SSL 证书上传到 IAM。


AWS推荐只有当您必须在 ACM 不支持的区域中支持 HTTPS 连接时，才应使用 IAM 作为证书管理器。

IAM 安全地加密您的私有密钥并将加密的版本存储在 IAM SSL 证书存储中。IAM 支持在所有区域中部署服务器证书，但您必须从外部提供商获得证书才能供 AWS 使用。

**您无法将 ACM 证书上传到 IAM。此外，您还无法从 IAM 控制台管理证书，也就是说IAM证书只能通过AWS API或 AWS CLI进行管理。**

ACM的使用方法较为简单。但使用AWS IAM管理证书，AWS目前仅支持AWS CLI和API的形式，无法在Web Console中可视化管理，具体的操作命令请参照[AWS 文档 » AWS Identity and Access Management » 用户指南 » 身份 (用户、组和角色) » IAM 用户 » 使用服务器证书](https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/id_credentials_server-certs.html)文档。

例如，您可以通过运行以下命令查看上传的IAM证书：

```
aws iam list-server-certificates
```

该命令将返回关于上传的证书的元数据，包括证书的 Amazon 资源名称 (ARN)、友好名称、标识符 (ID) 和过期日期。

删除命令
```
aws iam delete-server-certificate --server-certificate-name  xxx-cert-name
```

> 注意：如果您上传要用于 Amazon CloudFront 的服务器证书，必须使用 --path 指定路径。路径必须以 /cloudfront 开头，并且路径结尾必须包含反斜杠，例如 /cloudfront/test/。

[使用服务器证书](https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/id_credentials_server-certs.html)

[如何上传 SSL 证书并将其导入 AWS Identity and Access Management (IAM)？](https://aws.amazon.com/cn/premiumsupport/knowledge-center/import-ssl-certificate-to-iam/)

[为什么无法将我的自定义 SSL 证书用于我的 CloudFront 分配？](https://aws.amazon.com/cn/premiumsupport/knowledge-center/custom-ssl-certificate-cloudfront/)