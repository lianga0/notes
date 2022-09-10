# minikube 测试集群及Rancher测试环境的安装

> 2022.09.09

公司生产环境使用Rancher管理K8S集群，为了测试，自己在本地搭建一个简单的模拟环境。

为与生产环境一致，这里需要安装比较旧的rancher v2.5.11版本。

## K8S与Rancher的兼容问题

minikube安装时，测试环境因为网络问题，出现如下错误信息

```
* Creating docker container (CPUs=2, Memory=4000MB) ...
! This container is having trouble accessing https://k8s.gcr.io
* To pull new external images, you may need to configure a proxy: https://minikube.sigs.k8s.io/docs/reference/networking/proxy/
```

需要配置一下代理，从而使得minikube可以正确下载需要的资源。按照文档[Proxies and VPNs](https://minikube.sigs.k8s.io/docs/reference/networking/proxy/)，Windows中使用HTTP proxy命令如下：

```
set HTTP_PROXY=http://10.15.135.20:8080
set HTTPS_PROXY=http://10.15.135.20:8080
set NO_PROXY=localhost,127.0.0.1,10.96.0.0/12,192.168.59.0/24,192.168.49.0/24,192.168.39.0/24

```

按照[minikube start](https://minikube.sigs.k8s.io/docs/start/)介绍步骤安装完测试K8S集群后，
再测试集群中按照[Install/Upgrade Rancher on a Kubernetes Cluster](https://rancher.com/docs/rancher/v2.5/en/installation/install-rancher-on-k8s/)中步骤安装rancher v2.5，
Pod内总是出现如下错误日志：

```
2021/08/20 16:29:27 [INFO] Rancher version v2.5.9 (3c5418944) is starting
2021/08/20 16:29:27 [INFO] Rancher arguments {ACMEDomains:[] AddLocal:true Embedded:false BindHost: HTTPListenPort:80 HTTPSListenPort:443 K8sMode:auto Debug:false Trace:false NoCACerts:false AuditLogPath:/var/log/auditlog/rancher-api-audit.log AuditLogMaxage:10 AuditLogMaxsize:100 AuditLogMaxbackup:10 AuditLevel:0 Agent:false Features: ClusterRegistry:}
2021/08/20 16:29:27 [INFO] Listening on /tmp/log.sock
2021/08/20 16:29:27 [FATAL] the server could not find the requested resource
```

该问题有人回答为Rancher与K8S版本兼容存在问题。原始回答如下：
> From: [Install fail the server could not find the requested resource](https://forums.rancher.com/t/install-fail-the-server-could-not-find-the-requested-resource/20974)

This issue occurs because the current version 2.59 does not support Kubernetes version 1.22.
I have installed version 1.21 and am using it.

## 安装配置K8S v1.20.1 （生产环境采用版本）

按[minikube start](https://minikube.sigs.k8s.io/docs/start/)中命令，安装minikube。

然后创建集群时，修改文档中命令，创建指定版本K8S测试环境。


创建指定版本K8S命令

```
minikube start -p aged --kubernetes-version=v1.20.1
```

为指定环境安装 K8S dashboard，从而可以在浏览器中查看K8S集群状态

```
minikube -p aged  dashboard
```

如果dashboard容器已经在k8s中正常运行，那么可以使用下面命令转发服务端口，从而可以在本地浏览器直接访问 K8S dashboard

```
kubectl port-forward service/kubernetes-dashboard -n kubernetes-dashboard 8888:80
```

如果docker中minikube容器未启动，可以使用如下命令启动

```
minikube start  -p aged
```

## 安装配置Rancher v2.5.11（生产环境采用版本）

按照Rancher官网[Install/Upgrade Rancher on a Kubernetes Cluster](https://rancher.com/docs/rancher/v2.5/en/installation/install-rancher-on-k8s/)中步骤安装rancher v2.5即可。

单因为我们需要安装特定小版本号rancher，所以这里需要修改一下rancher helm安装时的参数，修改后如下：

```
helm install rancher rancher-stable/rancher --set rancherImageTag="v2.5.11"   --namespace cattle-system   --set hostname=rancher.my.org   --set bootstrapPassword=admin --version=v2.5.11
```

把官网中文档全部安装命令(默认Rancher Generated Certificates方式)按顺序放置如下：

```
helm repo add rancher-latest https://releases.rancher.com/server-charts/latest
kubectl create namespace cattle-system
# If you have installed the CRDs manually instead of with the `--set installCRDs=true` option added to your Helm install command, you should upgrade your CRD resources before upgrading the Helm chart:
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.5.1/cert-manager.crds.yaml

# Add the Jetstack Helm repository
helm repo add jetstack https://charts.jetstack.io

# Update your local Helm chart repository cache
helm repo update

# Install the cert-manager Helm chart
helm install cert-manager jetstack/cert-manager   --namespace cert-manager   --create-namespace   --version v1.5.1
helm install rancher rancher-stable/rancher --set rancherImageTag="v2.5.11" --namespace cattle-system --set hostname=rancher.my.org --set bootstrapPassword=admin --version=v2.5.11 --set replicas=1
```

安装完成后，同样可以使用`kubectl port-forward`命令转发服务端口到Windows本地，从而可以直接在浏览器访问rancher

```
kubectl port-forward service/rancher -n cattle-system 8443:443
```

> 注意:安装过程中，K8S中很容易出现拉取镜像超时错误。目前做法是，登陆进去`gcr.io/k8s-minikube/kicbase:v0.0.33`镜像对应的容器中，在容器内修改docker源，并手动使用docker pull拉取失败镜像到本地。例如：`docker pull rancher/rancher:v2.5.11`

参考文档：

[minikube start](https://minikube.sigs.k8s.io/docs/start/)

[RANCHER 2.5 - Install/Upgrade Rancher on a Kubernetes Cluster](https://rancher.com/docs/rancher/v2.5/en/installation/install-rancher-on-k8s/)
