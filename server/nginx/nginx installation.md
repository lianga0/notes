## nginx installation

> 2021.10.08

好早在EC2中自己编译的nginx被通报漏洞，需要升级到最新版本，发现之前的配置忘记的干干净净，所以记录下这次更新的过程吧。

下载nginx源代码及其依赖库源代码，文件和版本分别如下：

- nginx-1.21.3.tar.gz
- openssl-1.1.1l.tar.gz
- pcre-8.45.tar.bz2
- zlib-1.2.11.tar.gz

分别解压后，进入nginx源码目录，执行如下命令：

```
./configure --prefix=/usr/local/nginx-1.21.3  --with-pcre=../pcre-8.45 --with-zlib=../zlib-1.2.11 --with-openssl=../openssl-1.1.1l --with-http_realip_module --with-http_ssl_module

make

make install
```

安装完成后，去`/usr/local/nginx-1.21.3/config`目录修改nginx的配置以及其它服务即可。

如果缺少C/C++编译工具，直接用`apt-get install build-essential`命令安装即可。