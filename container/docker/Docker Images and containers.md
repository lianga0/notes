## Docker Images and containers

A container is launched by running an image. An image is an executable package that includes everything needed to run an application--the code, a runtime, libraries, environment variables, and configuration files.

A container is a runtime instance of an image--what the image becomes in memory when executed (that is, an image with state, or a user process). You can see a list of your running containers with the command, docker ps, just as you would in Linux.

### install Docker

https://docs.docker.com/install/linux/docker-ce/ubuntu/

### Test Docker version

Run `docker --version` and ensure that you have a supported version of Docker:

```
docker --version

Docker version 17.12.0-ce, build c97c6d6
```

Run `docker info` or (`docker version` without --) to view even more details about your docker installation:

```
docker info

Containers: 1
 Running: 1
 Paused: 0
 Stopped: 0
Images: 23
Server Version: 18.06.1-ce
Storage Driver: overlay2
 Backing Filesystem: extfs
 Supports d_type: true
 Native Overlay Diff: true
Logging Driver: json-file
Cgroup Driver: cgroupfs
Plugins:
...
```

### use Docker as a non-root user

If you would like to use Docker as a non-root user, you should now consider adding your user to the “docker” group with something like:

```
sudo usermod -aG docker your-user
```

Remember to log out and back in for this to take effect!

> Warning:

> Adding a user to the “docker” group grants them the ability to run containers which can be used to obtain root privileges on the Docker host. Refer to [Docker Daemon Attack Surface](https://docs.docker.com/engine/security/security/#docker-daemon-attack-surface) for more information.

默认情况下，docker 命令会使用`Unix socket`与 Docker 引擎通讯。而只有 root 用户和 docker 组的用户才可以访问 Docker 引擎的`Unix socket`。出于安全考虑，一般 Linux 系统上不会直接使用 root 用户。因此，更好地做法是将需要使用 docker 的用户加入 docker 用户组。

### docker进入运行中的容器查看目录结构

```
docker container ls -a

docker exec -it container_idxxxx /bin/bash
```

Reference:

[docker的入门使用](https://zhuanlan.zhihu.com/p/62515531)

[Get Docker CE for Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)

