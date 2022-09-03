# CentOS7安装grocksdb依赖

> 2022.03.31

0. 安装golang并设置代理

```
yum install golang -y
```

```
export GOPROXY=https://goproxy.cn,direct

```

1. CentOS7安装c++17



```
yum install centos-release-scl -y
yum-config-manager --enable rhel-server-rhscl-7-rpms
yum install devtoolset-7 -y
scl enable devtoolset-7 bash
```





2. 切换到c++17编译环境

```
scl enable devtoolset-7 bash

```



3. gflags:

```
git clone https://github.com/gflags/gflags.git
cd gflags
git checkout v2.0
./configure && make && sudo make install
```


4. 添加编译查找路径

```
export CPLUS_INCLUDE_PATH=${CPLUS_INCLUDE_PATH}:/usr/local/include
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:/usr/local/lib
export LIBRARY_PATH=${LIBRARY_PATH}:/usr/local/lib
```


5. 安装其它依赖

```
sudo yum install snappy snappy-devel -y
sudo yum install zlib zlib-devel  -y
sudo yum install bzip2 bzip2-devel  -y
sudo yum install lz4-devel  -y
sudo yum install libasan  -y
sudo yum install libzstd-devel  -y
```

6. 添加go代理

```
export GOPROXY=https://goproxy.cn,direct
```


7. 编译ocksdb（务必使用7.0.2版本）

```
PORTABLE=1 make shared_lib
INSTALL_PATH=/usr/local make install-shared

```


8. 编译grocksdb

```
CGO_CFLAGS="-I/root/tmp/rocksdb-7.0.2/include" \
CGO_LDFLAGS="-L/root/tmp/rocksdb-7.0.2 -lrocksdb -lstdc++ -lm -lz -lsnappy -llz4 -lzstd" \
  go build
```


9. 为我们的项目添加grocksdb依赖

```
CGO_CFLAGS="-I/root/tmp/rocksdb-7.0.2/include" \
CGO_LDFLAGS="-L/root/tmp/rocksdb-7.0.2 -lrocksdb -lstdc++ -lm -lz -lsnappy -llz4 -lzstd" \
go get github.com/linxGnu/grocksdb
```

or

```
CGO_CFLAGS="-I/usr/local/include" \
CGO_LDFLAGS="-L/usr/local/lib -lrocksdb -lstdc++ -lm -lz -lsnappy -llz4 -lzstd" \
go get github.com/linxGnu/grocksdb
```


参考连接：

[CentOS7安装c++17](https://www.jianshu.com/p/e9bfdc040dc1)

[rocksdb INSTALL](https://github.com/facebook/rocksdb/blob/master/INSTALL.md)


[rocksdb使用说明](https://www.jianshu.com/p/966f7dcafbdd)

[linxGnu/grocksdb](https://github.com/linxGnu/grocksdb)

[grocksdb, RocksDB wrapper for Go](https://pkg.go.dev/github.com/linxGnu/grocksdb)
