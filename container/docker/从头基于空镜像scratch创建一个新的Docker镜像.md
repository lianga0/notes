# 从头基于空镜像scratch创建一个新的Docker镜像

> 2023.01.06

我们在使用Dockerfile构建docker镜像时，一种方式是使用官方预先配置好的容器镜像。优点是我们不用从头开始构建，节省了很多工作量，但付出的代价是需要下载很大的镜像包。

比如我机器上docker images返回的这些基于nginx的镜像，每个都超过了100MB，而一个简单的Ubuntu的容器超过了200MB，如果安装了相关的软件，尺寸会更大。

如果我们的需求是在构建一个符合我们实际业务需求的Docker镜像的前提下，确保镜像尺寸尽可能的小，应该怎么做呢？

思路是使用空镜像scratch。

[scratch](https://hub.docker.com/_/scratch)镜像虽然在docker hub中也存在相应的镜像文件，但自Docker 1.5.0版本起docker其实并不会下载scratch镜像，此命名仅仅指示一个空操作。官网解释信息如下：

`FROM scratch`

This image is most useful in the context of building base images (such as debian and busybox) or super minimal images (that contain only a single binary and whatever it requires, such as hello-world).

As of Docker 1.5.0 (specifically, docker/docker#8827), FROM scratch is a no-op in the Dockerfile, and will not create an extra layer in your image (so a previously 2-layer image will be a 1-layer image instead).

From https://docs.docker.com/build/building/base-images/:

You can use Docker’s reserved, minimal image, scratch, as a starting point for building containers. Using the scratch “image” signals to the build process that you want the next command in the Dockerfile to be the first filesystem layer in your image.

While scratch appears in Docker’s repository on the hub, you can’t pull it, run it, or tag any image with the name scratch. Instead, you can refer to it in your Dockerfile. For example, to create a minimal container using scratch:

```
FROM scratch
COPY hello /
CMD ["/hello"]
```

## 为自己镜像添加一些debian的基础命令

新建一个文件夹，用wget下载rootfs.tar.xz压缩包。

```
wget -O rootfs.tar.xz https://github.com/debuerreotype/docker-debian-artifacts/raw/b024a792c752a5c6ccc422152ab0fd7197ae8860/jessie/rootfs.tar.xz
# 或
# wget -O rootfs.tar.xz https://raw.githubusercontent.com/debuerreotype/docker-debian-artifacts/dist-amd64/stable/rootfs.tar.xz
```

这个将近30MB的压缩包，包含了操作系统大部分常用命令。

使用如下dockerfile把上述基础命令加入自己做的镜像

```
FROM scratch

# add and unpack an archive that contains a Debian root filesystem
ADD rootfs.tar.xz /

# use the apt-get package manager to install nginx and wget
RUN apt-get update && \
apt-get -y install nginx wget
```

当然，如果你嫌麻烦，也可以直接使用[alpine](https://hub.docker.com/_/alpine)Linux镜像，该镜像尺寸也比较小，仅仅5M而已，不过你就不能用`apt-get`包管理工具安装软件了，也有一定学习成本。

Reference：

[scratch - an explicitly empty image, especially for building images "FROM scratch"](https://hub.docker.com/_/scratch)

[Create a base image](https://docs.docker.com/build/building/base-images/)

[最简单的Docker镜像教程：从头基于空镜像scratch创建一个新的Docker镜像](https://cloud.tencent.com/developer/article/1367035)

[alpine - A minimal Docker image based on Alpine Linux with a complete package index and only 5 MB in size!](https://hub.docker.com/_/alpine)
