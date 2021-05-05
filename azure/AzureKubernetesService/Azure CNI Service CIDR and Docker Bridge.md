# Azure CNI Service CIDR and Docker Bridge CIDR

> https://docs.microsoft.com/en-us/answers/questions/124451/azure-cni-service-cidr-and-docker-bridge-cidr.html

We are in the process of setting AKS for our Teams and we decided to go with CNI . I clearly understand the Range specification around POD CIDR , I have the below Question around Service CIDR and Docker Bridge CIDR . Would be great to get some ones expert opinion .

1. Documentation says the Service CIDR and Docker Bridge CIDR should not be from the VNET or any Address spaces of any of the existing VNET architecture and we can reuse the Service CIDR and Docker Bridge CIDR across various multiple AKS clusters we create . Will there be any impact if I use the Same Service CIDR and Docker CIDR across different multiple AKS clusters iam going to create ? What if the multiple clusters are inside the same VNET or what if the VNET's that those AKS clusters will be placed are peered ? Will using the same service CIDR have impact on any of the above scenarios .

2. Also What is the recommended address space for Service CIDR and Docker Bridge CIDR ?


Would be great if some one can help me clear these doubts , cuz i beleive setting this up perfectly will avoid any problems in the future and recreation of clusters will be a huge pain .

Thanks in advance.

## prmanhas-MSFT answered · Oct 13 2020 at 5:26 PM


We don’t use the docker bridge for pod communication, but as Docker is configured as part of the Kubernetes setup, this docker bridge it also gets created as well, so in order to avoid that it picks random unknown CIDR that could collide with any of your existent subnets, we give the option to change it and set it a known range. So the indication for docker bridge is to define any CIDR that doesn’t to Azure, and doesn’t collide with any other subnet. The Docker bridge network address represents the default docker0 bridge network address present in all Docker installations. While docker0 bridge is not used by AKS clusters or the pods themselves, you must set this address to continue to support scenarios such as docker build within the AKS cluster. It is required to select a CIDR for the Docker bridge network address because otherwise Docker will pick a subnet automatically which could conflict with other CIDRs. You must pick an address space that does not collide with the rest of the CIDRs on your networks, including the cluster's service CIDR and pod CIDR. You can reuse this range across different AKS clusters.


Any service of the clusterIP the type that you create from Kubernetes will get an IP from this CIDR, but this IP is only available in the cluster.

Also What is the recommended address space for Service CIDR and Docker Bridge CIDR ?

This range should not be used by any network element on or connected to this virtual network. Service address CIDR must be smaller than /12. You can reuse this range across different AKS clusters.

More information: [Configure Azure CNI networking in Azure Kubernetes Service (AKS)](https://docs.microsoft.com/en-us/azure/aks/configure-azure-cni).

The above article consist of this information as well.

## AKS CNI Deployment parameters

**Kubernetes service address range**: This parameter is the set of virtual IPs that Kubernetes assigns to internal services in your cluster. You can use any private address range that satisfies the following requirements:

- Must not be within the virtual network IP address range of your cluster
- Must not overlap with any other virtual networks with which the cluster virtual network peers
- Must not overlap with any on-premises IPs
- Must not be within the ranges 169.254.0.0/16, 172.30.0.0/16, 172.31.0.0/16, or 192.0.2.0/24

Although it's technically possible to specify a service address range within the same virtual network as your cluster, doing so is not recommended. Unpredictable behavior can result if overlapping IP ranges are used. For more information, see the FAQ section of this article. For more information on Kubernetes services, see Services in the Kubernetes documentation.

**Kubernetes DNS service IP address**: The IP address for the cluster's DNS service. This address must be within the Kubernetes service address range. Don't use the first IP address in your address range, such as .1. The first address in your subnet range is used for the kubernetes.default.svc.cluster.local address.

**Docker Bridge address**: The Docker bridge network address represents the default docker0 bridge network address present in all Docker installations. While docker0 bridge is not used by AKS clusters or the pods themselves, you must set this address to continue to support scenarios such as docker build within the AKS cluster. It is required to select a CIDR for the Docker bridge network address because otherwise Docker will pick a subnet automatically which could conflict with other CIDRs. You must pick an address space that does not collide with the rest of the CIDRs on your networks, including the cluster's service CIDR and pod CIDR.


Reference: [Configure Azure CNI networking in Azure Kubernetes Service (AKS)](https://docs.microsoft.com/en-us/azure/aks/configure-azure-cni)
