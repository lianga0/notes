# Neo4j入门基础之安装

> 2022.11.24

## 图数据库

一般认为具有“无索引邻接”特性的图数据库才称为原生图数据库

Neo4j是一个高性能的NOSQL图形数据库，它将结构化数据存储在网络上而不是表中。Neo4j也可以被看作是一个高性能的图引擎，该引擎具有成熟数据库的所有特性。

在一个图中包含两种基本的数据类型：Nodes（节点） 和 Relationships（关系）。Nodes 和 Relationships 包含key/value形式的属性。Nodes通过Relationships所定义的关系相连起来，形成关系型网络结构。


## Neo4j安装

Neo4j是开源的，它支持Windows、Linux和MAC平台。

对于仅在本地做开发测试，不想过多了解和配置Neo4j，可以直接安装使用[Neo4j Desktop](https://neo4j.com/download/)。

`Neo4j Desktop`包含多个组件，包括Neo4j Enterprise Server、Neo4j Browers、 Neo4j Bloom等服务组件。

### Neo4j Community Edition 安装

也可下载社区版[Neo4j Community Edition](https://neo4j.com/download-center/#community)安装包直接安装。

Ubuntu可以Neo4j的源来安装，可参考文档[Neo4j Debian Packages](https://debian.neo4j.com/) Adding the Debian repository。

安装完成后，打开终端输入命令：`neo4j console`即可运行社区版Neo4j Server。

在浏览器 http://localhost:7474 中查看Neo4j数据库 （默认的host是bolt://localhost:7687，默认的用户是neo4j，其默认的密码是：neo4j，第一次成功登陆到Neo4j服务器之后，需要重置密码。

如果忘记了密码，解决方法是停止服务，进入`/data/dbms`目录，删除auth文件 

### Neo4j 配置

Ubuntu平台使用apt安装后，配置文档默认存储在`/etc/neo4j/`目录下，Neo4j通过配置文件neo4j.conf控制服务器的工作。

默认情况下，不需要进行任意配置，就可以启动服务器。
