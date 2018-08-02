## NGINX logrotate

一般，通过linux包管理器（例如，apt）方式安装的nginx，系统默认会自动通过logrotate这个日志管理软件，按天进行分割。但是经过多次测试发现logrotate切割日志不会严格按照自己设置的时间点进行分割。

但由于服务器中Nginx是通过源码手动安装的，所以没有logrotate设置。且最近由于请求变多，服务器日志文件增长很快，虽然目前貌似对系统运行及性能影响不大。但是服务器磁盘较小，生怕服务器哪天磁盘满后，自己就挂掉了。

鉴于目前不需要保存太多Log，所以打算定时删除若干天之前的Nginx日志。因为nginx自己不会对日志文件进行切割，所以打算通过其他方式进行切割，我们可以通过两种不同的方式进行，分别是：通过logrotate和通过shell脚本。

### NGINX日志转储原理

如果向Nginx master 进程发送`-USR1`信号，那么Nginx将重新打开日志文件。这样可以实现在不重启Nginx的情况下，替换掉Nginx使用的日志文件。

```
$ mv access.log access.log.0
$ kill -USR1 `cat master.nginx.pid`  # send USR1 signal to nginx master process
$ sleep 1
$ gzip access.log.0    # do something with access.log.0
```

NGINX will re-open its logs in response to the `USR1` signal.

> The rotator should send the -USR1 signal to the master process.
The master process reopens files, does chown() and chmod() to enable
the worker processes to write to files, and send a notification to
the worker procesess. They reopen files instantly.

> If the rotator sends the -HUP signal, then them master does a
reconfiguration
and starts a new worker processes those write to the new log files, but
the old shuting down worker processes still uses the old log files.

> Any way, to send the -USR1 signal you should have the sudo permission.

### 1.使用logrotate切割

logrotate 程序是一个日志文件管理工具。用来把旧的日志文件删除，并创建新的日志文件，我们把它叫做“转储”。我们可以根据日志文件的大小，也可以根据其天数来转储，这个过程一般通过 cron 程序来执行。logrotate 程序还可以用于压缩日志文件，以及发送日志到指定的E-mail。

一般logrotate的配置文件是/etc/logrotate.conf，而/etc/logrotate.d/是用于存储其他配置文件的目录。该目录里的所有文件都会被主动的读入 /etc/logrotate.conf中执行。

#### /etc/logrotate.d/nginx logrotate配置文件详解

```
/usr/local/nginx-1.12.0/logs/*.log {
        daily
        missingok
        copytruncate
        rotate 5
        dateext
        compress
        notifempty
        create 640 root adm
        sharedscripts
        postrotate
                [ ! -f /usr/local/nginx-nginx-1.12.0/logs/nginx.pid ] || kill -USR1 `cat /usr/local/nginx-1.12.0/logs/nginx.pid`
        endscript
}
```

在该配置文件中，每个参数作用如下：

usr/local/nginx-1.12.0/logs/为nginx日志的存储目录，可以根据实际情况进行修改。

daily：日志文件将按天轮循。

weekly：日志文件将按周轮循。

monthly：日志文件将按月轮循。

missingok：在日志轮循期间，任何错误将被忽略，例如“文件无法找到”之类的错误。

rotate 7：一次存储7个日志文件。对于第8个日志文件，时间最久的那个日志文件将被删除。

dateext：定义日志文件后缀是日期格式,也就是切割后文件是:xxx.log-20160402.gz这样的格式。如果该参数被注释掉,切割出来是按数字递增,即前面说的 xxx.log-1这种格式。

compress：在轮循任务完成后，已轮循的归档将使用gzip进行压缩。

delaycompress：总是与compress选项一起用，delaycompress选项指示logrotate不要将最近的归档压缩，压缩将在下一次轮循周期进行。这在你或任何软件仍然需要读取最新归档时很有用。

notifempty：如果是空文件的话，不进行转储。

create 640 nginx adm：以指定的权限和用书属性，创建全新的日志文件，同时logrotate也会重命名原始日志文件。

postrotate/endscript：在所有其它指令完成后，postrotate和endscript里面指定的命令将被执行。在这种情况下，rsyslogd进程将立即再次读取其配置并继续运行。注意：这两个关键字必须单独成行。

> 注意：logrotate默认执行时间一般可以通过crontab配置文件(/etc/anacrontab)查看到。

#### 测试logrotate配置

将上述配置文件拷贝至`/etc/logrotate.d/`目录，并修改文件权限

```
sudo chown root  nginx
sudo chgrp root nginx
sudo chmod g-w nginx
```

执行`logrotate -vf /etc/logrotate.conf`命令，查看log文件是否被替换。

### 2.使用shell脚本切割

使用shell脚本切割nginx日志很简单，shell脚本内容如下：

```
#!/bin/bash

#初始化

LOGS_PATH=/var/log/nginx

YESTERDAY=$(date -d "yesterday" +%Y%m%d)

#按天切割日志

mv ${LOGS_PATH}/ilanni.com.log ${LOGS_PATH}/ilanni.com_${YESTERDAY}.log

#向nginx主进程发送USR1信号，重新打开日志文件，否则会继续往mv后的文件写数据的。原因在于：linux系统中，内核是根据文件描述符来找文件的。如果不这样操作导致日志切割失败。

kill -USR1 `ps axu | grep "nginx: master process" | grep -v grep | awk '{print $2}'`

#删除7天前的日志

cd ${LOGS_PATH}

find . -mtime +7 -name "*20[1-9][3-9]*" | xargs rm -f

exit 0
```

该shell脚本有两个功能，第一个是切割nginx日志，第二个是删除7天之前的nginx日志。

在切割nginx日志的功能中，我们要注意该shell脚本命名切割的日志是以切割时，是以前一天的时间就行命名该日志文件的。

最后，我们再把该shell脚本放在crontab中定时执行，然后检查结果就可以了。


Reference:

[Nginx Log Rotation](https://www.nginx.com/resources/wiki/start/topics/examples/logrotation/)

[Nginx Log Rotation - How it works](http://article.gmane.org/gmane.comp.web.nginx.english/583)

[烂泥：切割nginx日志](https://www.ilanni.com/?p=11150)

