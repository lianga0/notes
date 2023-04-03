# 搭建单节点presto测试服务

> 2023.04.03

按官网[Deploying Presto](https://prestodb.io/docs/current/installation/deployment.html#installing-presto)链接下载最新安装包[presto-server-0.280.tar.gz](https://repo1.maven.org/maven2/com/facebook/presto/presto-server/0.280/presto-server-0.280.tar.gz)解压后，在顶层目`presto-server-0.280`下创建`etc`目录，然后依次按照文档配置如下文件

```
etc
├── catalog
│   ├── mysql.properties
│   └── sqlserver.properties
├── config.properties
├── jvm.config
└── node.properties
```

配置完成后，使用`bin/launcher run`命令前台启动presto服务即可，这里我们分别配置了MySql和SqlServer两个Catalog。上述配置文件放置在etc.zip文件中，下载解压即可查看。

> 注意：

> 启动前，使用如下命令分别启动测试使用的MySQL和SqlServer服务（容器化部署）

```
docker run -p 3306:3306 --name mysql -e MYSQL_ROOT_PASSWORD=root -d mysql

docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=root!SQL123" -p 1433:1433  --name mssql  -d mcr.microsoft.com/mssql/server:2022-latest
```

下载[presto-cli-0.280-executable.jar](https://repo1.maven.org/maven2/com/facebook/presto/presto-cli/0.280/presto-cli-0.280-executable.jar)命令行客户端，在presto单节点上直接运行`./presto-cli-0.280-executable.jar`命令即可连接刚启动的presto测试服务。
