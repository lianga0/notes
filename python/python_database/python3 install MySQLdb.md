# python3 安装MySQLdb库

命令`pip3 install MySQLdb`安装MySQLdb时报错，找不到指定的库。

```
Collecting MySQLdb
  Could not find a version that satisfies the requirement MySQLdb (from versions: )
No matching distribution found for MySQLdb
```

可以改用`pip3 install mysqlclient`命令安装，但安装过程中出现如下错误：

```
pip3 install mysqlclient
Collecting mysqlclient
  Downloading https://files.pythonhosted.org/packages/d0/97/7326248ac8d5049968bf4ec708a5d3d4806e412a42e74160d7f266a3e03a/mysqlclient-1.4.6.tar.gz (85kB)
    100% |████████████████████████████████| 92kB 389kB/s 
    Complete output from command python setup.py egg_info:
    /bin/sh: 1: mysql_config: not found
    /bin/sh: 1: mariadb_config: not found
    /bin/sh: 1: mysql_config: not found
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "/tmp/pip-build-n9cz0x8s/mysqlclient/setup.py", line 16, in <module>
        metadata, options = get_config()
      File "/tmp/pip-build-n9cz0x8s/mysqlclient/setup_posix.py", line 61, in get_config
        libs = mysql_config("libs")
      File "/tmp/pip-build-n9cz0x8s/mysqlclient/setup_posix.py", line 29, in mysql_config
        raise EnvironmentError("%s not found" % (_mysql_config_path,))
    OSError: mysql_config not found
    
    ----------------------------------------
Command "python setup.py egg_info" failed with error code 1 in /tmp/pip-build-n9cz0x8s/mysqlclient/
```

错误原因在于 linux需要mysql相关的一些依赖包

使用命令`sudo apt-get install libmysqlclient-dev`安装完毕后就可以正常`pip3 install mysqlclient`了。

Reference: 

[python3安装MySQLdb](https://blog.csdn.net/a30501139/article/details/90143053)

[解决问题：OSError: mysql_config not found](https://www.jianshu.com/p/5b6deb15bd21)