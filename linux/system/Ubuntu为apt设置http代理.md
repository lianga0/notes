## ubuntu 为 apt 设置 http 代理

> 2019.03.03

如果不使用第三方的代理软件，`apt`可以通过以下种方式来指定代理。

### 1. 修改`apt`配置文件

```
sudo vi /etc/apt/apt.conf.d/10proxy   # 这个文件正常不存在，会新建一个
# 编辑内容为：
Acquire::http::Proxy "http://user:pwd@192.168.1.1:8080";
```

### 2. 指定`apt`运行参数

```
sudo apt -o Acquire::http::proxy="http://cnnjproxy-gfw.ww.xxx.org:8080" install build-essential
```

### 3. 修改bash环境变量

设置环境变量，如果想为所有用户设置，可以编辑`/etc/profile`或者`/etc/environment`；如果只是当前用户使用，可以设置`~/.profile`文件，如果使用的不是bash，可能要根据需要设置其它配置文件，具体看使用shell的帮助文件。另外不同的脚本设置环境变量的命令是不同的，注意区别使用。

以bash为例，把下面这行脚本写入配置文件。记着把代理的用户名、密码替换成自己的，如果没有密码也可以把@之前的部分包括@都去掉：

```
export HTTPS_PROXY=http://username:password@192.168.1.1:8080
export http_proxy=http://ip:port
export https_proxy=http://ip:port
```

如果使用的是socks5代理，可以写成这样：

```
export HTTPS_PROXY="socks5://192.168.1.1:8088"
# 或者
export ALL_PROXY="socks5://192.168.1.1:8088"
```

执行`source /etc/profile`，然后登出再登入生效。

Reference:

[三种方式给apt设置代理](https://www.cnblogs.com/andrewwang/p/9293031.html)