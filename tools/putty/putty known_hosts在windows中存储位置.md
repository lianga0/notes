### Putty的known_hosts在Windows中存储位置

Putty把unix/linux中ssh使用的known_hosts文件存储在什么地方了？

Putty把known hosts存储在注册表中了，注册表中的键如下:

```
HKEY_CURRENT_USER\SoftWare\SimonTatham\PuTTY\SshHostKeys
```

使用`regedit`命令可以打开windows的注册表编辑器。

From：

[Where does Putty store known_hosts information on Windows?](https://superuser.com/questions/197489/where-does-putty-store-known-hosts-information-on-windows)