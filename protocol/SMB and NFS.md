### SMB and NFS

SMB（Server Message Block）通信协议是微软（Microsoft）和英特尔(Intel)在1987年制定的协议，主要是作为Microsoft网络的通讯协议。Widows主机在局域网间共享文件时通常使用SMB协议。

在NetBIOS出现之后，Microsoft就使用NetBIOS实现了一个网络文件/打印服务系统，这个系统基于NetBIOS设定了一套文件共享协议，Microsoft称之为SMB（Server Message Block）协议。这个协议被Microsoft用于它们Lan Manager和Windows NT服务器系统中，而Windows系统均包括这个协议的客户软件，因而这个协议在局域网系统中影响很大。 　随着Internet的流行，Microsoft希望将这个协议扩展到Internet上去，成为Internet上计算机之间相互共享数据的一种标准。因此它将原有的几乎没有多少技术文档的SMB协议进行整理，重新命名为 CIFS（Common Internet File System），并打算将它与NetBIOS相脱离，试图使它成为Internet上的一个标准协议。
因此，为了让Windows和Unix计算机相集成，最好的办法即是在Unix中安装支持SMB/CIFS协议的软件，这样Windows客户就不需要更改设置，就能如同使用Windows NT服务器一样，使用Unix计算机上的资源了。

#### Linux主机访问SMB服务器共享文件

Linux主机也可以安装SMB客户端，从而可以访问Windows主机通过SMB服务共享的文件。下面以Ubuntu为例介绍访问过程。

1. 安装smbclient，smbclient命令属于samba套件，它提供一种命令行使用交互式方式访问samba服务器的共享资源。

```
sudo apt install smbclient
```

2. 像使用FTP客户端一样使用sbmclient

```
smbclient -m SMB3 -U username //server.ip.address/share_folder_name
```

回车后,会提示输入该的密码。或者直接在命令中指定密码（不建议，因为会存储在history中）

```
smbclient //192.168.0.1/tmp  -U username%password
```

执行smbclient命令成功后，进入smbclient环境，出现提示符：smb:/>

这里有许多命令和ftp命令相似，如cd 、lcd、get、megt、put、mput等。通过这些命令，我们可以访问远程主机的共享资源。

在命令前加上!会执行本地的命令 如 :

`\>!pwd` 是查询当前的本地的工作目录

`\>pwd`  查询远端SMB服务器上的工作目录


3. 直接一次性使用smbclient命令

```
smbclient -c "ls"  //192.168.0.1/tmp  -U username%password
```

上边命令，与下面交互式命令效果相似

```

smbclient //192.168.0.1/tmp  -U username%password
smb:/>ls
```

4. 列出某个IP地址所提供的共享文件夹

```
smbclient -L 198.168.0.1 -U username%password
```

5. smbclient mget

smbclient中mget子命令，可以通过通配符一次指定下载多个文件。

```
smb: \> help mget
HELP mget:
        <mask> get all the matching files
```

但是，默认情况下，需要手动确认每个下载的文件，令人感到非常繁琐。我们可以通过`prompt`子命令来关掉确认。

```
> smb: \> help prompt
HELP prompt:
        toggle prompting for filenames for mget and mput
```

#### Linux主机间共享文件——NFS

上面介绍了windows主机间共享文件一般采用的SMB协议，以及Linux主机访问SMB服务器共享文件的方法。

企业网络中，Linux以及类UNIX系统之间的文件共享往往采用NFS（Network File System，网络文件系统）。NFS采用C/S工作模式，在NFS服务器上将某个目录设置为共享目录，然后在客户端可以将这个目录挂载到本地使用。

NFS is the “Network File System” for Unix and Linux operating systems. It allows files to be shared transparently between servers, desktops, laptops etc. It is a client/server application that allows a user to view, store and update files on a remote computer as though they were on their own computer. Using NFS, the user or a system administrator can mount all or a portion of a file system.

#### ubuntu NFS 客户端

1. 安装NFS客户端

```
apt-get install nfs-common //下载nfs命令
```

2. 挂载服务器共享文件夹到本地

```
mount -t nfs 192.168.30.129:/opt/nfs_folder /opt/myfolder/
```

就完成了，这时候你在本地/opt/myfolder/下创建test.txt文件，在服务器/opt/nfs/nfs_folder/下看到test.txt

#### 安全性

由于NFS服务本身比较简单，尤其是在权限设置方面功能比较弱，所以如果对NFS服务设置不当，将会在企业网络中产生比较严重的安全隐患。

NFS 协议最初在设计时并不关注安全性，NFSv4 通过引入对更强大的安全服务和身份验证的支持，加强了该协议的安全性。

传统的 NFS 协议大多使用`AUTH_SYS`验证方式，基于 UNIX 的用户和组标识。在这种方式下，客户端只需要发送自己的 UID 和 GID 并与服务器上的 `/etc/passwd` 文件内容作对比，以决定其拥有怎样的权限。

所以当多个客户端存在 UID 相同的用户时，这些用户会拥有相同的文件权限。更进一步，拥有 root 权限的用户可以通过 su 命令切换到任意 UID 登录，服务器会因此给予其对应 UID 的权限。

为了防止上面的问题出现，服务器可选择使用更健壮的验证机制比如 `Kerberos` 结合 `NFS PRCSEC_GSS`。

NFS 共享目录的访问控制基于 `/etc/exports` 文件中定义的主机名或 IP 地址。但是客户端很容易针对其身份和 IP 地址造假，这也会导致一些安全问题。


#### Windows 系统挂载NFS共享目录

win10 系统默认不能挂载NFS共享目录，需要进入控制面板->程序->程序和功能->启用或关闭 Windows功能 ，勾选上`NFS`服务 。之后就可以使用 mount 命令挂载共享目录了。只是 Windows 系统并不使用 Linux 那样的用户管理，导致挂载的共享目录只能读取而没有写入的权限。

### Reference:

[SMB协议](https://baike.baidu.com/item/SMB%E5%8D%8F%E8%AE%AE/3770892)

[Linux 网络通讯 : smbclient 命令详解](https://blog.csdn.net/yexiangcsdn/article/details/82867469)

[Ubuntu16.04搭建NFS 文件共享服务器的方法](https://www.jb51.net/article/138141.htm)
