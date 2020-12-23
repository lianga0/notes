## Caching and performance in Azure storage disks

> 2020.12.22

了解Azure磁盘缓存的学习连接：

[Caching and performance in Azure storage disks](https://docs.microsoft.com/en-us/learn/modules/caching-and-performance-azure-storage-and-disks/)

[Effect of caching on disk performance in Azure](https://docs.microsoft.com/en-us/learn/modules/caching-and-performance-azure-storage-and-disks/2-effect-of-caching-on-disk-performance-in-azure)

[Enable and configure Azure VM disk cache with the Azure portal](https://docs.microsoft.com/en-us/learn/modules/caching-and-performance-azure-storage-and-disks/3-enable-and-configure-azure-vm-disk-cache-by-using-the-azure-portal)


### Azure virtual machine disk types

There are three types of disks used with Azure VMs:

- OS disk: 
When you create an Azure VM, Azure automatically attaches a VHD for the operating system (OS).

- Temporary disk: 
When you create an Azure VM, Azure also automatically adds a temporary disk. This disk is used for data, such as page and swap files. The data on this disk may be lost during maintenance or a VM redeploy. Don't use it for storing permanent data, such as database files or transaction logs.

- Data disks: 
A data disk is a VHD that's attached to a virtual machine to store application data or other data you need to keep.

OS disks and data disks take advantage of Azure VM disk caching. The cache size for a VM disk depends on the VM instance size and the number of disks mounted on the VM. Caching can be enabled for only up to 4 TiB sized disks.

### Cache options for Azure VMs

There are three common options for VM disk caching:

- Read/write – Write-back cache. Use this option only if your application properly handles writing cached data to persistent disks when needed.

- Read-only - Reads are done from the cache.

- None - No cache. Select this option for write-only and write-heavy disks. Log files are a good candidate because they're write-heavy operations.

Not every caching option is available for each type of disk. 

### Performance considerations for Azure VM disk caching

So, how can your cache settings affect the performance of your workloads running on Azure VMs?

#### OS disk

For a VM OS disk, the default behavior is to use the cache in read/write mode. If you have applications that store data files on the OS disk and the apps do lots of random read/write operations to data files, consider moving those files to a data disk that has the caching turned off. Why is that? Well, if the read queue does not contain sequential reads, caching will be of little or no benefit. The overhead of maintaining the cache, as if the data was sequential, can reduce disk performance.

#### Data disks

For performance-sensitive applications, you should use data disks rather than the OS disk. Using separate disks allows you to configure the appropriate cache settings for each one.

> For example, on Azure VMs running SQL Server, enabling **Read-only** caching on the data disks (for regular and TempDB data) can result in significant performance improvements. Log files, on the other hand, are good candidates for data disks with no caching.

**Warning**

> Changing the cache setting of an Azure disk detaches and then reattaches the target disk. If it's the operating system disk, the VM is restarted. Stop all applications/services that might be affected by this disruption before changing the disk cache setting.

想了解更多细节，可以参考[Azure premium storage: design for high performance](https://docs.microsoft.com/en-us/azure/virtual-machines/premium-storage-performance)
