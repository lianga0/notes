## 修改Docker已有镜像或容器内的文件

> 2019.12.26

> https://blog.csdn.net/jiankunking/article/details/62056392

1. 使用下载的镜像启动容器。

```
$ sudo docker run -t -i docker_image_name_or_id /bin/bash
root@0b2616b0e5a8:/#
```

> 注意：记住容器的 ID，稍后还会用到。

2. 在容器中添加 json 和 gem 两个应用。

```
root@0b2616b0e5a8:/# gem install json
```

3. 当结束后，我们使用 exit 来退出，现在我们的容器已经被我们改变了，使用 docker commit 命令来提交更新后的副本。

```
$ sudo docker commit -m "Added json gem" -a "Docker Newbee" 0b2616b0e5a8 new_docker_image_name
4f177bd27a9ff0f6dc2a830403925b5360bfe0b93d476f7fc3231110e7f71b1c
```

其中，-m 来指定提交的说明信息，跟我们使用的版本控制工具一样；-a 可以指定更新的用户信息；之后是用来创建镜像的容器的 ID；最后指定目标镜像的仓库名和 tag 信息。创建成功后会返回这个镜像的 ID 信息。

使用 docker images 来查看新创建的镜像。之后，可以使用新的镜像来启动容器。


### 向已有容器内写入或拷贝指定文件，然后重新生成镜像

> https://blog.csdn.net/dechengtju/article/details/85009836


1. docker ps    列出容器

```
$ docker ps
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES

```

2. docker cp   拷贝文件至容器

docker中宿主机与容器（container）互相拷贝传递文件的方法

从容器拷贝文件到宿主机

```
docker cp mycontainer:/opt/testnew/file.txt /opt/test/
```

从宿主机拷贝文件到容器

```
docker cp /opt/test/file.txt mycontainer:/opt/testnew/
```

> 需要注意的是，不管容器有没有启动，拷贝命令都会生效。

当结束后，我们使用 exit 来退出，现在我们的容器已经被我们改变了，使用 docker commit 命令来提交更新后的副本。

3. 提交修改

```
$ sudo docker commit -m "描述内容" -a "author name" 32555789dd00 new_docker_image_name
```

其中，-m 来指定提交的说明信息，跟我们使用的版本控制工具一样；-a 可以指定更新的用户信息；之后是用来创建镜像的容器的 ID；最后指定目标镜像的仓库名和 tag 信息。创建成功后会返回这个镜像的 ID 信息。

4. 使用 docker images 来查看新创建的镜像。

```
$ docker iamge
```
《完》