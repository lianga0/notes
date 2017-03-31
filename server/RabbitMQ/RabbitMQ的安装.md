##RabbitMQ的安装

Ubuntu 14.04 LTS安装RabbitMQ步骤：

#####1.执行Ubuntu安装命令
```
sudo apt-get install rabbitmq-server
```

如下输出显示安装已经成功。RabbitMQ安装成功后会自动把自己的服务启动，所以现在RabbitMQ的服务已经可以使用。
```
Reading package lists... Done
Building dependency tree
Reading state information... Done
The following extra packages will be installed:
  erlang-asn1 erlang-base erlang-corba erlang-crypto erlang-diameter
  erlang-edoc erlang-eldap erlang-erl-docgen erlang-eunit erlang-ic
  erlang-inets erlang-mnesia erlang-nox erlang-odbc erlang-os-mon
  erlang-parsetools erlang-percept erlang-public-key erlang-runtime-tools
  erlang-snmp erlang-ssh erlang-ssl erlang-syntax-tools erlang-tools
  erlang-webtool erlang-xmerl

...

Setting up erlang-nox (1:16.b.3-dfsg-1ubuntu2.1) ...
Setting up rabbitmq-server (3.2.4-1) ...
Adding group `rabbitmq' (GID 128) ...
Done.
Adding system user `rabbitmq' (UID 120) ...
Adding new user `rabbitmq' (UID 120) with group `rabbitmq' ...
Not creating home directory `/var/lib/rabbitmq'.
 * Starting message broker rabbitmq-server                                                                                                                                             [ OK ]
Processing triggers for ureadahead (0.100.0-16) ...

```

#####2.RabbitMQ GUID

RabbitMQ官方提供的一个web管理工具[rabbitmq_management](http://www.rabbitmq.com/management.html)。安装rabbitmq-server时，该管理工具默认也被安装，但默认此服务并没有开启，需要执行命令启动此管理服务。命令如下：
```
sudo rabbitmq-plugins enable rabbitmq_management
```

命令行显示如下输出表示服务启动成功，在安装RabbitMQ的电脑浏览器地址栏输入：[http://localhost:15672/](http://localhost:15672)，默认登录账号和密码都是：guest。
```
The following plugins have been enabled:
  mochiweb
  webmachine
  rabbitmq_web_dispatch
  amqp_client
  rabbitmq_management_agent
  rabbitmq_management

Applying plugin configuration to rabbit
```

#####3.rabbitmq命令行工具

查看rabbitmq服务状态
```
sudo rabbitmqctl list_queues
```

查看rabbitmq所有队列
```
sudo rabbitmqctl list_queues
```

#####4.python操作RabbitMQ示例

python使用pika库来操作RabbitMQ，可以使用`sudo pip install pika`命令来安装。

######4.1.连接RabbitMQ服务器

这里使用默认的配置与RabbitMQ服务器建立连接
```
#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
               'localhost'))
channel = connection.channel()
```

######4.2.创建消息队列

若要向消息队列发送消息，必须首先保证消息队列已经创建。可以使用下面示例代码创建消息队列
```
channel.queue_declare(queue='hello')
```

######4.3.发送消息

In RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange. But let's not get dragged down by the details ‒ you can read more about exchanges in the third part of this tutorial. All we need to know now is how to use a default exchange identified by an empty string. This exchange is special ‒ it allows us to specify exactly to which queue the message should go. The queue name needs to be specified in the routing_key parameter:

```
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
```

######4.4.关闭连接

Before exiting the program we need to make sure the network buffers were flushed and our message was actually delivered to RabbitMQ. We can do it by gently closing the connection.
```
connection.close()
```

>Sending doesn't work!

>>If this is your first time using RabbitMQ and you don't see the "Sent" message then you may be left scratching your head wondering what could be wrong. Maybe the broker was started without enough free disk space (by default it needs at least 1Gb free) and is therefore refusing to accept messages. Check the broker logfile to confirm and reduce the limit if necessary. The configuration file documentation will show you how to set disk_free_limit.

Reference:
[Installing on Debian / Ubuntu](http://www.rabbitmq.com/install-debian.html)

[Rabbitmq的使用及Web监控工具使用](http://www.cnblogs.com/gossip/p/4475978.html)

[tutorial of python client](http://www.rabbitmq.com/tutorials/tutorial-one-python.html)