### Amazon EC2 根设备卷（Root Device Volume）

When you launch an instance, the root device volume contains the image used to boot the instance. When we introduced Amazon EC2, all AMIs were backed by Amazon EC2 instance store, which means the root device for an instance launched from the AMI is an instance store volume created from a template stored in Amazon S3. After we introduced Amazon EBS, we introduced AMIs that are backed by Amazon EBS. This means that the root device for an instance launched from the AMI is an Amazon EBS volume created from an Amazon EBS snapshot.

当您启动一个实例时，根设备卷 包含用于启动该实例的映像。当我们介绍 Amazon EC2 时，所有 AMI 都由 Amazon EC2 实例存储提供支持，也就是说从该 AMI 启动的实例的根设备是从存储在 Amazon S3 中的模板创建的实例存储卷。介绍完 Amazon EBS 之后，我们将介绍由 Amazon EBS 提供支持的 AMI。这意味着从 AMI 启动的实例的根设备是一个从 Amazon EBS 快照创建的 Amazon EBS 卷。

You can choose between AMIs backed by Amazon EC2 instance store and AMIs backed by Amazon EBS. We recommend that you use AMIs backed by Amazon EBS, because they launch faster and use persistent storage.

您可以在 Amazon EC2 实例存储支持的 AMI 和 Amazon EBS 支持的 AMI 之间进行选择。我们建议您使用由 Amazon EBS 提供支持的实例，因为它们启动速度更快，而且采用了持久性存储。

For more information about the device names Amazon EC2 uses for your root volumes, see [Device Naming on Linux Instances](http://docs.aws.amazon.com/en_us/AWSEC2/latest/UserGuide/device_naming.html).

有关用于您的根卷的设备名称Amazon EC2的更多信息，请参阅Linux 实例上的设备命名。

##### Root Device Storage Concepts

根设备存储概念

You can launch an instance from either an instance store-backed AMI or an Amazon EBS-backed AMI. The description of an AMI includes which type of AMI it is; you'll see the root device referred to in some places as either `ebs` (for Amazon EBS-backed) or `instance store` (for instance store-backed). This is important because there are significant differences between what you can do with each type of AMI. For more information about these differences, see [Storage for the Root Device](http://docs.aws.amazon.com/en_us/AWSEC2/latest/UserGuide/ComponentsAMIs.html#storage-for-the-root-device).

您可以从实例存储支持 AMI 或Amazon EBS支持 AMI 启动实例。AMI 的说明中包括 AMI 的类型；您会看到根设备在一些地方被称为 ebs(表示由 Amazon EBS 提供支持) 或 instance store (示由实例存储提供支持)。这很重要，因为您可以使用每种 AMI 进行哪些操作有很大区别。有关这些区别的更多信息，请参阅根设备存储。

##### Storage for the Root Device

All AMIs are categorized as either backed by Amazon EBS or backed by instance store. The former means that the root device for an instance launched from the AMI is an Amazon EBS volume created from an Amazon EBS snapshot. The latter means that the root device for an instance launched from the AMI is an instance store volume created from a template stored in Amazon S3. For more information, see [Amazon EC2 Root Device Volume](http://docs.aws.amazon.com/en_us/AWSEC2/latest/UserGuide/RootDeviceStorage.html).

根设备存储

所有 AMI 均可归类为由 Amazon EBS 支持或由实例存储支持。前者是指从 AMI 启动的实例的根设备是从 Amazon EBS 快照创建的 Amazon EBS 卷。后者是指从 AMI 启动的实例的根设备是从存储在 Amazon S3 中的模板创建的实例存储卷。有关更多信息，请参阅Amazon EC2 根设备卷。

##### Instance Store-backed Instances

Instances that use instance stores for the root device automatically have one or more instance store volumes available, with one volume serving as the root device volume. When an instance is launched, the image that is used to boot the instance is copied to the root volume. Note that you can optionally use additional instance store volumes, depending on the instance type.

Any data on the instance store volumes persists as long as the instance is running, but this data is deleted when the instance is terminated (instance store-backed instances do not support the Stop action) or if it fails (such as if an underlying drive has issues).

After an instance store-backed instance fails or terminates, it cannot be restored. If you plan to use Amazon EC2 instance store-backed instances, we highly recommend that you distribute the data on your instance stores across multiple Availability Zones. You should also back up critical data data on your instance store volumes to persistent storage on a regular basis.

For more information, see [Amazon EC2 Instance Store](http://docs.aws.amazon.com/en_us/AWSEC2/latest/UserGuide/InstanceStorage.html).

##### Amazon EBS-backed Instances

Instances that use Amazon EBS for the root device automatically have an Amazon EBS volume attached. When you launch an Amazon EBS-backed instance, we create an Amazon EBS volume for each Amazon EBS snapshot referenced by the AMI you use. You can optionally use other Amazon EBS volumes or instance store volumes, depending on the instance type.

An Amazon EBS-backed instance can be stopped and later restarted without affecting data stored in the attached volumes. There are various instance– and volume-related tasks you can do when an Amazon EBS-backed instance is in a stopped state. For example, you can modify the properties of the instance, you can change the size of your instance or update the kernel it is using, or you can attach your root volume to a different running instance for debugging or any other purpose.

If an Amazon EBS-backed instance fails, you can restore your session by following one of these methods:

- Stop and then start again (try this method first).
- Automatically snapshot all relevant volumes and create a new AMI. For more information, see Creating an Amazon EBS-Backed Linux AMI.
- Attach the volume to the new instance by following these steps:
    + Create a snapshot of the root volume.
    + Register a new AMI using the snapshot.
    + Launch a new instance from the new AMI.
    + Detach the remaining Amazon EBS volumes from the old instance.
    + Reattach the Amazon EBS volumes to the new instance.

For more information, see [Amazon EBS Volumes](http://docs.aws.amazon.com/en_us/AWSEC2/latest/UserGuide/EBSVolumes.html).

Reference:
[Amazon EC2 根设备卷](http://docs.aws.amazon.com/zh_cn/AWSEC2/latest/UserGuide/RootDeviceStorage.html)
[Amazon EC2 Root Device Volume](http://docs.aws.amazon.com/en_us/AWSEC2/latest/UserGuide/RootDeviceStorage.html)