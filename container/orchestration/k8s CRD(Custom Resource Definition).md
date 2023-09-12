# What is k8s CRD?

Custom resources definition (CRD) is a powerful feature introduced in Kubernetes 1.7 which enables users to add their own/custom objects to the Kubernetes cluster and use it like any other native Kubernetes objects.

Custom Resource Definition (CRD) resource is a way to define your own resource kind like Deployment, StatefulSet etc. CRDs define the structure and validation of the custom kind.

Custom Resource (CR) are the resources that are created by following the structure from a Custom Resource Definition (CRD).

Custom Controller makes sure that our Kubernetes cluster or application always matches its current state with the desired state that we expect it to.

You can read more about this in the [Custom Resources](https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/) documentation page.

Reference:
[Prometheus Definitive Guide Part III - Prometheus Operator](https://www.infracloud.io/blogs/prometheus-operator-helm-guide/)