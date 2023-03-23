## Ubuntu docker 安装sshd服务Dockerfile

添加新用户ubuntu，并设置登陆密码

```
FROM ubuntu:latest

RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list

RUN apt-get clean && \
    apt-get update

RUN apt-get install -y openssh-server sudo && useradd -rm -d /opt/ubuntu -s /usr/bin/bash -g root -G sudo -u 1000 ubuntu && echo 'ubuntu:ubuntu' | chpasswd && service ssh start

EXPOSE 22

CMD ["/usr/sbin/sshd","-D"]

```

或者不新建用户，直接使用root用户登陆

```
FROM ubuntu:latest

RUN sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list

RUN apt-get clean && \
    apt-get update

RUN apt-get install -y openssh-server && echo 'root:123456' | chpasswd && service ssh start && echo "PermitRootLogin yes" >> /etc/ssh/sshd_config

EXPOSE 22

CMD ["/usr/sbin/sshd","-D"]
```


## Centos docker 安装sshd服务Dockerfile

```
FROM centos:centos7

RUN yum install openssh-server -y

RUN ssh-keygen -A

RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config

RUN echo "root:123456" | chpasswd

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]

```


Reference: 

[ubuntu首次SSH使用root账户远程登录教程](https://blog.csdn.net/howiecode/article/details/120457571)
