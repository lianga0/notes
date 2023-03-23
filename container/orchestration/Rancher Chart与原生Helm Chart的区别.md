# Rancher Chart与原生Helm Chart的区别

> 2022.09.15

> From: [Rancher创建应用商店应用](https://docs.rancher.cn/docs/rancher2/helm-charts/creating-apps/_index/)

## Helm `questions.yaml` 是什么

Helm 是一个软件包管理器，提供了一种简单的方法来查找、共享和使用为 Kubernetes 而构建的软件。它提供 key-value 或者 `values.yaml` 用于设置 Helm 应用的实例化参数。

`questions.yaml` 是为了提高蓝鲸容器服务中 Helm 功能的易用性，参考开源产品 Rancher 提供的一种动态表单生成技术。

用户可在 Chart 中提供 questions.yaml 文件，在蓝鲸容器服务产品中实例化 Helm 应用的时候，蓝鲸容器服务会根据 questions.yaml 生成表单供用户输入实例化参数。

## Rancher 支持两种不同类型的 Chart：

### Helm Chart

原生 Helm Charts 包括应用程序以及运行它所需的其他软件。部署原生 Helm Chart 时，您将需要了解学习每个 Chart 的参数，然后使用应答（它们是键值对的集合）来配置这些参数。

Rancher 中的 Helm Stable 和 Helm Incubators 均为原生的 Helm Chart。您也可以添加其他的 Helm Charts（尽管我们建议使用 Rancher Chart）。

### Rancher Chart

Rancher Chart 基本与原生 Helm Chart 一样。Rancher Chart 添加了两个额外的文件`app-readme.md`和`questions.yaml`来增强用户体验，但它们与原生 Helm Chart 的使用方式完全相同。在 Rancher Chart 独有的文件中了解有关它们的更多信息。

Rancher Charts 的优点包括：

- 增强的修订跟踪

    虽然 Helm 支持版本化的部署，但 Rancher 添加了修订跟踪历史记录，以显示 Charts 的不同版本之间的更改。

- 简化的应用启动流程

    Rancher Chart 添加了简化的 Chart 说明和配置表单，以简化应用商店中应用的部署。Rancher 用户无需阅读整个 Helm Chart 变量的列表即可了解如何启动应用。

- 应用资源管理

    Rancher 将跟踪由特定应用创建的所有资源。用户可以轻松地在 UI 上进行故障排查，该页面列出了此应用的所有工作负载和其他相关对象。

Reference:

[Rancher Creating Apps](https://docs.ranchermanager.rancher.io/how-to-guides/new-user-guides/helm-charts-in-rancher/create-apps)

[如何编写 Helm questions.yaml](https://bk.tencent.com/docs/document/6.0/144/6545)
