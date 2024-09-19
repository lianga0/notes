# Bitnami Helm Chart for Apache Kafka

Bitnami提供的Apache Kafka安装Helm Chart，最早使用`https://charts.bitnami.com/bitnami/kafka`站点托管chart资源。

后边，替换为`oci://registry-1.docker.io/bitnamicharts/kafka`站点托管。

我们使用的老版本`15.3.0`的chart已经不能在`oci://registry-1.docker.io`站点上找到了。仅可以从Github上找到历史标签`https://github.com/bitnami/charts/tree/kafka/15.3.0/bitnami/kafka`。

windows中可以使用helm命令下载我们想要版本的Chart包，这里我们以下载版本`https://github.com/bitnami/charts/tree/kafka/30.0.5/bitnami/kafka`为例。

Linux平台中设置代理很容易，Windows平台设置代理可以参考issue `https://github.com/helm/helm/issues/9576`，Powershell中命令如下：

```
# Set proxy via environment
$env:HTTP_PROXY="http://IP:port"
$env:HTTPS_PROXY="http://IP:port"
```

下载Chart包命令如下：

```
helm pull oci://registry-1.docker.io/bitnamicharts/kafka

helm pull oci://registry-1.docker.io/bitnamicharts/kafka --version 30.0.5
```
