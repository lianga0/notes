### 如何在Ubuntu中创建swap分区文件

> From [Jim](http://blog.163.com/ljf_gzhu/blog/static/1315534402015669052134/)

测试环境：Ubuntu 14.04 with root user

通常，Linux系统中swap分区可以通过两种方式指定，分别为：一、在磁盘分区的时候格式化一个swap分区；二、在文件系统中创建一个swap文件作为swap分区。此文主要介绍第二种方式。步骤如下：

1. 创建文件

```
fallocate -l 2G /swapfile
```
说明：2G 表示swap文件大小，/swapfile为swap文件路径和名称，可以任意指定。

2. 修改文件权限

```
chmod 600 /swapfile
```

3. 将 swapfile 初始化为交换文件

```
mkswap /swapfile
```

4. 启用交换文件

```
swapon /swapfile
```

5. 至此，linux系统已经将swapfile作为交换文件使用，但是重启之后是不会自动挂在刚才创建的文件的，因此需要手动修改 /etc/fstab 配置文件：
`gedit /etc/fstab`
在文件中添加如下内容：

```
/swapfile none swap sw 0 0
```

6. 完成，测试下：

```
swapon -s
```

提示：
    如果需要卸载swap分区文件，可以使用命令：`swapoff /swapfile`

reference: [如何在Ubuntu 14.04中创建SWAP交换分区文件](http://www.linuxidc.com/Linux/2014-08/105223.htm)